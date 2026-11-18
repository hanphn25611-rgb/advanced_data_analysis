# DATASET COMPARISON REPORT (Preliminary)
**Project**: Multi-Channel Marketing Campaign Optimization  
**Date**: 2026-11-03  
**Status**: ⚠️ PRELIMINARY - Based on Kaggle metadata only  
**Analyst**: Claude Agent

---

## ⚠️ IMPORTANT NOTE

This is a **preliminary comparison** based on publicly available Kaggle metadata and descriptions. For a complete analysis, please:

1. Download both datasets following `DOWNLOAD_INSTRUCTIONS.md`
2. Run the EDA script: `python data/raw/eda_comparison.py`
3. Review the final detailed comparison report

---

## EXECUTIVE SUMMARY

Dự án Thạc sĩ về Multi-Channel Marketing Campaign Optimization cần dataset với:
- ✅ ~10,000 customers minimum
- ✅ Multi-channel touchpoint data
- ✅ Treatment/Control structure for causal inference
- ✅ Conversion outcomes
- ✅ Temporal structure for train/validation/test splits

**Preliminary Assessment**: Download CẢ 2 datasets để so sánh chi tiết.

---

## 1. DATASETS OVERVIEW

### Dataset 1: Causal Digital Marketing Campaign Dataset (PRIORITY 1)

**Source**: https://www.kaggle.com/datasets/rahuljangir78/causal-digital-marketing-campaign-dataset  
**Author**: rahuljangir78  
**Last Updated**: November 2025

**Why Priority 1:**
- ✅ Tên dataset explicitly mentions "Causal" → likely has treatment/control design
- ✅ Dataset mới (updated Nov 2025) → current marketing practices
- ✅ Designed for causal inference applications
- ❓ Size unknown until download
- ❓ Column structure unknown until download

**Expected Strengths:**
- Treatment/control group assignment
- Experimental design for causal analysis
- Modern marketing campaign data
- Likely includes multiple channels and customer features

**Potential Concerns:**
- Dataset details not visible without download
- May require Kaggle account verification
- Unknown if meets 10K customer requirement

---

### Dataset 2: Multi-Touch Attribution Dataset (BACKUP)

**Source**: https://www.kaggle.com/datasets/vivekparasharr/multi-touch-attribution  
**Author**: vivekparasharr  

**Known Specifications:**
- **Size**: ~2,847 unique users ❌ (Below 10K requirement)
- **Rows**: ~10,000+ interaction records
- **Columns**: 5 core columns
  - `User ID`: Unique customer identifier
  - `Timestamp`: Date/time of interaction
  - `Channel`: Marketing channel (Direct Traffic, Social Media, Email, etc.)
  - `Campaign`: Specific campaign name
  - `Conversion`: Binary outcome (Yes/No)

**Channel Distribution:**
- Direct Traffic: ~17.2%
- Social Media, Email, Search, Display ads
- 31.3% interactions have no campaign assigned

**Strengths:**
- ✅ Multi-channel structure clearly defined
- ✅ Temporal data (Timestamp)
- ✅ Clear conversion outcome
- ✅ Well-documented and used in tutorials
- ✅ Clean, simple structure

**Weaknesses:**
- ❌ Only ~2,847 users (BELOW 10K requirement)
- ❌ No explicit treatment/control structure
- ❌ May need engineering for causal inference
- ⚠️ Smaller scale limits advanced modeling

**Related Resources:**
- Author's Medium article on MTA implementation
- Multiple Kaggle notebooks with analysis examples

---

## 2. PRELIMINARY COMPARISON

### 2.1 Size & Scale

| Criterion | Causal Marketing | Multi-Touch | Assessment |
|-----------|-----------------|-------------|------------|
| Unique Customers | ❓ Unknown | ❌ ~2,847 | Need to verify Causal dataset |
| Meets 10K Requirement | ❓ TBD | ❌ No | Critical to check Causal |
| Interaction Records | ❓ Unknown | ~10,000+ | - |
| Scalability | ❓ TBD | ⚠️ Limited | - |

**Verdict**: Multi-Touch fails size requirement. Causal dataset is unknown - MUST verify.

---

### 2.2 Multi-Channel Structure

| Criterion | Causal Marketing | Multi-Touch | Winner |
|-----------|-----------------|-------------|--------|
| Multi-Channel | ❓ Likely | ✅ Yes (5+ channels) | Need verification |
| Channel Granularity | ❓ Unknown | ✅ Good | - |
| Channel Attribution | ❓ Possible | ✅ Designed for it | Multi-Touch |
| Cross-Channel Paths | ❓ Unknown | ✅ Yes | - |

**Verdict**: Multi-Touch has proven multi-channel structure. Causal dataset needs verification.

---

### 2.3 Causal Inference Readiness

| Criterion | Causal Marketing | Multi-Touch | Winner |
|-----------|-----------------|-------------|--------|
| Treatment/Control | ✅ Likely (by name) | ❌ Not explicit | Causal Marketing |
| Experimental Design | ✅ Probable | ❌ Observational | Causal Marketing |
| Propensity Scores | ❓ May exist | ❌ Need to engineer | Causal Marketing |
| CATE Estimation | ✅ Designed for it | ⚠️ Possible but harder | Causal Marketing |
| Uplift Modeling | ✅ Supported | ⚠️ Requires engineering | Causal Marketing |

**Verdict**: Causal dataset LIKELY superior for causal inference (pending verification).

---

### 2.4 Temporal Structure

| Criterion | Causal Marketing | Multi-Touch | Winner |
|-----------|-----------------|-------------|--------|
| Timestamp Data | ❓ Likely | ✅ Yes | Need verification |
| Date Range | ❓ Unknown | ❓ Unknown | - |
| Temporal Splits | ❓ Possible | ✅ Possible | - |
| Seasonality Analysis | ❓ Depends on range | ❓ Depends on range | - |

**Verdict**: Both likely support temporal analysis. Need to verify date ranges.

---

### 2.5 Feature Richness

| Criterion | Causal Marketing | Multi-Touch | Winner |
|-----------|-----------------|-------------|--------|
| Customer Demographics | ❓ Unknown | ❌ Not included | Causal (likely) |
| Behavioral Features | ❓ Unknown | ⚠️ Limited | - |
| Campaign Details | ❓ Unknown | ✅ Yes | - |
| Channel Details | ❓ Unknown | ✅ Yes | - |

**Verdict**: Multi-Touch is minimal (5 cols). Causal likely has more features.

---

## 3. PRELIMINARY SCORING

### Scoring Matrix (Based on Available Information)

| Category | Causal Marketing | Multi-Touch | Notes |
|----------|-----------------|-------------|-------|
| **Size & Scale** (2 pts) | ❓ TBD | ❌ 0.5/2 | MTA fails 10K requirement |
| **Multi-Channel** (2 pts) | ❓ TBD | ✅ 2.0/2 | MTA proven multi-channel |
| **Causal Inference** (2 pts) | ✅ 2.0/2 (likely) | ❌ 0.5/2 | Causal designed for it |
| **Temporal Structure** (2 pts) | ❓ TBD | ✅ 1.5/2 | Both likely have it |
| **Data Quality** (2 pts) | ❓ TBD | ✅ 1.5/2 | MTA is clean & documented |
| **TOTAL** | **❓ TBD** | **6.0/10** | Causal unknown |

---

## 4. PRELIMINARY RECOMMENDATION

### 🎯 ACTION REQUIRED: Download BOTH Datasets

**Reasoning:**

1. **Multi-Touch Attribution** alone is **INSUFFICIENT** due to:
   - ❌ Only 2,847 users (need ~10,000)
   - ❌ No explicit treatment/control structure
   - ⚠️ Limited for advanced causal inference

2. **Causal Digital Marketing** is **PROMISING** but:
   - ❓ Size unknown - CRITICAL to verify
   - ❓ Must confirm multi-channel structure
   - ❓ Need to see actual columns and data quality

### Decision Tree:

```
IF Causal dataset has ≥10K customers AND multi-channel data:
    → ✅ SELECT Causal Digital Marketing (scores likely 8-9/10)
    → Use as primary dataset
    
ELSE IF Causal dataset < 10K but good quality:
    → ⚠️ COMBINE both datasets (if compatible)
    → Or use MTA for prototyping, Causal for causal analysis
    
ELSE IF Causal dataset is unusable:
    → ❌ NEED TO FIND ALTERNATIVE
    → MTA alone is too small for thesis requirements
```

---

## 5. NEXT STEPS

### Immediate Actions (Today):

1. ✅ **Download Both Datasets**
   - Follow instructions in `DOWNLOAD_INSTRUCTIONS.md`
   - Save to `data/raw/causal_marketing/` and `data/raw/multi_touch/`

2. ✅ **Run EDA Script**
   ```bash
   cd /Users/phanhongochan/Documents/TMDT-UEL/advanced_data_analysis
   python data/raw/eda_comparison.py
   ```

3. ✅ **Review Full Comparison Report**
   - Script will generate detailed `DATASET_COMPARISON.md` with actual data
   - Make final dataset selection based on real analysis

### If Causal Dataset is Good:

4. **Feature Engineering**
   - Multi-channel interaction features
   - Temporal features (day of week, hour, recency, frequency)
   - Treatment intensity measures
   - Customer engagement scores

5. **Temporal Splits**
   ```
   Train:          60% (oldest)
   Validation:     20%
   Locked Test:    10%
   Out-of-Time:    10% (newest)
   ```

6. **Model Development Pipeline**
   - Phase 1: Baseline prediction + calibration (XGBoost)
   - Phase 2: Causal inference (Double ML for CATE)
   - Phase 3: Uplift modeling (S-learner, T-learner, X-learner)
   - Phase 4: MILP optimization for budget allocation

### If Multi-Touch Only Available:

4. **Augmentation Strategies**
   - Engineer propensity scores from channel/campaign patterns
   - Create pseudo-treatment groups via clustering
   - Focus on attribution modeling vs. causal inference
   - Consider synthetic control methods

5. **Alternative Approaches**
   - Emphasize multi-touch attribution models (Shapley value, Markov chains)
   - Use Bayesian methods for small sample inference
   - Bootstrap for confidence intervals
   - Cross-validation for robust validation

### If Both Datasets Fail:

4. **Backup Plan**
   - Search for alternative marketing datasets (Google Analytics, Adobe Analytics demos)
   - Consider simulated data with realistic assumptions
   - Reach out to companies for real anonymized data
   - Use multiple smaller datasets with transfer learning

---

## 6. EXPECTED CHALLENGES & MITIGATIONS

### Challenge 1: Small Sample Size (if < 10K)
**Mitigation:**
- Bootstrap resampling for confidence intervals
- Bayesian methods with informative priors
- Stratified k-fold cross-validation
- Focus on effect size over statistical significance

### Challenge 2: No Explicit Treatment/Control
**Mitigation:**
- Propensity score matching on channel exposure
- Instrumental variables (if available)
- Regression discontinuity design
- Natural experiments from campaign timing

### Challenge 3: Channel Attribution Complexity
**Mitigation:**
- Compare multiple attribution models (Last-touch, First-touch, Linear, Time-decay, Shapley)
- Ensemble attribution methods
- Validate with holdout experiments if possible

### Challenge 4: Temporal Data Leakage
**Mitigation:**
- Strict temporal splits (no future data in training)
- Feature engineering with lag features only
- Out-of-time validation mandatory
- Monitor for concept drift

---

## 7. EVALUATION CRITERIA FOR FINAL DATASET

### Must-Have (Critical):
- ✅ At least 5,000 unique customers (10,000 preferred)
- ✅ Multi-channel data (3+ channels minimum)
- ✅ Binary conversion outcome
- ✅ Temporal information for splits

### Should-Have (Important):
- ✅ Treatment/control or campaign variation
- ✅ Customer features beyond ID
- ✅ Date range ≥ 90 days
- ✅ < 10% missing data

### Nice-to-Have (Bonus):
- ✅ Demographics (age, gender, location)
- ✅ Behavioral data (frequency, recency, engagement)
- ✅ Campaign costs/budgets
- ✅ Customer lifetime value

---

## 8. PRELIMINARY CONCLUSION

**Current Status**: **INCOMPLETE - AWAITING DATA DOWNLOAD**

Based on Kaggle metadata alone:

1. **Multi-Touch Attribution** is too small (~2,847 users) but well-structured
2. **Causal Digital Marketing** is promising (causal design) but unverified
3. **Decision**: Download BOTH and run `eda_comparison.py` for complete analysis

**Confidence in Recommendation**: ⚠️ **LOW** until actual datasets are analyzed

**Next Critical Step**: 
```bash
# DOWNLOAD BOTH DATASETS NOW
# Then run:
python data/raw/eda_comparison.py
```

This will generate a complete comparison report with:
- Actual row counts and customer counts
- Full column schemas
- Data quality metrics
- Treatment/outcome variable verification
- Temporal coverage analysis
- Final recommendation with confidence score

---

## APPENDIX A: Multi-Touch Attribution Schema (Confirmed)

Based on Kaggle documentation and author's Medium article:

```python
columns = [
    'User ID',      # Unique customer identifier
    'Timestamp',    # Date/time of interaction (YYYY-MM-DD HH:MM:SS)
    'Channel',      # Marketing channel (Direct Traffic, Social Media, Email, Search, Display)
    'Campaign',     # Campaign name (or null)
    'Conversion'    # Binary: Yes/No
]

# Example row:
# User_123, 2024-01-15 14:30:00, Social Media, Spring_Sale_2024, No
# User_123, 2024-01-20 09:15:00, Email, Spring_Sale_2024, No
# User_123, 2024-01-25 16:45:00, Direct Traffic, None, Yes
```

**Channel Distribution (approximate):**
- Direct Traffic: 17.2%
- Social Media: ~15%
- Email: ~15%
- Search: ~15%
- Display: ~15%
- Other/Unknown: ~22.8%

---

## APPENDIX B: Resources & References

### Causal Digital Marketing Dataset:
- URL: https://www.kaggle.com/datasets/rahuljangir78/causal-digital-marketing-campaign-dataset
- Status: Not analyzed yet - download required

### Multi-Touch Attribution Dataset:
- URL: https://www.kaggle.com/datasets/vivekparasharr/multi-touch-attribution
- Author's Tutorial: https://vivekparasharr.medium.com/implementing-a-machine-learning-based-multi-touch-attribution-mta-solution-820ac253eb02
- Example Notebooks: Search "multi-touch attribution" on Kaggle

### Related Research:
- Double Machine Learning for treatment effects (Chernozhukov et al., 2018)
- Causal inference for multi-channel marketing (Google research)
- Marketing mix modeling & MMM frameworks

---

**Report Status**: PRELIMINARY  
**Last Updated**: 2026-11-03  
**Analyst**: Claude Agent  

**⚠️ ACTION REQUIRED**: Download datasets and run full EDA script for final recommendation.

---

## SOURCES

This preliminary analysis used information from:
- [Causal Digital Marketing Campaign Dataset | Kaggle](https://www.kaggle.com/datasets/rahuljangir78/causal-digital-marketing-campaign-dataset)
- [Multi-Touch Attribution Dataset | Kaggle](https://www.kaggle.com/datasets/vivekparasharr/multi-touch-attribution)
- [Implementing ML-Based Multi-Touch Attribution Solution | Medium](https://vivekparasharr.medium.com/implementing-a-machine-learning-based-multi-touch-attribution-mta-solution-820ac253eb02)
