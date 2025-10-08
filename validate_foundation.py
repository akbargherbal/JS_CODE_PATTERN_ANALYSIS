"""
Validation Script - Test Phase 1 + Phase 2 Implementation
Place this file in the root directory: JS_CODE_PATTERN_ANALYSIS/validate_foundation.py
"""
import sys
from pathlib import Path

import pandas as pd

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from scripts.state_manager import StateManager


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_state_manager_initialization():
    """Test 1: Initialize queue from DF_REPO_LINKS.pkl"""
    print_section("TEST 1: State Manager Initialization")
    
    try:
        state = StateManager()
        
        # Check if queue already exists
        if state.queue_exists():
            print("ℹ️  Queue already exists")
            df = state.load_queue()
            print(f"✅ Loaded existing queue: {len(df)} repos")
        else:
            print("📂 Initializing queue from DF_REPO_LINKS.pkl...")
            df = state.initialize_from_pickle()
            print(f"✅ Initialized queue: {len(df)} repos")
        
        # Validate structure
        required_cols = [
            'repo_id', 'url', 'name', 'status', 'attempt_count',
            'patterns_extracted', 'total_frequency'
        ]
        
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False
        
        print(f"✅ All required columns present")
        
        # Check statuses
        status_counts = df['status'].value_counts()
        print(f"\nStatus breakdown:")
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_state_transitions():
    """Test 2: State transitions (pending -> processing -> completed)"""
    print_section("TEST 2: State Transitions")
    
    try:
        state = StateManager()
        df = state.load_queue()
        
        # Get next pending repo
        next_repo = state.get_next_pending(df)
        
        if next_repo is None:
            print("⚠️  No pending repos to test with")
            return True
        
        print(f"📦 Selected repo: {next_repo['name']}")
        print(f"   URL: {next_repo['url']}")
        print(f"   Initial status: {next_repo['status']}")
        
        # Test: Mark as processing
        print("\n🔄 Marking as processing...")
        state.mark_processing(df, next_repo['url'])
        df = state.load_queue()
        
        status = df[df['url'] == next_repo['url']]['status'].iloc[0]
        if status != 'processing':
            print(f"❌ Expected 'processing', got '{status}'")
            return False
        print(f"✅ Status updated to: {status}")
        
        # Test: Mark as completed (with mock stats)
        print("\n✅ Marking as completed...")
        mock_stats = {
            'files_processed': 42,
            'files_skipped': 5,
            'parse_errors': 2,
            'skip_reasons': {'minified': 3, 'too_large': 2},
            'patterns_extracted': 123,
            'total_frequency': 456,
            'duration': 12.3
        }
        
        state.mark_completed(df, next_repo['url'], mock_stats)
        df = state.load_queue()
        
        repo_row = df[df['url'] == next_repo['url']].iloc[0]
        if repo_row['status'] != 'completed':
            print(f"❌ Expected 'completed', got '{repo_row['status']}'")
            return False
        
        print(f"✅ Status updated to: {repo_row['status']}")
        print(f"✅ Files processed: {repo_row['files_processed']}")
        print(f"✅ Patterns extracted: {repo_row['patterns_extracted']}")
        
        # Reset back to pending for future tests
        print("\n🔄 Resetting to pending for future tests...")
        state.reset_repo(next_repo['url'])
        df = state.load_queue()
        
        status = df[df['url'] == next_repo['url']]['status'].iloc[0]
        print(f"✅ Reset to: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_progress_stats():
    """Test 3: Progress statistics"""
    print_section("TEST 3: Progress Statistics")
    
    try:
        state = StateManager()
        stats = state.get_progress_stats()
        
        print("📊 Current Progress:")
        print(f"   Total repos:      {stats['total']}")
        print(f"   ✅ Completed:     {stats['completed']}")
        print(f"   ⏳ Pending:       {stats['pending']}")
        print(f"   ❌ Failed:        {stats['failed']}")
        print(f"   🔄 Processing:    {stats['processing']}")
        
        completion_pct = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"\n   Progress: {completion_pct:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backup_creation():
    """Test 4: Backup creation"""
    print_section("TEST 4: Backup Creation")
    
    try:
        state = StateManager()
        
        print("💾 Creating backup...")
        backup_path = state.create_backup()
        
        if not backup_path.exists():
            print(f"❌ Backup file not created: {backup_path}")
            return False
        
        print(f"✅ Backup created: {backup_path}")
        print(f"   Size: {backup_path.stat().st_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pattern_storage():
    """Test 5: Pattern storage (without actual mining)"""
    print_section("TEST 5: Pattern Storage")
    
    try:
        state = StateManager()
        
        # Create mock pattern DataFrame
        mock_patterns = pd.DataFrame({
            'pattern_hash': ['abc123', 'def456', 'ghi789'],
            'abstract_signature': [
                'const IDENTIFIER = VALUE',
                'FUNCTION(ARGUMENTS)',
                'import IDENTIFIER from STRING'
            ],
            'semantic_signature': [
                'const IDENTIFIER = FETCH_API(...)',
                'CONSOLE_METHOD(ARGUMENTS)',
                'import IDENTIFIER from STRING'
            ],
            'node_type': ['lexical_declaration', 'call_expression', 'import_statement'],
            'category': ['VARIABLE_DECLARATIONS', 'FUNCTION_CALLS', 'IMPORTS_EXPORTS'],
            'frequency': [10, 8, 5],
            'examples_json': ['[]', '[]', '[]']
        })
        
        print("📦 Saving mock patterns...")
        filepath = state.save_repo_patterns(999, 'test/mock', mock_patterns)
        
        if not filepath.exists():
            print(f"❌ Pattern file not created: {filepath}")
            return False
        
        print(f"✅ Saved to: {filepath}")
        print(f"   Size: {filepath.stat().st_size / 1024:.1f} KB")
        
        # Load back and verify
        print("\n📂 Loading back...")
        df_loaded = pd.read_pickle(filepath)
        
        if len(df_loaded) != len(mock_patterns):
            print(f"❌ Expected {len(mock_patterns)} patterns, got {len(df_loaded)}")
            return False
        
        print(f"✅ Loaded {len(df_loaded)} patterns")
        print("\nSample patterns:")
        for _, row in df_loaded.iterrows():
            print(f"   • {row['abstract_signature']} (freq: {row['frequency']})")
        
        # Cleanup test file
        print("\n🧹 Cleaning up test file...")
        filepath.unlink()
        print("✅ Cleanup complete")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests"""
    print("\n" + "=" * 70)
    print("  🧪 FOUNDATION VALIDATION SUITE")
    print("  Testing Phase 1 (State Manager) Implementation")
    print("=" * 70)
    
    tests = [
        ("State Manager Initialization", test_state_manager_initialization),
        ("State Transitions", test_state_transitions),
        ("Progress Statistics", test_progress_stats),
        ("Backup Creation", test_backup_creation),
        ("Pattern Storage", test_pattern_storage),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {test_name}")
    
    print(f"\n{'=' * 70}")
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Phase 1 is ready.")
        print("\nNext steps:")
        print("  1. Review the generated files in data/")
        print("  2. Move on to Phase 2: Pattern Miner Wrapper")
        print("  3. Run: python validate_foundation.py again after changes")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        print("   Check the traceback for details on what went wrong.")
    
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
