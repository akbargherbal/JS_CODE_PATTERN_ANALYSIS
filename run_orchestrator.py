#!/usr/bin/env python3
"""
Main entry point to run the JS Pattern Mining Orchestration System.
"""
import sys
from pathlib import Path

# Add project root to path to allow imports from src
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.js_pattern_analyzer.orchestrator import Orchestrator


def main():
    """Initializes and runs the orchestrator."""
    print("=" * 70)
    print("  JS Pattern Mining Orchestration System")
    print("=" * 70)

    try:
        orchestrator = Orchestrator()
        orchestrator.run()
        print("\nOrchestration finished.")
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: A required file was not found: {e}")
        print("\nPlease ensure the following:")
        print("  1. `config.yaml` exists and is configured correctly.")
        print("  2. The repo links file (e.g., `data/DF_REPO_LINKS.pkl`) exists.")
        print(
            "     - You can create it by running: python scripts/setup/setup_repo_links.py"
        )
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
