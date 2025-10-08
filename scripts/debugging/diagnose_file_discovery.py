#!/usr/bin/env python3
"""
Diagnostic script to debug file discovery issue
Run this to understand why PatternMiner isn't finding files
"""

from pathlib import Path

# Add project root to path
import sys

project_root = Path(__file__).resolve().parents[2]
print(f"Adding {project_root} to path")
sys.path.insert(0, str(project_root))


def diagnose_test_repo():
    """Check what's happening with the test repo"""

    test_repo = Path("./temp/test_repo")

    print("=" * 70)
    print("FILE DISCOVERY DIAGNOSTIC")
    print("=" * 70)

    # 1. Check directory exists
    print(f"\n1. Directory check:")
    print(f"   Path: {test_repo}")
    print(f"   Absolute: {test_repo.absolute()}")
    print(f"   Exists: {test_repo.exists()}")
    print(f"   Is dir: {test_repo.is_dir()}")

    if not test_repo.exists():
        print("\n❌ ERROR: Test repo doesn't exist!")
        print("   Run: python validate_phase2.py first")
        return

    # 2. List all files
    print(f"\n2. All files in directory:")
    try:
        all_files = list(test_repo.iterdir())
        print(f"   Total items: {len(all_files)}")
        for item in all_files:
            print(f"   - {item.name} ({'dir' if item.is_dir() else 'file'})")
    except Exception as e:
        print(f"   ❌ Error listing: {e}")

    # 3. Test rglob patterns
    print(f"\n3. Testing rglob patterns:")
    patterns = ["*.js", "*.jsx", "*.ts", "*.tsx", "*.mjs", "*.cjs"]

    for pattern in patterns:
        try:
            matches = list(test_repo.rglob(pattern))
            print(f"   {pattern:10} → {len(matches)} files")
            for match in matches:
                print(f"      - {match.name} ({match.stat().st_size} bytes)")
        except Exception as e:
            print(f"   {pattern:10} → ERROR: {e}")

    # 4. Test glob (non-recursive)
    print(f"\n4. Testing glob (non-recursive):")
    for pattern in patterns:
        try:
            matches = list(test_repo.glob(pattern))
            print(f"   {pattern:10} → {len(matches)} files")
            for match in matches:
                print(f"      - {match.name}")
        except Exception as e:
            print(f"   {pattern:10} → ERROR: {e}")

    # 5. Manual check
    print(f"\n5. Manual file check:")
    expected_files = ["index.js", "utils.js", "config.js"]
    for filename in expected_files:
        filepath = test_repo / filename
        exists = filepath.exists()
        size = filepath.stat().st_size if exists else 0
        print(f"   {filename:15} → {'✅' if exists else '❌'} ({size} bytes)")

    # 6. Test with PatternMiner
    print(f"\n6. Testing with PatternMiner:")
    try:
        from src.js_pattern_analyzer.pattern_miner import PatternMiner

        # Test with different path types
        print("\n   a) With Path object:")
        miner1 = PatternMiner(test_repo)
        files1 = miner1.discover_files()
        print(f"      Found: {len(files1)} files")

        print("\n   b) With string path:")
        miner2 = PatternMiner(str(test_repo))
        files2 = miner2.discover_files()
        print(f"      Found: {len(files2)} files")

        print("\n   c) With absolute path:")
        miner3 = PatternMiner(test_repo.absolute())
        files3 = miner3.discover_files()
        print(f"      Found: {len(files3)} files")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("DIAGNOSIS COMPLETE")
    print("=" * 70)


def test_path_operations():
    """Test basic Path operations"""
    print("\n" + "=" * 70)
    print("PATH OPERATIONS TEST")
    print("=" * 70)

    test_dir = Path("./temp/test_repo")

    print(f"\n1. Path creation:")
    print(f"   From string: {Path('./temp/test_repo')}")
    print(f"   Type: {type(test_dir)}")

    print(f"\n2. Path methods:")
    if test_dir.exists():
        print(f"   .exists(): {test_dir.exists()}")
        print(f"   .is_dir(): {test_dir.is_dir()}")
        print(f"   .absolute(): {test_dir.absolute()}")
        print(f"   .resolve(): {test_dir.resolve()}")
    else:
        print("   ⚠️  Directory doesn't exist")

    print(f"\n3. Creating test file:")
    test_file = test_dir / "diagnostic_test.js"
    try:
        if test_dir.exists():
            test_file.write_text('console.log("test");')
            print(f"   Created: {test_file.name}")
            print(f"   Exists: {test_file.exists()}")

            # Test discovery
            matches = list(test_dir.glob("*.js"))
            print(f"   glob('*.js'): {len(matches)} files")

            matches_r = list(test_dir.rglob("*.js"))
            print(f"   rglob('*.js'): {len(matches_r)} files")

            # Cleanup
            test_file.unlink()
            print(f"   Cleaned up test file")
        else:
            print("   ⚠️  Can't create test - directory missing")
    except Exception as e:
        print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    print("\nDIAGNOSTIC TOOL FOR FILE DISCOVERY ISSUE\n")

    if len(sys.argv) > 1 and sys.argv[1] == "--path-test":
        test_path_operations()
    else:
        diagnose_test_repo()

    print("\n💡 Tip: Run with --path-test to test basic Path operations")
