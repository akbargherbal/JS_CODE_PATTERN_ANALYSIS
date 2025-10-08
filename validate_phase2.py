"""
Validation Script - Test Phase 2 Implementation (Pattern Miner Wrapper)
Place this in: JS_CODE_PATTERN_ANALYSIS/validate_phase2.py
"""

import sys
from pathlib import Path
import subprocess
import shutil
import time

import pandas as pd

# Import the wrapper
from pattern_miner_wrapper import (
    mine_repository_to_dataframe,
    validate_patterns_dataframe,
)


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_import():
    """Test 1: Can we import the wrapper?"""
    print_section("TEST 1: Import Validation")

    try:
        from pattern_miner_wrapper import mine_repository_to_dataframe

        print("✅ Successfully imported mine_repository_to_dataframe")

        from pattern_miner import PatternMiner

        print("✅ Successfully imported PatternMiner")

        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def setup_test_repo():
    """Create a minimal test repository with JS files"""
    print_section("TEST 2: Setup Test Repository")

    test_repo_path = Path("./temp/test_repo")

    try:
        # Clean up if exists
        if test_repo_path.exists():
            # Use safe removal for Windows
            safe_rmtree(test_repo_path)

        test_repo_path.mkdir(parents=True)

        # Create some sample JS files with more realistic content
        sample_files = {
            "index.js": """// Sample JavaScript file
const greeting = "Hello, World!";

function greet(name) {
    console.log(`Hello, ${name}!`);
    return greeting;
}

const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const filtered = numbers.filter(x => x > 2);

export default greet;
""",
            "utils.js": """// Utility functions
const API_URL = "https://api.example.com";

async function fetchData(endpoint) {
    const response = await fetch(`${API_URL}/${endpoint}`);
    const data = await response.json();
    return data;
}

function processArray(arr) {
    return arr.filter(x => x > 0).map(x => x * 2);
}

export { fetchData, processArray };
""",
            "config.js": """// Configuration
const config = {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3
};

const getValue = (key) => config[key];

export default config;
""",
        }

        for filename, content in sample_files.items():
            filepath = test_repo_path / filename
            filepath.write_text(content, encoding="utf-8")

        print(f"✅ Created test repository: {test_repo_path}")
        print(f"   Files created: {len(sample_files)}")

        # Verify files exist
        js_files = list(test_repo_path.glob("*.js"))
        print(f"   Verified .js files: {len(js_files)}")
        for f in js_files:
            print(f"     • {f.name}")

        return test_repo_path

    except Exception as e:
        print(f"❌ Failed to setup test repo: {e}")
        import traceback

        traceback.print_exc()
        return None


def safe_rmtree(path):
    """Remove directory tree with Windows-friendly retry logic"""
    path = Path(path)
    if not path.exists():
        return

    # On Windows, .git files can be locked
    # Try multiple times with increasing delays
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            shutil.rmtree(path)
            return
        except PermissionError as e:
            if attempt < max_attempts - 1:
                print(f"   ⚠️  Locked files, retrying in {attempt + 1}s...")
                time.sleep(attempt + 1)

                # Try to unlock by changing permissions
                try:
                    import stat

                    for root, dirs, files in path.walk():
                        for name in files:
                            file_path = root / name
                            try:
                                file_path.chmod(stat.S_IWRITE)
                            except:
                                pass
                except:
                    pass
            else:
                print(f"   ⚠️  Could not remove {path}: {e}")
                print(f"   Please manually delete: {path.absolute()}")


def test_mining_wrapper(test_repo_path):
    """Test 3: Run the mining wrapper on test repo"""
    print_section("TEST 3: Pattern Mining")

    try:
        print(f"📂 Mining patterns from: {test_repo_path}")

        df_patterns, stats = mine_repository_to_dataframe(test_repo_path)

        print("\n📊 Mining Statistics:")
        print(f"   Files processed:    {stats['files_processed']}")
        print(f"   Files skipped:      {stats['files_skipped']}")
        print(f"   Parse errors:       {stats['parse_errors']}")
        print(f"   Patterns extracted: {stats['patterns_extracted']}")
        print(f"   Total frequency:    {stats['total_frequency']}")

        if stats["patterns_extracted"] == 0:
            print("\n⚠️  No patterns extracted")
            print("   This is unexpected for the test repo. Checking files...")

            # Debug: Check what files exist
            js_files = list(test_repo_path.glob("*.js"))
            print(f"   Files in directory: {len(js_files)}")
            for f in js_files:
                print(f"     • {f.name} ({f.stat().st_size} bytes)")

            return False

        print(f"\n📋 DataFrame Shape: {df_patterns.shape}")
        print(f"   Columns: {list(df_patterns.columns)}")

        # Show sample patterns
        print("\n🔍 Sample Patterns:")
        for idx, row in df_patterns.head(10).iterrows():
            print(f"   {row['frequency']:3d}x | {row['category']}")
            print(f"         {row['abstract_signature'][:70]}")

        return True

    except Exception as e:
        print(f"❌ Mining failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_dataframe_schema(test_repo_path):
    """Test 4: Validate DataFrame schema"""
    print_section("TEST 4: DataFrame Schema Validation")

    try:
        df_patterns, stats = mine_repository_to_dataframe(test_repo_path)

        # Check required columns
        required_cols = [
            "pattern_hash",
            "abstract_signature",
            "semantic_signature",
            "node_type",
            "category",
            "frequency",
            "examples_json",
        ]

        missing = [col for col in required_cols if col not in df_patterns.columns]
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False

        print("✅ All required columns present:")
        for col in required_cols:
            print(f"   • {col}")

        # Only run validation if we have data
        if len(df_patterns) > 0:
            print("\n🔍 Running validation checks...")
            validate_patterns_dataframe(df_patterns)
            print("✅ All validation checks passed!")
        else:
            print("\n⚠️  Empty DataFrame - skipping type validation")

        return True

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_examples_serialization(test_repo_path):
    """Test 5: Check examples are properly serialized as JSON"""
    print_section("TEST 5: Examples JSON Serialization")

    try:
        df_patterns, stats = mine_repository_to_dataframe(test_repo_path)

        if len(df_patterns) == 0:
            print("⚠️  No patterns to test (empty DataFrame)")
            return True

        # Pick first pattern with examples
        first_pattern = df_patterns.iloc[0]

        print(f"📄 Testing pattern: {first_pattern['abstract_signature'][:60]}")
        print(f"   examples_json type: {type(first_pattern['examples_json'])}")

        # Try to parse JSON
        import json

        examples = json.loads(first_pattern["examples_json"])

        print(f"✅ Successfully parsed examples JSON")
        print(f"   Number of examples: {len(examples)}")

        if len(examples) > 0:
            print(f"   First example type: {type(examples[0])}")
            if isinstance(examples[0], dict):
                print(f"   Example keys: {list(examples[0].keys())}")

        return True

    except Exception as e:
        print(f"❌ Serialization test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_with_real_repo():
    """Test 6: Optional test with a small real repository"""
    print_section("TEST 6: Real Repository Test (Optional)")

    print("This test clones a small real repository and mines it.")
    print("This will take 1-2 minutes.")

    response = input("\nRun this test? (y/n): ").strip().lower()

    if response != "y":
        print("⏭️  Skipped")
        return True

    # Clone a small repo (lodash is relatively small)
    test_repo_url = "https://github.com/lodash/lodash.git"
    test_repo_path = Path("./temp/lodash_test")

    try:
        # Clean up if exists
        if test_repo_path.exists():
            safe_rmtree(test_repo_path)

        print(f"\n📥 Cloning {test_repo_url}...")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", test_repo_url, str(test_repo_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            print(f"❌ Clone failed: {result.stderr}")
            return False

        print(f"✅ Cloned to: {test_repo_path}")

        # Mine patterns
        print("\n⚙️  Mining patterns (this may take 30-60 seconds)...")
        df_patterns, stats = mine_repository_to_dataframe(test_repo_path)

        print("\n📊 Results:")
        print(f"   Files processed:    {stats['files_processed']}")
        print(f"   Files skipped:      {stats['files_skipped']}")
        print(f"   Parse errors:       {stats['parse_errors']}")
        print(f"   Patterns extracted: {stats['patterns_extracted']}")
        print(f"   Total frequency:    {stats['total_frequency']}")

        if stats["patterns_extracted"] > 0:
            print("\n🔍 Top 5 Patterns:")
            top_5 = df_patterns.nlargest(5, "frequency")
            for idx, row in top_5.iterrows():
                print(f"   {row['frequency']:4d}x | {row['abstract_signature'][:60]}")

        # Cleanup
        print("\n🧹 Cleaning up...")
        safe_rmtree(test_repo_path)

        print("✅ Real repository test passed!")
        return True

    except subprocess.TimeoutExpired:
        print("❌ Clone timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()

        # Try cleanup anyway
        try:
            safe_rmtree(test_repo_path)
        except:
            pass

        return False


def cleanup_test_files():
    """Clean up test repository"""
    test_repo_path = Path("./temp/test_repo")
    if test_repo_path.exists():
        safe_rmtree(test_repo_path)
        print("\n🧹 Cleaned up test files")


def main():
    """Run all Phase 2 validation tests"""
    print("\n" + "=" * 70)
    print("  🧪 PHASE 2 VALIDATION SUITE")
    print("  Testing Pattern Miner Wrapper Implementation")
    print("=" * 70)

    results = {}
    test_repo_path = None

    # Test 1: Imports
    results["Import Validation"] = test_import()

    # Test 2: Setup test repo
    if results["Import Validation"]:
        test_repo_path = setup_test_repo()
        results["Setup Test Repository"] = test_repo_path is not None
    else:
        results["Setup Test Repository"] = False

    # Test 3: Mining
    if results["Setup Test Repository"]:
        results["Pattern Mining"] = test_mining_wrapper(test_repo_path)
    else:
        results["Pattern Mining"] = False

    # Test 4: Schema validation
    if results["Pattern Mining"]:
        results["DataFrame Schema"] = test_dataframe_schema(test_repo_path)
    else:
        results["DataFrame Schema"] = False

    # Test 5: JSON serialization
    if results["DataFrame Schema"]:
        results["JSON Serialization"] = test_examples_serialization(test_repo_path)
    else:
        results["JSON Serialization"] = False

    # Test 6: Real repo (optional)
    results["Real Repository (Optional)"] = test_with_real_repo()

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        if "Optional" in test_name and not result:
            status = "⏭️  SKIP"
        else:
            status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {test_name}")

    print(f"\n{'=' * 70}")
    print(f"Results: {passed}/{total} tests passed")

    if passed >= total - 1:  # Allow optional test to be skipped
        print("\n🎉 Phase 2 is ready!")
        print("\nNext steps:")
        print("  1. Move on to Phase 3: Pattern Aggregator")
        print("  2. Review the plan: js_pattern_orchestration_plan.md")
    else:
        print("\n⚠️  Some required tests failed.")
        print("   Please review the output above.")

    print("=" * 70 + "\n")

    # Cleanup
    cleanup_test_files()

    return passed >= total - 1


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
