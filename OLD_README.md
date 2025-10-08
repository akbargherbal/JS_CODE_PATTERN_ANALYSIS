# JS Code Pattern Analysis

This project analyzes JavaScript and TypeScript code from open-source repositories to create a data-driven "phrasebook" of the most common code patterns used in modern development.

Instead of just learning syntax, this tool helps developers understand frequency. It identifies the idiomatic code patterns that appear most often in real-world projects, providing a practical guide for learning, teaching, and engineering.

## Why It Matters

Most developers learn what's _possible_ with a language, but not what's _common_. This project grounds learning in real-world data to address this gap.

- **For Beginners**: Discover the 50-100 essential patterns that form the foundation of most projects.
- **For Experienced Developers**: See which idioms dominate modern codebases and identify emerging trends.
- **For Educators**: Build a data-backed curriculum focused on the patterns that students will encounter most frequently.

By mapping the building blocks of thousands of real repositories, this project turns code analysis into practical, actionable insight.

## How It Works

The core of this project is the `pattern_miner.py` script, a sophisticated tool that automates the analysis process:

1.  **File Discovery**: The miner intelligently scans a repository, identifying all relevant JavaScript/TypeScript files (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`). It automatically skips `node_modules`, build directories, and minified files.
2.  **Robust Parsing**: Using the `tree-sitter` library, the script parses the source code into a Concrete Syntax Tree (CST). This allows it to understand the code's structure with high fidelity, even for different dialects like JSX and TSX.
3.  **Pattern Normalization**: The script traverses the CST and converts concrete code snippets into abstract, normalized signatures. For example, `const user = 'Alice'` and `let count = 100` both normalize to a pattern like `const IDENTIFIER = VALUE`.
4.  **Semantic Enrichment**: The normalizer is equipped with rules to identify common APIs and frameworks. It can recognize `useState` as a `REACT_HOOK`, `document.getElementById` as a `DOM_METHOD`, and `await fetch(...)` as an `ASYNC_OPERATION`.
5.  **Frequency Analysis**: The tool counts the occurrences of each unique pattern across the entire codebase.
6.  **Reporting**: Finally, it generates a ranked report of the most common patterns, categorized for clarity (e.g., `ASYNC_OPERATIONS`, `ARRAY_OPERATIONS`, `REACT_PATTERNS`).

## Features

- **Multi-Dialect Support**: Analyzes JavaScript, TypeScript, JSX, and TSX.
- **Semantic Categorization**: Groups patterns by function, such as `DOM_MANIPULATION`, `HTTP_REQUESTS`, and `TEST_PATTERNS`.
- **Intelligent Filtering**: Ignores trivial patterns and boilerplate to focus on meaningful code structures.
- **Flexible Output**: Exports results in both `JSON` and detailed `Markdown` formats.
- **Command-Line Interface**: Easy to run and configure with arguments for customizing the analysis.

## Usage

To analyze a local repository, run the `pattern_miner.py` script from your terminal.

**1. Prerequisites:**

Install the required Python packages:

````shell
pip install tree-sitter tree-sitter-javascript tree-sitter-typescript tqdm```

**2. Run the Analysis:**

Point the script to the path of the repository you want to analyze.

```shell
python pattern_miner.py /path/to/your/repo
````

**3. Command-Line Options:**

Customize the analysis with the following options:

- `--top-k <N>`: Set the number of top patterns to export (default: 200).
- `--format <TYPE>`: Choose the output format: `json`, `markdown`, or `all` (default: json).
- `--output <NAME>`: Specify the output file name (without extension).
- `--min-freq <N>`: Set the minimum frequency for a pattern to be included (default: 2).

**Example:**

To generate a Markdown report of the top 150 patterns from a project, saving it as `react_patterns.md`:

```shell
python pattern_miner.py /path/to/react-project --top-k 150 --format markdown --output react_patterns
```
