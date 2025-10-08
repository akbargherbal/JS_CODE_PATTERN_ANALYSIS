"""
Setup Script - Create or Locate DF_REPO_LINKS.pkl
Place this in: JS_CODE_PATTERN_ANALYSIS/setup_repo_links.py
"""
import pandas as pd
from pathlib import Path
import sys


def find_existing_file():
    """Search for DF_REPO_LINKS.pkl in common locations"""
    search_paths = [
        Path('./data/DF_REPO_LINKS.pkl'),
        Path('./DF_REPO_LINKS.pkl'),
        Path('../DF_REPO_LINKS.pkl'),
        Path('../data/DF_REPO_LINKS.pkl'),
    ]
    
    print("🔍 Searching for existing DF_REPO_LINKS.pkl...")
    for path in search_paths:
        if path.exists():
            print(f"✅ Found: {path.absolute()}")
            return path
    
    print("❌ File not found in common locations")
    return None


def inspect_file(filepath):
    """Show contents of existing file"""
    try:
        df = pd.read_pickle(filepath)
        print(f"\n📊 File contains {len(df)} repositories")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 5 rows:")
        print(df.head())
        
        # Check if it has 'REPO' column (expected format)
        if 'REPO' in df.columns:
            print(f"\n✅ File has expected 'REPO' column")
            return df
        else:
            print(f"\n⚠️  File doesn't have 'REPO' column. Found: {list(df.columns)}")
            return df
            
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def copy_to_data_dir(source_path):
    """Copy file to data/ directory"""
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    
    target_path = data_dir / 'DF_REPO_LINKS.pkl'
    
    if target_path.exists():
        print(f"\n⚠️  Target already exists: {target_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False
    
    import shutil
    shutil.copy(source_path, target_path)
    print(f"\n✅ Copied to: {target_path}")
    return True


def create_sample_file():
    """Create a sample DF_REPO_LINKS.pkl with popular JS repos"""
    print("\n📝 Creating sample DF_REPO_LINKS.pkl with 10 popular repos...")
    
    sample_repos = [
        'https://github.com/facebook/react.git',
        'https://github.com/vuejs/vue.git',
        'https://github.com/angular/angular.git',
        'https://github.com/nodejs/node.git',
        'https://github.com/microsoft/TypeScript.git',
        'https://github.com/axios/axios.git',
        'https://github.com/lodash/lodash.git',
        'https://github.com/expressjs/express.git',
        'https://github.com/webpack/webpack.git',
        'https://github.com/prettier/prettier.git',
    ]
    
    df = pd.DataFrame({'REPO': sample_repos})
    
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    
    output_path = data_dir / 'DF_REPO_LINKS.pkl'
    df.to_pickle(output_path)
    
    print(f"✅ Created sample file: {output_path}")
    print(f"   Contains {len(df)} repositories")
    print("\n⚠️  NOTE: This is a SAMPLE file for testing.")
    print("   Replace it with your actual 170-repo list!")
    
    return output_path


def create_from_csv():
    """Create from a CSV file"""
    print("\n📄 Create from CSV file")
    csv_path = input("Enter path to CSV file (with 'url' or 'repo' column): ")
    
    csv_path = Path(csv_path.strip())
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        return None
    
    try:
        df = pd.read_csv(csv_path)
        print(f"\nColumns found: {list(df.columns)}")
        
        # Try to find URL column
        url_col = None
        for col in df.columns:
            if col.lower() in ['repo', 'url', 'repository', 'git', 'github']:
                url_col = col
                break
        
        if not url_col:
            print("Available columns:", list(df.columns))
            url_col = input("Enter column name containing repo URLs: ")
        
        if url_col not in df.columns:
            print(f"❌ Column '{url_col}' not found")
            return None
        
        # Create DataFrame with 'REPO' column
        df_repos = pd.DataFrame({'REPO': df[url_col]})
        
        # Save to data/
        data_dir = Path('./data')
        data_dir.mkdir(exist_ok=True)
        output_path = data_dir / 'DF_REPO_LINKS.pkl'
        
        df_repos.to_pickle(output_path)
        print(f"\n✅ Created: {output_path}")
        print(f"   Contains {len(df_repos)} repositories")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_from_list():
    """Manually paste a list of repo URLs"""
    print("\n📝 Create from manual list")
    print("Paste repository URLs (one per line)")
    print("Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done:")
    print()
    
    repos = []
    try:
        while True:
            line = input()
            line = line.strip()
            if line:
                repos.append(line)
    except EOFError:
        pass
    
    if not repos:
        print("❌ No repositories entered")
        return None
    
    df = pd.DataFrame({'REPO': repos})
    
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)
    output_path = data_dir / 'DF_REPO_LINKS.pkl'
    
    df.to_pickle(output_path)
    print(f"\n✅ Created: {output_path}")
    print(f"   Contains {len(df)} repositories")
    
    return output_path


def main():
    print("=" * 70)
    print("  🔧 DF_REPO_LINKS.pkl Setup Wizard")
    print("=" * 70)
    
    # Try to find existing file
    existing = find_existing_file()
    
    if existing:
        df = inspect_file(existing)
        if df is not None:
            target = Path('./data/DF_REPO_LINKS.pkl')
            if existing.absolute() == target.absolute():
                print("\n✅ File is already in the correct location!")
                print("\nYou can now run: python validate_foundation.py")
                return
            else:
                copy_to_data_dir(existing)
                print("\n✅ Setup complete!")
                print("\nYou can now run: python validate_foundation.py")
                return
    
    # File not found - offer options
    print("\n" + "=" * 70)
    print("  Options:")
    print("=" * 70)
    print("1. Create sample file (10 popular repos for testing)")
    print("2. Create from CSV file")
    print("3. Create from manual list (paste URLs)")
    print("4. Exit (I'll create the file manually)")
    print()
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == '1':
        path = create_sample_file()
        if path:
            print("\n✅ Setup complete!")
            print("\nNext steps:")
            print("  1. Run: python validate_foundation.py")
            print("  2. Replace sample file with your 170 repos when ready")
    
    elif choice == '2':
        path = create_from_csv()
        if path:
            print("\n✅ Setup complete!")
            print("\nYou can now run: python validate_foundation.py")
    
    elif choice == '3':
        path = create_from_list()
        if path:
            print("\n✅ Setup complete!")
            print("\nYou can now run: python validate_foundation.py")
    
    elif choice == '4':
        print("\n📝 Manual creation instructions:")
        print("\nCreate a file at: data/DF_REPO_LINKS.pkl")
        print("\nUsing Python:")
        print("```python")
        print("import pandas as pd")
        print()
        print("repos = [")
        print("    'https://github.com/facebook/react.git',")
        print("    'https://github.com/vuejs/vue.git',")
        print("    # ... add your 170 repos ...")
        print("]")
        print()
        print("df = pd.DataFrame({'REPO': repos})")
        print("df.to_pickle('data/DF_REPO_LINKS.pkl')")
        print("```")
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
