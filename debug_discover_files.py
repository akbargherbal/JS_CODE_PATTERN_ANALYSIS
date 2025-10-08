#!/usr/bin/env python3
"""
Deep dive into discover_files() to find why files are filtered out
"""

from pathlib import Path
from pattern_miner import PatternMiner

def debug_discover_files():
    """Step through discover_files() logic manually"""
    
    test_repo_path = Path('./temp/test_repo')
    
    print("=" * 70)
    print("DEEP DIVE: discover_files() METHOD")
    print("=" * 70)
    
    # Setup
    miner = PatternMiner(test_repo_path)
    
    print(f"\n1. SETUP")
    print(f"   repo_path: {miner.repo_path}")
    print(f"   max_file_size: {miner.max_file_size / 1024 / 1024:.1f} MB")
    
    # Ignore patterns (copied from pattern_miner.py)
    ignore_patterns = {
        'node_modules', 'dist', 'build', '.git', 'coverage', 'vendor',
        '.next', '.nuxt', 'out', 'public', '__pycache__', '.cache',
        'tmp', 'temp', '.venv', 'venv', 'bower_components',
    }
    
    print(f"\n2. IGNORE PATTERNS")
    print(f"   {ignore_patterns}")
    
    # Test each file
    print(f"\n3. TESTING EACH FILE")
    
    extensions = ['*.js', '*.jsx', '*.ts', '*.tsx', '*.mjs', '*.cjs']
    all_files_found = []
    
    for ext in extensions:
        matches = list(miner.repo_path.rglob(ext))
        print(f"\n   Extension: {ext}")
        print(f"   Raw matches: {len(matches)}")
        
        for filepath in matches:
            print(f"\n   Processing: {filepath.name}")
            print(f"     - Path parts: {filepath.parts}")
            
            # Check 1: Ignored directories
            ignored_match = [p for p in ignore_patterns if p in filepath.parts]
            if ignored_match:
                print(f"     ❌ FILTERED: Matched ignore pattern '{ignored_match[0]}'")
                continue
            else:
                print(f"     ✅ Not in ignored directories")
            
            # Check 2: Minified filename
            if '.min.' in filepath.name or '-min.' in filepath.name:
                print(f"     ❌ FILTERED: Minified filename pattern")
                continue
            else:
                print(f"     ✅ Not minified filename")
            
            # Check 3: File size
            try:
                size = filepath.stat().st_size
                print(f"     - File size: {size} bytes ({size / 1024:.1f} KB)")
                
                if size > miner.max_file_size:
                    print(f"     ❌ FILTERED: Too large (>{miner.max_file_size / 1024 / 1024:.1f} MB)")
                    continue
                else:
                    print(f"     ✅ Size OK")
            except Exception as e:
                print(f"     ❌ FILTERED: Error checking size: {e}")
                continue
            
            # Check 4: Minified content
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    first_line = f.readline()
                    print(f"     - First line length: {len(first_line)} chars")
                    
                    if len(first_line) > 500:
                        print(f"     ❌ FILTERED: Likely minified (first line > 500 chars)")
                        continue
                    else:
                        print(f"     ✅ Not minified content")
            except Exception as e:
                print(f"     ⚠️  Could not check content: {e}")
            
            print(f"     ✅✅✅ SHOULD BE INCLUDED")
            all_files_found.append(filepath)
    
    print(f"\n" + "=" * 70)
    print(f"MANUAL FILTER RESULTS")
    print(f"=" * 70)
    print(f"Files that should pass all filters: {len(all_files_found)}")
    for f in all_files_found:
        print(f"  ✅ {f.name}")
    
    # Now compare with actual discover_files()
    print(f"\n" + "=" * 70)
    print(f"ACTUAL discover_files() RESULTS")
    print(f"=" * 70)
    
    actual_files = miner.discover_files()
    print(f"Files returned: {len(actual_files)}")
    for f in actual_files:
        print(f"  - {f.name}")
    
    # Compare
    print(f"\n" + "=" * 70)
    print(f"COMPARISON")
    print(f"=" * 70)
    
    if len(all_files_found) == len(actual_files):
        print(f"✅ MATCH: Both found {len(all_files_found)} files")
    else:
        print(f"❌ MISMATCH:")
        print(f"   Expected: {len(all_files_found)} files")
        print(f"   Got:      {len(actual_files)} files")
        print(f"   Missing:  {len(all_files_found) - len(actual_files)} files")
        
        # Show what's missing
        if len(all_files_found) > 0 and len(actual_files) == 0:
            print(f"\n   All expected files were filtered out!")
            print(f"   There must be a bug in discover_files() logic")


def check_path_parts():
    """Check if 'temp' in path.parts is causing issues"""
    
    print("\n" + "=" * 70)
    print("PATH PARTS ANALYSIS")
    print("=" * 70)
    
    test_repo_path = Path('./temp/test_repo')
    
    ignore_patterns = {
        'node_modules', 'dist', 'build', '.git', 'coverage', 'vendor',
        '.next', '.nuxt', 'out', 'public', '__pycache__', '.cache',
        'tmp', 'temp', '.venv', 'venv', 'bower_components',
    }
    
    print(f"\nTest repo path: {test_repo_path}")
    print(f"Path parts: {test_repo_path.parts}")
    
    # Check files
    for filepath in test_repo_path.glob('*.js'):
        print(f"\nFile: {filepath.name}")
        print(f"  Full path: {filepath}")
        print(f"  Parts: {filepath.parts}")
        
        # Check against ignore patterns
        matches = [p for p in ignore_patterns if p in filepath.parts]
        
        if matches:
            print(f"  ❌ MATCHES IGNORE PATTERN: {matches}")
            print(f"     ⚠️  THIS IS THE BUG!")
        else:
            print(f"  ✅ No ignore pattern matches")


if __name__ == "__main__":
    debug_discover_files()
    check_path_parts()
    
    print("\n" + "=" * 70)
    print("DIAGNOSIS COMPLETE")
    print("=" * 70)
    print("\nIf 'temp' in ignore patterns is causing the issue:")
    print("  The fix is to check DIRECTORY names, not ALL path parts")
    print("  Or exclude the repo_path itself from the check")
    print("=" * 70 + "\n")
