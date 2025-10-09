#!/usr/bin/env python3
"""
Enhanced Code Pattern Mining System (Backward Compatible)
Extracts JavaScript/TypeScript patterns with improved semantic analysis.

Key improvements:
- Preserves semantic anchors (console, Promise, React, etc.)
- Better pattern complexity filtering
- Enhanced categorization
- SAME output format as original (backward compatible)

Usage:
    python pattern_miner.py <repo_path> [--top-k 200] [--format json]
"""

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import sys

try:
    from tree_sitter import Language, Parser, Node, Tree
    import tree_sitter_javascript as tsjs
    import tree_sitter_typescript as tsts
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install tree-sitter tree-sitter-javascript tree-sitter-typescript")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    class tqdm:
        def __init__(self, iterable=None, **kwargs):
            self.iterable = iterable
        def __iter__(self):
            return iter(self.iterable)
        def update(self, n=1):
            pass


# ============================================================================
# Data Models (UNCHANGED - Backward Compatible)
# ============================================================================

@dataclass
class PatternOccurrence:
    """Records where a pattern was found."""
    file_path: str
    line_number: int
    concrete_code: str


@dataclass
class CodePattern:
    """Represents a normalized code pattern with multi-level abstraction."""
    pattern_hash: str
    abstract_signature: str
    semantic_signature: Optional[str]
    node_type: str
    category: str
    frequency: int
    examples: List[PatternOccurrence]


# ============================================================================
# Semantic Anchors - NEW: Preserve Important APIs
# ============================================================================

SEMANTIC_ANCHORS = {
    # Preserve these identifiers as-is (don't abstract them)
    'console', 'Promise', 'Array', 'Object', 'Math', 'JSON', 'Date',
    'React', 'useState', 'useEffect', 'useContext', 'useCallback', 'useMemo', 'useRef',
    'expect', 'describe', 'it', 'test', 'beforeEach', 'afterEach', 'jest', 'vi',
    'document', 'window', 'localStorage', 'sessionStorage',
    'fetch', 'axios', 'express', 'req', 'res',
    'Error', 'TypeError', 'ReferenceError',
}

METHOD_SEMANTICS = {
    # Array methods
    'map': 'ARRAY_TRANSFORM',
    'filter': 'ARRAY_FILTER',
    'reduce': 'ARRAY_REDUCE',
    'forEach': 'ARRAY_ITERATE',
    'find': 'ARRAY_SEARCH',
    'findIndex': 'ARRAY_SEARCH',
    'some': 'ARRAY_TEST',
    'every': 'ARRAY_TEST',
    'includes': 'ARRAY_TEST',
    'slice': 'ARRAY_SLICE',
    'splice': 'ARRAY_MUTATE',
    'push': 'ARRAY_MUTATE',
    'pop': 'ARRAY_MUTATE',
    'shift': 'ARRAY_MUTATE',
    'unshift': 'ARRAY_MUTATE',
    'join': 'ARRAY_TO_STRING',
    
    # Promise methods
    'then': 'PROMISE_CHAIN',
    'catch': 'ERROR_HANDLER',
    'finally': 'CLEANUP',
    'all': 'PROMISE_COMBINE',
    'race': 'PROMISE_COMBINE',
    'resolve': 'PROMISE_CREATE',
    'reject': 'PROMISE_CREATE',
    
    # Object methods
    'keys': 'OBJECT_KEYS',
    'values': 'OBJECT_VALUES',
    'entries': 'OBJECT_ENTRIES',
    'assign': 'OBJECT_MERGE',
    'create': 'OBJECT_CREATE',
    'freeze': 'OBJECT_IMMUTABLE',
    
    # Testing assertions
    'toBe': 'ASSERTION',
    'toEqual': 'ASSERTION',
    'toHaveBeenCalled': 'SPY_ASSERTION',
    'toHaveBeenCalledWith': 'SPY_ASSERTION',
    'toHaveLength': 'ASSERTION',
    'toContain': 'ASSERTION',
}


# ============================================================================
# Multi-Dialect Parser (UNCHANGED)
# ============================================================================

class MultiDialectParser:
    """Handles JS, JSX, TS, TSX with intelligent fallback parsing."""
    
    def __init__(self):
        self.js_lang = Language(tsjs.language())
        self.ts_lang = Language(tsts.language_typescript())
        self.tsx_lang = Language(tsts.language_tsx())
        
        self.js_parser = Parser(self.js_lang)
        self.ts_parser = Parser(self.ts_lang)
        self.tsx_parser = Parser(self.tsx_lang)
    
    def parse_file(self, filepath: Path) -> Tuple[Optional[Tree], Optional[bytes], Optional[str]]:
        """Parse file with appropriate grammar and fallback. Returns (tree, source_code, error)."""
        suffix = filepath.suffix.lower()
        
        try:
            with open(filepath, 'rb') as f:
                source_code = f.read()
            
            if b'\x00' in source_code[:1024]:
                return None, None, "Binary file"
            
            if suffix in ['.ts']:
                tree = self.ts_parser.parse(source_code)
            elif suffix in ['.tsx']:
                tree = self.tsx_parser.parse(source_code)
            else:
                tree = self.js_parser.parse(source_code)
            
            if suffix in ['.js', '.mjs', '.cjs', '.jsx'] and tree.root_node.has_error:
                error_count = self._count_errors(tree.root_node)
                if error_count > 5:
                    tree = self.tsx_parser.parse(source_code)
            
            error_msg = "Partial parse" if tree.root_node.has_error else None
            return tree, source_code, error_msg
            
        except Exception as e:
            return None, None, f"Parse error: {str(e)[:50]}"
    
    def _count_errors(self, node: Node) -> int:
        count = 1 if node.is_error or node.is_missing else 0
        for child in node.children:
            count += self._count_errors(child)
        return count


# ============================================================================
# Enhanced CST Normalizer - IMPROVED LOGIC
# ============================================================================

class CSTNormalizer:
    """Normalizes CST nodes with preserved semantic anchors."""
    
    PATTERN_NODE_TYPES = {
        'call_expression',
        'lexical_declaration',
        'variable_declaration',
        'arrow_function',
        'function_declaration',
        'method_definition',
        'assignment_expression',
        'member_expression',
        'await_expression',
        'for_in_statement',
        'for_of_statement',
        'if_statement',
        'try_statement',
        'return_statement',
        'class_declaration',
        'new_expression',
        'import_statement',
        'export_statement',
    }
    
    def __init__(self):
        self.semantic_rules = self._load_semantic_rules()
        self.categories = self._load_categories()
    
    def _load_semantic_rules(self) -> Dict[str, Dict[str, str]]:
        """Load semantic mapping rules."""
        return {
            'identifier': dict.fromkeys(SEMANTIC_ANCHORS, lambda x: x),  # Preserve as-is
            'method': METHOD_SEMANTICS,
        }
    
    def _load_categories(self) -> Dict[str, List[str]]:
        """Enhanced pattern categories."""
        return {
            'DATA_FETCHING': ['fetch', 'axios', 'FETCH_API', 'XHR_API', 'HTTP_LIB', 'await', 'response', 'json'],
            'STATE_MANAGEMENT': ['useState', 'useReducer', 'setState', 'REACT_HOOK', 'state'],
            'ASYNC_OPERATIONS': ['async', 'await', 'PROMISE', 'FETCH_API', 'then', 'catch'],
            'ARRAY_OPERATIONS': ['ARRAY_TRANSFORM', 'ARRAY_FILTER', 'ARRAY_REDUCE', 'ARRAY_ITERATE', 'ARRAY_SEARCH', 'map', 'filter', 'reduce'],
            'ERROR_HANDLING': ['try', 'catch', 'throw', 'Error', 'ERROR_HANDLER'],
            'CONTROL_FLOW': ['if', 'for', 'while', 'switch', 'return'],
            'VARIABLE_DECLARATIONS': ['const', 'let', 'var'],
            'FUNCTION_DEFINITIONS': ['function', 'arrow_function', '=>'],
            'REACT_PATTERNS': ['React', 'REACT_HOOK', 'useState', 'useEffect', 'jsx'],
            'TEST_PATTERNS': ['expect', 'describe', 'it', 'test', 'ASSERTION', 'SPY_ASSERTION'],
            'DOM_MANIPULATION': ['document', 'window', 'DOM_METHOD', 'querySelector', 'getElementById'],
            'OBJECT_OPERATIONS': ['OBJECT_KEYS', 'OBJECT_VALUES', 'OBJECT_ENTRIES', 'OBJECT_MERGE', 'Object'],
        }
    
    def should_extract(self, node: Node) -> bool:
        """Check if node should be extracted as a pattern."""
        if node.type not in self.PATTERN_NODE_TYPES or node.has_error:
            return False
        
        # NEW: Filter by complexity
        complexity = self._calculate_complexity(node)
        return complexity >= 2  # Must be at least "simple" complexity
    
    def _calculate_complexity(self, node: Node) -> int:
        """Calculate pattern complexity (1=trivial, 2=simple, 3=compound, 4=idiom)."""
        depth = self._get_depth(node)
        child_count = node.child_count
        
        if depth <= 1 and child_count <= 2:
            return 1  # Trivial
        elif depth <= 2 and child_count <= 4:
            return 2  # Simple
        elif depth <= 3 or child_count <= 8:
            return 3  # Compound
        else:
            return 4  # Idiom
    
    def _get_depth(self, node: Node, max_depth: int = 5) -> int:
        """Calculate tree depth."""
        if node.child_count == 0 or max_depth == 0:
            return 1
        return 1 + max(self._get_depth(child, max_depth - 1) for child in node.children)
    
    def normalize(self, node: Node, source_code: bytes, level: str = "abstract") -> str:
        """Convert CST node to normalized signature."""
        self.source_code = source_code
        signature = self._recursive_normalize(node, level)
        return ' '.join(signature.split())
    
    def _recursive_normalize(self, node: Node, level: str) -> str:
        """Core recursive normalization."""
        if node.type == "ERROR" or node.has_error:
            return ""
        
        if node.child_count == 0:
            return self._handle_terminal(node, level)
        
        handler = getattr(self, f"_handle_{node.type}", self._handle_default)
        return handler(node, level)
    
    def _get_text(self, node: Node) -> str:
        return self.source_code[node.start_byte:node.end_byte].decode('utf8', errors='ignore')
    
    def _handle_terminal(self, node: Node, level: str) -> str:
        """ENHANCED: Handle leaf nodes with semantic preservation."""
        text = self._get_text(node)
        
        if node.type == 'identifier':
            # NEW: Preserve semantic anchors
            if level == 'semantic' and text in SEMANTIC_ANCHORS:
                return text
            return 'IDENTIFIER'
        elif node.type in ['string', 'template_string']:
            return 'STRING'
        elif node.type == 'number':
            return 'NUMBER'
        elif node.type in ['true', 'false']:
            return 'BOOLEAN'
        elif node.type in ['null', 'undefined']:
            return node.type.upper()
        else:
            return text
    
    def _handle_call_expression(self, node: Node, level: str) -> str:
        """Handle: func(args)"""
        function = node.child_by_field_name('function')
        arguments = node.child_by_field_name('arguments')
        
        func_sig = self._recursive_normalize(function, level) if function else 'FUNCTION'
        args_sig = self._recursive_normalize(arguments, level) if arguments else '()'
        
        return f"{func_sig}{args_sig}"
    
    def _handle_member_expression(self, node: Node, level: str) -> str:
        """ENHANCED: Handle obj.property with semantic enrichment."""
        obj = node.child_by_field_name('object')
        prop = node.child_by_field_name('property')
        
        obj_sig = self._recursive_normalize(obj, level) if obj else 'OBJECT'
        
        if prop and level == 'semantic':
            prop_text = self._get_text(prop)
            # NEW: Enrich common methods
            if prop_text in METHOD_SEMANTICS:
                prop_sig = METHOD_SEMANTICS[prop_text]
            elif prop_text in SEMANTIC_ANCHORS:
                prop_sig = prop_text
            else:
                prop_sig = self._recursive_normalize(prop, level)
        else:
            prop_sig = self._recursive_normalize(prop, level) if prop else 'PROPERTY'
        
        return f"{obj_sig}.{prop_sig}"
    
    def _handle_lexical_declaration(self, node: Node, level: str) -> str:
        """Handle: const/let/var x = value"""
        parts = []
        for child in node.children:
            if child.type in ['const', 'let', 'var']:
                parts.append(child.type)
            elif child.type == 'variable_declarator':
                name = child.child_by_field_name('name')
                value = child.child_by_field_name('value')
                
                if name:
                    parts.append(self._recursive_normalize(name, level))
                if value:
                    parts.append('=')
                    parts.append(self._recursive_normalize(value, level))
        
        return ' '.join(parts)
    
    def _handle_arrow_function(self, node: Node, level: str) -> str:
        """Handle: (params) => body"""
        params = node.child_by_field_name('parameters')
        params_sig = self._recursive_normalize(params, level) if params else '()'
        return f"{params_sig} => BODY"
    
    def _handle_arguments(self, node: Node, level: str) -> str:
        """Handle function arguments."""
        args = []
        for child in node.children:
            if child.type not in ['(', ')', ',']:
                arg_sig = self._recursive_normalize(child, level)
                if arg_sig:
                    args.append(arg_sig)
        return f"({', '.join(args)})" if args else "()"
    
    def _handle_await_expression(self, node: Node, level: str) -> str:
        """Handle: await expr"""
        expr = node.child_by_field_name('argument')
        expr_sig = self._recursive_normalize(expr, level) if expr else 'EXPRESSION'
        return f"await {expr_sig}"
    
    def _handle_new_expression(self, node: Node, level: str) -> str:
        """Handle: new Constructor()"""
        constructor = node.child_by_field_name('constructor')
        arguments = node.child_by_field_name('arguments')
        
        const_sig = self._recursive_normalize(constructor, level) if constructor else 'CLASS'
        args_sig = self._recursive_normalize(arguments, level) if arguments else '()'
        
        return f"new {const_sig}{args_sig}"
    
    def _handle_default(self, node: Node, level: str) -> str:
        """Default: join normalized children."""
        parts = [self._recursive_normalize(child, level) for child in node.children]
        return ' '.join(p for p in parts if p and p.strip())
    
    def categorize_pattern(self, abstract_sig: str, semantic_sig: str, node_type: str) -> str:
        """ENHANCED: Better category determination."""
        sig_check = (semantic_sig or abstract_sig).lower()
        
        # Score each category
        category_scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for kw in keywords if kw.lower() in sig_check)
            if score > 0:
                category_scores[category] = score
        
        # Return highest scoring category
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        
        # Fallback based on node type
        if 'call' in node_type:
            return 'FUNCTION_CALLS'
        elif 'declaration' in node_type:
            return 'DECLARATIONS'
        elif 'expression' in node_type:
            return 'EXPRESSIONS'
        else:
            return 'OTHER'
    
    @staticmethod
    def hash_signature(signature: str) -> str:
        """Generate stable hash."""
        return hashlib.sha256(signature.encode('utf8')).hexdigest()[:16]
    
    def is_trivial(self, signature: str, frequency: int) -> bool:
        """ENHANCED: Better trivial pattern filtering."""
        # Filter very short patterns
        if len(signature) < 5:
            return True
        
        # Must appear at least twice
        if frequency < 2:
            return True
        
        # Filter bare identifiers/values
        trivial_patterns = {
            'IDENTIFIER', 'VALUE', 'FUNCTION', 'EXPRESSION', 'STATEMENT',
            'OBJECT', 'PROPERTY', 'BODY', 'ARGUMENT'
        }
        if signature in trivial_patterns:
            return True
        
        # NEW: Filter single property access without semantic meaning
        if signature.count('.') == 1 and 'IDENTIFIER.' in signature and signature.endswith('IDENTIFIER'):
            return True
        
        return False


# ============================================================================
# Pattern Mining Engine (MINIMAL CHANGES)
# ============================================================================

class PatternMiner:
    """Main mining engine - backward compatible."""
    
    def __init__(self, repo_path: Path, max_file_size_mb: float = 2.0):
        self.repo_path = Path(repo_path)
        self.max_file_size = max_file_size_mb * 1024 * 1024
        self.parser = MultiDialectParser()
        self.normalizer = CSTNormalizer()
        self.patterns: Dict[str, CodePattern] = {}
        self.stats = {
            'files_processed': 0,
            'files_skipped': 0,
            'skip_reasons': Counter(),
            'patterns_extracted': 0,
            'parse_errors': 0,
        }
    
    def discover_files(self) -> List[Path]:
        """Find all JS/TS files with intelligent filtering."""
        ignore_patterns = {
            'node_modules', 'dist', 'build', '.git', 'coverage', 'vendor',
            '.next', '.nuxt', 'out', 'public', '__pycache__', '.cache',
            'tmp', 'temp', '.venv', 'venv', 'bower_components',
        }
        
        files = []
        for ext in ['*.js', '*.jsx', '*.ts', '*.tsx', '*.mjs', '*.cjs']:
            for filepath in self.repo_path.rglob(ext):
                try:
                    relative_path = filepath.relative_to(self.repo_path)
                    if any(ignored in relative_path.parts for ignored in ignore_patterns):
                        continue
                except ValueError:
                    continue
                
                if '.min.' in filepath.name or '-min.' in filepath.name:
                    self.stats['skip_reasons']['minified'] += 1
                    continue
                
                try:
                    if filepath.stat().st_size > self.max_file_size:
                        self.stats['skip_reasons']['too_large'] += 1
                        continue
                except:
                    continue
                
                if self._is_likely_minified(filepath):
                    self.stats['skip_reasons']['minified_content'] += 1
                    continue
                
                files.append(filepath)
        
        return sorted(files)
    
    def _is_likely_minified(self, filepath: Path) -> bool:
        """Fast heuristic check for minification."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline()
                if len(first_line) > 500:
                    return True
        except:
            pass
        return False
    
    def extract_patterns_from_file(self, filepath: Path) -> bool:
        """Extract patterns from a single file."""
        tree, source_code, error = self.parser.parse_file(filepath)
        
        if not tree or not source_code:
            self.stats['files_skipped'] += 1
            self.stats['skip_reasons'][error or 'unknown'] += 1
            return False
        
        try:
            self._traverse_and_extract(tree.root_node, source_code, filepath)
            self.stats['files_processed'] += 1
            
            if error:
                self.stats['parse_errors'] += 1
            
            return True
        except Exception as e:
            self.stats['files_skipped'] += 1
            self.stats['skip_reasons']['extraction_error'] += 1
            return False
    
    def _traverse_and_extract(self, node: Node, source_code: bytes, filepath: Path):
        """Recursively extract patterns."""
        if self.normalizer.should_extract(node):
            self._record_pattern(node, source_code, filepath)
        
        for child in node.children:
            self._traverse_and_extract(child, source_code, filepath)
    
    def _record_pattern(self, node: Node, source_code: bytes, filepath: Path):
        """ENHANCED: Record pattern with semantic grouping."""
        try:
            # Generate both levels
            abstract_sig = self.normalizer.normalize(node, source_code, 'abstract')
            semantic_sig = self.normalizer.normalize(node, source_code, 'semantic')
            
            if not abstract_sig:
                return
            
            # NEW: Use semantic signature for grouping when available
            grouping_sig = semantic_sig if semantic_sig and semantic_sig != abstract_sig else abstract_sig
            pattern_hash = self.normalizer.hash_signature(grouping_sig)
            
            # Capture concrete code
            concrete = source_code[node.start_byte:node.end_byte].decode('utf8', errors='ignore')[:200]
            line_num = node.start_point[0] + 1
            
            occurrence = PatternOccurrence(
                file_path=str(filepath.relative_to(self.repo_path)),
                line_number=line_num,
                concrete_code=concrete
            )
            
            if pattern_hash not in self.patterns:
                category = self.normalizer.categorize_pattern(abstract_sig, semantic_sig, node.type)
                self.patterns[pattern_hash] = CodePattern(
                    pattern_hash=pattern_hash,
                    abstract_signature=abstract_sig,
                    semantic_signature=semantic_sig,
                    node_type=node.type,
                    category=category,
                    frequency=0,
                    examples=[]
                )
            
            pattern = self.patterns[pattern_hash]
            pattern.frequency += 1
            
            if len(pattern.examples) < 5:
                pattern.examples.append(occurrence)
            
            self.stats['patterns_extracted'] += 1
            
        except Exception:
            pass
    
    def mine_repository(self) -> List[CodePattern]:
        """Main mining orchestration."""
        print(f"🔍 Discovering files in {self.repo_path}...")
        files = self.discover_files()
        print(f"📁 Found {len(files)} files to analyze")
        
        if not files:
            print("❌ No valid files found!")
            return []
        
        print("\n⚙️  Extracting patterns...")
        for filepath in tqdm(files, desc="Processing files", unit="file"):
            self.extract_patterns_from_file(filepath)
        
        # Filter trivial patterns
        filtered_patterns = [
            p for p in self.patterns.values()
            if not self.normalizer.is_trivial(p.abstract_signature, p.frequency)
        ]
        
        print(f"\n✅ Extracted {len(filtered_patterns)} unique patterns")
        print(f'📊 Files processed: {self.stats["files_processed"]}')
        
        if self.stats['files_skipped'] > 0:
            print(f'⚠️  Files skipped: {self.stats["files_skipped"]}')
            for reason, count in self.stats['skip_reasons'].most_common(5):
                print(f"   - {reason}: {count}")
        
        if self.stats['parse_errors'] > 0:
            print(f'⚠️  Files with parse errors: {self.stats["parse_errors"]}')
        
        return sorted(filtered_patterns, key=lambda p: p.frequency, reverse=True)
    
    # ============================================================================
    # Export Methods (UNCHANGED - Backward Compatible)
    # ============================================================================
    
    def export_to_json(self, patterns: List[CodePattern], output_path: Path, top_k: int):
        """Export to JSON - SAME FORMAT AS ORIGINAL."""
        total_occurrences = sum(p.frequency for p in patterns)
        
        output = {
            'metadata': {
                'repository': str(self.repo_path),
                'total_patterns': len(patterns),
                'total_occurrences': total_occurrences,
                'top_k': min(top_k, len(patterns)),
                'files_processed': self.stats['files_processed'],
                'files_skipped': self.stats['files_skipped'],
                'files_with_errors': self.stats['parse_errors'],
            },
            'patterns': [
                {
                    'rank': i + 1,
                    'hash': p.pattern_hash,
                    'abstract_signature': p.abstract_signature,
                    'semantic_signature': p.semantic_signature,
                    'node_type': p.node_type,
                    'category': p.category,
                    'frequency': p.frequency,
                    'percentage': round(p.frequency / total_occurrences * 100, 2),
                    'examples': [asdict(ex) for ex in p.examples],
                }
                for i, p in enumerate(patterns[:top_k])
            ],
        }
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f'💾 Exported top {len(output["patterns"])} patterns to {output_path}')
    
    def export_to_markdown(self, patterns: List[CodePattern], output_path: Path, top_k: int):
        """Export Markdown report - SAME FORMAT AS ORIGINAL."""
        total_occurrences = sum(p.frequency for p in patterns)
        
        by_category = defaultdict(list)
        for p in patterns[:top_k]:
            by_category[p.category].append(p)
        
        with open(output_path, 'w') as f:
            f.write("# 📊 Code Pattern Analysis\n\n")
            f.write(f"**Repository:** `{self.repo_path}`\n\n")
            f.write(f'**Files Processed:** {self.stats["files_processed"]}\n\n')
            f.write(f"**Total Unique Patterns:** {len(patterns)}\n\n")
            f.write(f"**Total Occurrences:** {total_occurrences:,}\n\n")
            f.write("---\n\n")
            
            f.write("## 🔑 Category Summary\n\n")
            f.write("| Category | Patterns | Total Occurrences |\n")
            f.write("|----------|----------|------------------|\n")
            for category in sorted(by_category.keys()):
                cat_patterns = by_category[category]
                cat_freq = sum(p.frequency for p in cat_patterns)
                f.write(f"| {category} | {len(cat_patterns)} | {cat_freq:,} |\n")
            f.write("\n---\n\n")
            
            overall_rank = 1
            for category in sorted(by_category.keys()):
                f.write(f"## {category}\n\n")
                
                for pattern in by_category[category]:
                    percentage = round(pattern.frequency / total_occurrences * 100, 2)
                    f.write(f"### {overall_rank}. {pattern.abstract_signature}\n\n")
                    f.write(f"- **Frequency:** {pattern.frequency:,} ({percentage}%)\n")
                    f.write(f"- **Node Type:** `{pattern.node_type}`\n")
                    
                    if pattern.semantic_signature and pattern.semantic_signature != pattern.abstract_signature:
                        f.write(f"- **Semantic:** `{pattern.semantic_signature}`\n")
                    
                    f.write("\n")
                    
                    if pattern.examples:
                        f.write("**Examples:**\n\n")
                        for ex in pattern.examples[:2]:
                            f.write(f"```javascript\n{ex.concrete_code}\n```\n")
                            f.write(f"*{ex.file_path}:{ex.line_number}*\n\n")
                    
                    overall_rank += 1
                
                f.write("---\n\n")
        
        print(f"📄 Exported categorized patterns to {output_path}")


# ============================================================================
# Main Entry Point (UNCHANGED)
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Code Pattern Mining System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pattern_miner.py /path/to/repo
  python pattern_miner.py /path/to/repo --top-k 200 --format markdown
  python pattern_miner.py /path/to/repo --output results --min-freq 5
        """
    )
    parser.add_argument('repo_path', type=str, help='Path to the repository')
    parser.add_argument(
        '--top-k',
        type=int,
        default=200,
        help='Number of top patterns to export (default: 200)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='patterns',
        help='Output file name without extension (default: patterns)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'all'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--max-file-size',
        type=float,
        default=2.0,
        help='Maximum file size in MB (default: 2.0)'
    )
    parser.add_argument(
        '--min-freq',
        type=int,
        default=2,
        help='Minimum frequency to include pattern (default: 2)'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        print(f"❌ Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    print("=" * 70)
    print("🔬 Enhanced Code Pattern Miner")
    print("=" * 70)
    
    # Run the miner
    start_time = time.time()
    miner = PatternMiner(repo_path, max_file_size_mb=args.max_file_size)
    patterns = miner.mine_repository()
    
    # Filter by minimum frequency
    if args.min_freq > 1:
        patterns = [p for p in patterns if p.frequency >= args.min_freq]
        print(f"🔍 Filtered to {len(patterns)} patterns (min frequency: {args.min_freq})")
    
    if not patterns:
        print("❌ No patterns found!")
        sys.exit(1)
    
    # Export results
    output_base = Path(args.output)
    print("\n📤 Exporting results...")
    
    if args.format in ['json', 'all']:
        json_path = output_base.with_suffix('.json')
        miner.export_to_json(patterns, json_path, args.top_k)
    
    if args.format in ['markdown', 'all']:
        md_path = output_base.with_suffix('.md')
        miner.export_to_markdown(patterns, md_path, args.top_k)
    
    elapsed = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 70)
    print("📈 Top 15 Most Common Patterns:")
    print("=" * 70)
    total = sum(p.frequency for p in patterns)
    for i, p in enumerate(patterns[:15], 1):
        pct = round(p.frequency / total * 100, 1)
        print(f"{i:2d}. [{p.frequency:5d}x | {pct:5.1f}%] {p.abstract_signature[:55]}")
        print(f"    Category: {p.category}")
        if p.semantic_signature and p.semantic_signature != p.abstract_signature:
            semantic_display = p.semantic_signature[:55]
            print(f"    Semantic: {semantic_display}")
    
    print(f"\n⏱️  Total time: {elapsed:.1f}s")
    print("✨ Done!")


if __name__ == "__main__":
    main()