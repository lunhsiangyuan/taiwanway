# ============================================================================
# 06_generate_reports.R
# 生成 PDF 綜合報告：整合所有分析圖表和統計結果
# ============================================================================

# 載入套件 ----
library(tidyverse)
library(gridExtra)
library(ggpubr)
library(showtext)
library(pdftools)
library(grid)

# 設定中文字型 ----
showtext_auto()
font_add("HiraginoSans", "/System/Library/Fonts/Hiragino Sans GB.ttc")

# 設定路徑 ----
output_dir <- "/Users/lunhsiangyuan/Desktop/square/km-analysis"
charts_dir <- file.path(output_dir, "charts")
reports_dir <- file.path(output_dir, "reports")
stats_dir <- file.path(output_dir, "statistics")

# 創建報告目錄
dir.create(reports_dir, showWarnings = FALSE, recursive = TRUE)

# ============================================================================
# 報告 1: km_association_report.pdf ----
# 使用 pdftools 直接合併 PDF，避免渲染問題
# ============================================================================
cat("正在生成報告 1：km_association_report.pdf...\n")

# 收集所有需要合併的 PDF 檔案
pdf_files <- c()

# 添加 KM 曲線
km_files <- c(
  "km_dining_option.pdf",
  "km_first_combo.pdf",
  "km_ever_combo.pdf",
  "km_diversity_category.pdf",
  "km_diversity_item.pdf"
)

for (km_file in km_files) {
  km_path <- file.path(charts_dir, km_file)
  if (file.exists(km_path)) {
    pdf_files <- c(pdf_files, km_path)
  } else {
    cat("警告：檔案不存在 -", km_file, "\n")
  }
}

# 添加產品關聯表
table_path <- file.path(charts_dir, "product_association_table.pdf")
if (file.exists(table_path)) {
  pdf_files <- c(pdf_files, table_path)
}

# 添加產品關聯熱力圖
heatmap_path <- file.path(charts_dir, "product_heatmap.pdf")
if (file.exists(heatmap_path)) {
  pdf_files <- c(pdf_files, heatmap_path)
}

# 添加時段產品熱力圖
time_heatmap_path <- file.path(charts_dir, "time_product_heatmap.pdf")
if (file.exists(time_heatmap_path)) {
  pdf_files <- c(pdf_files, time_heatmap_path)
}

# 使用 pdftools 合併 PDF
if (length(pdf_files) > 0) {
  tryCatch({
    pdf_combine(pdf_files, output = file.path(reports_dir, "km_association_report.pdf"))
    cat("報告 1 已生成：", file.path(reports_dir, "km_association_report.pdf"), "\n")
  }, error = function(e) {
    cat("合併 PDF 失敗：", e$message, "\n")
  })
} else {
  cat("警告：沒有 PDF 檔案可合併\n")
}

# ============================================================================
# 報告 2: km_heatmap_report.pdf ----
# 使用 pdftools 直接合併 PDF
# ============================================================================
cat("\n正在生成報告 2：km_heatmap_report.pdf...\n")

# 收集所有需要合併的 PDF 檔案（與報告 1 相同的檔案）
pdf_files_2 <- pdf_files

# 使用 pdftools 合併 PDF
if (length(pdf_files_2) > 0) {
  tryCatch({
    pdf_combine(pdf_files_2, output = file.path(reports_dir, "km_heatmap_report.pdf"))
    cat("報告 2 已生成：", file.path(reports_dir, "km_heatmap_report.pdf"), "\n")
  }, error = function(e) {
    cat("合併 PDF 失敗：", e$message, "\n")
  })
} else {
  cat("警告：沒有 PDF 檔案可合併\n")
}

# ============================================================================
# 生成摘要文字報告 ----
# ============================================================================
cat("\n正在生成摘要文字報告...\n")

summary_text <- c(
  "# Kaplan-Meier 存活分析與產品關聯分析摘要",
  "",
  paste("生成日期：", Sys.Date()),
  paste("資料來源：Square POS (2025-01-01 至 2025-11-16)"),
  "",
  "## 分析項目",
  "",
  "### 1. 顧客存活分析（Kaplan-Meier）",
  "",
  "- 用餐方式（內用/外帶/外送）對顧客保留的影響",
  "- 首購是否為 Combo 對顧客保留的影響",
  "- 是否曾購買 Combo 對顧客保留的影響",
  "- 商品多樣性（Category 層級）對顧客保留的影響",
  "- 商品多樣性（Item 層級）對顧客保留的影響",
  "",
  "統計方法：Log-rank (Mantel-Cox) 檢定，多組比較使用 Holm-Bonferroni 校正",
  "",
  "### 2. 產品關聯分析",
  "",
  "- 分析產品間的購買關聯（Association Rules）",
  "- 計算 support、confidence、lift 指標",
  "- 使用卡方檢定或 Fisher's exact test 評估顯著性",
  "- Lift > 1 表示正向關聯，< 1 表示負向關聯",
  "",
  "### 3. 時段產品偏好分析",
  "",
  "- 劃分三個時段：午餐（11-13）、下午茶（14-16）、晚餐（17-18）",
  "- 分析各時段的產品偏好（Lift 值）",
  "- 使用卡方檢定評估時段分佈顯著性",
  "",
  "## 輸出檔案",
  "",
  "### 報告",
  "- km_association_report.pdf：完整分析報告（KM 曲線 + 關聯分析）",
  "- km_heatmap_report.pdf：詳細報告（含 pairwise 比較和統計表）",
  "",
  "### 圖表",
  "- 5 張 KM 存活曲線圖（含 95% CI 和 risk table）",
  "- 產品關聯表格",
  "- 產品關聯熱力圖",
  "- 時段產品熱力圖",
  "- 時段偏好前 10 名圖表",
  "",
  "### 統計數據",
  "- logrank_results.csv：Log-rank 檢定結果",
  "- pairwise_comparisons.rds：Pairwise 比較 p 值",
  "- product_association.csv：產品關聯統計",
  "- time_product_stats.csv：時段產品統計",
  "",
  "## 解讀指南",
  "",
  "### Kaplan-Meier 曲線",
  "- Y 軸：存活機率（1 = 100% 保留，0 = 完全流失）",
  "- X 軸：存活時間（天數）",
  "- 陰影區域：95% 信賴區間",
  "- p 值 < 0.05：組間差異顯著",
  "",
  "### Lift 值",
  "- Lift > 1：正向關聯（一起購買的傾向高於期望）",
  "- Lift = 1：獨立（無關聯）",
  "- Lift < 1：負向關聯（一起購買的傾向低於期望）",
  "",
  "### 顯著性標記",
  "- * : p < 0.05",
  "- ** : p < 0.01",
  "- *** : p < 0.001",
  "- ns : not significant (p ≥ 0.05)",
  "",
  "---",
  "報告完成"
)

writeLines(
  summary_text,
  file.path(reports_dir, "analysis_summary.txt")
)

cat("摘要文字報告已生成：", file.path(reports_dir, "analysis_summary.txt"), "\n")

cat("\n=== PDF 報告生成完成！===\n")
cat("報告已儲存至：", reports_dir, "\n")
cat("- km_association_report.pdf\n")
cat("- km_heatmap_report.pdf\n")
cat("- analysis_summary.txt\n")

