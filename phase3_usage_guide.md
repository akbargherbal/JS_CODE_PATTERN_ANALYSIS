# Phase 3: Pattern Aggregator - Usage Guide

## 🎯 What Phase 3 Does

The Pattern Aggregator combines patterns from multiple repositories into a unified dataset, calculating:
- **Total frequency** across all repos
- **Prevalence** (what % of repos contain each pattern)
- **Category statistics**
- **Cross-repo examples**

---

## 🚀 Quick Start

### 1. Run Validation Tests

```bash
cd JS_CODE_PATTERN_ANALYSIS
python validate_phase3.py
```

This will:
- Create mock pattern files
- Test aggregation logic
- Test export functionality
- Verify all calculations

**Expected output:** All 6 tests should pass ✅

---

### 2. Using with Real Data

After you've mined patterns from real repositories (Phase 2), aggregate them:

```bash
# From project root
cd JS_CODE_PATTERN_ANALYSIS

# Run aggregation
python scripts/pattern_aggregator.py
```

**Default behavior:**
- Loads all `data/patterns_by_repo/repo_*.pkl` files
- Filters: `min_repo_count=2`, `min_total_frequency=5`
- Exports top 200 patterns to `results/`

---

### 3. Custom Aggregation

```bash
# More strict filtering
python scripts/pattern_aggregator.py --min-repos 5 --min-freq 20 --top-k 100

# Less strict (include rare patterns)
python scripts/pattern_aggregator.py --min-repos 1 --min-freq 1 --top-k 500
```

**Parameters:**
- `--min-repos N`: Pattern must appear in at least N repositories
- `--min-freq N`: Pattern must have total frequency ≥ N
- `--top-k N`: Export top N patterns

---

## 📊 Output Files

After running aggregation, you'll find:

### `results/patterns_top_200.json`
```json
{
  "metadata": {
    "generated_at": "2025-10-08T...",
    "top_k": 200,
    "total_patterns": 5432,
    "total_occurrences": 125678
  },
  "patterns": [
    {
      "rank": 1,
      "pattern_hash": "abc123...",
      "abstract_signature": "const IDENTIFIER = VALUE",
      "total_frequency": 15234,
      "repo_count": 89,
      "prevalence_pct": 52.35,
      "examples": [...]
    }
  ]
}
```

### `results/patterns_top_200.md`
Human-readable Markdown report with:
- Summary statistics
- Patterns grouped by category
- Code examples
- Easy to share/publish

### `results/patterns_full.parquet`
Complete dataset in compressed columnar format:
- All patterns (not just top-k)
- Efficient for pandas/data analysis
- Can load with: `df = pd.read_parquet('patterns_full.parquet')`

### `results/category_summary.csv`
Category-level statistics:
- Pattern count per category
- Total frequency per category
- Average prevalence

---

## 🔍 Programmatic Usage

### Basic Aggregation

```python
from scripts.pattern_aggregator import PatternAggregator

# Initialize
aggregator = PatternAggregator()

# Aggregate all patterns
df_agg = aggregator.aggregate_all_patterns(
    min_repo_count=2,
    min_total_frequency=5
)

# View top 10
print(df_agg.head(10))
```

### Custom Export

```python
# Export top 500 to custom directory
aggregator.export_top_k(
    df_agg, 
    k=500, 
    output_dir='./results/top_500'
)
```

### Category Analysis

```python
# Get category summary
category_stats = aggregator.get_category_summary(df_agg)
print(category_stats)

# Filter by category
react_patterns = df_agg[df_agg['category'] == 'REACT_PATTERNS']
print(f"React patterns: {len(react_patterns)}")
```

### Custom Filtering

```python
# Find universal patterns (in 90%+ of repos)
universal = df_agg[df_agg['prevalence_pct'] > 90]
print(f"Universal patterns: {len(universal)}")

# Find high-frequency patterns
frequent = df_agg[df_agg['total_frequency'] > 1000]
print(f"High-frequency patterns: {len(frequent)}")
```

---

## 📈 Understanding the Output

### Key Columns

| Column | Description | Example |
|--------|-------------|---------|
| `rank` | Position by total_frequency | 1, 2, 3, ... |
| `pattern_hash` | Unique identifier | "abc123def456" |
| `abstract_signature` | Generic pattern | "const IDENTIFIER = VALUE" |
| `semantic_signature` | Enriched pattern | "const IDENTIFIER = FETCH_API(...)" |
| `total_frequency` | Sum across all repos | 15234 |
| `repo_count` | Number of repos containing it | 89 |
| `prevalence_pct` | % of repos (repo_count/total*100) | 52.35 |
| `category` | Pattern category | "VARIABLE_DECLARATIONS" |

### Prevalence Interpretation

- **>90%**: Universal patterns (foundational JavaScript)
- **50-90%**: Very common patterns
- **25-50%**: Common patterns
- **10-25%**: Moderately common
- **<10%**: Specialized/niche patterns

---

## 🛠️ Troubleshooting

### "No pattern files found"
**Problem:** `data/patterns_by_repo/` is empty

**Solution:** 
1. Run Phase 2 validation: `python validate_phase2.py`
2. Or mine real repositories first

### "Memory error during aggregation"
**Problem:** Too many patterns to load at once

**Solution:**
- Increase minimum thresholds: `--min-repos 5 --min-freq 20`
- Or process in batches (modify code to load repos incrementally)

### "Export files not created"
**Problem:** `results/` directory permission issues

**Solution:**
```bash
mkdir -p results
chmod 755 results
```

---

## ✅ Validation Checklist

Before moving to Phase 4, verify:

- [ ] `validate_phase3.py` passes all tests
- [ ] Mock aggregation works correctly
- [ ] All output files are created
- [ ] JSON structure is valid
- [ ] Markdown is readable
- [ ] Parquet can be loaded
- [ ] Math checks out (frequency sums, prevalence %)

---

## 🎯 Next Steps

After Phase 3 is validated:

1. **Test with real data** (if you have mined repos from Phase 2)
2. **Review aggregated patterns** to ensure quality
3. **Move to Phase 4:** Implement `repo_cloner.py`
4. **Then Phase 5:** Build the orchestrator

---

## 📚 Additional Examples

### Find Framework-Specific Patterns

```python
# React patterns
react = df_agg[df_agg['abstract_signature'].str.contains('REACT', na=False)]
print(f"React patterns: {len(react)}")
print(react[['abstract_signature', 'total_frequency', 'prevalence_pct']].head(10))

# Async patterns
async_patterns = df_agg[df_agg['category'] == 'ASYNC_OPERATIONS']
print(f"Async patterns: {len(async_patterns)}")
```

### Compare Categories

```python
category_summary = aggregator.get_category_summary(df_agg)

# Plot (if matplotlib available)
import matplotlib.pyplot as plt

category_summary[('total_frequency', 'sum')].plot(kind='bar')
plt.title('Patterns by Category')
plt.xlabel('Category')
plt.ylabel('Total Frequency')
plt.tight_layout()
plt.savefig('category_distribution.png')
```

### Export Specific Categories

```python
# Export only React patterns
react_patterns = df_agg[df_agg['category'] == 'REACT_PATTERNS']

aggregator.export_top_k(
    react_patterns,
    k=50,
    output_dir='./results/react_only'
)
```

---

## 🎓 Understanding Aggregation Logic

The aggregator performs these steps:

1. **Load** all `repo_*.pkl` files from `data/patterns_by_repo/`
2. **Add** `repo_id` and `repo_name` to each DataFrame
3. **Concatenate** all DataFrames into one large DataFrame
4. **Group** by `pattern_hash` and aggregate:
   - `total_frequency` = sum of frequencies
   - `repo_count` = count of unique repo_ids
   - `repos_list` = list of repo names
   - Keep first occurrence of metadata fields
5. **Calculate** `prevalence_pct` = (repo_count / total_repos) * 100
6. **Filter** by minimum thresholds
7. **Sort** by total_frequency (descending)
8. **Export** to multiple formats

---

## 💡 Tips

- Start with strict filters (`min_repo_count=5`) to focus on truly common patterns
- Use Parquet for custom analysis (much faster than JSON for large datasets)
- Review Markdown report for human verification of results
- Check category distribution to ensure mining worked correctly
- Universal patterns (>90% prevalence) are good for teaching fundamentals

---

**Ready to continue?** Run `python validate_phase3.py` to verify everything works!
