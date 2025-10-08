#!/usr/bin/env python3
"""
Create a persistent test repository for debugging
This won't be cleaned up automatically
"""

from pathlib import Path


# Add project root to path
import sys

project_root = Path(__file__).resolve().parents[2]
print(f"Adding {project_root} to path")
sys.path.insert(0, str(project_root))


def create_test_repo():
    """Create test repo with sample JS files"""

    test_repo_path = Path("./temp/test_repo")

    # Create directory
    test_repo_path.mkdir(parents=True, exist_ok=True)

    # Sample files with realistic content
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

    # Write files
    for filename, content in sample_files.items():
        filepath = test_repo_path / filename
        filepath.write_text(content, encoding="utf-8")

    print("=" * 70)
    print("TEST REPOSITORY CREATED")
    print("=" * 70)
    print(f"\nLocation: {test_repo_path.absolute()}")
    print(f"\nFiles created:")

    for filename in sample_files.keys():
        filepath = test_repo_path / filename
        size = filepath.stat().st_size
        print(f"  ✅ {filename:15} ({size:4} bytes)")

    return test_repo_path


def verify_files(test_repo_path):
    """Verify files are discoverable"""

    print("\n" + "=" * 70)
    print("FILE DISCOVERY TEST")
    print("=" * 70)

    # Test different methods
    print("\n1. Using iterdir():")
    items = list(test_repo_path.iterdir())
    print(f"   Found: {len(items)} items")
    for item in items:
        print(f"   - {item.name}")

    print("\n2. Using glob('*.js'):")
    matches = list(test_repo_path.glob("*.js"))
    print(f"   Found: {len(matches)} files")
    for match in matches:
        print(f"   - {match.name}")

    print("\n3. Using rglob('*.js'):")
    matches = list(test_repo_path.rglob("*.js"))
    print(f"   Found: {len(matches)} files")
    for match in matches:
        print(f"   - {match.name}")

    return len(matches) > 0


def test_pattern_miner(test_repo_path):
    """Test PatternMiner on the test repo"""

    print("\n" + "=" * 70)
    print("PATTERN MINER TEST")
    print("=" * 70)

    try:
        from src.js_pattern_analyzer.pattern_miner import PatternMiner

        print(f"\nTesting PatternMiner with: {test_repo_path}")
        print(f"  Path type: {type(test_repo_path)}")
        print(f"  Exists: {test_repo_path.exists()}")
        print(f"  Is dir: {test_repo_path.is_dir()}")

        # Create miner
        print("\nCreating PatternMiner...")
        miner = PatternMiner(test_repo_path)

        print(f"  Miner repo_path: {miner.repo_path}")
        print(f"  Miner repo_path type: {type(miner.repo_path)}")

        # Discover files
        print("\nDiscovering files...")
        files = miner.discover_files()

        print(f"  Found: {len(files)} files")
        for f in files:
            print(f"    - {f.name}")

        if len(files) == 0:
            print("\n❌ PROBLEM: PatternMiner found 0 files!")
            print("\n🔍 Debugging info:")
            print(f"  miner.repo_path = {miner.repo_path}")
            print(f"  miner.repo_path.exists() = {miner.repo_path.exists()}")
            print(f"  type(miner.repo_path) = {type(miner.repo_path)}")

            # Try manual discovery
            print("\n  Manual check:")
            for ext in ["*.js", "*.jsx", "*.ts", "*.tsx"]:
                manual_matches = list(miner.repo_path.rglob(ext))
                print(f"    rglob('{ext}'): {len(manual_matches)} files")

            return False

        # Try mining
        print("\nMining patterns...")
        patterns = miner.mine_repository()

        print(f"  Extracted: {len(patterns)} unique patterns")

        if len(patterns) > 0:
            print("\n  Top 5 patterns:")
            for i, p in enumerate(patterns[:5], 1):
                print(f"    {i}. [{p.frequency}x] {p.abstract_signature[:60]}")

        print("\n✅ SUCCESS!")
        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main test flow"""

    print("\n" + "=" * 70)
    print("  FILE DISCOVERY DIAGNOSTIC & TEST")
    print("=" * 70)

    # Step 1: Create test repo
    test_repo_path = create_test_repo()

    # Step 2: Verify files exist
    files_ok = verify_files(test_repo_path)

    if not files_ok:
        print("\n❌ Files not discoverable! Check filesystem.")
        return False

    # Step 3: Test PatternMiner
    miner_ok = test_pattern_miner(test_repo_path)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if miner_ok:
        print("✅ All checks passed!")
        print("\nNext steps:")
        print("  1. The test repo is at: temp/test_repo/")
        print("  2. You can now run: python validate_phase2.py")
        print("  3. Test repo will persist for debugging")
    else:
        print("❌ PatternMiner has issues")
        print("\nRequired fix:")
        print("  Edit pattern_miner.py, line ~260")
        print("  Change: self.repo_path = repo_path")
        print("  To:     self.repo_path = Path(repo_path)")
        print("\nThen run this script again to verify the fix")

    print("=" * 70 + "\n")

    return miner_ok


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
