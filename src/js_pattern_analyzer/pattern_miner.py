#!/usr/bin/env python3
"""
Enhanced Code Pattern Mining System
Extracts JavaScript/TypeScript patterns with multi-level abstraction and production-grade analysis.

Usage:
    python enhanced_pattern_miner.py <repo_path> [--workers 4] [--top-k 200]
"""

import argparse
import hashlib
import json
import csv
import pickle
import sqlite3
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from multiprocessing import Pool, cpu_count
import sys

try:
    from tree_sitter import Language, Parser, Node, Tree
    import tree_sitter_javascript as tsjs
    import tree_sitter_typescript as tsts
except ImportError:
    print("Error: Required packages not installed.")
    print(
        "Install with: pip install tree-sitter tree-sitter-javascript tree-sitter-typescript"
    )
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
# Data Models
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
# Multi-Dialect Parser with Error Recovery
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

    def parse_file(
        self, filepath: Path
    ) -> Tuple[Optional[Tree], Optional[bytes], Optional[str]]:
        """Parse file with appropriate grammar and fallback. Returns (tree, source_code, error)."""
        suffix = filepath.suffix.lower()

        try:
            with open(filepath, "rb") as f:
                source_code = f.read()

            # Binary file check
            if b"\x00" in source_code[:1024]:
                return None, None, "Binary file"

            # Select primary parser
            if suffix in [".ts"]:
                tree = self.ts_parser.parse(source_code)
            elif suffix in [".tsx"]:
                tree = self.tsx_parser.parse(source_code)
            else:
                tree = self.js_parser.parse(source_code)

            # Fallback to TSX for problematic .js files (handles Flow, etc.)
            if suffix in [".js", ".mjs", ".cjs", ".jsx"] and tree.root_node.has_error:
                error_count = self._count_errors(tree.root_node)
                if error_count > 5:
                    tree = self.tsx_parser.parse(source_code)

            error_msg = "Partial parse" if tree.root_node.has_error else None
            return tree, source_code, error_msg

        except Exception as e:
            return None, None, f"Parse error: {str(e)[:50]}"

    def _count_errors(self, node: Node) -> int:
        """Count ERROR nodes recursively."""
        count = 1 if node.is_error or node.is_missing else 0
        for child in node.children:
            count += self._count_errors(child)
        return count


# ============================================================================
# Enhanced CST Normalizer with Semantic Enrichment
# ============================================================================


class CSTNormalizer:
    """Normalizes CST nodes to abstract and semantic signatures."""

    PATTERN_NODE_TYPES = {
        "call_expression",
        "lexical_declaration",
        "variable_declaration",
        "arrow_function",
        "function_declaration",
        "method_definition",
        "assignment_expression",
        "member_expression",
        "await_expression",
        "for_in_statement",
        "for_of_statement",
        "if_statement",
        "try_statement",
        "return_statement",
        "class_declaration",
        "new_expression",
        "import_statement",
        "export_statement",
    }

    def __init__(self):
        self.semantic_rules = self._load_semantic_rules()
        self.categories = self._load_categories()

    def _load_semantic_rules(self) -> Dict[str, Dict[str, str]]:
        """Enhanced semantic mapping for common APIs and patterns."""
        return {
            "identifier": {
                # Browser APIs
                "console": "CONSOLE_OBJECT",
                "document": "DOM_OBJECT",
                "window": "WINDOW_OBJECT",
                "localStorage": "STORAGE_API",
                "sessionStorage": "STORAGE_API",
                "fetch": "FETCH_API",
                "XMLHttpRequest": "XHR_API",
                # Timers
                "setTimeout": "TIMER_API",
                "setInterval": "TIMER_API",
                "requestAnimationFrame": "RAF_API",
                # Async
                "Promise": "PROMISE_CLASS",
                # React
                "useState": "REACT_HOOK",
                "useEffect": "REACT_HOOK",
                "useContext": "REACT_HOOK",
                "useCallback": "REACT_HOOK",
                "useMemo": "REACT_HOOK",
                "useRef": "REACT_HOOK",
                "React": "REACT_OBJECT",
                # Testing
                "describe": "TEST_SUITE",
                "it": "TEST_CASE",
                "test": "TEST_CASE",
                "expect": "ASSERTION",
                "jest": "TEST_FRAMEWORK",
                # Libraries
                "axios": "HTTP_LIB",
                "express": "EXPRESS_FRAMEWORK",
            },
            "method": {
                "getElementById": "DOM_METHOD",
                "querySelector": "DOM_METHOD",
                "addEventListener": "DOM_METHOD",
                "map": "ARRAY_METHOD",
                "filter": "ARRAY_METHOD",
                "reduce": "ARRAY_METHOD",
                "forEach": "ARRAY_METHOD",
                "find": "ARRAY_METHOD",
                "then": "PROMISE_METHOD",
                "catch": "PROMISE_METHOD",
            },
        }

    def _load_categories(self) -> Dict[str, List[str]]:
        """Pattern categories based on semantic keywords."""
        return {
            "DOM_MANIPULATION": [
                "DOM_OBJECT",
                "DOM_METHOD",
                "WINDOW_OBJECT",
                "querySelector",
                "getElementById",
            ],
            "ASYNC_OPERATIONS": [
                "async",
                "await",
                "PROMISE",
                "FETCH_API",
                "then",
                "catch",
            ],
            "ARRAY_OPERATIONS": ["ARRAY_METHOD", "map", "filter", "reduce", "forEach"],
            "CONTROL_FLOW": ["if", "for", "while", "switch", "try", "catch"],
            "VARIABLE_DECLARATIONS": ["const", "let", "var"],
            "FUNCTION_DEFINITIONS": ["function", "arrow_function", "=>"],
            "REACT_PATTERNS": ["REACT", "REACT_HOOK", "jsx"],
            "TEST_PATTERNS": ["TEST_SUITE", "TEST_CASE", "ASSERTION"],
            "HTTP_REQUESTS": ["FETCH_API", "XHR_API", "HTTP_LIB", "axios"],
            "STORAGE_OPERATIONS": ["STORAGE_API", "localStorage", "sessionStorage"],
            "TIMER_OPERATIONS": ["TIMER_API", "RAF_API"],
            "IMPORTS_EXPORTS": ["import", "export", "require"],
        }

    def should_extract(self, node: Node) -> bool:
        """Check if node should be extracted as a pattern."""
        return node.type in self.PATTERN_NODE_TYPES and not node.has_error

    def normalize(self, node: Node, source_code: bytes, level: str = "abstract") -> str:
        """Convert CST node to normalized signature at specified abstraction level."""
        self.source_code = source_code
        signature = self._recursive_normalize(node, level)
        return " ".join(signature.split())  # Collapse whitespace

    def _recursive_normalize(self, node: Node, level: str) -> str:
        """Core recursive normalization."""
        if node.type == "ERROR" or node.has_error:
            return ""

        if node.child_count == 0:
            return self._handle_terminal(node, level)

        # Dispatch to specialized handlers
        handler = getattr(self, f"_handle_{node.type}", self._handle_default)
        return handler(node, level)

    def _get_text(self, node: Node) -> str:
        """Extract text from node."""
        return self.source_code[node.start_byte : node.end_byte].decode(
            "utf8", errors="ignore"
        )

    def _handle_terminal(self, node: Node, level: str) -> str:
        """Handle leaf nodes with semantic enrichment."""
        text = self._get_text(node)

        if node.type == "identifier":
            if level == "semantic" and text in self.semantic_rules["identifier"]:
                return self.semantic_rules["identifier"][text]
            return "IDENTIFIER"
        elif node.type in ["string", "template_string"]:
            return "STRING"
        elif node.type == "number":
            return "NUMBER"
        elif node.type in ["true", "false"]:
            return "BOOLEAN"
        elif node.type in ["null", "undefined"]:
            return node.type.upper()
        else:
            return text

    def _handle_call_expression(self, node: Node, level: str) -> str:
        """Handle: func(args)"""
        function = node.child_by_field_name("function")
        arguments = node.child_by_field_name("arguments")

        func_sig = (
            self._recursive_normalize(function, level) if function else "FUNCTION"
        )
        args_sig = self._recursive_normalize(arguments, level) if arguments else "()"

        return f"{func_sig}{args_sig}"

    def _handle_member_expression(self, node: Node, level: str) -> str:
        """Handle: obj.property with semantic enrichment for methods."""
        obj = node.child_by_field_name("object")
        prop = node.child_by_field_name("property")

        obj_sig = self._recursive_normalize(obj, level) if obj else "OBJECT"

        if prop and level == "semantic":
            prop_text = self._get_text(prop)
            prop_sig = self.semantic_rules["method"].get(
                prop_text, self._recursive_normalize(prop, level)
            )
        else:
            prop_sig = self._recursive_normalize(prop, level) if prop else "PROPERTY"

        return f"{obj_sig}.{prop_sig}"

    def _handle_lexical_declaration(self, node: Node, level: str) -> str:
        """Handle: const/let/var x = value"""
        parts = []
        for child in node.children:
            if child.type in ["const", "let", "var"]:
                parts.append(child.type)
            elif child.type == "variable_declarator":
                name = child.child_by_field_name("name")
                value = child.child_by_field_name("value")

                if name:
                    parts.append(self._recursive_normalize(name, level))
                if value:
                    parts.append("=")
                    parts.append(self._recursive_normalize(value, level))

        return " ".join(parts)

    def _handle_arrow_function(self, node: Node, level: str) -> str:
        """Handle: (params) => body"""
        params = node.child_by_field_name("parameters")
        params_sig = self._recursive_normalize(params, level) if params else "()"
        return f"{params_sig} => BODY"

    def _handle_arguments(self, node: Node, level: str) -> str:
        """Handle function arguments."""
        args = []
        for child in node.children:
            if child.type not in ["(", ")", ","]:
                arg_sig = self._recursive_normalize(child, level)
                if arg_sig:
                    args.append(arg_sig)
        return f"({', '.join(args)})" if args else "()"

    def _handle_await_expression(self, node: Node, level: str) -> str:
        """Handle: await expr"""
        expr = node.child_by_field_name("argument")
        expr_sig = self._recursive_normalize(expr, level) if expr else "EXPRESSION"
        return f"await {expr_sig}"

    def _handle_new_expression(self, node: Node, level: str) -> str:
        """Handle: new Constructor()"""
        constructor = node.child_by_field_name("constructor")
        arguments = node.child_by_field_name("arguments")

        const_sig = (
            self._recursive_normalize(constructor, level) if constructor else "CLASS"
        )
        args_sig = self._recursive_normalize(arguments, level) if arguments else "()"

        return f"new {const_sig}{args_sig}"

    def _handle_default(self, node: Node, level: str) -> str:
        """Default: join normalized children."""
        parts = [self._recursive_normalize(child, level) for child in node.children]
        return " ".join(p for p in parts if p and p.strip())

    def categorize_pattern(
        self, abstract_sig: str, semantic_sig: str, node_type: str
    ) -> str:
        """Determine pattern category from signatures."""
        # Check semantic signature first
        sig_check = (semantic_sig or abstract_sig).lower()

        for category, keywords in self.categories.items():
            if any(kw.lower() in sig_check for kw in keywords):
                return category

        # Fallback based on node type
        if "call" in node_type:
            return "FUNCTION_CALLS"
        elif "declaration" in node_type:
            return "DECLARATIONS"
        elif "expression" in node_type:
            return "EXPRESSIONS"
        else:
            return "OTHER"

    @staticmethod
    def hash_signature(signature: str) -> str:
        """Generate stable hash."""
        return hashlib.sha256(signature.encode("utf8")).hexdigest()[:16]

    def is_trivial(self, signature: str, frequency: int) -> bool:
        """Filter trivial/noise patterns."""
        if len(signature) < 5 or frequency < 2:
            return True
        if signature in ["IDENTIFIER", "VALUE", "FUNCTION", "EXPRESSION", "STATEMENT"]:
            return True
        return False


# ============================================================================
# Pattern Mining Engine with Multi-Level Extraction
# ============================================================================


class PatternMiner:
    """Main mining engine with production-grade features."""

    def __init__(self, repo_path: Path, max_file_size_mb: float = 2.0):
        self.repo_path = Path(repo_path)
        self.max_file_size = max_file_size_mb * 1024 * 1024
        self.parser = MultiDialectParser()
        self.normalizer = CSTNormalizer()
        self.patterns: Dict[str, CodePattern] = {}
        self.stats = {
            "files_processed": 0,
            "files_skipped": 0,
            "skip_reasons": Counter(),
            "patterns_extracted": 0,
            "parse_errors": 0,
        }

    def discover_files(self) -> List[Path]:
        """Find all JS/TS files with intelligent filtering."""
        ignore_patterns = {
            "node_modules",
            "dist",
            "build",
            ".git",
            "coverage",
            "vendor",
            ".next",
            ".nuxt",
            "out",
            "public",
            "__pycache__",
            ".cache",
            "tmp",
            "temp",
            ".venv",
            "venv",
            "bower_components",
        }

        files = []
        for ext in ["*.js", "*.jsx", "*.ts", "*.tsx", "*.mjs", "*.cjs"]:
            for filepath in self.repo_path.rglob(ext):
                # Skip ignored directories
                try:
                    relative_path = filepath.relative_to(self.repo_path)
                    if any(
                        ignored in relative_path.parts for ignored in ignore_patterns
                    ):
                        continue
                except ValueError:
                    continue

                # Skip minified files
                if ".min." in filepath.name or "-min." in filepath.name:
                    self.stats["skip_reasons"]["minified"] += 1
                    continue

                # Check file size
                try:
                    if filepath.stat().st_size > self.max_file_size:
                        self.stats["skip_reasons"]["too_large"] += 1
                        continue
                except:
                    continue

                # Quick minification check
                if self._is_likely_minified(filepath):
                    self.stats["skip_reasons"]["minified_content"] += 1
                    continue

                files.append(filepath)

        return sorted(files)

    def _is_likely_minified(self, filepath: Path) -> bool:
        """Fast heuristic check for minification."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                first_line = f.readline()
                if len(first_line) > 500:
                    return True
        except:
            pass
        return False

    def extract_patterns_from_file(self, filepath: Path) -> bool:
        """Extract patterns from a single file. Returns success status."""
        tree, source_code, error = self.parser.parse_file(filepath)

        if not tree or not source_code:
            self.stats["files_skipped"] += 1
            self.stats["skip_reasons"][error or "unknown"] += 1
            return False

        try:
            self._traverse_and_extract(tree.root_node, source_code, filepath)
            self.stats["files_processed"] += 1

            if error:
                self.stats["parse_errors"] += 1

            return True
        except Exception as e:
            self.stats["files_skipped"] += 1
            self.stats["skip_reasons"]["extraction_error"] += 1
            return False

    def _traverse_and_extract(self, node: Node, source_code: bytes, filepath: Path):
        """Recursively extract patterns."""
        if self.normalizer.should_extract(node):
            self._record_pattern(node, source_code, filepath)

        for child in node.children:
            self._traverse_and_extract(child, source_code, filepath)

    def _record_pattern(self, node: Node, source_code: bytes, filepath: Path):
        """Record pattern with both abstract and semantic signatures."""
        try:
            # Generate both levels of abstraction
            abstract_sig = self.normalizer.normalize(node, source_code, "abstract")
            semantic_sig = self.normalizer.normalize(node, source_code, "semantic")

            if not abstract_sig:
                return

            # Use abstract signature for grouping
            pattern_hash = self.normalizer.hash_signature(abstract_sig)

            # Capture concrete code example
            concrete = source_code[node.start_byte : node.end_byte].decode(
                "utf8", errors="ignore"
            )[:200]
            line_num = node.start_point[0] + 1

            occurrence = PatternOccurrence(
                file_path=str(filepath.relative_to(self.repo_path)),
                line_number=line_num,
                concrete_code=concrete,
            )

            if pattern_hash not in self.patterns:
                category = self.normalizer.categorize_pattern(
                    abstract_sig, semantic_sig, node.type
                )
                self.patterns[pattern_hash] = CodePattern(
                    pattern_hash=pattern_hash,
                    abstract_signature=abstract_sig,
                    semantic_signature=semantic_sig,
                    node_type=node.type,
                    category=category,
                    frequency=0,
                    examples=[],
                )

            pattern = self.patterns[pattern_hash]
            pattern.frequency += 1

            # Keep diverse examples (max 5)
            if len(pattern.examples) < 5:
                pattern.examples.append(occurrence)

            self.stats["patterns_extracted"] += 1

        except Exception:
            pass  # Silently skip problematic patterns

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
            p
            for p in self.patterns.values()
            if not self.normalizer.is_trivial(p.abstract_signature, p.frequency)
        ]

        print(f"\n✅ Extracted {len(filtered_patterns)} unique patterns")
        print(f'📊 Files processed: {self.stats["files_processed"]}')

        if self.stats["files_skipped"] > 0:
            print(f'⚠️  Files skipped: {self.stats["files_skipped"]}')
            for reason, count in self.stats["skip_reasons"].most_common(5):
                print(f"   - {reason}: {count}")

        if self.stats["parse_errors"] > 0:
            print(
                f'⚠️  Files with parse errors (partial extraction): {self.stats["parse_errors"]}'
            )

        # Sort by frequency
        return sorted(filtered_patterns, key=lambda p: p.frequency, reverse=True)

    def export_to_json(
        self, patterns: List[CodePattern], output_path: Path, top_k: int
    ):
        """Export to JSON with enhanced metadata."""
        total_occurrences = sum(p.frequency for p in patterns)

        output = {
            "metadata": {
                "repository": str(self.repo_path),
                "total_patterns": len(patterns),
                "total_occurrences": total_occurrences,
                "top_k": min(top_k, len(patterns)),
                "files_processed": self.stats["files_processed"],
                "files_skipped": self.stats["files_skipped"],
                "files_with_errors": self.stats["parse_errors"],
            },
            "patterns": [
                {
                    "rank": i + 1,
                    "hash": p.pattern_hash,
                    "abstract_signature": p.abstract_signature,
                    "semantic_signature": p.semantic_signature,
                    "node_type": p.node_type,
                    "category": p.category,
                    "frequency": p.frequency,
                    "percentage": round(p.frequency / total_occurrences * 100, 2),
                    "examples": [asdict(ex) for ex in p.examples],
                }
                for i, p in enumerate(patterns[:top_k])
            ],
        }

        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)

        print(f'💾 Exported top {len(output["patterns"])} patterns to {output_path}')

    def export_to_markdown(
        self, patterns: List[CodePattern], output_path: Path, top_k: int
    ):
        """Export comprehensive Markdown report."""
        total_occurrences = sum(p.frequency for p in patterns)

        # Group by category
        by_category = defaultdict(list)
        for p in patterns[:top_k]:
            by_category[p.category].append(p)

        with open(output_path, "w") as f:
            f.write("# 📊 Code Pattern Analysis\n\n")
            f.write(f"**Repository:** `{self.repo_path}`\n\n")
            f.write(f'**Files Processed:** {self.stats["files_processed"]}\n\n')
            f.write(f"**Total Unique Patterns:** {len(patterns)}\n\n")
            f.write(f"**Total Occurrences:** {total_occurrences:,}\n\n")
            f.write("---\n\n")

            # Category summary
            f.write("## 📑 Category Summary\n\n")
            f.write("| Category | Patterns | Total Occurrences |\n")
            f.write("|----------|----------|------------------|\n")
            for category in sorted(by_category.keys()):
                cat_patterns = by_category[category]
                cat_freq = sum(p.frequency for p in cat_patterns)
                f.write(f"| {category} | {len(cat_patterns)} | {cat_freq:,} |\n")
            f.write("\n---\n\n")

            # Patterns by category
            overall_rank = 1
            for category in sorted(by_category.keys()):
                f.write(f"## {category}\n\n")

                for pattern in by_category[category]:
                    percentage = round(pattern.frequency / total_occurrences * 100, 2)
                    f.write(f"### {overall_rank}. {pattern.abstract_signature}\n\n")
                    f.write(f"- **Frequency:** {pattern.frequency:,} ({percentage}%)\n")
                    f.write(f"- **Node Type:** `{pattern.node_type}`\n")

                    if (
                        pattern.semantic_signature
                        and pattern.semantic_signature != pattern.abstract_signature
                    ):
                        f.write(f"- **Semantic:** `{pattern.semantic_signature}`\n")

                    f.write("\n")

                    if pattern.examples:
                        f.write("**Examples:**\n\n")
                        for ex in pattern.examples[:2]:
                            f.write(f"```javascript\n{ex.concrete_code}\n```\n")
                            f.write(f"*{ex.file_path}:{ex.line_number}*\n\n")

                    overall_rank += 1

                f.write("---\n\n")

        print(f"📝 Exported categorized patterns to {output_path}")


# ============================================================================
# Main Entry Point
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Code Pattern Mining System with Multi-Level Abstraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_pattern_miner.py /path/to/repo
  python enhanced_pattern_miner.py /path/to/repo --top-k 200 --format markdown
  python enhanced_pattern_miner.py /path/to/repo --output results --min-freq 5
        """,
    )
    parser.add_argument("repo_path", type=str, help="Path to the repository")
    parser.add_argument(
        "--top-k",
        type=int,
        default=200,
        help="Number of top patterns to export (default: 200)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="patterns",
        help="Output file name without extension (default: patterns)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "all"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--max-file-size",
        type=float,
        default=2.0,
        help="Maximum file size in MB (default: 2.0)",
    )
    parser.add_argument(
        "--min-freq",
        type=int,
        default=2,
        help="Minimum frequency to include pattern (default: 2)",
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
        print(
            f"🔍 Filtered to {len(patterns)} patterns (min frequency: {args.min_freq})"
        )

    if not patterns:
        print("❌ No patterns found!")
        sys.exit(1)

    # Export results
    output_base = Path(args.output)
    print("\n📤 Exporting results...")

    if args.format in ["json", "all"]:
        json_path = output_base.with_suffix(".json")
        miner.export_to_json(patterns, json_path, args.top_k)

    if args.format in ["markdown", "all"]:
        md_path = output_base.with_suffix(".md")
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
            print(f"    Semantic: {p.semantic_signature[:55]}")

    print(f"\n⏱️  Total time: {elapsed:.1f}s")
    print("✨ Done!")


if __name__ == "__main__":
    main()
