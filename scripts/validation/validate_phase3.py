"""
Validation Script - Test Phase 3 Implementation (Pattern Aggregator)
Place this in: JS_CODE_PATTERN_ANALYSIS/validate_phase3.py
"""

import sys
from pathlib import Path
import json

import pandas as pd


# Add project root to path
import sys

project_root = Path(__file__).resolve().parents[2]
print(f"Adding {project_root} to path")
sys.path.insert(0, str(project_root))

from src.js_pattern_analyzer.pattern_aggregator import PatternAggregator


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def create_mock_pattern_files():
    """Create mock pattern files for testing."""
    print_section("TEST 1: Creating Mock Pattern Files")

    patterns_dir = Path("./data/patterns_by_repo")
    patterns_dir.mkdir(parents=True, exist_ok=True)

    # Mock repo 1: React-like patterns
    df1 = pd.DataFrame(
        {
            "pattern_hash": ["abc123", "def456", "ghi789", "jkl012"],
            "abstract_signature": [
                "const IDENTIFIER = REACT_HOOK()",
                "IDENTIFIER.map(IDENTIFIER => BODY)",
                "import IDENTIFIER from STRING",
                "export default IDENTIFIER",
            ],
            "semantic_signature": [
                "const IDENTIFIER = useState()",
                "IDENTIFIER.map(IDENTIFIER => BODY)",
                "import IDENTIFIER from STRING",
                "export default IDENTIFIER",
            ],
            "node_type": [
                "lexical_declaration",
                "call_expression",
                "import_statement",
                "export_statement",
            ],
            "category": [
                "REACT_PATTERNS",
                "ARRAY_OPERATIONS",
                "IMPORTS_EXPORTS",
                "IMPORTS_EXPORTS",
            ],
            "frequency": [45, 32, 28, 15],
            "examples_json": [
                json.dumps(
                    [
                        {
                            "file_path": "App.js",
                            "line_number": 10,
                            "concrete_code": "const [count, setCount] = useState(0)",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "List.js",
                            "line_number": 5,
                            "concrete_code": "items.map(item => <Item key={item.id} />)",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "utils.js",
                            "line_number": 1,
                            "concrete_code": "import React from 'react'",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "App.js",
                            "line_number": 50,
                            "concrete_code": "export default App",
                        }
                    ]
                ),
            ],
        }
    )

    # Mock repo 2: Similar patterns (overlap)
    df2 = pd.DataFrame(
        {
            "pattern_hash": ["def456", "ghi789", "mno345", "pqr678"],
            "abstract_signature": [
                "IDENTIFIER.map(IDENTIFIER => BODY)",
                "import IDENTIFIER from STRING",
                "const IDENTIFIER = VALUE",
                "IDENTIFIER.filter(IDENTIFIER => BODY)",
            ],
            "semantic_signature": [
                "IDENTIFIER.map(IDENTIFIER => BODY)",
                "import IDENTIFIER from STRING",
                "const IDENTIFIER = FETCH_API(...)",
                "IDENTIFIER.filter(IDENTIFIER => BODY)",
            ],
            "node_type": [
                "call_expression",
                "import_statement",
                "lexical_declaration",
                "call_expression",
            ],
            "category": [
                "ARRAY_OPERATIONS",
                "IMPORTS_EXPORTS",
                "VARIABLE_DECLARATIONS",
                "ARRAY_OPERATIONS",
            ],
            "frequency": [28, 22, 18, 12],
            "examples_json": [
                json.dumps(
                    [
                        {
                            "file_path": "data.js",
                            "line_number": 15,
                            "concrete_code": "data.map(x => x * 2)",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "index.js",
                            "line_number": 1,
                            "concrete_code": "import Vue from 'vue'",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "api.js",
                            "line_number": 8,
                            "concrete_code": "const response = await fetch(url)",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "utils.js",
                            "line_number": 20,
                            "concrete_code": "arr.filter(x => x > 0)",
                        }
                    ]
                ),
            ],
        }
    )

    # Mock repo 3: Different patterns
    df3 = pd.DataFrame(
        {
            "pattern_hash": ["ghi789", "stu901", "vwx234", "yz5678"],
            "abstract_signature": [
                "import IDENTIFIER from STRING",
                "function IDENTIFIER(PARAMETERS) BODY",
                "if (CONDITION) BODY",
                "IDENTIFIER.forEach(IDENTIFIER => BODY)",
            ],
            "semantic_signature": [
                "import IDENTIFIER from STRING",
                "function IDENTIFIER(PARAMETERS) BODY",
                "if (CONDITION) BODY",
                "IDENTIFIER.forEach(IDENTIFIER => BODY)",
            ],
            "node_type": [
                "import_statement",
                "function_declaration",
                "if_statement",
                "call_expression",
            ],
            "category": [
                "IMPORTS_EXPORTS",
                "FUNCTION_DEFINITIONS",
                "CONTROL_FLOW",
                "ARRAY_OPERATIONS",
            ],
            "frequency": [35, 25, 20, 10],
            "examples_json": [
                json.dumps(
                    [
                        {
                            "file_path": "main.js",
                            "line_number": 1,
                            "concrete_code": "import express from 'express'",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "helpers.js",
                            "line_number": 10,
                            "concrete_code": "function add(a, b) { return a + b }",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "auth.js",
                            "line_number": 15,
                            "concrete_code": "if (user.isAdmin) { ... }",
                        }
                    ]
                ),
                json.dumps(
                    [
                        {
                            "file_path": "logger.js",
                            "line_number": 5,
                            "concrete_code": "logs.forEach(log => console.log(log))",
                        }
                    ]
                ),
            ],
        }
    )

    # Save mock files
    mock_files = {
        "repo_001_facebook_react.pkl": df1,
        "repo_002_vuejs_vue.pkl": df2,
        "repo_003_nodejs_node.pkl": df3,
    }

    for filename, df in mock_files.items():
        filepath = patterns_dir / filename
        df.to_pickle(filepath)
        print(f"   ✅ Created: {filename} ({len(df)} patterns)")

    print(f"\n✅ Created {len(mock_files)} mock pattern files")
    print(f"   Location: {patterns_dir}")

    return patterns_dir


def test_loading_patterns():
    """Test loading pattern files."""
    print_section("TEST 2: Loading Pattern Files")

    try:
        aggregator = PatternAggregator()
        repo_data = aggregator.load_all_repo_patterns()

        print(f"\n✅ Loaded {len(repo_data)} repository pattern files")

        # Verify structure
        for repo_id, repo_name, df in repo_data:
            print(f"\n   Repo {repo_id}: {repo_name}")
            print(f"      Patterns: {len(df)}")
            print(f"      Total frequency: {df['frequency'].sum()}")

            # Check required columns
            required_cols = ["pattern_hash", "frequency", "repo_id", "repo_name"]
            missing = [col for col in required_cols if col not in df.columns]

            if missing:
                print(f"      ❌ Missing columns: {missing}")
                return False

            print(f"      ✅ All required columns present")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_aggregation():
    """Test pattern aggregation."""
    print_section("TEST 3: Pattern Aggregation")

    try:
        aggregator = PatternAggregator()

        # Run aggregation
        df_agg = aggregator.aggregate_all_patterns(
            min_repo_count=1,  # Include all patterns for testing
            min_total_frequency=1,
        )

        print(f"\n📊 Aggregation Results:")
        print(f"   Unique patterns: {len(df_agg)}")
        print(f"   Total occurrences: {df_agg['total_frequency'].sum()}")

        # Verify schema
        required_cols = [
            "rank",
            "pattern_hash",
            "abstract_signature",
            "total_frequency",
            "repo_count",
            "prevalence_pct",
        ]

        missing = [col for col in required_cols if col not in df_agg.columns]

        if missing:
            print(f"\n❌ Missing columns: {missing}")
            return False

        print(f"\n✅ All required columns present")

        # Test specific patterns
        print(f"\n🔍 Verifying aggregation logic:")

        # Pattern 'ghi789' should appear in all 3 repos
        ghi_pattern = df_agg[df_agg["pattern_hash"] == "ghi789"]

        if len(ghi_pattern) > 0:
            row = ghi_pattern.iloc[0]
            print(f"\n   Pattern: {row['abstract_signature']}")
            print(f"   Total frequency: {row['total_frequency']} (expected: 85)")
            print(f"   Repo count: {row['repo_count']} (expected: 3)")
            print(f"   Prevalence: {row['prevalence_pct']}% (expected: 100%)")

            # Verify calculations
            if row["repo_count"] != 3:
                print(f"   ❌ Expected repo_count=3, got {row['repo_count']}")
                return False

            if row["total_frequency"] != 85:  # 28 + 22 + 35
                print(
                    f"   ❌ Expected total_frequency=85, got {row['total_frequency']}"
                )
                return False

            print(f"   ✅ Aggregation math is correct!")

        else:
            print(f"   ⚠️  Pattern 'ghi789' not found in aggregation")

        # Pattern 'abc123' should only be in repo 1
        abc_pattern = df_agg[df_agg["pattern_hash"] == "abc123"]

        if len(abc_pattern) > 0:
            row = abc_pattern.iloc[0]
            print(f"\n   Pattern: {row['abstract_signature']}")
            print(f"   Repo count: {row['repo_count']} (expected: 1)")
            print(f"   Prevalence: {row['prevalence_pct']}% (expected: 33.33%)")

            if row["repo_count"] != 1:
                print(f"   ❌ Expected repo_count=1, got {row['repo_count']}")
                return False

            print(f"   ✅ Unique pattern correctly handled!")

        print(f"\n✅ Aggregation test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_filtering():
    """Test filtering by thresholds."""
    print_section("TEST 4: Filtering by Thresholds")

    try:
        aggregator = PatternAggregator()

        # Test with strict filters
        print(f"\n🔍 Testing with min_repo_count=2, min_total_frequency=50")

        df_filtered = aggregator.aggregate_all_patterns(
            min_repo_count=2, min_total_frequency=50
        )

        print(f"\n📊 Filtered Results:")
        print(f"   Patterns remaining: {len(df_filtered)}")

        # Verify all patterns meet criteria
        invalid_repo_count = df_filtered[df_filtered["repo_count"] < 2]
        invalid_frequency = df_filtered[df_filtered["total_frequency"] < 50]

        if len(invalid_repo_count) > 0:
            print(f"   ❌ Found {len(invalid_repo_count)} patterns with repo_count < 2")
            return False

        if len(invalid_frequency) > 0:
            print(f"   ❌ Found {len(invalid_frequency)} patterns with frequency < 50")
            return False

        print(f"   ✅ All patterns meet minimum thresholds")

        # Test with loose filters
        print(f"\n🔍 Testing with min_repo_count=1, min_total_frequency=10")

        df_loose = aggregator.aggregate_all_patterns(
            min_repo_count=1, min_total_frequency=10
        )

        print(f"   Patterns remaining: {len(df_loose)}")

        if len(df_loose) <= len(df_filtered):
            print(f"   ❌ Loose filters should return more patterns")
            return False

        print(f"   ✅ Loose filters return more patterns (as expected)")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_exports():
    """Test export functionality."""
    print_section("TEST 5: Export Functionality")

    try:
        aggregator = PatternAggregator()

        # Create test results directory
        test_results_dir = Path("./data/test_results")
        test_results_dir.mkdir(parents=True, exist_ok=True)

        # Aggregate patterns
        df_agg = aggregator.aggregate_all_patterns(
            min_repo_count=1, min_total_frequency=1
        )

        # Export top 5 for testing
        print(f"\n💾 Exporting top 5 patterns...")

        output_paths = aggregator.export_top_k(df_agg, k=5, output_dir=test_results_dir)

        print(f"\n📁 Checking exported files:")

        # Check each file
        for format_name, filepath in output_paths.items():
            if not filepath.exists():
                print(f"   ❌ {format_name}: File not created: {filepath}")
                return False

            size_kb = filepath.stat().st_size / 1024
            print(f"   ✅ {format_name}: {filepath.name} ({size_kb:.1f} KB)")

        # Validate JSON structure
        json_path = output_paths["json"]
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if "metadata" not in json_data:
            print(f"   ❌ JSON missing 'metadata' key")
            return False

        if "patterns" not in json_data:
            print(f"   ❌ JSON missing 'patterns' key")
            return False

        if len(json_data["patterns"]) != 5:
            print(
                f"   ❌ JSON should have 5 patterns, got {len(json_data['patterns'])}"
            )
            return False

        print(f"   ✅ JSON structure is valid")

        # Validate Markdown exists and has content
        md_path = output_paths["markdown"]
        md_content = md_path.read_text(encoding="utf-8")

        if len(md_content) < 100:
            print(f"   ❌ Markdown file is too short")
            return False

        if "# JavaScript/TypeScript Code Patterns" not in md_content:
            print(f"   ❌ Markdown missing header")
            return False

        print(f"   ✅ Markdown content is valid")

        # Validate Parquet can be loaded
        parquet_path = output_paths["parquet"]
        df_loaded = pd.read_parquet(parquet_path)

        if len(df_loaded) != len(df_agg):
            print(f"   ❌ Parquet should have {len(df_agg)} rows, got {len(df_loaded)}")
            return False

        print(f"   ✅ Parquet can be loaded correctly")

        print(f"\n✅ All export tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_category_summary():
    """Test category summary generation."""
    print_section("TEST 6: Category Summary")

    try:
        aggregator = PatternAggregator()

        df_agg = aggregator.aggregate_all_patterns(
            min_repo_count=1, min_total_frequency=1
        )

        # Get category summary
        category_summary = aggregator.get_category_summary(df_agg)

        print(f"\n📊 Category Summary:")
        print(f"   Total categories: {len(category_summary)}")

        print(f"\n   Category Statistics:")
        for category, row in category_summary.iterrows():
            print(f"      {category}: {row[('pattern_hash', 'count')]} patterns")

        if len(category_summary) == 0:
            print(f"   ❌ No categories found")
            return False

        print(f"\n✅ Category summary test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def cleanup_test_files():
    """Clean up test files."""
    print_section("Cleanup")

    try:
        # Remove mock pattern files
        patterns_dir = Path("./data/patterns_by_repo")
        if patterns_dir.exists():
            for file in patterns_dir.glob("repo_*.pkl"):
                file.unlink()
                print(f"   🗑️  Removed: {file.name}")

        # Remove test results
        test_results_dir = Path("./data/test_results")
        if test_results_dir.exists():
            import shutil

            shutil.rmtree(test_results_dir)
            print(f"   🗑️  Removed: test_results/")

        print(f"\n✅ Cleanup complete")

    except Exception as e:
        print(f"\n⚠️  Cleanup warning: {e}")


def main():
    """Run all Phase 3 validation tests."""
    print("\n" + "=" * 70)
    print("  🧪 PHASE 3 VALIDATION SUITE")
    print("  Testing Pattern Aggregator Implementation")
    print("=" * 70)

    results = {}

    # Test 1: Create mock files
    try:
        create_mock_pattern_files()
        results["Create Mock Files"] = True
    except Exception as e:
        print(f"\n❌ Failed to create mock files: {e}")
        results["Create Mock Files"] = False
        return False

    # Test 2: Loading
    if results["Create Mock Files"]:
        results["Load Pattern Files"] = test_loading_patterns()
    else:
        results["Load Pattern Files"] = False

    # Test 3: Aggregation
    if results["Load Pattern Files"]:
        results["Pattern Aggregation"] = test_aggregation()
    else:
        results["Pattern Aggregation"] = False

    # Test 4: Filtering
    if results["Pattern Aggregation"]:
        results["Threshold Filtering"] = test_filtering()
    else:
        results["Threshold Filtering"] = False

    # Test 5: Exports
    if results["Threshold Filtering"]:
        results["Export Functionality"] = test_exports()
    else:
        results["Export Functionality"] = False

    # Test 6: Category summary
    if results["Export Functionality"]:
        results["Category Summary"] = test_category_summary()
    else:
        results["Category Summary"] = False

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {test_name}")

    print(f"\n{'=' * 70}")
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 Phase 3 is ready!")
        print("\nNext steps:")
        print("  1. Test with real repository pattern files")
        print("  2. Move on to Phase 4: Repo Cloner")
        print("  3. Review the plan: js_pattern_orchestration_plan.md")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")

    print("=" * 70 + "\n")

    # Cleanup
    cleanup_test_files()

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
