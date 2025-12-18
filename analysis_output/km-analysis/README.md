# Kaplan-Meier 存活分析與產品關聯分析

## 專案概述

本專案針對 Taiwanway 餐廳的交易資料進行深度分析，使用 **Kaplan-Meier 存活分析**方法探討影響顧客保留的關鍵因子，並透過**產品關聯分析**（Association Rules Mining）識別產品交叉銷售機會與時段消費偏好。

### 核心分析內容

1. **顧客存活分析**：評估不同顧客群體的保留率與生命週期
2. **產品關聯分析**：發現產品間的購買關聯與搭配機會
3. **時段偏好分析**：識別不同時段的產品消費偏好

### 技術特色

- ✅ **學術論文標準**：符合期刊投稿的統計檢定與視覺化規範
- ✅ **完整統計檢定**：Log-rank、卡方檢定、Fisher's exact test，並包含多重檢定校正（Holm-Bonferroni）
- ✅ **中文字型支援**：所有圖表完美顯示繁體中文
- ✅ **可重現性**：完整的 R 腳本與文件，可輕鬆重跑分析

## 系統需求

### R 環境
- R version ≥ 4.0.0
- RStudio（建議）

### 必要套件

```r
install.packages(c(
  "tidyverse",    # 資料處理
  "lubridate",    # 時間處理
  "survival",     # 存活分析
  "survminer",    # KM 曲線視覺化
  "arules",       # 關聯規則挖掘
  "arulesViz",    # 關聯視覺化
  "pheatmap",     # 熱力圖
  "showtext",     # 中文字型支援
  "ggpubr",       # 學術圖表
  "gridExtra",    # 多圖排版
  "pdftools",     # PDF 操作
  "here"          # 路徑管理
))
```

### 字型要求（macOS）
- Hiragino Sans GB（系統內建）
- 路徑：`/System/Library/Fonts/Hiragino Sans GB.ttc`

## 快速開始

### 1. 資料準備

將原始資料放置於指定位置：
```
/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv
```

### 2. 一鍵執行所有分析

```r
setwd("/Users/lunhsiangyuan/Desktop/square/km-analysis")
source("run_all.R")
```

### 3. 查看結果

報告將自動生成於 `reports/` 目錄：
- `km_association_report.pdf`：完整分析報告
- `km_heatmap_report.pdf`：詳細報告（含 pairwise 比較）
- `analysis_summary.txt`：文字摘要

## 專案結構

```
km-analysis/
├── 01_data_preprocessing.R          # 資料前處理
├── 02_build_cohort.R               # 建構顧客世代
├── 03_survival_analysis.R          # Kaplan-Meier 存活分析
├── 04_product_association.R        # 產品關聯分析
├── 05_time_product_analysis.R      # 時段產品分析
├── 06_generate_reports.R           # 生成 PDF 報告
├── run_all.R                       # 主控腳本
├── README.md                       # 本文件
├── research_design.md              # 研究設計企劃書
│
├── data/                           # 資料目錄
│   ├── cleaned_data.csv            # 清理後的交易資料
│   └── customer_cohort.csv         # 顧客世代資料
│
├── charts/                         # 圖表目錄
│   ├── km_dining_option.pdf        # KM 曲線：用餐方式
│   ├── km_first_combo.pdf          # KM 曲線：首購 Combo
│   ├── km_ever_combo.pdf           # KM 曲線：曾買 Combo
│   ├── km_diversity_category.pdf   # KM 曲線：商品多樣性（Category）
│   ├── km_diversity_item.pdf       # KM 曲線：商品多樣性（Item）
│   ├── product_association_table.pdf  # 產品關聯表
│   ├── product_heatmap.pdf         # 產品關聯熱力圖
│   ├── time_product_heatmap.pdf    # 時段產品熱力圖
│   ├── time_period_top10.pdf       # 時段偏好前 10 名
│   └── font_test.pdf               # 中文字型測試
│
├── reports/                        # 報告目錄
│   ├── km_association_report.pdf   # 綜合報告
│   ├── km_heatmap_report.pdf       # 詳細報告
│   └── analysis_summary.txt        # 文字摘要
│
└── statistics/                     # 統計結果目錄
    ├── logrank_results.csv         # Log-rank 檢定結果
    ├── pairwise_comparisons.rds    # Pairwise 比較 p 值
    ├── product_association.csv     # 產品關聯統計
    └── time_product_stats.csv      # 時段產品統計
```

## 分析流程詳解

### 步驟 1：資料前處理（01_data_preprocessing.R）

#### 主要功能
- 合併 `Date` 和 `Time` 欄位為 `DateTime`
- 時間平移 +12 小時對應實際營業時間（11:00-19:00）
- 轉換為紐約時區，考慮日光節約時間（2025-11-02 起為 EST）
- 資料清理：
  - 只保留 `Event Type == "Payment"`
  - 移除 `Price Point Name` 為空（Custom Amount）
  - 移除 `SKU` 缺失的記錄
- 測試中文字型顯示

#### 輸出
- `data/cleaned_data.csv`
- `charts/font_test.pdf`

### 步驟 2：建構顧客世代（02_build_cohort.R）

#### 主要功能
- 以 `Customer ID` 分組
- 計算首購日（`first_purchase_date`）和末購日（`last_purchase_date`）
- 計算存活時間（天數）
- 定義流失狀態：末購後 60 天未再消費 → 流失（status = 1）
- 建構 5 個分組變數：
  1. 用餐方式（內用/外帶/外送/Unknown）
  2. 首購是否 Combo（Yes/No）
  3. 是否曾買過 Combo（Yes/No）
  4. 商品多樣性 - Category（1種/2-3種/4種以上）
  5. 商品多樣性 - Item（1種/2-3種/4種以上）

#### 輸出
- `data/customer_cohort.csv`

### 步驟 3：Kaplan-Meier 存活分析（03_survival_analysis.R）

#### 主要功能
- 對 5 個分組變數分別擬合 KM 曲線
- 執行 log-rank（Mantel-Cox）檢定
- 多組變數進行 pairwise 比較，Holm-Bonferroni 校正
- 繪製學術級 KM 曲線圖：
  - 95% Greenwood 信賴區間
  - Risk table（at-risk 人數表）
  - p 值標註
  - JCO 配色（期刊標準）

#### 輸出
- `charts/km_*.pdf`（5 張圖）
- `statistics/logrank_results.csv`
- `statistics/pairwise_comparisons.rds`

### 步驟 4：產品關聯分析（04_product_association.R）

#### 主要功能
- 建構購物籃資料（Transaction ID × SKU）
- 使用 `arules::apriori` 挖掘關聯規則
- 計算 support、confidence、lift
- 對每對 SKU 進行統計檢定：
  - 期望值 ≥ 5：卡方檢定
  - 期望值 < 5：Fisher's exact test
- Holm-Bonferroni 多重檢定校正
- 篩選條件：共現次數 ≥ 10
- 輸出 Top 30 lift 配對

#### 視覺化
- 關聯表格：SKU_A, SKU_B, co_occur, A→B%, B→A%, lift, p 值
- 熱力圖：顯示 lift 值，標註顯著性（* p<0.05）

#### 輸出
- `charts/product_association_table.pdf`
- `charts/product_heatmap.pdf`
- `statistics/product_association.csv`

### 步驟 5：時段產品分析（05_time_product_analysis.R）

#### 主要功能
- 劃分 3 個時段（基於紐約時間）：
  - 午餐：11:00-13:59
  - 下午茶：14:00-16:59
  - 晚餐：17:00-18:59
- 計算時段 × SKU 的 lift 值
- 對每個 SKU 進行卡方檢定（時段分佈偏離檢定）
- Holm-Bonferroni 校正
- 額外分析：各時段 lift 前 10 名產品

#### 視覺化
- 熱力圖：SKU（行）× 時段（列），顯示 lift 值
- 條形圖：各時段 lift 前 10 名

#### 輸出
- `charts/time_product_heatmap.pdf`
- `charts/time_period_top10.pdf`
- `statistics/time_product_stats.csv`

### 步驟 6：生成 PDF 報告（06_generate_reports.R）

#### 主要功能
- 整合所有圖表與統計結果
- 生成兩份 PDF 綜合報告：
  1. **km_association_report.pdf**：
     - 封面
     - 5 張 KM 曲線
     - 產品關聯表
     - 產品關聯熱力圖
     - 時段產品熱力圖
  
  2. **km_heatmap_report.pdf**：
     - 封面
     - 5 張 KM 曲線
     - Pairwise log-rank p 值矩陣
     - 產品關聯熱力圖
     - 時段產品熱力圖
     - 統計檢定匯總表

#### 輸出
- `reports/km_association_report.pdf`
- `reports/km_heatmap_report.pdf`
- `reports/analysis_summary.txt`

## 研究設計

詳細的研究設計、變數定義、統計方法與解讀指南，請參閱：

📄 **[research_design.md](research_design.md)**

內容包括：
- 研究背景與目的
- 資料來源與處理
- 變數定義（依變數、自變數、關聯指標）
- 統計方法（KM 估計、Log-rank 檢定、卡方檢定、多重檢定校正）
- 解讀指南（KM 曲線、Lift 值、顯著性標記）
- 研究限制與未來方向

## 關鍵概念解釋

### Kaplan-Meier 存活分析
- **目的**：估計顧客保留率隨時間的變化
- **優點**：可處理右設限資料（censored data）
- **應用**：識別影響顧客流失的風險因子

### Log-rank 檢定
- **目的**：比較不同組別的存活曲線是否有顯著差異
- **虛無假設**：各組存活曲線相同
- **判斷標準**：p < 0.05 表示組間差異顯著

### Lift 值
- **Lift > 1**：正向關聯（一起購買的機率高於期望）
- **Lift = 1**：獨立（無關聯）
- **Lift < 1**：負向關聯（互斥或替代）

### 多重檢定校正（Holm-Bonferroni）
- **目的**：控制 Family-Wise Error Rate (FWER)
- **方法**：依 p 值排序後逐步調整
- **優點**：比 Bonferroni 更有檢定力

## 使用範例

### 僅執行特定分析

```r
# 只執行資料前處理
source("01_data_preprocessing.R")

# 只執行存活分析
source("03_survival_analysis.R")
```

### 修改參數

#### 修改流失定義（60 天 → 90 天）
編輯 `02_build_cohort.R`：

```r
# 原本
status = ifelse(days_since_last > 60, 1, 0)

# 修改為
status = ifelse(days_since_last > 90, 1, 0)
```

#### 修改時段劃分
編輯 `05_time_product_analysis.R`：

```r
time_period = case_when(
  Hour >= 11 & Hour <= 14 ~ "午餐",      # 延長午餐時段
  Hour >= 15 & Hour <= 17 ~ "下午茶",
  Hour >= 18 & Hour <= 20 ~ "晚餐",      # 延長晚餐時段
  TRUE ~ "其他"
)
```

## 常見問題

### Q1: 中文字顯示為方框或亂碼
**A**: 檢查字型路徑是否正確。在 R 中執行：

```r
list.files("/System/Library/Fonts", pattern = "Hiragino")
```

如果找不到字型，請使用備選字型：

```r
font_add("STHeiti", "/System/Library/Fonts/STHeiti Medium.ttc")
```

### Q2: 報告生成失敗
**A**: 確保已安裝所有必要套件，特別是 `pdftools` 和 `showtext`：

```r
install.packages(c("pdftools", "showtext"))
```

### Q3: 執行速度慢
**A**: 產品關聯分析的計算量較大。如果 SKU 數量很多，可以：
- 增加最小 support 閾值（減少規則數）
- 只分析 Top N 熱門 SKU

### Q4: 想要匯出為 Excel 而非 CSV
**A**: 安裝 `writexl` 套件並修改輸出語句：

```r
install.packages("writexl")
library(writexl)
write_xlsx(data, "output.xlsx")
```

## 效能指標

在標準配置下（Intel i7, 16GB RAM），處理約 9,000 筆交易記錄：

- 資料前處理：~5 秒
- 顧客世代建構：~3 秒
- 存活分析：~15 秒（含 5 張圖）
- 產品關聯分析：~20 秒
- 時段產品分析：~10 秒
- PDF 報告生成：~30 秒

**總執行時間**：約 1.5 分鐘

## 授權與引用

本專案為 Taiwanway 餐廳內部分析工具。如需引用分析方法或結果，請參考：

```
Taiwanway Data Analytics Team (2025). 
Kaplan-Meier Survival Analysis and Product Association Mining 
for Restaurant Customer Retention. 
Internal Technical Report.
```

## 聯絡方式

如有問題或建議，請聯絡：
- 專案負責人：請參考主專案 README.md
- GitHub Issues：（如適用）

## 更新紀錄

### Version 1.0 (2025-11-16)
- 初始版本發布
- 完整實作 5 組 KM 存活分析
- 產品關聯分析與時段偏好分析
- 兩份 PDF 綜合報告
- 完整的研究設計文件

---

**最後更新**：2025-11-16  
**文件版本**：1.0

