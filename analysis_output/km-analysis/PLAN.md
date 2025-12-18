# Kaplan-Meier 存活分析與產品關聯分析（R 語言實作）

## 專案目標

使用 R 語言對 Taiwanway 交易資料進行學術級別的 Kaplan-Meier 存活分析、產品關聯分析、時段偏好分析，包含完整統計檢定與多重檢定校正，並產生符合學術論文標準的 PDF 報告。

## 1. 資料前處理 (01_data_preprocessing.R)

### 套件
```r
library(tidyverse)
library(lubridate)
library(here)
```

### 時間處理
- 合併 `Date` + `Time` 為 `DateTime` (Taipei 時區)
- 時間平移 +12 小時對應營業時間 11:00-19:00
- 轉換紐約時區（考慮 DST）：
  - 2025-11-02 前：EDT (UTC-4)
  - 2025-11-02 後：EST (UTC-5)
- 使用 `lubridate::with_tz()` 處理時區
- 觀察終點：`max(DateTime)`

### 資料清理
- 篩選 `Event Type == "Payment"`
- 移除 `Price Point Name == ""` (Custom Amount)
- 移除 `is.na(SKU)` 或 `SKU == ""`
- 輸出：`km-analysis/data/cleaned_data.csv`

## 2. 顧客世代建構 (02_build_cohort.R)

### 套件
```r
library(tidyverse)
library(survival)
```

### 顧客追蹤邏輯
- 按 `Customer ID` 分組
- 計算首購日 (`first_purchase_date`)
- 計算末購日 (`last_purchase_date`)
- 計算存活時間：`time = as.numeric(last_purchase_date - first_purchase_date)`
- 流失定義：
  - 若 `last_purchase_date + 60 天 < 觀察終點` → `status = 1` (流失)
  - 否則 → `status = 0` (censored)

### 分組變數
1. **用餐方式** (`dining_group`)：For Here / To Go / Delivery / Unknown
2. **首購 Combo** (`first_purchase_combo`)：Yes / No
   - 檢查首筆交易 `Category` 是否包含 "Combo"
3. **曾買 Combo** (`ever_bought_combo`)：Yes / No
   - 整體交易史是否出現 "Combo"
4. **商品多樣性 Category** (`diversity_category`)：1種 / 2-3種 / 4種以上
5. **商品多樣性 Item** (`diversity_item`)：1種 / 2-3種 / 4種以上

輸出：`km-analysis/data/customer_cohort.csv`

## 3. Kaplan-Meier 存活分析 (03_survival_analysis.R)

### 套件
```r
library(survival)      # survfit, survdiff
library(survminer)     # ggsurvplot
library(showtext)      # 中文字型
library(ggpubr)        # ggarrange, stat_pvalue_manual
```

### 字型設定（學術論文標準）
```r
showtext_auto()
font_add("Hiragino Sans GB", "/System/Library/Fonts/Hiragino Sans GB.ttc")
theme_set(theme_bw(base_size = 12, base_family = "Hiragino Sans GB"))
```

### 存活分析流程（每個分組變數）

#### a) 擬合 KM 曲線
```r
fit <- survfit(Surv(time, status) ~ group_var, data = cohort)
```

#### b) Log-rank 檢定
- **兩組**：`survival::survdiff(..., rho=0)`
- **多組**：
  - 整體檢定：`survdiff()`
  - Pairwise：`pairwise_survdiff()`
  - 多重檢定校正：Holm-Bonferroni (`p.adjust(method="holm")`)

#### c) 視覺化（學術論文級別）
```r
ggsurvplot(
  fit,
  data = cohort,
  conf.int = TRUE,           # 95% Greenwood CI
  pval = TRUE,               # 顯示 p 值
  risk.table = TRUE,         # At-risk 人數表
  risk.table.height = 0.25,
  xlab = "存活時間（天）",
  ylab = "存活機率",
  legend.title = "分組",
  palette = "jco",           # 學術期刊配色
  ggtheme = theme_bw(base_size = 12)
)
```

輸出圖表：
- `km-analysis/charts/km_dining_option.pdf`
- `km-analysis/charts/km_first_combo.pdf`
- `km-analysis/charts/km_ever_combo.pdf`
- `km-analysis/charts/km_diversity_category.pdf`
- `km-analysis/charts/km_diversity_item.pdf`

輸出統計：`km-analysis/statistics/logrank_results.csv`

## 4. 產品關聯分析 (04_product_association.R)

### 套件
```r
library(tidyverse)
library(arules)        # apriori, interestMeasure
library(arulesViz)     # plot
library(pheatmap)      # 熱力圖
```

### 購物籃建構
```r
transactions <- cleaned_data %>%
  filter(!is.na(SKU), SKU != "") %>%
  group_by(Transaction_ID) %>%
  summarise(items = list(unique(SKU)))

# 轉換為 arules 格式
trans <- as(transactions$items, "transactions")
```

### 關聯規則挖掘
```r
rules <- apriori(trans, 
  parameter = list(supp = 10/length(trans), conf = 0.01, minlen = 2, maxlen = 2),
  control = list(verbose = FALSE)
)

# 計算 lift
rules_df <- as(rules, "data.frame") %>%
  arrange(desc(lift)) %>%
  head(30)
```

### 統計檢定（每對 SKU）
- 建立 2×2 列聯表：
  - 有 A 有 B, 有 A 無 B, 無 A 有 B, 無 A 無 B
- 檢定選擇：
  - 期望值 ≥ 5：`chisq.test()`
  - 期望值 < 5：`fisher.test()`
- 多重檢定校正：`p.adjust(method = "holm")`

### 視覺化

#### a) 關聯表格
使用 `gridExtra::tableGrob()` 或 `ggpubr::ggtexttable()` 產生學術級表格：
- 欄位：SKU_A, SKU_B, co_occur, A→B%, B→A%, lift, p.value, significance

#### b) 熱力圖
```r
pheatmap(
  lift_matrix,
  color = colorRampPalette(c("blue", "white", "red"))(100),
  display_numbers = significance_matrix,  # 顯示 * 表示 p<0.05
  cluster_rows = TRUE,
  cluster_cols = TRUE,
  fontsize = 10,
  main = "產品關聯 Lift 熱力圖",
  filename = "km-analysis/charts/product_heatmap.pdf"
)
```

輸出：
- `km-analysis/charts/product_association_table.pdf`
- `km-analysis/charts/product_heatmap.pdf`
- `km-analysis/statistics/product_association.csv`

## 5. 時段產品分析 (05_time_product_analysis.R)

### 時段劃分
```r
cleaned_data <- cleaned_data %>%
  mutate(
    hour = hour(DateTime_NY),
    time_period = case_when(
      hour >= 11 & hour <= 13 ~ "午餐",
      hour >= 14 & hour <= 16 ~ "下午茶",
      hour >= 17 & hour <= 18 ~ "晚餐",
      TRUE ~ "其他"
    )
  ) %>%
  filter(time_period != "其他")
```

### 時段 × SKU 關聯分析
```r
# 計算每個 SKU 在各時段的出現次數
time_sku <- cleaned_data %>%
  count(time_period, SKU) %>%
  filter(n >= 10)  # 篩選共現 ≥ 10

# 計算 lift
sku_total <- cleaned_data %>% count(SKU, name = "sku_total")
period_total <- cleaned_data %>% count(time_period, name = "period_total")
overall_total <- nrow(cleaned_data)

time_sku_lift <- time_sku %>%
  left_join(sku_total, by = "SKU") %>%
  left_join(period_total, by = "time_period") %>%
  mutate(
    expected = (sku_total * period_total) / overall_total,
    lift = n / expected
  )
```

### 卡方檢定（每個 SKU）
```r
chi_results <- cleaned_data %>%
  group_by(SKU) %>%
  summarise(
    p.value = if(n() >= 10) {
      tbl <- table(time_period)
      chisq.test(tbl)$p.value
    } else NA_real_
  ) %>%
  mutate(p.adj = p.adjust(p.value, method = "holm"))
```

### 視覺化
```r
# 熱力圖
lift_wide <- time_sku_lift %>%
  select(SKU, time_period, lift) %>%
  pivot_wider(names_from = time_period, values_from = lift, values_fill = 1)

sig_wide <- chi_results %>%
  select(SKU, p.adj) %>%
  mutate(sig = ifelse(p.adj < 0.05, "*", ""))

pheatmap(
  lift_wide[, -1],
  labels_row = lift_wide$SKU,
  color = colorRampPalette(c("blue", "white", "red"))(100),
  breaks = seq(0.5, 2, length.out = 101),
  display_numbers = TRUE,
  main = "時段 × 產品 Lift 熱力圖",
  filename = "km-analysis/charts/time_product_heatmap.pdf"
)
```

輸出：
- `km-analysis/charts/time_product_heatmap.pdf`
- `km-analysis/statistics/time_product_stats.csv`

## 6. PDF 綜合報告 (06_generate_reports.R)

### 套件
```r
library(pdftools)
library(gridExtra)
library(ggpubr)
```

### km_association_report.pdf
使用 `cairo_pdf()` 整合多頁：
- 頁 1-5：5 組 KM 曲線（含 risk table）
- 頁 6：產品關聯表（Top 30）
- 頁 7：產品關聯熱力圖
- 頁 8：時段產品熱力圖

### km_heatmap_report.pdf
- 頁 1-5：5 組 KM 曲線
- 頁 6：Pairwise log-rank p 值矩陣（多組比較）
- 頁 7：產品關聯熱力圖（lift + p 值標註）
- 頁 8：時段產品熱力圖（lift + 卡方 p 值）
- 頁 9：統計檢定匯總表

### 技術細節
```r
cairo_pdf(
  "km-analysis/reports/km_association_report.pdf",
  width = 10, height = 8,
  family = "Hiragino Sans GB"
)
# 繪圖程式碼
dev.off()
```

## 7. 研究設計企劃書 (research_design.md)

內容包含（繁體中文）：
- **研究背景**：顧客保留與產品組合策略
- **研究目的**：識別流失風險因子、產品交叉銷售機會
- **資料來源**：Square POS 2025-01-01 至 2025-11-16
- **變數定義**：
  - 依變數：存活時間、流失狀態
  - 自變數：用餐方式、Combo 購買、商品多樣性
  - 關聯指標：support, confidence, lift
- **統計方法**：
  - Kaplan-Meier 估計（Greenwood 標準誤）
  - Log-rank 檢定（Mantel-Cox）
  - Pairwise 比較 + Holm-Bonferroni 校正
  - 卡方檢定 / Fisher's exact test
- **解讀指南**：
  - Hazard ratio 意義
  - Lift > 1 正向關聯、< 1 負向關聯
  - p < 0.05 顯著水準
- **研究限制**：右設限資料、選擇性偏誤、因果推論限制

存放：`km-analysis/research_design.md`

## 8. 主控腳本 (run_all.R)

```r
# 依序執行所有分析
source("km-analysis/01_data_preprocessing.R")
source("km-analysis/02_build_cohort.R")
source("km-analysis/03_survival_analysis.R")
source("km-analysis/04_product_association.R")
source("km-analysis/05_time_product_analysis.R")
source("km-analysis/06_generate_reports.R")

cat("分析完成！報告位於 km-analysis/reports/\n")
```

## 中文字型處理方案

### macOS 系統字型路徑
- **Hiragino Sans GB**: `/System/Library/Fonts/Hiragino Sans GB.ttc`
- **備選**: `/System/Library/Fonts/STHeiti Medium.ttc`

### 每個 R 腳本開頭必須包含
```r
library(showtext)
showtext_auto()

# 載入中文字型
font_add("HiraginoSans", "/System/Library/Fonts/Hiragino Sans GB.ttc")

# 設定全域主題
theme_set(theme_bw(base_size = 12, base_family = "HiraginoSans"))
```

### ggplot2 圖表
```r
ggplot(...) +
  theme_bw(base_family = "HiraginoSans") +
  theme(
    text = element_text(family = "HiraginoSans"),
    plot.title = element_text(family = "HiraginoSans"),
    axis.title = element_text(family = "HiraginoSans"),
    axis.text = element_text(family = "HiraginoSans"),
    legend.text = element_text(family = "HiraginoSans")
  )
```

### survminer KM 曲線
```r
ggsurvplot(
  ...,
  font.family = "HiraginoSans",
  ggtheme = theme_bw(base_family = "HiraginoSans")
)
```

### pheatmap 熱力圖
```r
pheatmap(
  ...,
  fontfamily = "HiraginoSans",
  fontfamily_row = "HiraginoSans",
  fontfamily_col = "HiraginoSans"
)
```

### PDF 輸出
```r
cairo_pdf(
  "output.pdf",
  width = 10, height = 8,
  family = "HiraginoSans",
  onefile = TRUE
)
# 繪圖程式碼
dev.off()
```

### 測試中文顯示
```r
# 01_data_preprocessing.R 最後加入測試
library(ggplot2)
ggplot(data.frame(x=1:3, y=c("內用","外帶","外送")), aes(x,x,label=y)) +
  geom_text(family="HiraginoSans", size=5) +
  ggtitle("中文字型測試") +
  theme_bw(base_family = "HiraginoSans")
ggsave("km-analysis/charts/font_test.pdf", width=6, height=4, device=cairo_pdf)
```

## R 套件依賴

```r
install.packages(c(
  "tidyverse",    # 資料處理
  "lubridate",    # 時間處理
  "survival",     # 存活分析
  "survminer",    # KM 曲線視覺化
  "arules",       # 關聯規則
  "arulesViz",    # 關聯視覺化
  "pheatmap",     # 熱力圖
  "showtext",     # 中文字型（必須）
  "ggpubr",       # 學術圖表
  "gridExtra",    # 多圖排版
  "pdftools",     # PDF 操作
  "here",         # 路徑管理
  "extrafont"     # 備用字型方案
))
```

## 輸出結構

```
km-analysis/
├── 01_data_preprocessing.R
├── 02_build_cohort.R
├── 03_survival_analysis.R
├── 04_product_association.R
├── 05_time_product_analysis.R
├── 06_generate_reports.R
├── run_all.R
├── install_packages.R
├── README.md
├── PLAN.md
├── research_design.md
├── data/
│   ├── cleaned_data.csv
│   └── customer_cohort.csv
├── charts/
│   ├── km_dining_option.pdf
│   ├── km_first_combo.pdf
│   ├── km_ever_combo.pdf
│   ├── km_diversity_category.pdf
│   ├── km_diversity_item.pdf
│   ├── product_association_table.pdf
│   ├── product_heatmap.pdf
│   ├── time_product_heatmap.pdf
│   ├── time_period_top10.pdf
│   └── font_test.pdf
├── reports/
│   ├── km_association_report.pdf
│   ├── km_heatmap_report.pdf
│   └── analysis_summary.txt
└── statistics/
    ├── logrank_results.csv
    ├── pairwise_comparisons.rds
    ├── product_association.csv
    └── time_product_stats.csv
```

## 學術論文標準

- 圖表尺寸：10×8 英吋（適合期刊投稿）
- 字型大小：12pt（主文）、10pt（軸標籤）
- 配色：ColorBrewer / JCO palette（色盲友善）
- 統計顯著性：p < 0.05 (*), p < 0.01 (**), p < 0.001 (***)
- 信賴區間：95% CI（Greenwood 方法）
- 圖表解析度：300 DPI

## 執行步驟

1. **安裝套件**
   ```r
   source("km-analysis/install_packages.R")
   ```

2. **執行所有分析**
   ```r
   source("km-analysis/run_all.R")
   ```

3. **查看結果**
   - 打開 `km-analysis/reports/km_association_report.pdf`
   - 閱讀 `km-analysis/research_design.md` 了解方法
   - 檢視 `km-analysis/statistics/*.csv` 查看數據

## 關鍵統計概念

### Kaplan-Meier 估計
存活函數：$\hat{S}(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$

### Log-rank 檢定
比較兩組或多組存活曲線是否有顯著差異，虛無假設為各組存活曲線相同。

### Lift 值
- Lift > 1：正向關聯
- Lift = 1：獨立
- Lift < 1：負向關聯

### 多重檢定校正（Holm-Bonferroni）
控制 Family-Wise Error Rate (FWER)，確保多組比較的統計效度。

---

**版本**：1.0  
**最後更新**：2025-11-16  
**狀態**：所有分析腳本已完成



