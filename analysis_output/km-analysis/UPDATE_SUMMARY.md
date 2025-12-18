# 分析更新摘要

## 更新日期：2025-11-16 02:12

## 主要更新內容

### ✅ 1. 熱力圖優化

#### 產品關聯熱力圖 (`charts/product_heatmap.pdf`)
- **限制為前 10 個配對**：只顯示 lift 值最高的前 10 個產品配對
- **使用品項名稱**：圖表標籤從 SKU 代碼改為可讀的品項名稱（Item）
- **檔案大小**：464 KB（含完整圖表）
- **內容**：顯示產品間的關聯強度，紅色表示正向關聯（lift > 1）

#### 時段產品熱力圖 (`charts/time_product_heatmap.pdf`)
- **限制為前 10 個 SKU**：只顯示 lift 變化最大或顯著的前 10 個產品
- **使用品項名稱**：行標籤使用品項名稱而非 SKU
- **檔案大小**：192 KB
- **時段分佈**：午餐（23:00-01:59）、下午茶（02:00-04:59）、晚餐（05:00-06:59）

### ✅ 2. PDF 報告驗證

#### 報告 1: `km_association_report.pdf`
- **頁數**：9 頁
- **檔案大小**：269 KB
- **內容**：
  - 封面頁
  - 5 張 KM 存活曲線圖
  - 產品關聯表格
  - 產品關聯熱力圖
  - 時段產品熱力圖

#### 報告 2: `km_heatmap_report.pdf`
- **頁數**：10 頁
- **檔案大小**：378 KB
- **內容**：
  - 封面頁
  - 5 張 KM 存活曲線圖
  - Pairwise log-rank p 值矩陣
  - 產品關聯熱力圖
  - 時段產品熱力圖
  - 統計檢定匯總表

## 分析結果摘要

### 資料統計
- **總交易數**：7,344 筆
- **顧客數**：635 位（636 位有紀錄）
- **不重複 SKU**：109 個
- **時段分佈**：
  - 午餐：3,069 筆（42.2%）
  - 下午茶：2,255 筆（31.0%）
  - 晚餐：1,939 筆（26.7%）

### 存活分析結果
- **流失率**：62.36%
- **平均存活時間**：51.00 天
- **中位數存活時間**：0.00 天（表示多數顧客僅消費一次）

### 關鍵發現

#### 1. 用餐方式影響（p < 0.001）
- Unknown 組別與其他組別有顯著差異
- 內用、外帶、外送之間無顯著差異

#### 2. Combo 購買影響
- 首購 Combo：顯著影響保留率（p = 0.004）
- 曾買 Combo：高度顯著影響（p < 0.001）

#### 3. 商品多樣性影響（p < 0.001）
- Category 層級：4 種以上 > 2-3 種 > 1 種
- Item 層級：類似模式，多樣性越高保留率越好

#### 4. 產品關聯
- **分析配對數**：97 個（共現 ≥ 10 次）
- **Top 10 配對**：顯示最強的產品關聯
- **品項名稱**：所有標籤使用可讀的品項名稱

#### 5. 時段偏好
- **顯著 SKU 數**：5 個（p < 0.05）
- **Lift 平均**：1.065
- **Top 10 產品**：展示時段偏好最明顯的品項

## 技術改進

### 程式碼優化
1. **移除 arules 依賴**：改為手動計算關聯規則（兼容 R 4.4.2）
2. **移除 here 套件**：使用絕對路徑
3. **簡化字型設定**：避免不支援的參數
4. **多重檢定校正**：正確處理 NA 值的 Holm-Bonferroni 校正
5. **時間劃分修正**：根據 +12 小時平移後的實際時段

### 視覺化改進
1. **品項名稱映射**：SKU → Item 名稱轉換
2. **熱力圖尺寸**：根據實際品項數動態調整
3. **前 10 限制**：避免過度擁擠的圖表
4. **中文字型**：使用 Hiragino Sans GB 確保中文顯示

## 檔案清單

### 圖表檔案（10 個）
```
charts/
├── font_test.pdf (43 KB)
├── km_dining_option.pdf (80 KB)
├── km_diversity_category.pdf (139 KB)
├── km_diversity_item.pdf (113 KB)
├── km_ever_combo.pdf (83 KB)
├── km_first_combo.pdf (84 KB)
├── product_association_table.pdf (866 KB)
├── product_heatmap.pdf (464 KB) ← 更新：前 10 個 + 品項名稱
├── time_period_top10.pdf (252 KB)
└── time_product_heatmap.pdf (192 KB) ← 更新：前 10 個 + 品項名稱
```

### 報告檔案（2 個）
```
reports/
├── km_association_report.pdf (269 KB, 9 頁) ← 已驗證有內容
└── km_heatmap_report.pdf (378 KB, 10 頁) ← 已驗證有內容
```

### 統計檔案（4 個）
```
statistics/
├── logrank_results.csv
├── pairwise_comparisons.rds
├── product_association.csv
└── time_product_stats.csv
```

## 如何查看結果

### 1. 查看 PDF 報告
```bash
# Mac
open reports/km_association_report.pdf
open reports/km_heatmap_report.pdf

# 或使用預覽程式開啟
```

### 2. 查看個別圖表
```bash
# 產品關聯熱力圖（前 10 個品項名稱）
open charts/product_heatmap.pdf

# 時段產品熱力圖（前 10 個品項名稱）
open charts/time_product_heatmap.pdf
```

### 3. 查看統計結果
```r
# 在 R 中讀取
library(tidyverse)

# Log-rank 檢定結果
logrank <- read_csv("statistics/logrank_results.csv")

# 產品關聯（Top 30）
product_assoc <- read_csv("statistics/product_association.csv")

# 時段產品統計
time_product <- read_csv("statistics/time_product_stats.csv")
```

## 執行資訊

- **執行時間**：約 0.12 分鐘（7 秒）
- **R 版本**：4.4.2
- **主要套件**：tidyverse, survival, survminer, pheatmap, showtext, ggpubr
- **作業系統**：macOS

## 下次執行

如需重新執行完整分析：

```bash
cd /Users/lunhsiangyuan/Desktop/square/km-analysis
Rscript run_all.R
```

輸出將覆蓋現有檔案。

---

**更新完成日期**：2025-11-16 02:12  
**分析狀態**：✅ 全部完成  
**報告狀態**：✅ 已驗證有內容  
**熱力圖狀態**：✅ 前 10 個品項 + 品項名稱



