# JS Pattern Mining Orchestration System

This project analyzes JavaScript and TypeScript code from thousands of open-source repositories to create a data-driven "phrasebook" of the most common code patterns used in modern development.

It is a multi-stage orchestration system designed for large-scale, resilient analysis.

## How It Works

The system processes a list of Git repositories in several phases:

1.  **State Management**: A persistent queue (`data/repo_queue.pkl`) tracks the status of each repository (`pending`, `processing`, `completed`, `failed`).
2.  **Orchestration Loop**: The main `run_orchestrator.py` script iterates through pending repositories.
3.  **Cloning**: For each repo, a temporary, shallow clone is created.
4.  **Pattern Mining**: The cloned repository is scanned by a `tree-sitter`-based parser that extracts and normalizes code patterns into abstract signatures (e.g., `const IDENTIFIER = VALUE`).
5.  **Pattern Storage**: The mined patterns for each repository are saved as individual `*.pkl` files in `data/patterns_by_repo/`.
6.  **Aggregation**: After processing all repositories, the `pattern_aggregator.py` script combines all individual pattern files into a final, ranked dataset, exporting reports in JSON, Markdown, and Parquet formats.

## Features

- **Scalable**: Designed to process thousands of repositories.
- **Resilient**: Tracks state and can recover from interruptions. Failed repositories can be retried automatically.
- **Multi-Dialect Support**: Analyzes JavaScript, TypeScript, JSX, and TSX.
- **Semantic Analysis**: Enriches patterns with semantic information (e.g., identifying `useState` as a `REACT_HOOK`).
- **Configurable**: All major parameters are controlled via `config.yaml`.

## Usage

### 1. Setup

First, you need to create the list of repositories to analyze. A setup wizard is provided for this.

```shell
python scripts/setup/setup_repo_links.py
```

This will guide you through creating the `data/DF_REPO_LINKS.pkl` file, which is the input for the system.

### 2. Configuration

Review and edit `config.yaml` to adjust settings like the number of repositories to process (`max_repos`), temporary directories, and pattern filtering thresholds.

### 3. Run the Orchestrator

Start the main processing pipeline. The system will automatically initialize the repository queue and begin cloning and analyzing.

```shell
python run_orchestrator.py
```

The orchestrator will process repositories one by one, updating the queue and saving pattern files. You can stop and restart this script, and it will resume where it left off.

### 4. Aggregate the Results

Once the orchestrator has processed all the desired repositories, run the aggregator to produce the final reports.

```shell
python src/js_pattern_analyzer/pattern_aggregator.py
```

This will analyze all files in `data/patterns_by_repo/` and generate the final outputs in the `results/` directory. You can customize the aggregation thresholds using command-line arguments:

```shell
# Example: Export top 100 patterns that appear in at least 5 repos
python src/js_pattern_analyzer/pattern_aggregator.py --top-k 100 --min-repos 5
```

## Project Structure

- `run_orchestrator.py`: Main entry point to start the analysis.
- `config.yaml`: Central configuration file.
- `src/js_pattern_analyzer/`: Contains the core Python source code.
  - `orchestrator.py`: The main processing loop controller.
  - `state_manager.py`: Manages the repository queue and state.
  - `repo_cloner.py`: Handles cloning and cleaning up Git repositories.
  - `pattern_miner.py`: The core `tree-sitter` based pattern extraction engine.
  - `pattern_miner_wrapper.py`: Bridges the pattern miner with the orchestration system.
  - `pattern_aggregator.py`: Combines results from all repos into a final report.
- `scripts/`: Contains setup, validation, and debugging scripts.
- `data/`: Default directory for input files, the repo queue, and intermediate pattern files.
- `results/`: Default directory for final aggregated reports.
