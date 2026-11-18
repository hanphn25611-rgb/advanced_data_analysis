# Hướng dẫn Download Datasets từ Kaggle

## 📋 TÓM TẮT DATASETS CẦN DOWNLOAD

### Dataset 1: Causal Digital Marketing Campaign Dataset (PRIORITY 1)
- **URL**: https://www.kaggle.com/datasets/rahuljangir78/causal-digital-marketing-campaign-dataset
- **Tác giả**: rahuljangir78
- **Lý do ưu tiên**: Tên dataset suggest có treatment/control design cho causal inference
- **Thư mục lưu**: `data/raw/causal_marketing/`

### Dataset 2: Multi-Touch Attribution Dataset (BACKUP)
- **URL**: https://www.kaggle.com/datasets/vivekparasharr/multi-touch-attribution
- **Tác giả**: vivekparasharr
- **Thông tin dataset**:
  - Size: ~2,847 unique users
  - Columns: User ID, Timestamp, Channel, Campaign, Conversion
  - Multi-channel: Direct Traffic (17.2%), Social Media, Email, etc.
- **Thư mục lưu**: `data/raw/multi_touch/`

---

## 🚀 CÁCH DOWNLOAD

### Bước 1: Chuẩn bị Kaggle Account

1. Đăng nhập vào https://www.kaggle.com
2. Nếu chưa có account, đăng ký free account

### Bước 2: Download Dataset 1 - Causal Digital Marketing

1. Truy cập: https://www.kaggle.com/datasets/rahuljangir78/causal-digital-marketing-campaign-dataset
2. Click nút **"Download"** (góc phải)
3. Chấp nhận terms nếu được yêu cầu
4. File .zip sẽ được download về máy
5. **Giải nén vào**: `/Users/phanhongochan/Documents/TMDT-UEL/advanced_data_analysis/data/raw/causal_marketing/`

### Bước 3: Download Dataset 2 - Multi-Touch Attribution

1. Truy cập: https://www.kaggle.com/datasets/vivekparasharr/multi-touch-attribution
2. Click nút **"Download"**
3. File .zip sẽ được download
4. **Giải nén vào**: `/Users/phanhongochan/Documents/TMDT-UEL/advanced_data_analysis/data/raw/multi_touch/`

---

## 📂 CẤU TRÚC THƯ MỤC SAU KHI DOWNLOAD

```
advanced_data_analysis/
└── data/
    └── raw/
        ├── causal_marketing/
        │   ├── [các file .csv từ dataset 1]
        │   └── README.md (nếu có)
        └── multi_touch/
            ├── [các file .csv từ dataset 2]
            └── README.md (nếu có)
```

---

## ✅ VERIFY DOWNLOAD

Sau khi download xong, chạy lệnh sau để kiểm tra:

```bash
ls -lh data/raw/causal_marketing/
ls -lh data/raw/multi_touch/
```

Hoặc chạy script Python:

```python
import os
import glob

# Check dataset 1
causal_files = glob.glob("data/raw/causal_marketing/*.csv")
print(f"Dataset 1 - Causal Marketing: {len(causal_files)} files")
for f in causal_files:
    print(f"  - {os.path.basename(f)}")

# Check dataset 2
mta_files = glob.glob("data/raw/multi_touch/*.csv")
print(f"\nDataset 2 - Multi-Touch Attribution: {len(mta_files)} files")
for f in mta_files:
    print(f"  - {os.path.basename(f)}")
```

---

## 🔄 NEXT STEPS

Sau khi download xong CẢ 2 datasets:

1. Chạy script EDA: `python data/raw/eda_comparison.py`
2. Xem báo cáo so sánh: `data/raw/DATASET_COMPARISON.md`
3. Quyết định dataset cuối cùng cho dự án

---

## ⚠️ LƯU Ý

- **QUAN TRỌNG**: Download CẢ 2 datasets để so sánh chi tiết
- File sizes có thể lớn (hàng trăm MB), đảm bảo có đủ dung lượng
- Nếu download bị fail, thử refresh page và download lại
- Một số datasets yêu cầu accept competition rules trước khi download

---

## 📞 TROUBLESHOOTING

### Vấn đề: "You must accept competition rules"
→ Vào trang dataset, scroll xuống dưới, click "I Understand and Accept"

### Vấn đề: "Download button disabled"
→ Đăng nhập lại vào Kaggle account

### Vấn đề: "File too large"
→ Download từng file riêng lẻ thay vì download all

---

**Prepared by**: Claude Agent
**Date**: 2026-11-03
**Project**: Multi-Channel Marketing Campaign Optimization
