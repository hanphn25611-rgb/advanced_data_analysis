# Uplift Modeling cho Marketing Đa Kênh

**Tiểu luận:** Phân tích Dữ liệu Nâng cao - Thạc sĩ Thương mại Điện tử

**Học viên:** Phan Hồ Ngọc Hân
**MSSV:** C25611249


---

## Tổng quan

Dự án xây dựng pipeline end-to-end cho bài toán **uplift modeling** trong marketing đa kênh, nhằm ước lượng tác động nhân quả (CATE) của chiến dịch quảng cáo lên từng khách hàng và tối ưu hóa phân bổ ngân sách.

Pipeline gồm 8 giai đoạn: kiểm định dữ liệu, ước lượng CATE bằng T-learner, hiệu chỉnh xác suất (Isotonic Regression), phân loại Four Groups (Persuadables/Sure Things/Lost Causes/Sleeping Dogs), tối ưu hóa phân bổ bằng MILP, action router với guardrails, giám sát MLOps (drift detection, release gates) và báo cáo.

---

## Cấu trúc thư mục

```
advanced_data_analysis/
├── README.md              # File này
├── requirements.txt       # Python dependencies
├── .gitignore             # Files loại trừ khỏi git
│
├── notebooks/             # 5 Jupyter notebooks (chạy theo thứ tự)
│   ├── 01_data_exploration_FIXED.ipynb
│   ├── 02_predictive_modeling_FIXED.ipynb
│   ├── 03_causal_inference_FIXED.ipynb
│   ├── 04_optimization_FIXED.ipynb
│   └── 05_mlops_FIXED.ipynb
│
└── data/
    ├── raw/               # Dữ liệu gốc (Criteo Uplift)
    └── processed/         # Parquet, JSON, Pickle (tạo từ notebooks)
```

---

## Cài đặt

**Yêu cầu:** Python >= 3.10

```bash
# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Cài dependencies
pip install -r requirements.txt
```

---

## Hướng dẫn chạy

Chạy 5 notebooks theo thứ tự (mỗi notebook tạo outputs cho notebook tiếp theo):

| STT | Notebook | Mục đích | Thời gian |
|-----|----------|----------|-----------|
| 1 | `01_data_exploration_FIXED.ipynb` | Kiểm định dữ liệu, feature engineering, temporal splits | ~2 phút |
| 2 | `02_predictive_modeling_FIXED.ipynb` | Train HistGradientBoosting + hiệu chỉnh Isotonic | ~5 phút |
| 3 | `03_causal_inference_FIXED.ipynb` | Ước lượng CATE bằng T-learner, phân loại Four Groups | ~3 phút |
| 4 | `04_optimization_FIXED.ipynb` | Tối ưu hóa phân bổ ngân sách bằng MILP vs Greedy | ~1 phút |
| 5 | `05_mlops_FIXED.ipynb` | Drift detection (PSI/TVD), guardrails, release gates | ~2 phút |

---

## Kết quả chính

**Mô hình dự đoán (Notebook 02):**
- AUC trên test: 0.5354 (chỉ 8 pre-treatment features)
- Brier Score: 0.0884
- ECE giảm 65.9% nhờ Isotonic Regression (0.0529 → 0.0180)

**Ước lượng CATE (Notebook 03):**
- Mean CATE: +6.31 pp
- Heterogeneity ratio (Std/Mean): 1.68 → biến thiên cao
- Phân loại Four Groups: 46.6% Persuadables, 9.2% Sleeping Dogs

**Tối ưu hóa (Notebook 04):**
- MILP cải thiện 1.96% so với Greedy
- Trade-off: MILP chậm hơn 5.6× (13.7ms vs 2.4ms)

**MLOps (Notebook 05):**
- 4/4 release gates PASS trên out-of-time set
- PSI max: 0.0465, TVD actions: 0.0181 → không có drift

---

## Tech Stack

| Thành phần | Thư viện |
|------------|----------|
| Data processing | `pandas`, `numpy`, `pyarrow` |
| Machine Learning | `scikit-learn` (HistGradientBoosting, Isotonic, Logistic) |
| Optimization | `scipy.optimize.milp` |
| Causal Inference | Custom T-learner implementation |
| Monitoring | Custom PSI/ECE/TVD |
| Visualization | `matplotlib`, `seaborn` |

---

## Dataset

**Nguồn:** Criteo Uplift Prediction Dataset (Kaggle)

Dataset gốc không được commit (dung lượng lớn). Để tải:

```bash
# Cần Kaggle API key trong ~/.kaggle/kaggle.json
kaggle datasets download -d arashnic/uplift-modeling
unzip uplift-modeling.zip -d data/raw/
```

---

## Reproducibility

Tất cả notebooks dùng `SEED=42` cố định. Các bước đảm bảo tính tái lập:

- Temporal splits dựa trên cột `split` (train/validation/locked_test/out_of_time)
- Hyperparameter tuning bằng 5-fold CV trên **train set only** (validation không được dùng cho tuning)
- Pre-treatment features only (loại bỏ post-treatment: `impressions`, `clicks`, `spend_usd`, `revenue_usd`)
- Model checksums (SHA256) được lưu trong `data/processed/model_version.json`

---

## Tài liệu tham khảo chính

1. Gutierrez, P., & Gérardy, J. Y. (2017). *Causal Inference and Uplift Modelling: A Review of the Literature*. ICML Workshop.
2. Künzel, S. R., et al. (2019). Metalearners for estimating heterogeneous treatment effects using machine learning. *PNAS*, 116(10).
3. Elmachtoub, A. N., & Grigas, P. (2022). Smart "Predict, then Optimize". *Management Science*, 68(1), 9-26.
4. Platt, J. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. *Advances in Large Margin Classifiers*.
5. Zadrozny, B., & Elkan, C. (2002). Transforming classifier scores into accurate multiclass probability estimates. *KDD '02*.

---

## License

Academic project - Không dùng cho mục đích thương mại

---

**Cập nhật lần cuối:** 14/11/2026
