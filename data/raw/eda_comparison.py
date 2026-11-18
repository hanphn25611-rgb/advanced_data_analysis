"""
EDA & Comparison Script cho 2 Datasets
=======================================
Script này thực hiện:
1. Load cả 2 datasets
2. Exploratory Data Analysis cho mỗi dataset
3. So sánh chi tiết
4. Tạo file DATASET_COMPARISON.md với recommendation

Author: Claude Agent
Date: 2026-11-03
Project: Multi-Channel Marketing Campaign Optimization
"""

import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = "data/raw"
CAUSAL_DIR = os.path.join(BASE_DIR, "causal_marketing")
MTA_DIR = os.path.join(BASE_DIR, "multi_touch")
OUTPUT_FILE = os.path.join(BASE_DIR, "DATASET_COMPARISON.md")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_dataset(folder_path, dataset_name):
    """Load all CSV files from a folder"""
    print(f"\n{'='*60}")
    print(f"Loading {dataset_name}...")
    print(f"{'='*60}")

    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not csv_files:
        print(f"⚠️  No CSV files found in {folder_path}")
        return None

    print(f"Found {len(csv_files)} CSV file(s):")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")

    # Load first CSV (hoặc merge nếu có nhiều)
    df = pd.read_csv(csv_files[0])
    print(f"\n✅ Loaded: {csv_files[0]}")
    print(f"Shape: {df.shape}")

    return df, csv_files[0]


def analyze_schema(df, dataset_name):
    """Phân tích schema của dataset"""
    print(f"\n{'='*60}")
    print(f"SCHEMA ANALYSIS: {dataset_name}")
    print(f"{'='*60}")

    schema_info = {
        'total_rows': len(df),
        'total_cols': len(df.columns),
        'columns': [],
        'dtypes': df.dtypes.value_counts().to_dict(),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024**2
    }

    # Column details
    for col in df.columns:
        col_info = {
            'name': col,
            'dtype': str(df[col].dtype),
            'missing_pct': (df[col].isna().sum() / len(df)) * 100,
            'unique_count': df[col].nunique(),
            'sample_values': df[col].dropna().head(3).tolist() if len(df) > 0 else []
        }
        schema_info['columns'].append(col_info)

    # Print summary
    print(f"\nDimensions: {schema_info['total_rows']:,} rows × {schema_info['total_cols']} columns")
    print(f"Memory usage: {schema_info['memory_mb']:.2f} MB")
    print(f"\nData types distribution:")
    for dtype, count in schema_info['dtypes'].items():
        print(f"  - {dtype}: {count} columns")

    print(f"\nColumn Details:")
    print(f"{'Column':<30} {'Type':<15} {'Missing %':<12} {'Unique':<10} {'Sample Values'}")
    print("-" * 100)
    for col in schema_info['columns']:
        sample_str = str(col['sample_values'])[:40]
        print(f"{col['name']:<30} {col['dtype']:<15} {col['missing_pct']:>10.2f}% {col['unique_count']:>9,}  {sample_str}")

    return schema_info


def analyze_temporal(df, dataset_name):
    """Phân tích temporal structure"""
    print(f"\n{'='*60}")
    print(f"TEMPORAL ANALYSIS: {dataset_name}")
    print(f"{'='*60}")

    # Tìm date columns
    date_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in ['date', 'time', 'timestamp', 'day', 'month', 'year']):
            date_cols.append(col)

    if not date_cols:
        print("❌ No obvious date/time columns found")
        return None

    print(f"Found {len(date_cols)} potential date column(s): {date_cols}")

    temporal_info = {}
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            if df[col].notna().sum() > 0:
                temporal_info[col] = {
                    'min_date': df[col].min(),
                    'max_date': df[col].max(),
                    'date_range': (df[col].max() - df[col].min()).days,
                    'valid_pct': (df[col].notna().sum() / len(df)) * 100
                }
                print(f"\n{col}:")
                print(f"  Range: {temporal_info[col]['min_date']} to {temporal_info[col]['max_date']}")
                print(f"  Duration: {temporal_info[col]['date_range']} days")
                print(f"  Valid: {temporal_info[col]['valid_pct']:.1f}%")
        except Exception as e:
            print(f"  ⚠️  Could not parse {col} as date: {e}")

    return temporal_info


def analyze_multichannel(df, dataset_name):
    """Phân tích multi-channel structure"""
    print(f"\n{'='*60}")
    print(f"MULTI-CHANNEL ANALYSIS: {dataset_name}")
    print(f"{'='*60}")

    # Tìm channel column
    channel_col = None
    for col in df.columns:
        col_lower = col.lower()
        if 'channel' in col_lower or 'source' in col_lower or 'medium' in col_lower:
            channel_col = col
            break

    if not channel_col:
        print("❌ No obvious channel column found")
        return None

    print(f"Channel column: {channel_col}")

    channel_dist = df[channel_col].value_counts()
    channel_pct = df[channel_col].value_counts(normalize=True) * 100

    print(f"\nChannel Distribution:")
    print(f"{'Channel':<30} {'Count':<12} {'Percentage'}")
    print("-" * 60)
    for channel, count in channel_dist.head(10).items():
        print(f"{str(channel):<30} {count:>10,}  {channel_pct[channel]:>8.2f}%")

    return {
        'channel_col': channel_col,
        'unique_channels': df[channel_col].nunique(),
        'distribution': channel_dist.to_dict()
    }


def analyze_treatment_outcome(df, dataset_name):
    """Phân tích treatment/control và outcome variables"""
    print(f"\n{'='*60}")
    print(f"TREATMENT & OUTCOME ANALYSIS: {dataset_name}")
    print(f"{'='*60}")

    results = {
        'treatment_cols': [],
        'outcome_cols': [],
        'conversion_rate': None
    }

    # Tìm treatment columns
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in ['treatment', 'control', 'test', 'variant', 'group', 'campaign']):
            results['treatment_cols'].append(col)
            print(f"\nPotential Treatment: {col}")
            print(df[col].value_counts().head(10))

    # Tìm outcome columns
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in ['conversion', 'convert', 'purchase', 'buy', 'outcome', 'response']):
            results['outcome_cols'].append(col)
            print(f"\nPotential Outcome: {col}")
            outcome_dist = df[col].value_counts()
            print(outcome_dist)

            # Calculate conversion rate if binary
            if df[col].nunique() <= 5:
                positive_vals = [v for v in df[col].unique() if v in [1, '1', 'Yes', 'yes', 'Y', 'TRUE', True]]
                if positive_vals:
                    conv_rate = (df[col].isin(positive_vals).sum() / len(df)) * 100
                    results['conversion_rate'] = conv_rate
                    print(f"  → Conversion Rate: {conv_rate:.2f}%")

    if not results['treatment_cols']:
        print("\n❌ No obvious treatment columns found")
    if not results['outcome_cols']:
        print("\n❌ No obvious outcome columns found")

    return results


def analyze_quality(df, dataset_name):
    """Phân tích data quality"""
    print(f"\n{'='*60}")
    print(f"DATA QUALITY ANALYSIS: {dataset_name}")
    print(f"{'='*60}")

    quality = {
        'total_rows': len(df),
        'duplicate_rows': df.duplicated().sum(),
        'duplicate_pct': (df.duplicated().sum() / len(df)) * 100,
        'missing_cells': df.isna().sum().sum(),
        'missing_pct': (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100,
        'columns_with_missing': (df.isna().sum() > 0).sum()
    }

    print(f"Total rows: {quality['total_rows']:,}")
    print(f"Duplicate rows: {quality['duplicate_rows']:,} ({quality['duplicate_pct']:.2f}%)")
    print(f"Missing cells: {quality['missing_cells']:,} ({quality['missing_pct']:.2f}%)")
    print(f"Columns with missing: {quality['columns_with_missing']}/{len(df.columns)}")

    # Columns with high missing rate
    high_missing = df.isna().sum() / len(df)
    high_missing = high_missing[high_missing > 0.1]

    if len(high_missing) > 0:
        print(f"\n⚠️  Columns with >10% missing:")
        for col, pct in high_missing.items():
            print(f"  - {col}: {pct*100:.1f}%")

    return quality


# ============================================================================
# MAIN COMPARISON FUNCTION
# ============================================================================

def compare_datasets(df1, name1, df2, name2):
    """So sánh 2 datasets và tạo comparison report"""

    print(f"\n\n{'#'*60}")
    print(f"# DATASET COMPARISON")
    print(f"{'#'*60}\n")

    # Analyze both datasets
    print("\n" + "="*60)
    print("ANALYZING DATASET 1: " + name1)
    print("="*60)

    schema1 = analyze_schema(df1, name1)
    temporal1 = analyze_temporal(df1, name1)
    channel1 = analyze_multichannel(df1, name1)
    treatment1 = analyze_treatment_outcome(df1, name1)
    quality1 = analyze_quality(df1, name1)

    print("\n" + "="*60)
    print("ANALYZING DATASET 2: " + name2)
    print("="*60)

    schema2 = analyze_schema(df2, name2)
    temporal2 = analyze_temporal(df2, name2)
    channel2 = analyze_multichannel(df2, name2)
    treatment2 = analyze_treatment_outcome(df2, name2)
    quality2 = analyze_quality(df2, name2)

    # Create comparison report
    report = create_comparison_report(
        name1, schema1, temporal1, channel1, treatment1, quality1,
        name2, schema2, temporal2, channel2, treatment2, quality2
    )

    return report


def create_comparison_report(name1, schema1, temporal1, channel1, treatment1, quality1,
                            name2, schema2, temporal2, channel2, treatment2, quality2):
    """Tạo markdown report so sánh 2 datasets"""

    report = f"""# DATASET COMPARISON REPORT
**Project**: Multi-Channel Marketing Campaign Optimization
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analyst**: Claude Agent

---

## EXECUTIVE SUMMARY

Đây là báo cáo so sánh chi tiết giữa 2 datasets ứng viên cho dự án Thạc sĩ về tối ưu hóa chiến dịch marketing đa kênh.

**Datasets được so sánh:**
1. **{name1}** (Priority 1)
2. **{name2}** (Backup)

---

## 1. DATASET OVERVIEW

### Dataset 1: {name1}

- **Size**: {schema1['total_rows']:,} rows × {schema1['total_cols']} columns
- **Memory**: {schema1['memory_mb']:.2f} MB
- **Unique Customers**: {schema1['columns'][0]['unique_count']:,} (assuming first col is ID)

### Dataset 2: {name2}

- **Size**: {schema2['total_rows']:,} rows × {schema2['total_cols']} columns
- **Memory**: {schema2['memory_mb']:.2f} MB
- **Unique Customers**: {schema2['columns'][0]['unique_count']:,}

---

## 2. DETAILED COMPARISON

### 2.1 Size & Scale

| Criterion | {name1} | {name2} | Winner |
|-----------|---------|---------|--------|
| Total Rows | {schema1['total_rows']:,} | {schema2['total_rows']:,} | {"✅ " + name1 if schema1['total_rows'] >= schema2['total_rows'] else "✅ " + name2} |
| Total Columns | {schema1['total_cols']} | {schema2['total_cols']} | {"✅ " + name1 if schema1['total_cols'] >= schema2['total_cols'] else "✅ " + name2} |
| Unique Customers | {schema1['columns'][0]['unique_count']:,} | {schema2['columns'][0]['unique_count']:,} | {"✅ " + name1 if schema1['columns'][0]['unique_count'] >= schema2['columns'][0]['unique_count'] else "✅ " + name2} |
| Meets 10K Requirement | {'✅ Yes' if schema1['columns'][0]['unique_count'] >= 10000 else '❌ No'} | {'✅ Yes' if schema2['columns'][0]['unique_count'] >= 10000 else '❌ No'} | {"✅ " + name1 if schema1['columns'][0]['unique_count'] >= 10000 else ("✅ " + name2 if schema2['columns'][0]['unique_count'] >= 10000 else "❌ Neither")} |

### 2.2 Multi-Channel Structure

| Criterion | {name1} | {name2} | Winner |
|-----------|---------|---------|--------|
| Has Channel Column | {'✅ Yes' if channel1 else '❌ No'} | {'✅ Yes' if channel2 else '❌ No'} | {"✅ " + name1 if channel1 and not channel2 else ("✅ " + name2 if channel2 and not channel1 else "🟰 Tie" if channel1 and channel2 else "❌ Neither")} |
| Unique Channels | {channel1['unique_channels'] if channel1 else 'N/A'} | {channel2['unique_channels'] if channel2 else 'N/A'} | {"✅ " + name1 if channel1 and channel2 and channel1['unique_channels'] >= channel2['unique_channels'] else ("✅ " + name2 if channel1 and channel2 else "N/A")} |

**{name1} Channels**: {', '.join(list(channel1['distribution'].keys())[:5]) if channel1 else 'N/A'}

**{name2} Channels**: {', '.join(list(channel2['distribution'].keys())[:5]) if channel2 else 'N/A'}

### 2.3 Treatment & Outcome Variables

| Criterion | {name1} | {name2} | Winner |
|-----------|---------|---------|--------|
| Treatment/Control | {'✅ Found: ' + ', '.join(treatment1['treatment_cols'][:2]) if treatment1['treatment_cols'] else '❌ Not found'} | {'✅ Found: ' + ', '.join(treatment2['treatment_cols'][:2]) if treatment2['treatment_cols'] else '❌ Not found'} | {"✅ " + name1 if treatment1['treatment_cols'] and not treatment2['treatment_cols'] else ("✅ " + name2 if treatment2['treatment_cols'] and not treatment1['treatment_cols'] else "🟰 Tie" if treatment1['treatment_cols'] and treatment2['treatment_cols'] else "❌ Neither")} |
| Outcome Variable | {'✅ Found: ' + ', '.join(treatment1['outcome_cols'][:2]) if treatment1['outcome_cols'] else '❌ Not found'} | {'✅ Found: ' + ', '.join(treatment2['outcome_cols'][:2]) if treatment2['outcome_cols'] else '❌ Not found'} | {"✅ " + name1 if treatment1['outcome_cols'] and not treatment2['outcome_cols'] else ("✅ " + name2 if treatment2['outcome_cols'] and not treatment1['outcome_cols'] else "🟰 Tie")} |
| Conversion Rate | {f"{treatment1['conversion_rate']:.2f}%" if treatment1['conversion_rate'] else 'N/A'} | {f"{treatment2['conversion_rate']:.2f}%" if treatment2['conversion_rate'] else 'N/A'} | - |

### 2.4 Temporal Structure

| Criterion | {name1} | {name2} | Winner |
|-----------|---------|---------|--------|
| Has Timestamp | {'✅ Yes' if temporal1 else '❌ No'} | {'✅ Yes' if temporal2 else '❌ No'} | {"✅ " + name1 if temporal1 and not temporal2 else ("✅ " + name2 if temporal2 and not temporal1 else "🟰 Tie" if temporal1 and temporal2 else "❌ Neither")} |
| Date Range (days) | {list(temporal1.values())[0]['date_range'] if temporal1 else 'N/A'} | {list(temporal2.values())[0]['date_range'] if temporal2 else 'N/A'} | {"✅ " + name1 if temporal1 and temporal2 and list(temporal1.values())[0]['date_range'] >= list(temporal2.values())[0]['date_range'] else ("✅ " + name2 if temporal1 and temporal2 else "N/A")} |

**{name1} Date Range**: {f"{list(temporal1.values())[0]['min_date']} to {list(temporal1.values())[0]['max_date']}" if temporal1 else 'N/A'}

**{name2} Date Range**: {f"{list(temporal2.values())[0]['min_date']} to {list(temporal2.values())[0]['max_date']}" if temporal2 else 'N/A'}

### 2.5 Data Quality

| Criterion | {name1} | {name2} | Winner |
|-----------|---------|---------|--------|
| Duplicate Rows | {quality1['duplicate_rows']:,} ({quality1['duplicate_pct']:.2f}%) | {quality2['duplicate_rows']:,} ({quality2['duplicate_pct']:.2f}%) | {"✅ " + name1 if quality1['duplicate_pct'] <= quality2['duplicate_pct'] else "✅ " + name2} |
| Missing Data | {quality1['missing_pct']:.2f}% | {quality2['missing_pct']:.2f}% | {"✅ " + name1 if quality1['missing_pct'] <= quality2['missing_pct'] else "✅ " + name2} |
| Data Completeness | {100 - quality1['missing_pct']:.2f}% | {100 - quality2['missing_pct']:.2f}% | {"✅ " + name1 if quality1['missing_pct'] <= quality2['missing_pct'] else "✅ " + name2} |

### 2.6 Fit for Project Requirements

**Project Requirements Checklist:**

| Requirement | {name1} | {name2} |
|-------------|---------|---------|
| ✅ ~10,000 customers | {'✅' if schema1['columns'][0]['unique_count'] >= 10000 else '❌ Only ' + f"{schema1['columns'][0]['unique_count']:,}"} | {'✅' if schema2['columns'][0]['unique_count'] >= 10000 else '❌ Only ' + f"{schema2['columns'][0]['unique_count']:,}"} |
| ✅ Multi-channel data | {'✅' if channel1 else '❌'} | {'✅' if channel2 else '❌'} |
| ✅ Treatment/Control for causal inference | {'✅' if treatment1['treatment_cols'] else '❌'} | {'✅' if treatment2['treatment_cols'] else '❌'} |
| ✅ Conversion outcomes | {'✅' if treatment1['outcome_cols'] else '❌'} | {'✅' if treatment2['outcome_cols'] else '❌'} |
| ✅ Temporal structure for splits | {'✅' if temporal1 else '❌'} | {'✅' if temporal2 else '❌'} |

---

## 3. SCORING MATRIX

### Overall Scores (Out of 10)

"""

    # Calculate scores
    score1 = calculate_score(schema1, temporal1, channel1, treatment1, quality1)
    score2 = calculate_score(schema2, temporal2, channel2, treatment2, quality2)

    report += f"""
| Category | {name1} | {name2} |
|----------|---------|---------|
| Size & Scale (2 pts) | {score1['size']:.1f} | {score2['size']:.1f} |
| Multi-Channel (2 pts) | {score1['channel']:.1f} | {score2['channel']:.1f} |
| Treatment/Control (2 pts) | {score1['treatment']:.1f} | {score2['treatment']:.1f} |
| Temporal Structure (2 pts) | {score1['temporal']:.1f} | {score2['temporal']:.1f} |
| Data Quality (2 pts) | {score1['quality']:.1f} | {score2['quality']:.1f} |
| **TOTAL SCORE** | **{score1['total']:.1f}/10** | **{score2['total']:.1f}/10** |

---

## 4. RECOMMENDATION

"""

    if score1['total'] > score2['total']:
        winner = name1
        winner_score = score1['total']
        reason = f"{name1} scores higher ({score1['total']:.1f}/10 vs {score2['total']:.1f}/10)"
    else:
        winner = name2
        winner_score = score2['total']
        reason = f"{name2} scores higher ({score2['total']:.1f}/10 vs {score1['total']:.1f}/10)"

    report += f"""
### 🏆 SELECTED DATASET: **{winner}**

**Overall Score**: {winner_score:.1f}/10

**Key Reasons:**

"""

    # Add specific reasons based on scores
    winner_data = (schema1, temporal1, channel1, treatment1, quality1) if winner == name1 else (schema2, temporal2, channel2, treatment2, quality2)
    schema_w, temporal_w, channel_w, treatment_w, quality_w = winner_data

    reasons = []

    if schema_w['columns'][0]['unique_count'] >= 10000:
        reasons.append(f"✅ Meets sample size requirement ({schema_w['columns'][0]['unique_count']:,} unique customers)")

    if channel_w:
        reasons.append(f"✅ Strong multi-channel structure ({channel_w['unique_channels']} channels)")

    if treatment_w['treatment_cols']:
        reasons.append(f"✅ Has treatment/control variables: {', '.join(treatment_w['treatment_cols'][:2])}")

    if treatment_w['outcome_cols']:
        reasons.append(f"✅ Clear outcome variable: {', '.join(treatment_w['outcome_cols'][:2])}")
        if treatment_w['conversion_rate']:
            reasons.append(f"  → Conversion rate: {treatment_w['conversion_rate']:.2f}%")

    if temporal_w:
        days = list(temporal_w.values())[0]['date_range']
        reasons.append(f"✅ Temporal coverage: {days} days")

    if quality_w['missing_pct'] < 5:
        reasons.append(f"✅ High data quality (only {quality_w['missing_pct']:.2f}% missing)")

    for reason in reasons:
        report += f"{reason}\n"

    report += f"""

### Next Steps for {winner}:

1. **Feature Engineering**
   - Create channel interaction features
   - Engineer temporal features (day of week, time of day, recency)
   - Calculate customer lifetime value proxies
   - Create treatment intensity measures

2. **Temporal Splits Strategy**
   ```
   Train Set:      First 60% chronologically
   Validation:     Next 20%
   Locked Test:    Next 10%
   Out-of-Time:    Final 10% (future data)
   ```

3. **Expected Challenges**
   - {f"Low sample size - need bootstrap/cross-validation" if schema_w['columns'][0]['unique_count'] < 10000 else "Handle class imbalance in conversion"}
   - {f"High missing data in some features - imputation needed" if quality_w['missing_pct'] > 5 else "Channel attribution complexity"}
   - Need to engineer treatment propensity scores

4. **Model Development Path**
   - Phase 1: Baseline conversion prediction (XGBoost + calibration)
   - Phase 2: Causal inference (Double ML for CATE estimation)
   - Phase 3: Uplift modeling (S-learner, T-learner, X-learner)
   - Phase 4: MILP optimization for budget allocation

---

## 5. APPENDIX: COLUMN SCHEMAS

### {name1} Columns

"""

    for col in schema1['columns']:
        report += f"- **{col['name']}** ({col['dtype']}): {col['unique_count']:,} unique, {col['missing_pct']:.1f}% missing\n"

    report += f"\n### {name2} Columns\n\n"

    for col in schema2['columns']:
        report += f"- **{col['name']}** ({col['dtype']}): {col['unique_count']:,} unique, {col['missing_pct']:.1f}% missing\n"

    report += f"""

---

## 6. CONCLUSION

Based on comprehensive analysis across size, multi-channel structure, causal inference readiness, temporal coverage, and data quality, **{winner}** is the recommended dataset for the Multi-Channel Marketing Campaign Optimization project.

The dataset provides {"solid" if winner_score >= 7 else "adequate"} foundation for:
- Predictive modeling with calibration
- Causal inference (Double ML, CATE, Uplift)
- Budget optimization via MILP
- Temporal validation with out-of-time testing

**Confidence Level**: {"High" if winner_score >= 8 else "Medium" if winner_score >= 6 else "Low"} ({winner_score:.1f}/10)

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analyst**: Claude Agent
**Project**: Multi-Channel Marketing Campaign Optimization
"""

    return report


def calculate_score(schema, temporal, channel, treatment, quality):
    """Calculate scores for each category"""
    scores = {}

    # Size & Scale (2 points)
    customer_count = schema['columns'][0]['unique_count']
    if customer_count >= 10000:
        scores['size'] = 2.0
    elif customer_count >= 5000:
        scores['size'] = 1.5
    elif customer_count >= 2000:
        scores['size'] = 1.0
    else:
        scores['size'] = 0.5

    # Multi-Channel (2 points)
    if channel:
        if channel['unique_channels'] >= 5:
            scores['channel'] = 2.0
        elif channel['unique_channels'] >= 3:
            scores['channel'] = 1.5
        else:
            scores['channel'] = 1.0
    else:
        scores['channel'] = 0.0

    # Treatment/Control (2 points)
    if treatment['treatment_cols'] and treatment['outcome_cols']:
        scores['treatment'] = 2.0
    elif treatment['outcome_cols']:
        scores['treatment'] = 1.0
    elif treatment['treatment_cols']:
        scores['treatment'] = 0.5
    else:
        scores['treatment'] = 0.0

    # Temporal (2 points)
    if temporal:
        days = list(temporal.values())[0]['date_range']
        if days >= 365:
            scores['temporal'] = 2.0
        elif days >= 180:
            scores['temporal'] = 1.5
        elif days >= 90:
            scores['temporal'] = 1.0
        else:
            scores['temporal'] = 0.5
    else:
        scores['temporal'] = 0.0

    # Quality (2 points)
    missing_pct = quality['missing_pct']
    dup_pct = quality['duplicate_pct']

    quality_score = 2.0
    if missing_pct > 10:
        quality_score -= 0.5
    if missing_pct > 20:
        quality_score -= 0.5
    if dup_pct > 5:
        quality_score -= 0.5
    if dup_pct > 10:
        quality_score -= 0.5

    scores['quality'] = max(0, quality_score)

    # Total
    scores['total'] = sum([scores['size'], scores['channel'], scores['treatment'],
                          scores['temporal'], scores['quality']])

    return scores


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          MULTI-CHANNEL MARKETING DATASET COMPARISON          ║
    ║                                                              ║
    ║  Project: Multi-Channel Marketing Campaign Optimization      ║
    ║  Author: Claude Agent                                        ║
    ║  Date: 2026-11-03                                            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Load datasets
    try:
        df_causal, file1 = load_dataset(CAUSAL_DIR, "Causal Digital Marketing")
        df_mta, file2 = load_dataset(MTA_DIR, "Multi-Touch Attribution")

        if df_causal is None or df_mta is None:
            print("\n❌ ERROR: Could not load one or both datasets")
            print("\nPlease ensure you have downloaded both datasets to:")
            print(f"  1. {CAUSAL_DIR}")
            print(f"  2. {MTA_DIR}")
            print("\nSee DOWNLOAD_INSTRUCTIONS.md for details.")
            exit(1)

        # Run comparison
        report = compare_datasets(
            df_causal, "Causal Digital Marketing",
            df_mta, "Multi-Touch Attribution"
        )

        # Save report
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n\n{'='*60}")
        print(f"✅ ANALYSIS COMPLETE")
        print(f"{'='*60}")
        print(f"\nComparison report saved to:")
        print(f"  → {OUTPUT_FILE}")
        print(f"\nPlease review the report for dataset recommendation.")
        print(f"\n{'='*60}\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
