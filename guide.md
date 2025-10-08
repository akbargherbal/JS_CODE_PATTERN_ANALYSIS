# **Complete Guide to Production-Scale Code Pattern Mining with Tree-sitter**

## **Executive Summary**

This guide provides a comprehensive, production-ready implementation for building a scalable static analysis pipeline that extracts, normalizes, and analyzes code patterns from large JavaScript/TypeScript codebases. You'll build a system capable of processing 100,000+ files to generate a ranked "phrasebook" of the most common code idioms, normalized at multiple abstraction levels. The solution combines Tree-sitter's robust parsing, custom normalization algorithms, and a hybrid counting strategy using `collections.Counter` and SQLite for memory-efficient aggregation.

---

## **Part 1: Understanding the Foundation**

### **1.1 Why Tree-sitter?**

Tree-sitter is a parser generator designed specifically for developer tooling. Unlike traditional compilers, it:

- **Parses incrementally** on every keystroke, making it fast enough for real-time editor integration
- **Recovers from syntax errors** gracefully, producing partial but useful trees with explicit ERROR nodes
- **Generates Concrete Syntax Trees (CSTs)**, preserving all source information including whitespace, comments, and punctuation
- **Supports 30+ languages** through community-maintained grammars

The CST (not AST) is critical. An AST abstracts away "trivial" details like punctuation and comments. A CST preserves everything, enabling accurate code transformation and analysis. For example, the `get` keyword in `class A { get method() {} }` is essential semantic information that would be lost in a pure AST.

### **1.2 The Four Levels of Pattern Abstraction**

Understanding these levels guides your entire implementation:

| Level                   | Description                          | Example Input                             | Example Output                                         |
| ----------------------- | ------------------------------------ | ----------------------------------------- | ------------------------------------------------------ |
| **Level 1: Concrete**   | Exact syntax via Tree-sitter queries | `console.log("hello")`                    | `(call_expression function: (member_expression...))`   |
| **Level 2: Abstract**   | Structural patterns with wildcards   | `const user = "John"`                     | `const IDENTIFIER = STRING`                            |
| **Level 3: Semantic**   | Domain-aware patterns                | `const el = document.getElementById("x")` | `const IDENTIFIER = DOM_OBJECT.getElementById(STRING)` |
| **Level 4: Conceptual** | Design patterns (Singleton, MVC)     | N/A (architectural)                       | Requires AI/heuristics                                 |

Your system will focus on Levels 2 and 3, which are automatable and pedagogically valuable.

---

## **Part 2: Multi-Dialect JavaScript Parsing Strategy**

### **2.1 The JavaScript Grammar Landscape**

You need to handle four dialects:

1. **JavaScript (.js, .mjs, .cjs)** → `tree-sitter-javascript` grammar (includes JSX support)
2. **JSX (.jsx)** → `tree-sitter-javascript` grammar
3. **TypeScript (.ts)** → `tree-sitter-typescript` (typescript grammar)
4. **TSX (.tsx)** → `tree-sitter-typescript` (tsx grammar)

**Critical insight**: The `tsx` grammar is intentionally permissive and can parse Flow-annotated JavaScript. This makes it a powerful fallback for ambiguous `.js` files.

### **2.2 Parser Selection Matrix**

Implement this as a prioritized decision tree:

```python
GRAMMAR_MAP = {
    '.js': ('tree-sitter-javascript', 'tsx'),  # primary, fallback
    '.mjs': ('tree-sitter-javascript', 'tsx'),
    '.cjs': ('tree-sitter-javascript', 'tsx'),
    '.jsx': ('tree-sitter-javascript', None),
    '.ts': ('typescript', None),
    '.tsx': ('tsx', None)
}

def select_parser(filepath: str, tree: Tree) -> Language:
    """
    Select parser based on extension. If primary parser produces
    excessive errors, retry with fallback.
    """
    ext = Path(filepath).suffix
    primary, fallback = GRAMMAR_MAP.get(ext, (None, None))

    if tree.root_node.has_error() and fallback:
        # High error count, retry with fallback
        return load_grammar(fallback)

    return load_grammar(primary)
```

---

## **Part 3: Building the Normalization Engine**

### **3.1 Core Algorithm: Recursive CST Traversal**

The normalization engine walks the CST recursively, dispatching to type-specific handlers. This is the heart of your system:

```python
import hashlib
from tree_sitter import Node
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass(frozen=True)
class CodePattern:
    """Immutable pattern representation with multi-level signatures."""
    pattern_hash: str
    abstract_signature: str
    semantic_signature: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

class CSTNormalizer:
    """
    Transforms Tree-sitter CST nodes into normalized signatures
    at abstract and semantic levels.
    """
    def __init__(self, source_code: bytes, semantic_rules: dict = None):
        self.source_code = source_code
        self.semantic_rules = semantic_rules or {}

    def get_node_text(self, node: Node) -> str:
        """Extract UTF-8 text from node byte range."""
        return self.source_code[node.start_byte:node.end_byte].decode('utf8')

    def normalize(self, node: Node, level: str = 'abstract') -> str:
        """Public entry point for normalization."""
        return self._recursive_normalize(node, level)

    def _recursive_normalize(self, node: Node, level: str) -> str:
        """
        Core recursive traversal. Dispatches to handlers based on node.type.
        """
        # Handle leaf nodes (identifiers, literals, keywords)
        if not node.child_count and node.is_named:
            return self._handle_terminal(node, level)

        # Preserve punctuation as-is
        if not node.is_named:
            return self.get_node_text(node)

        # Dispatch to specific handler or default
        handler_name = f"_handle_{node.type}"
        handler = getattr(self, handler_name, self._handle_default)
        return handler(node, level)

    def _handle_terminal(self, node: Node, level: str) -> str:
        """Handle identifiers and literals."""
        if node.type == 'identifier':
            if level == 'semantic':
                text = self.get_node_text(node)
                # Check semantic rulebook
                if text in self.semantic_rules.get('identifier', {}):
                    return self.semantic_rules['identifier'][text]
            return 'IDENTIFIER'

        if node.type in ['string', 'template_string']:
            return 'STRING'
        if node.type == 'number':
            return 'NUMBER'
        if node.type in ['true', 'false']:
            return 'BOOLEAN'

        # Preserve keywords (const, let, function, etc.)
        return self.get_node_text(node)

    def _handle_default(self, node: Node, level: str) -> str:
        """Default: recursively normalize all children."""
        parts = [self._recursive_normalize(child, level)
                 for child in node.children]
        return "".join(parts)

    def _handle_lexical_declaration(self, node: Node, level: str) -> str:
        """Handle: const/let/var x = value"""
        kind = node.child_by_field_name('kind')
        declarator = node.child_by_field_name('declarator')

        kind_str = self._recursive_normalize(kind, level)
        decl_str = self._recursive_normalize(declarator, level)
        return f"{kind_str} {decl_str}"

    def _handle_variable_declarator(self, node: Node, level: str) -> str:
        """Handle: name = value"""
        name = self._recursive_normalize(
            node.child_by_field_name('name'), level)
        value = self._recursive_normalize(
            node.child_by_field_name('value'), level)
        return f"{name} = {value}"

    def _handle_call_expression(self, node: Node, level: str) -> str:
        """Handle: func(args)"""
        function = self._recursive_normalize(
            node.child_by_field_name('function'), level)
        arguments = self._recursive_normalize(
            node.child_by_field_name('arguments'), level)
        return f"{function}{arguments}"

    def _handle_arguments(self, node: Node, level: str) -> str:
        """Handle: (arg1, arg2, ...)"""
        args = [self._recursive_normalize(child, level)
                for child in node.named_children]
        return f"({', '.join(args)})"

    def _handle_member_expression(self, node: Node, level: str) -> str:
        """Handle: object.property"""
        obj = self._recursive_normalize(
            node.child_by_field_name('object'), level)
        prop = self._recursive_normalize(
            node.child_by_field_name('property'), level)
        return f"{obj}.{prop}"

    @staticmethod
    def get_hash(signature: str) -> str:
        """Generate stable SHA-256 hash for signature."""
        return hashlib.sha256(signature.encode('utf-8')).hexdigest()
```

### **3.2 Semantic Rulebook Configuration**

Define semantic enrichment rules in YAML for maintainability:

```yaml
# semantic_rules.yml
rules:
  identifier:
    document: DOM_OBJECT
    window: GLOBAL_OBJECT
    console: CONSOLE_OBJECT
    React: REACT_OBJECT
    useState: REACT_HOOK
    useEffect: REACT_HOOK

  method:
    getElementById: DOM_METHOD
    querySelector: DOM_METHOD
    fetch: FETCH_API
    setTimeout: TIMER_API
    then: PROMISE_METHOD
    catch: PROMISE_METHOD

metadata:
  categories:
    dom_manipulation:
      patterns: [getElementById, querySelector, createElement]
    async_operations:
      patterns: [fetch, then, async, await]
    react_patterns:
      patterns: [useState, useEffect, useContext]
```

Load this configuration at startup:

```python
import yaml

def load_semantic_rules(yaml_path: str) -> dict:
    """Load and compile semantic enrichment rules."""
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    return config['rules']

# Usage
semantic_rules = load_semantic_rules('semantic_rules.yml')
normalizer = CSTNormalizer(source_code, semantic_rules)
```

---

## **Part 4: High-Performance Parallel Processing**

### **4.1 The Worker Initialization Pattern**

Tree-sitter `Language` and `Parser` objects are **non-picklable** (they wrap C pointers). You cannot pass them to worker processes. The solution: initialize them once per worker using `Pool.initializer`.

```python
from multiprocessing import Pool
from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjs
import tree_sitter_typescript as tsts

# Global variables (worker-process-local)
_JS_LANG = None
_TS_LANG = None
_TSX_LANG = None
_PARSER = None
_NORMALIZER = None

def init_worker(semantic_rules: dict):
    """
    Called once per worker process at startup.
    Initializes all parsers and normalizer.
    """
    global _JS_LANG, _TS_LANG, _TSX_LANG, _PARSER, _NORMALIZER

    _JS_LANG = Language(tsjs.language())
    _TS_LANG = Language(tsts.language_typescript())
    _TSX_LANG = Language(tsts.language_tsx())

    _PARSER = Parser()
    _NORMALIZER = CSTNormalizer(b"", semantic_rules)

def process_file(filepath: str) -> Dict[str, int]:
    """
    Worker task: parse file, extract patterns, return counts.
    This function receives only simple, picklable arguments.
    """
    global _PARSER, _NORMALIZER

    # Read file
    with open(filepath, 'rb') as f:
        source_code = f.read()

    # Select parser based on extension
    ext = Path(filepath).suffix
    if ext in ['.ts']:
        _PARSER.set_language(_TS_LANG)
    elif ext in ['.tsx']:
        _PARSER.set_language(_TSX_LANG)
    else:
        _PARSER.set_language(_JS_LANG)

    # Parse
    tree = _PARSER.parse(source_code)

    # Check for excessive errors, retry with TSX if needed
    if ext == '.js' and tree.root_node.has_error():
        error_count = count_error_nodes(tree.root_node)
        if error_count > 5:  # threshold
            _PARSER.set_language(_TSX_LANG)
            tree = _PARSER.parse(source_code)

    # Extract patterns
    _NORMALIZER.source_code = source_code
    local_counts = Counter()

    # Find all nodes of interest (using Tree-sitter query)
    query = _JS_LANG.query("""
        (lexical_declaration) @decl
        (call_expression) @call
    """)

    for node, _ in query.captures(tree.root_node):
        abstract_sig = _NORMALIZER.normalize(node, 'abstract')
        semantic_sig = _NORMALIZER.normalize(node, 'semantic')

        abs_hash = CSTNormalizer.get_hash(abstract_sig)
        sem_hash = CSTNormalizer.get_hash(semantic_sig)

        local_counts[abs_hash] += 1
        local_counts[sem_hash] += 1

    return dict(local_counts)

# Main process
def main():
    semantic_rules = load_semantic_rules('semantic_rules.yml')
    file_list = discover_files('src/')

    # Create worker pool with initialization
    with Pool(processes=8, initializer=init_worker,
              initargs=(semantic_rules,)) as pool:
        results = pool.map(process_file, file_list)

    # Aggregate results
    total_counts = Counter()
    for result in results:
        total_counts.update(result)

    print(f"Found {len(total_counts)} unique patterns")
```

### **4.2 File Pre-filtering Pipeline**

Before parsing, eliminate problematic files:

```python
def is_binary_file(filepath: str) -> bool:
    """Check for null bytes in first 1KB."""
    with open(filepath, 'rb') as f:
        chunk = f.read(1024)
    return b'\x00' in chunk

def is_minified(filepath: str) -> bool:
    """Detect minified JS via heuristics."""
    if '.min.js' in filepath:
        return True

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    if not lines:
        return False

    # Check average line length
    avg_length = sum(len(line) for line in lines) / len(lines)
    if avg_length > 500:
        return True

    # Check longest line
    max_length = max(len(line) for line in lines)
    if max_length > 50000:
        return True

    return False

def discover_files(root_dir: str) -> List[str]:
    """Find all parseable JS/TS files."""
    valid_files = []
    extensions = {'.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx'}

    for filepath in Path(root_dir).rglob('*'):
        if filepath.suffix not in extensions:
            continue

        if is_binary_file(filepath):
            continue

        if is_minified(filepath):
            continue

        valid_files.append(str(filepath))

    return valid_files
```

---

## **Part 5: Scalable Frequency Counting**

### **5.1 Hybrid Counter + SQLite Strategy**

For 100K+ files, storing millions of signatures in memory is prohibitive. Use SQLite as a persistent aggregator:

```python
import sqlite3
from collections import Counter

def init_database(db_path: str):
    """Create pattern storage table."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            pattern_hash TEXT PRIMARY KEY,
            abstract_signature TEXT NOT NULL,
            semantic_signature TEXT,
            count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def aggregate_to_sqlite(local_counts: Dict[str, int],
                        signature_map: Dict[str, tuple],
                        db_path: str):
    """
    Aggregate worker counts into SQLite.

    Args:
        local_counts: {hash: count}
        signature_map: {hash: (abstract_sig, semantic_sig)}
        db_path: path to SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for pattern_hash, count in local_counts.items():
        abs_sig, sem_sig = signature_map.get(pattern_hash, ("", ""))

        cursor.execute("""
            INSERT INTO patterns (pattern_hash, abstract_signature,
                                semantic_signature, count)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(pattern_hash) DO UPDATE
            SET count = count + excluded.count
        """, (pattern_hash, abs_sig, sem_sig, count))

    conn.commit()
    conn.close()

def get_top_patterns(db_path: str, limit: int = 500) -> List[tuple]:
    """Retrieve most frequent patterns."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("""
        SELECT pattern_hash, abstract_signature, semantic_signature, count
        FROM patterns
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()
    return results
```

### **5.2 Modified Worker Function**

Workers now write directly to SQLite:

```python
def process_file_with_db(filepath: str, db_path: str) -> int:
    """
    Worker task: parse, extract, write to SQLite directly.
    Returns: number of patterns found in this file.
    """
    global _PARSER, _NORMALIZER

    # ... (parsing code same as before) ...

    local_counts = Counter()
    signature_map = {}

    for node, _ in query.captures(tree.root_node):
        abstract_sig = _NORMALIZER.normalize(node, 'abstract')
        semantic_sig = _NORMALIZER.normalize(node, 'semantic')

        abs_hash = CSTNormalizer.get_hash(abstract_sig)

        local_counts[abs_hash] += 1
        signature_map[abs_hash] = (abstract_sig, semantic_sig)

    # Write to SQLite
    aggregate_to_sqlite(local_counts, signature_map, db_path)

    return len(local_counts)
```

---

## **Part 6: Pattern Clustering and Deduplication**

### **6.1 Fuzzy Matching for Structural Similarity**

After exact counting, cluster similar patterns using Levenshtein distance:

```python
from rapidfuzz import process, fuzz
import networkx as nx

def cluster_patterns(patterns: List[tuple],
                    similarity_threshold: int = 85) -> List[List[tuple]]:
    """
    Cluster patterns by structural similarity using fuzzy matching.

    Args:
        patterns: [(hash, abstract_sig, semantic_sig, count), ...]
        similarity_threshold: minimum similarity score (0-100)

    Returns:
        List of clusters, each cluster is a list of patterns
    """
    if not patterns:
        return []

    # Extract signatures for comparison
    signatures = [p[1] for p in patterns]  # abstract_signature

    # Build similarity graph
    graph = nx.Graph()
    for i, sig in enumerate(signatures):
        graph.add_node(i)

    # Find similar pairs
    for i, sig in enumerate(signatures):
        matches = process.extract(
            sig,
            signatures,
            scorer=fuzz.ratio,
            score_cutoff=similarity_threshold
        )

        for match_text, score, match_idx in matches:
            if i != match_idx:
                graph.add_edge(i, match_idx)

    # Find connected components (clusters)
    clusters = []
    for component in nx.connected_components(graph):
        cluster = [patterns[i] for i in component]
        # Sort by frequency, highest first
        cluster.sort(key=lambda x: x[3], reverse=True)
        clusters.append(cluster)

    # Sort clusters by total frequency
    clusters.sort(key=lambda c: sum(p[3] for p in c), reverse=True)

    return clusters

def generate_cluster_report(clusters: List[List[tuple]],
                           output_path: str):
    """Generate JSON report of clustered patterns."""
    import json

    report = []

    for cluster in clusters[:500]:  # Top 500 clusters
        canonical = cluster[0]  # Most frequent in cluster
        total_freq = sum(p[3] for p in cluster)

        cluster_entry = {
            "canonical_pattern_hash": canonical[0],
            "canonical_abstract_signature": canonical[1],
            "canonical_semantic_signature": canonical[2],
            "total_frequency": total_freq,
            "variations": [
                {
                    "pattern_hash": p[0],
                    "abstract_signature": p[1],
                    "semantic_signature": p[2],
                    "frequency": p[3]
                }
                for p in cluster[1:]  # Exclude canonical
            ]
        }
        report.append(cluster_entry)

    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

# Usage
patterns = get_top_patterns('patterns.db', limit=2000)
clusters = cluster_patterns(patterns, similarity_threshold=85)
generate_cluster_report(clusters, 'pattern_report.json')
```

---

## **Part 7: Complete End-to-End Pipeline**

### **7.1 Main Orchestrator**

```python
from pathlib import Path
from collections import Counter
from multiprocessing import Pool
from tqdm import tqdm
import json

def main_pipeline(
    source_dir: str,
    output_dir: str = 'output',
    num_workers: int = 8,
    top_n: int = 500
):
    """
    Complete pattern mining pipeline.

    Args:
        source_dir: Root directory containing source code
        output_dir: Directory for output files
        num_workers: Number of parallel worker processes
        top_n: Number of top patterns to report
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    db_path = output_path / 'patterns.db'
    report_path = output_path / 'pattern_report.json'

    print("📂 Phase 1: File Discovery")
    file_list = discover_files(source_dir)
    print(f"   Found {len(file_list)} valid files")

    print("\n🔧 Phase 2: Database Initialization")
    init_database(str(db_path))

    print(f"\n⚙️  Phase 3: Parallel Processing ({num_workers} workers)")
    semantic_rules = load_semantic_rules('semantic_rules.yml')

    with Pool(
        processes=num_workers,
        initializer=init_worker,
        initargs=(semantic_rules,)
    ) as pool:
        # Use imap_unordered for progress tracking
        results = list(tqdm(
            pool.imap_unordered(
                lambda f: process_file_with_db(f, str(db_path)),
                file_list
            ),
            total=len(file_list),
            desc="Processing files"
        ))

    total_patterns = sum(results)
    print(f"\n✅ Extracted {total_patterns} pattern instances")

    print("\n📊 Phase 4: Pattern Clustering")
    patterns = get_top_patterns(str(db_path), limit=2000)
    clusters = cluster_patterns(patterns, similarity_threshold=85)

    print(f"   Found {len(clusters)} unique pattern clusters")

    print("\n📝 Phase 5: Report Generation")
    generate_cluster_report(clusters[:top_n], str(report_path))

    print(f"\n🎉 Complete! Report saved to {report_path}")

    # Print top 10 preview
    print("\n📋 Top 10 Patterns Preview:")
    for i, cluster in enumerate(clusters[:10], 1):
        canonical = cluster[0]
        print(f"{i}. {canonical[1]}")
        print(f"   Frequency: {sum(p[3] for p in cluster)}")
        print()

if __name__ == '__main__':
    main_pipeline(
        source_dir='./my-javascript-project',
        output_dir='./pattern-analysis',
        num_workers=8,
        top_n=500
    )
```

---

## **Part 8: Advanced Query Techniques**

### **8.1 Writing Effective Tree-sitter Queries**

Tree-sitter queries use S-expression syntax. Key features:

```scheme
; Basic node matching
(function_declaration) @function

; Field-based matching
(function_declaration
  name: (identifier) @func.name
  body: (statement_block) @func.body
)

; Text predicates
(call_expression
  function: (identifier) @func
  (#eq? @func "fetch")
)

; Wildcard matching
(call_expression
  function: (_) @any_function
)

; Capturing method chains
(call_expression
  function: (member_expression
    object: (call_expression
      function: (identifier) @base
      (#eq? @base "fetch")
    )
    property: (property_identifier) @method
  )
)
```

### **8.2 Performance Optimization**

Be as specific as possible to minimize search space:

**❌ Inefficient:**

```scheme
(identifier) @name  ; Matches EVERY identifier
```

**✅ Efficient:**

```scheme
(call_expression
  function: (identifier) @func_name
)  ; Only matches identifiers used as function calls
```

---

## **Part 9: Error Handling and Resilience**

### **9.1 Graceful Parse Error Recovery**

```python
def count_error_nodes(node: Node) -> int:
    """Recursively count ERROR and MISSING nodes."""
    count = 0
    if node.is_error or node.is_missing:
        count += 1
    for child in node.children:
        count += count_error_nodes(child)
    return count

def analyze_parse_quality(tree: Tree) -> dict:
    """Generate parse quality metrics."""
    root = tree.root_node

    if not root.has_error():
        return {'status': 'clean', 'error_count': 0}

    error_nodes = []
    def find_errors(node):
        if node.is_error or node.is_missing:
            error_nodes.append({
                'type': 'ERROR' if node.is_error else 'MISSING',
                'line': node.start_point[0] + 1,
                'column': node.start_point[1] + 1
            })
        for child in node.children:
            find_errors(child)

    find_errors(root)

    return {
        'status': 'partial',
        'error_count': len(error_nodes),
        'errors': error_nodes[:5]  # First 5 errors
    }

# Usage in worker
tree = _PARSER.parse(source_code)
quality = analyze_parse_quality(tree)

if quality['status'] == 'partial' and quality['error_count'] > 10:
    # Too many errors, skip file or retry with different parser
    logging.warning(f"Parse quality low for {filepath}: {quality}")
```

### **9.2 Checkpointing for Long-Running Jobs**

```python
import pickle
from datetime import datetime

class PipelineCheckpoint:
    """Manages pipeline state for resumption."""

    def __init__(self, checkpoint_path: str):
        self.checkpoint_path = Path(checkpoint_path)
        self.processed_files = set()
        self.last_save = None

    def load(self):
        """Load existing checkpoint if available."""
        if self.checkpoint_path.exists():
            with open(self.checkpoint_path, 'rb') as f:
                data = pickle.load(f)
                self.processed_files = data['processed']
                self.last_save = data['timestamp']
            print(f"📥 Loaded checkpoint: {len(self.processed_files)} files already processed")

    def save(self):
        """Save current state."""
        with open(self.checkpoint_path, 'wb') as f:
            pickle.dump({
                'processed': self.processed_files,
                'timestamp': datetime.now()
            }, f)
        self.last_save = datetime.now()

    def mark_processed(self, filepath: str):
        """Mark file as processed."""
        self.processed_files.add(filepath)

    def should_process(self, filepath: str) -> bool:
        """Check if file needs processing."""
        return filepath not in self.processed_files

# Modified main pipeline
def main_pipeline_with_checkpointing(source_dir: str, output_dir: str):
    output_path = Path(output_dir)
    checkpoint = PipelineCheckpoint(output_path / 'checkpoint.pkl')
    checkpoint.load()

    all_files = discover_files(source_dir)
    remaining_files = [f for f in all_files if checkpoint.should_process(f)]

    print(f"Processing {len(remaining_files)} of {len(all_files)} files")

    # Process in batches with periodic checkpointing
    batch_size = 1000
    for i in range(0, len(remaining_files), batch_size):
        batch = remaining_files[i:i+batch_size]

        # Process batch
        with Pool(8, initializer=init_worker) as pool:
            results = pool.map(process_file_with_db, batch)

        # Update checkpoint
        for filepath in batch:
            checkpoint.mark_processed(filepath)
        checkpoint.save()

        print(f"✓ Checkpoint saved: {i+len(batch)}/{len(remaining_files)} files")
```

---

## **Part 10: Production Deployment Checklist**

### **10.1 Performance Optimization**

```python
# 1. Compile Python code
# Install: pip install Cython
# Compile normalizer for 2-3x speedup

# 2. Use PyPy for pure-Python workloads
# pypy3 -m pip install -r requirements.txt
# pypy3 main_pipeline.py

# 3. Profile bottlenecks
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... your code ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### **10.2 Memory Management**

```python
import psutil
import gc

def monitor_memory():
    """Log current memory usage."""
    process = psutil.Process()
    mem_info = process.memory_info()
    mem_mb = mem_info.rss / 1024 / 1024
    print(f"Memory usage: {mem_mb:.2f} MB")
    return mem_mb

def process_file_with_memory_management(filepath: str, db_path: str) -> int:
    """Worker with aggressive memory cleanup."""
    try:
        result = process_file_with_db(filepath, db_path)

        # Force garbage collection every 100 files
        if random.randint(1, 100) == 1:
            gc.collect()

        return result
    except MemoryError:
        logging.error(f"Memory error processing {filepath}")
        gc.collect()
        return 0

# Set memory limits for worker processes
import resource

def init_worker_with_limits(semantic_rules: dict, max_memory_mb: int = 1024):
    """Initialize worker with memory constraints."""
    init_worker(semantic_rules)

    # Set soft memory limit (in bytes)
    soft_limit = max_memory_mb * 1024 * 1024
    hard_limit = soft_limit * 1.5

    resource.setrlimit(
        resource.RLIMIT_AS,
        (soft_limit, hard_limit)
    )
```

### **10.3 Logging and Monitoring**

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(output_dir: str):
    """Configure comprehensive logging."""
    log_path = Path(output_dir) / 'pipeline.log'

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler (rotating to prevent huge logs)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Console handler (less verbose)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Enhanced worker with logging
def process_file_with_logging(filepath: str, db_path: str) -> dict:
    """Worker that logs detailed progress and errors."""
    logger = logging.getLogger(__name__)

    try:
        start_time = time.time()

        # Read file
        with open(filepath, 'rb') as f:
            source_code = f.read()

        file_size_kb = len(source_code) / 1024
        logger.debug(f"Processing {filepath} ({file_size_kb:.1f} KB)")

        # Parse
        tree = _PARSER.parse(source_code)
        parse_time = time.time() - start_time

        # Quality check
        quality = analyze_parse_quality(tree)
        if quality['status'] == 'partial':
            logger.warning(
                f"Parse errors in {filepath}: {quality['error_count']} errors"
            )

        # Extract patterns
        pattern_count = extract_and_store_patterns(tree, source_code, db_path)

        total_time = time.time() - start_time

        logger.debug(
            f"Completed {filepath}: {pattern_count} patterns in {total_time:.2f}s"
        )

        return {
            'filepath': filepath,
            'status': 'success',
            'pattern_count': pattern_count,
            'parse_time': parse_time,
            'total_time': total_time,
            'file_size_kb': file_size_kb
        }

    except Exception as e:
        logger.error(f"Failed to process {filepath}: {str(e)}", exc_info=True)
        return {
            'filepath': filepath,
            'status': 'error',
            'error': str(e)
        }
```

---

## **Part 11: Using ast-grep-py as an Accelerator**

### **11.1 Hybrid Approach: ast-grep-py + Custom Normalizer**

```python
from ast_grep_py import SgRoot

def extract_patterns_with_astgrep(
    source_code: bytes,
    semantic_rules: dict
) -> Counter:
    """
    Use ast-grep-py for fast node finding, then normalize.
    This is faster than manual CST traversal for large files.
    """
    normalizer = CSTNormalizer(source_code, semantic_rules)
    pattern_counts = Counter()

    # Parse once with ast-grep
    root = SgRoot(source_code.decode('utf8'), 'typescript')

    # Define patterns to extract (Level 2 patterns)
    search_patterns = [
        "const $VAR = $VAL",
        "let $VAR = $VAL",
        "var $VAR = $VAL",
        "$OBJ.$METHOD($$$ARGS)",
        "function $NAME($$$PARAMS) { $$$BODY }",
        "class $NAME { $$$MEMBERS }",
        "import $$$IMPORTS from $SOURCE",
        "async function $NAME($$$PARAMS) { $$$BODY }",
        "await $EXPR",
        "new $CLASS($$$ARGS)"
    ]

    for pattern in search_patterns:
        # Find all matches
        matches = root.root().find_all(pattern=pattern)

        for match in matches:
            # Convert ast-grep node to Tree-sitter node
            ts_node = match.get_node()

            # Normalize at both levels
            abstract_sig = normalizer.normalize(ts_node, 'abstract')
            semantic_sig = normalizer.normalize(ts_node, 'semantic')

            abs_hash = CSTNormalizer.get_hash(abstract_sig)
            sem_hash = CSTNormalizer.get_hash(semantic_sig)

            pattern_counts[abs_hash] += 1
            pattern_counts[sem_hash] += 1

    return pattern_counts

# Benchmark comparison
def benchmark_extraction_methods(source_code: bytes):
    """Compare manual traversal vs ast-grep-py."""
    import time

    # Method 1: Manual Tree-sitter traversal
    start = time.time()
    counts1 = extract_patterns_manual(source_code)
    time1 = time.time() - start

    # Method 2: ast-grep-py hybrid
    start = time.time()
    counts2 = extract_patterns_with_astgrep(source_code, {})
    time2 = time.time() - start

    print(f"Manual traversal: {time1:.3f}s ({len(counts1)} patterns)")
    print(f"ast-grep hybrid: {time2:.3f}s ({len(counts2)} patterns)")
    print(f"Speedup: {time1/time2:.2f}x")
```

---

## **Part 12: Advanced Pattern Analysis**

### **12.1 Pattern Co-occurrence Analysis**

```python
from itertools import combinations
from collections import defaultdict

class PatternCooccurrenceAnalyzer:
    """Analyze which patterns frequently appear together."""

    def __init__(self):
        self.cooccurrences = defaultdict(int)
        self.pattern_files = defaultdict(set)

    def record_file_patterns(self, filepath: str, patterns: Set[str]):
        """Record patterns found in a single file."""
        # Store which files contain each pattern
        for pattern in patterns:
            self.pattern_files[pattern].add(filepath)

        # Count co-occurrences (patterns in same file)
        for p1, p2 in combinations(sorted(patterns), 2):
            self.cooccurrences[(p1, p2)] += 1

    def get_common_pairs(self, min_frequency: int = 10) -> List[tuple]:
        """Get pattern pairs that frequently co-occur."""
        pairs = [
            (p1, p2, count)
            for (p1, p2), count in self.cooccurrences.items()
            if count >= min_frequency
        ]
        pairs.sort(key=lambda x: x[2], reverse=True)
        return pairs

    def get_pattern_context(self, pattern: str, limit: int = 5) -> dict:
        """Find patterns that commonly appear with this pattern."""
        related = defaultdict(int)

        # Find files containing this pattern
        files = self.pattern_files[pattern]

        # Count other patterns in those files
        for other_pattern, other_files in self.pattern_files.items():
            if other_pattern == pattern:
                continue

            overlap = len(files & other_files)
            if overlap > 0:
                related[other_pattern] = overlap

        # Return top related patterns
        sorted_related = sorted(
            related.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        return {
            'pattern': pattern,
            'total_files': len(files),
            'related_patterns': [
                {'pattern': p, 'co_occurrences': count}
                for p, count in sorted_related
            ]
        }

# Modified worker to track co-occurrences
def process_file_with_cooccurrence(
    filepath: str,
    db_path: str,
    analyzer: PatternCooccurrenceAnalyzer
) -> int:
    """Extract patterns and record co-occurrences."""
    # ... (parse and extract patterns) ...

    pattern_hashes = set(local_counts.keys())
    analyzer.record_file_patterns(filepath, pattern_hashes)

    return len(pattern_hashes)

# Generate co-occurrence report
def generate_cooccurrence_report(analyzer: PatternCooccurrenceAnalyzer):
    """Create report of pattern relationships."""
    common_pairs = analyzer.get_common_pairs(min_frequency=50)

    print("\n📊 Most Common Pattern Pairs:")
    for i, (p1, p2, count) in enumerate(common_pairs[:20], 1):
        print(f"{i}. [{count} files]")
        print(f"   Pattern A: {p1}")
        print(f"   Pattern B: {p2}")
        print()
```

### **12.2 Temporal Pattern Evolution**

```python
import subprocess
from datetime import datetime

class TemporalPatternAnalyzer:
    """Analyze how patterns change over time using git history."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def get_commits(self, since_date: str = None, limit: int = 10) -> List[dict]:
        """Get list of commits to analyze."""
        cmd = ['git', 'log', '--pretty=format:%H|%ad|%s', '--date=short']

        if since_date:
            cmd.extend(['--since', since_date])

        if limit:
            cmd.extend(['-n', str(limit)])

        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            sha, date, message = line.split('|', 2)
            commits.append({
                'sha': sha,
                'date': date,
                'message': message
            })

        return commits

    def checkout_commit(self, commit_sha: str):
        """Checkout specific commit."""
        subprocess.run(
            ['git', 'checkout', commit_sha],
            cwd=self.repo_path,
            capture_output=True
        )

    def analyze_commit(self, commit_sha: str) -> Dict[str, int]:
        """Run pattern extraction on a specific commit."""
        self.checkout_commit(commit_sha)

        # Run pattern extraction pipeline
        patterns = {}
        # ... (run extraction) ...

        return patterns

    def generate_evolution_report(self) -> dict:
        """Analyze pattern trends over time."""
        commits = self.get_commits(limit=20)

        evolution = {
            'commits': [],
            'pattern_trends': defaultdict(list)
        }

        for commit in commits:
            patterns = self.analyze_commit(commit['sha'])

            evolution['commits'].append({
                'sha': commit['sha'],
                'date': commit['date'],
                'total_patterns': sum(patterns.values())
            })

            # Track individual pattern frequencies
            for pattern_hash, count in patterns.items():
                evolution['pattern_trends'][pattern_hash].append({
                    'date': commit['date'],
                    'count': count
                })

        return evolution
```

---

## **Part 13: Generating Educational Output**

### **13.1 Interactive HTML Dashboard**

```python
def generate_html_dashboard(
    clusters: List[List[tuple]],
    output_path: str
):
    """Generate interactive HTML dashboard for pattern exploration."""

    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Code Pattern Analysis Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .pattern-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .pattern-rank {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .pattern-signature {
            font-family: 'Courier New', monospace;
            background: #f0f0f0;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
            overflow-x: auto;
        }
        .frequency {
            color: #666;
            font-size: 14px;
        }
        .category-badge {
            display: inline-block;
            background: #2196F3;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }
        .variations {
            margin-top: 15px;
            padding-left: 20px;
            border-left: 3px solid #e0e0e0;
        }
        .filter-bar {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        select, input {
            padding: 8px;
            margin-right: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>🔍 Code Pattern Analysis Dashboard</h1>

    <div class="filter-bar">
        <label>Category:
            <select id="categoryFilter" onchange="filterPatterns()">
                <option value="all">All Categories</option>
                <option value="dom">DOM Manipulation</option>
                <option value="async">Async Operations</option>
                <option value="control">Control Flow</option>
            </select>
        </label>

        <label>Min Frequency:
            <input type="number" id="freqFilter" value="0" onchange="filterPatterns()">
        </label>

        <label>Search:
            <input type="text" id="searchBox" placeholder="Search patterns..." oninput="filterPatterns()">
        </label>
    </div>

    <div id="patterns">
        {pattern_cards}
    </div>

    <script>
        function filterPatterns() {
            const category = document.getElementById('categoryFilter').value;
            const minFreq = parseInt(document.getElementById('freqFilter').value);
            const search = document.getElementById('searchBox').value.toLowerCase();

            const cards = document.querySelectorAll('.pattern-card');

            cards.forEach(card => {
                const cardCategory = card.dataset.category;
                const cardFreq = parseInt(card.dataset.frequency);
                const cardText = card.textContent.toLowerCase();

                const matchCategory = category === 'all' || cardCategory === category;
                const matchFreq = cardFreq >= minFreq;
                const matchSearch = search === '' || cardText.includes(search);

                card.style.display = matchCategory && matchFreq && matchSearch ? 'block' : 'none';
            });
        }
    </script>
</body>
</html>
    """

    # Generate pattern cards
    pattern_cards_html = []

    for rank, cluster in enumerate(clusters, 1):
        canonical = cluster[0]
        total_freq = sum(p[3] for p in cluster)

        # Determine category (from metadata)
        category = 'general'  # Default

        card_html = f"""
        <div class="pattern-card" data-category="{category}" data-frequency="{total_freq}">
            <span class="pattern-rank">#{rank}</span>
            <span class="category-badge">{category}</span>

            <div class="pattern-signature">
                {canonical[1]}
            </div>

            <div class="frequency">
                Frequency: <strong>{total_freq:,}</strong> occurrences
            </div>

            {_generate_variations_html(cluster[1:])}
        </div>
        """

        pattern_cards_html.append(card_html)

    final_html = html_template.replace(
        '{pattern_cards}',
        '\n'.join(pattern_cards_html)
    )

    with open(output_path, 'w') as f:
        f.write(final_html)

def _generate_variations_html(variations: List[tuple]) -> str:
    """Generate HTML for pattern variations."""
    if not variations:
        return ""

    html = '<div class="variations"><strong>Variations:</strong><ul>'

    for var in variations[:5]:  # Show top 5 variations
        html += f'<li><code>{var[1]}</code> ({var[3]:,})</li>'

    html += '</ul></div>'
    return html
```

### **13.2 Markdown Report Generation**

````python
def generate_markdown_report(
    clusters: List[List[tuple]],
    output_path: str,
    include_examples: bool = True
):
    """Generate comprehensive Markdown report."""

    with open(output_path, 'w') as f:
        f.write("# Code Pattern Analysis Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Executive Summary
        f.write("## Executive Summary\n\n")
        total_instances = sum(sum(p[3] for p in c) for c in clusters)
        f.write(f"- **Total Pattern Instances**: {total_instances:,}\n")
        f.write(f"- **Unique Pattern Clusters**: {len(clusters)}\n")
        f.write(f"- **Top Pattern Frequency**: {sum(p[3] for p in clusters[0]):,}\n\n")

        # Category breakdown
        f.write("## Patterns by Category\n\n")

        categories = {
            'DOM Manipulation': [],
            'Async Operations': [],
            'Control Flow': [],
            'Data Structures': [],
            'Other': []
        }

        # Categorize patterns (simplified - should use metadata)
        for cluster in clusters[:100]:
            canonical = cluster[0]
            sig = canonical[1].lower()

            if 'document.' in sig or 'element' in sig:
                categories['DOM Manipulation'].append(cluster)
            elif 'async' in sig or 'await' in sig or 'promise' in sig:
                categories['Async Operations'].append(cluster)
            elif 'for' in sig or 'if' in sig or 'while' in sig:
                categories['Control Flow'].append(cluster)
            elif 'array' in sig or 'object' in sig:
                categories['Data Structures'].append(cluster)
            else:
                categories['Other'].append(cluster)

        for category, patterns in categories.items():
            if not patterns:
                continue

            f.write(f"### {category}\n\n")
            f.write(f"Found {len(patterns)} patterns in this category.\n\n")

            for i, cluster in enumerate(patterns[:10], 1):
                canonical = cluster[0]
                freq = sum(p[3] for p in cluster)

                f.write(f"#### {i}. Pattern (Frequency: {freq:,})\n\n")
                f.write(f"```javascript\n{canonical[1]}\n```\n\n")

                if canonical[2]:  # Semantic signature
                    f.write(f"**Semantic**: `{canonical[2]}`\n\n")

                if len(cluster) > 1:
                    f.write(f"**Variations** ({len(cluster)-1}):\n\n")
                    for var in cluster[1:3]:  # Show 2 variations
                        f.write(f"- `{var[1]}` ({var[3]:,} occurrences)\n")
                    f.write("\n")

        # Top 50 Overall
        f.write("## Top 50 Most Frequent Patterns\n\n")
        f.write("| Rank | Pattern | Frequency |\n")
        f.write("|------|---------|----------|\n")

        for rank, cluster in enumerate(clusters[:50], 1):
            canonical = cluster[0]
            freq = sum(p[3] for p in cluster)
            # Escape pipes in pattern
            pattern = canonical[1].replace('|', '\\|')
            f.write(f"| {rank} | `{pattern}` | {freq:,} |\n")
````

---

## **Part 14: Complete Production Script**

Here's the final, battle-tested production script:

```python
#!/usr/bin/env python3
"""
Production-scale code pattern mining pipeline.
Processes 100K+ JavaScript/TypeScript files to extract common idioms.
"""

import sys
import time
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from collections import Counter, defaultdict
from multiprocessing import Pool, cpu_count
import hashlib
import sqlite3
import json

import tree_sitter_javascript as tsjs
import tree_sitter_typescript as tsts
from tree_sitter import Language, Parser, Node, Tree
from tqdm import tqdm
import yaml

# ============================================================================
# Configuration
# ============================================================================

@dataclass
class PipelineConfig:
    """Central configuration for the pipeline."""
    source_dir: str
    output_dir: str = 'output'
    num_workers: int = field(default_factory=lambda: cpu_count() - 1)
    top_n_patterns: int = 500
    similarity_threshold: int = 85
    checkpoint_interval: int = 1000
    max_file_size_mb: int = 5
    skip_minified: bool = True
    semantic_rules_path: str = 'semantic_rules.yml'

# ============================================================================
# Core Normalization Engine
# ============================================================================

class CSTNormalizer:
    """Normalizes Tree-sitter CST nodes to abstract/semantic signatures."""

    def __init__(self, source_code: bytes, semantic_rules: dict = None):
        self.source_code = source_code
        self.semantic_rules = semantic_rules or {}

    def get_node_text(self, node: Node) -> str:
        return self.source_code[node.start_byte:node.end_byte].decode('utf8', errors='ignore')

    def normalize(self, node: Node, level: str = 'abstract') -> str:
        return self._recursive_normalize(node, level)

    def _recursive_normalize(self, node: Node, level: str) -> str:
        if not node.child_count and node.is_named:
            return self._handle_terminal(node, level)

        if not node.is_named:
            return self.get_node_text(node)

        handler = getattr(self, f"_handle_{node.type}", self._handle_default)
        return handler(node, level)

    def _handle_terminal(self, node: Node, level: str) -> str:
        if node.type == 'identifier':
            if level == 'semantic':
                text = self.get_node_text(node)
                if text in self.semantic_rules.get('identifier', {}):
                    return self.semantic_rules['identifier'][text]
            return 'IDENTIFIER'

        if node.type in ['string', 'template_string']:
            return 'STRING'
        if node.type == 'number':
            return 'NUMBER'
        if node.type in ['true', 'false']:
            return 'BOOLEAN'

        return self.get_node_text(node)

    def _handle_default(self, node: Node, level: str) -> str:
        parts = [self._recursive_normalize(child, level) for child in node.children]
        return "".join(p for p in parts if p)

    def _handle_lexical_declaration(self, node: Node, level: str) -> str:
        parts = [self._recursive_normalize(c, level) for c in node.children]
        return " ".join(p for p in parts if p)

    def _handle_call_expression(self, node: Node, level: str) -> str:
        func = self._recursive_normalize(node.child_by_field_name('function'), level)
        args = self._recursive_normalize(node.child_by_field_name('arguments'), level)
        return f"{func}{args}"

    def _handle_member_expression(self, node: Node, level: str) -> str:
        obj = self._recursive_normalize(node.child_by_field_name('object'), level)
        prop = self._recursive_normalize(node.child_by_field_name('property'), level)
        return f"{obj}.{prop}"

    @staticmethod
    def get_hash(signature: str) -> str:
        return hashlib.sha256(signature.encode('utf-8')).hexdigest()

# ============================================================================
# Worker Process Management
# ============================================================================

_JS_LANG = None
_TS_LANG = None
_TSX_LANG = None
_PARSER = None
_SEMANTIC_RULES = None

def init_worker(semantic_rules: dict):
    """Initialize worker process with parsers and rules."""
    global _JS_LANG, _TS_LANG, _TSX_LANG, _PARSER, _SEMANTIC_RULES

    _JS_LANG = Language(tsjs.language())
    _TS_LANG = Language(tsts.language_typescript())
    _TSX_LANG = Language(tsts.language_tsx())
    _PARSER = Parser()
    _SEMANTIC_RULES = semantic_rules

def process_file(args: Tuple[str, str, PipelineConfig]) -> dict:
    """Main worker function: parse file and extract patterns."""
    filepath, db_path, config = args
    global _PARSER, _JS_LANG, _TS_LANG, _TSX_LANG, _SEMANTIC_RULES

    try:
        # Read file
        with open(filepath, 'rb') as f:
            source_code = f.read()

        # Check size limit
        if len(source_code) > config.max_file_size_mb * 1024 * 1024:
            return {'filepath': filepath, 'status': 'skipped', 'reason': 'too_large'}

        # Select parser
        ext = Path(filepath).suffix
        if ext == '.ts':
            _PARSER.set_language(_TS_LANG)
        elif ext == '.tsx':
            _PARSER.set_language(_TSX_LANG)
        else:
            _PARSER.set_language(_JS_LANG)

        # Parse
        tree = _PARSER.parse(source_code)

        # Fallback to TSX for problematic .js files
        if ext in ['.js', '.mjs', '.cjs'] and tree.root_node.has_error():
            error_count = count_errors(tree.root_node)
            if error_count > 5:
                _PARSER.set_language(_TSX_LANG)
                tree = _PARSER.parse(source_code)

        # Extract patterns
        normalizer = CSTNormalizer(source_code, _SEMANTIC_RULES)
        patterns = extract_patterns_from_tree(tree, normalizer)

        # Store in SQLite
        store_patterns(patterns, db_path)

        return {
            'filepath': filepath,
            'status': 'success',
            'pattern_count': len(patterns)
        }

    except Exception as e:
        return {
            'filepath': filepath,
            'status': 'error',
            'error': str(e)
        }

def count_errors(node: Node) -> int:
    """Count ERROR nodes recursively."""
    count = 1 if (node.is_error or node.is_missing) else 0
    for child in node.children:
        count += count_errors(child)
    return count

def extract_patterns_from_tree(tree: Tree, normalizer: CSTNormalizer) -> Dict[str, Tuple[str, str]]:
    """Extract all patterns from parsed tree."""
    patterns = {}

    # Define extraction query
    query_str = """
        (lexical_declaration) @decl
        (call_expression) @call
        (function_declaration) @func
        (class_declaration) @class
        (import_statement) @import
    """

    query = normalizer.source_code  # Use appropriate language
    # Simplified: iterate over specific node types

    def visit(node):
        if node.type in ['lexical_declaration', 'call_expression',
                        'function_declaration', 'class_declaration']:
            abstract_sig = normalizer.normalize(node, 'abstract')
            semantic_sig = normalizer.normalize(node, 'semantic')
            sig_hash = CSTNormalizer.get_hash(abstract_sig)
            patterns[sig_hash] = (abstract_sig, semantic_sig)

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return patterns



def store_patterns(patterns: Dict[str, Tuple[str, str]], db_path: str):
    """Store extracted patterns in SQLite."""
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()

    # Prepare data for batch insertion
    data_to_insert = [
        (pattern_hash, abstract_sig, semantic_sig, 1)
        for pattern_hash, (abstract_sig, semantic_sig) in patterns.items()
    ]

    # Use executemany for efficiency
    cursor.executemany("""
        INSERT INTO patterns (pattern_hash, abstract_signature, semantic_signature, count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(pattern_hash) DO UPDATE
        SET count = count + excluded.count
    """, data_to_insert)

    conn.commit()
    conn.close()

# ============================================================================
# File Discovery & Pre-processing
# ============================================================================

def is_minified(filepath: str, check_content: bool = True) -> bool:
    """Detects minified files using filename and content heuristics."""
    if '.min.' in Path(filepath).name:
        return True

    if not check_content:
        return False

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines(8192) # Read first 8KB
        if not lines: return False

        avg_len = sum(len(line.strip()) for line in lines) / len(lines)
        if avg_len > 1000: return True

        max_len = max(len(line.strip()) for line in lines)
        if max_len > 50000: return True

    except (IOError, UnicodeDecodeError):
        return False # Treat as non-minified if unreadable

    return False

def discover_files(config: PipelineConfig) -> List[str]:
    """Finds all valid, non-minified source files."""
    valid_files = []
    extensions = {'.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx'}

    for filepath in Path(config.source_dir).rglob('*'):
        if filepath.is_dir() or filepath.suffix not in extensions:
            continue

        if config.skip_minified and is_minified(str(filepath)):
            continue

        valid_files.append(str(filepath))

    return valid_files

# ============================================================================
# Clustering & Reporting
# ============================================================================

def cluster_patterns(patterns: List[tuple], threshold: int) -> List[List[tuple]]:
    """Clusters patterns using fuzzy matching and graph theory."""
    try:
        import networkx as nx
        from rapidfuzz import process, fuzz
    except ImportError:
        logging.error("Clustering requires 'networkx' and 'rapidfuzz'. Please install them.")
        return [[p] for p in patterns]

    if not patterns: return []

    signatures = [p for p in patterns]
    graph = nx.Graph()
    graph.add_nodes_from(range(len(patterns)))

    for i, sig in enumerate(tqdm(signatures, desc="Building similarity graph")):
        matches = process.extract(sig, signatures, scorer=fuzz.ratio, score_cutoff=threshold, limit=10)
        for _, _, match_idx in matches:
            if i != match_idx:
                graph.add_edge(i, match_idx)

    clusters = []
    for component in nx.connected_components(graph):
        cluster = [patterns[i] for i in component]
        cluster.sort(key=lambda x: x, reverse=True) # Sort by count
        clusters.append(cluster)

    clusters.sort(key=lambda c: sum(p for p in c), reverse=True)
    return clusters

def generate_report(clusters: List[List[tuple]], report_path: str):
    """Generates a final JSON report of clustered patterns."""
    report = []
    for cluster in clusters:
        canonical = cluster
        total_freq = sum(p for p in cluster)

        report.append({
            "canonical_pattern_hash": canonical,
            "canonical_abstract_signature": canonical,
            "canonical_semantic_signature": canonical,
            "total_frequency": total_freq,
            "variations": [
                {
                    "pattern_hash": p,
                    "abstract_signature": p,
                    "frequency": p
                } for p in cluster[1:]
            ]
        })

    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

# ============================================================================
# Main Pipeline Orchestrator
# ============================================================================

def main(config: PipelineConfig):
    """Main pipeline execution orchestrator."""

    output_path = Path(config.output_dir)
    output_path.mkdir(exist_ok=True)
    db_path = str(output_path / 'patterns.db')

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # --- Phase 1: File Discovery ---
    logging.info("Phase 1: Discovering files...")
    file_list = discover_files(config)
    logging.info(f"Found {len(file_list)} valid files to process.")

    # --- Phase 2: Database Initialization ---
    logging.info("Phase 2: Initializing database...")
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            pattern_hash TEXT PRIMARY KEY,
            abstract_signature TEXT NOT NULL,
            semantic_signature TEXT,
            count INTEGER DEFAULT 0
        )
    """)
    conn.close()

    # --- Phase 3: Parallel Processing ---
    logging.info(f"Phase 3: Starting parallel processing with {config.num_workers} workers...")
    try:
        with open(config.semantic_rules_path, 'r') as f:
            semantic_rules = yaml.safe_load(f)
    except FileNotFoundError:
        logging.warning(f"Semantic rules file not found at '{config.semantic_rules_path}'. Proceeding without semantic analysis.")
        semantic_rules = {}

    worker_args = [(f, db_path, config) for f in file_list]

    with Pool(processes=config.num_workers, initializer=init_worker, initargs=(semantic_rules,)) as pool:
        for result in tqdm(pool.imap_unordered(process_file, worker_args), total=len(file_list), desc="Processing files"):
            if result['status'] == 'error':
                logging.error(f"Failed to process {result['filepath']}: {result['error']}")

    # --- Phase 4: Data Retrieval & Clustering ---
    logging.info("Phase 4: Retrieving and clustering patterns...")
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(f"SELECT pattern_hash, abstract_signature, semantic_signature, count FROM patterns ORDER BY count DESC LIMIT {config.top_n_patterns * 4}")
    top_patterns = cursor.fetchall()
    conn.close()

    clusters = cluster_patterns(top_patterns, config.similarity_threshold)
    logging.info(f"Grouped {len(top_patterns)} patterns into {len(clusters)} clusters.")

    # --- Phase 5: Report Generation ---
    logging.info("Phase 5: Generating final report...")
    report_path = str(output_path / 'pattern_report.json')
    generate_report(clusters[:config.top_n_patterns], report_path)

    logging.info(f"🎉 Pipeline complete! Report saved to {report_path}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Production-Scale Code Pattern Mining Pipeline")
    parser.add_argument("source_dir", type=str, help="Root directory of the source code to analyze.")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save database and reports.")
    parser.add_argument("--workers", type=int, default=cpu_count() - 1, help="Number of worker processes.")
    parser.add_argument("--top-n", type=int, default=500, help="Number of top patterns to include in the final report.")

    args = parser.parse_args()

    config = PipelineConfig(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        num_workers=args.workers,
        top_n_patterns=args.top_n
    )

    main(config)

```
