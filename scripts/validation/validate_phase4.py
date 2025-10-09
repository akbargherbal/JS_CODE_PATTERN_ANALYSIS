import sys
from pathlib import Path
import yaml

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.js_pattern_analyzer.repo_cloner import RepoCloner


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def load_config():
    """Load project configuration."""
    config_path = project_root / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def test_successful_clone(cloner: RepoCloner):
    """Test 1: Clone a small, valid repository."""
    print_section("TEST 1: Successful Clone")

    repo_url = "https://github.com/jquery/jquery-mousewheel.git"
    repo_id = 999

    print(f"Cloning: {repo_url}")
    repo_path, error = cloner.clone(repo_url, repo_id)

    if error:
        print(f"❌ FAIL: Clone failed unexpectedly.")
        print(f"   Error: {error}")
        return False

    print(f"✅ Cloned to: {repo_path}")

    if not repo_path.exists() or not (repo_path / ".git").exists():
        print("❌ FAIL: Repository directory or .git folder not found.")
        return False

    print("✅ Directory and .git folder exist.")

    # Test cleanup
    print("\nTesting cleanup...")
    success, cleanup_error = cloner.cleanup(repo_path)

    if not success:
        print(f"❌ FAIL: Cleanup failed.")
        print(f"   Error: {cleanup_error}")
        return False

    if repo_path.exists():
        print("❌ FAIL: Directory still exists after cleanup.")
        return False

    print("✅ Cleanup successful.")
    return True


def test_failed_clone(cloner: RepoCloner):
    """Test 2: Attempt to clone a non-existent repository."""
    print_section("TEST 2: Failed Clone (Non-existent Repo)")

    repo_url = "https://github.com/nonexistent/repo.git"
    repo_id = 998

    print(f"Attempting to clone: {repo_url}")
    repo_path, error = cloner.clone(repo_url, repo_id)

    if not error:
        print("❌ FAIL: Expected an error, but clone succeeded.")
        cloner.cleanup(repo_path)  # cleanup just in case
        return False

    print(f"✅ Received expected error:")
    print(f"   {error.splitlines()[0]}")

    if repo_path.exists():
        print("⚠️  Directory was created but should be cleaned up.")
        cloner.cleanup(repo_path)

    return True


def main():
    """Run all Phase 4 validation tests."""
    print("\n" + "=" * 70)
    print("  🧪 PHASE 4 VALIDATION SUITE")
    print("  Testing Repo Cloner Implementation")
    print("=" * 70)

    try:
        config = load_config()
        cloner = RepoCloner(config)
    except Exception as e:
        print(f"❌ FAIL: Could not initialize RepoCloner: {e}")
        return False

    results = {}
    results["Successful Clone & Cleanup"] = test_successful_clone(cloner)
    results["Failed Clone (Non-existent)"] = test_failed_clone(cloner)

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
        print("\n🎉 Phase 4 is ready!")
        print("\nNext steps:")
        print("  1. Integrate RepoCloner into the Orchestrator.")
        print("  2. Move on to Phase 5: Orchestrator.")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")

    print("=" * 70 + "\n")
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
