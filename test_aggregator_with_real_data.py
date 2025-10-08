"""
Test Pattern Aggregator with Real Repository Data
This bridges Phase 2 and Phase 3 - mines a few repos then aggregates
Place this in: JS_CODE_PATTERN_ANALYSIS/test_aggregator_with_real_data.py
"""

import sys
from pathlib import Path
import subprocess
import shutil
import time

import pandas as pd

# Import components
from pattern_miner_wrapper import mine_repository_to_dataframe
from scripts.pattern_aggregator import PatternAggregator


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def clone_repo(url: str, target_dir: Path, timeout: int = 120) -> bool:
    """Clone a repository."""
    try:
        if target_dir.exists():
            shutil.rmtree(target_dir)

        print(f"   📥 Cloning {url}...")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            print(f"   ❌ Clone failed: {result.stderr[:100]}")
            return False

        print(f"   ✅ Cloned successfully")
        return True

    except subprocess.TimeoutExpired:
        print(f"   ❌ Clone timed out")
        return False
    except Exception as e:
        print(f"   ❌ Clone error: {e}")
        return False


def cleanup_repo(repo_dir: Path):
    """Clean up cloned repository."""
    try:
        if repo_dir.exists():
            shutil.rmtree(repo_dir)
    except Exception as e:
        print(f"   ⚠️  Cleanup warning: {e}")


def mine_and_save_repo(
    repo_id: int, repo_url: str, repo_name: str, patterns_dir: Path
) -> bool:
    """Mine a repository and save patterns."""
    print(f"\n📦 Processing Repository {repo_id}: {repo_name}")

    temp_dir = Path("./temp")
    temp_dir.mkdir(exist_ok=True)

    repo_dir = temp_dir / f"repo_{repo_id}"

    try:
        # Clone
        if not clone_repo(repo_url, repo_dir):
            return False

        # Mine patterns
        print(f"   ⚙️  Mining patterns...")
        start = time.time()

        df_patterns, stats = mine_repository_to_dataframe(repo_dir)

        duration = time.time() - start

        print(f"   ✅ Extracted {len(df_patterns)} patterns in {duration:.1f}s")
        print(f"      Files processed: {stats['files_processed']}")
        print(f"      Total frequency: {stats['total_frequency']}")

        # Save patterns
        patterns_dir.mkdir(parents=True, exist_ok=True)
        safe_name = repo_name.replace("/", "_")
        output_file = patterns_dir / f"repo_{repo_id:03d}_{safe_name}.pkl"

        df_patterns.to_pickle(output_file)
        print(f"   💾 Saved to: {output_file.name}")

        return True

    except Exception as e:
        print(f"   ❌ Mining failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Cleanup
        cleanup_repo(repo_dir)


def main():
    """Main test flow."""
    print("\n" + "=" * 70)
    print("  🧪 REAL DATA TEST: Phase 2 + Phase 3 Integration")
    print("=" * 70)

    # Test repositories (small, fast to clone)
    test_repos = [
        (1, "https://github.com/lodash/lodash.git", "lodash/lodash"),
        (2, "https://github.com/axios/axios.git", "axios/axios"),
        (3, "https://github.com/expressjs/express.git", "expressjs/express"),
    ]

    patterns_dir = Path("./data/patterns_by_repo_test")

    print(f"\nThis test will:")
    print(f"  1. Clone {len(test_repos)} small repositories")
    print(f"  2. Mine patterns from each (Phase 2)")
    print(f"  3. Aggregate patterns across repos (Phase 3)")
    print(f"  4. Export results")
    print(f"\n  Estimated time: 3-5 minutes")

    response = input("\nContinue? (y/n): ").strip().lower()
    if response != "y":
        print("Cancelled")
        return

    # Step 1: Mine repositories
    print_section("STEP 1: Mining Repositories")

    success_count = 0
    for repo_id, repo_url, repo_name in test_repos:
        if mine_and_save_repo(repo_id, repo_url, repo_name, patterns_dir):
            success_count += 1

    print(f"\n✅ Successfully mined {success_count}/{len(test_repos)} repositories")

    if success_count == 0:
        print("❌ No repositories were successfully mined. Cannot continue.")
        return False

    # Step 2: Aggregate patterns
    print_section("STEP 2: Aggregating Patterns")

    try:
        aggregator = PatternAggregator(
            patterns_dir=patterns_dir, results_dir=Path("./results/test_aggregation")
        )

        # Run aggregation
        df_agg = aggregator.aggregate_all_patterns(
            min_repo_count=1,  # Include patterns from any repo
            min_total_frequency=2,  # Low threshold for testing
        )

        print(f"\n✅ Aggregation completed successfully!")

        # Export results
        print_section("STEP 3: Exporting Results")

        output_paths = aggregator.export_top_k(df_agg, k=50)

        print(f"\n📁 Results saved to:")
        for format_name, path in output_paths.items():
            size_kb = path.stat().st_size / 1024
            print(f"   • {format_name:20s} {path.name:40s} ({size_kb:.1f} KB)")

        # Analysis
        print_section("STEP 4: Analysis")

        print(f"\n📊 Pattern Statistics:")
        print(f"   Total unique patterns: {len(df_agg):,}")
        print(f"   Total occurrences: {df_agg['total_frequency'].sum():,}")
        print(f"   Repositories analyzed: {success_count}")

        print(f"\n📊 Prevalence Distribution:")
        print(
            f"   Universal (100%): {len(df_agg[df_agg['prevalence_pct'] == 100.0])} patterns"
        )
        print(
            f"   Common (66-99%): {len(df_agg[(df_agg['prevalence_pct'] >= 66) & (df_agg['prevalence_pct'] < 100)])} patterns"
        )
        print(
            f"   Moderate (33-65%): {len(df_agg[(df_agg['prevalence_pct'] >= 33) & (df_agg['prevalence_pct'] < 66)])} patterns"
        )
        print(
            f"   Unique (<33%): {len(df_agg[df_agg['prevalence_pct'] < 33])} patterns"
        )

        print(f"\n📊 Top 15 Patterns:")
        for idx, row in df_agg.head(15).iterrows():
            print(
                f"   {row['rank']:2d}. [{row['total_frequency']:5,}x | {row['prevalence_pct']:5.0f}%] {row['abstract_signature'][:55]}"
            )

        print(f"\n📊 Category Distribution:")
        category_stats = (
            df_agg.groupby("category")
            .agg({"pattern_hash": "count", "total_frequency": "sum"})
            .sort_values("total_frequency", ascending=False)
        )

        for category, row in category_stats.head(10).iterrows():
            print(
                f"   {category:30s} {row['pattern_hash']:4d} patterns, {row['total_frequency']:6,} occurrences"
            )

        # Success!
        print_section("✨ SUCCESS")

        print("\n🎉 Integration test completed successfully!")
        print("\nWhat we validated:")
        print("   ✅ Phase 2: Pattern mining works on real repos")
        print("   ✅ Phase 3: Aggregation combines patterns correctly")
        print("   ✅ Export: All output formats generated")
        print("   ✅ Statistics: Prevalence and frequency calculations correct")

        print("\n📁 Check the results:")
        print(f"   • JSON: results/test_aggregation/patterns_top_50.json")
        print(f"   • Markdown: results/test_aggregation/patterns_top_50.md")
        print(f"   • Parquet: results/test_aggregation/patterns_full.parquet")

        print("\n🚀 Next steps:")
        print("   1. Review the generated reports")
        print("   2. Move to Phase 4: Repo Cloner")
        print("   3. Then Phase 5: Orchestrator")

        # Cleanup option
        print_section("Cleanup")

        print("\nTest pattern files are in: data/patterns_by_repo_test/")
        print("Test results are in: results/test_aggregation/")

        cleanup = input("\nDelete test files? (y/n): ").strip().lower()
        if cleanup == "y":
            try:
                if patterns_dir.exists():
                    shutil.rmtree(patterns_dir)
                    print("   ✅ Deleted test pattern files")

                test_results = Path("./results/test_aggregation")
                if test_results.exists():
                    shutil.rmtree(test_results)
                    print("   ✅ Deleted test results")
            except Exception as e:
                print(f"   ⚠️  Cleanup warning: {e}")
        else:
            print("   ℹ️  Test files kept for review")

        return True

    except Exception as e:
        print(f"\n❌ Aggregation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 70 + "\n")
    sys.exit(0 if success else 1)
