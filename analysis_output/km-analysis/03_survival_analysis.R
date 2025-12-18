# ============================================================================
# 03_survival_analysis.R
# Kaplan-Meier 存活分析：擬合 KM 曲線、log-rank 檢定、視覺化
# ============================================================================

# 載入套件 ----
library(tidyverse)
library(survival)
library(survminer)
library(showtext)
library(ggpubr)

# 設定中文字型 ----
showtext_auto()
font_add("HiraginoSans", "/System/Library/Fonts/Hiragino Sans GB.ttc")

# 設定路徑 ----
output_dir <- "/Users/lunhsiangyuan/Desktop/square/km-analysis"
input_file <- file.path(output_dir, "data", "customer_cohort.csv")

# 讀取顧客世代資料 ----
cat("正在讀取顧客世代資料...\n")
cohort <- read_csv(input_file, show_col_types = FALSE)

cat("顧客總數：", nrow(cohort), "\n")
cat("流失顧客：", sum(cohort$status == 1), "\n")

# 創建統計結果儲存目錄 ----
dir.create(file.path(output_dir, "statistics"), showWarnings = FALSE, recursive = TRUE)

# 初始化統計結果 ----
logrank_results <- list()

# ============================================================================
# 1. 用餐方式（Dining Option）----
# ============================================================================
cat("\n=== 分析 1：用餐方式 ===\n")

# 擬合 KM 曲線
fit_dining <- survfit(Surv(survival_time, status) ~ dining_group, data = cohort)

# Log-rank 檢定
survdiff_dining <- survdiff(Surv(survival_time, status) ~ dining_group, data = cohort)
cat("Log-rank 檢定 p 值：", 
    pchisq(survdiff_dining$chisq, length(survdiff_dining$n) - 1, lower.tail = FALSE), "\n")

# Pairwise 比較
pairwise_dining <- pairwise_survdiff(
  Surv(survival_time, status) ~ dining_group, 
  data = cohort,
  p.adjust.method = "holm"
)

cat("Pairwise 比較（Holm 校正）：\n")
print(pairwise_dining$p.value)

# 儲存統計結果
logrank_results$dining_option <- list(
  overall_pvalue = pchisq(survdiff_dining$chisq, length(survdiff_dining$n) - 1, lower.tail = FALSE),
  pairwise = pairwise_dining$p.value
)

# 視覺化
p_dining <- ggsurvplot(
  fit_dining,
  data = cohort,
  conf.int = FALSE,  # 暫時關閉以避免繪圖錯誤
  pval = TRUE,
  risk.table = TRUE,
  risk.table.height = 0.3,
  xlab = "存活時間（天）",
  ylab = "存活機率",
  title = "顧客存活分析：用餐方式",
  legend.title = "用餐方式",
  legend.labs = levels(factor(cohort$dining_group)),
  palette = "jco",
  ggtheme = theme_bw(base_size = 12),
  font.family = "HiraginoSans"
)

# 儲存圖表
ggsave(
  file.path(output_dir, "charts", "km_dining_option.pdf"),
  plot = p_dining$plot,
  width = 10,
  height = 8,
  device = cairo_pdf
)

cat("已儲存：km_dining_option.pdf\n")

# ============================================================================
# 2. 首購是否 Combo ----
# ============================================================================
cat("\n=== 分析 2：首購是否 Combo ===\n")

# 擬合 KM 曲線
fit_first_combo <- survfit(Surv(survival_time, status) ~ first_purchase_combo, data = cohort)

# Log-rank 檢定
survdiff_first_combo <- survdiff(Surv(survival_time, status) ~ first_purchase_combo, data = cohort)
pval_first_combo <- pchisq(survdiff_first_combo$chisq, 
                            length(survdiff_first_combo$n) - 1, 
                            lower.tail = FALSE)
cat("Log-rank 檢定 p 值：", pval_first_combo, "\n")

# 儲存統計結果
logrank_results$first_purchase_combo <- list(
  pvalue = pval_first_combo
)

# 視覺化
p_first_combo <- ggsurvplot(
  fit_first_combo,
  data = cohort,
  conf.int = FALSE,  # 暫時關閉以避免繪圖錯誤
  pval = TRUE,
  risk.table = TRUE,
  risk.table.height = 0.3,
  xlab = "存活時間（天）",
  ylab = "存活機率",
  title = "顧客存活分析：首購是否 Combo",
  legend.title = "首購 Combo",
  legend.labs = c("No", "Yes"),
  palette = c("#E64B35FF", "#4DBBD5FF"),
  ggtheme = theme_bw(base_size = 12),
  font.family = "HiraginoSans"
)

ggsave(
  file.path(output_dir, "charts", "km_first_combo.pdf"),
  plot = p_first_combo$plot,
  width = 10,
  height = 8,
  device = cairo_pdf
)

cat("已儲存：km_first_combo.pdf\n")

# ============================================================================
# 3. 是否曾買過 Combo ----
# ============================================================================
cat("\n=== 分析 3：是否曾買過 Combo ===\n")

# 擬合 KM 曲線
fit_ever_combo <- survfit(Surv(survival_time, status) ~ ever_bought_combo, data = cohort)

# Log-rank 檢定
survdiff_ever_combo <- survdiff(Surv(survival_time, status) ~ ever_bought_combo, data = cohort)
pval_ever_combo <- pchisq(survdiff_ever_combo$chisq, 
                          length(survdiff_ever_combo$n) - 1, 
                          lower.tail = FALSE)
cat("Log-rank 檢定 p 值：", pval_ever_combo, "\n")

# 儲存統計結果
logrank_results$ever_bought_combo <- list(
  pvalue = pval_ever_combo
)

# 視覺化
p_ever_combo <- ggsurvplot(
  fit_ever_combo,
  data = cohort,
  conf.int = FALSE,  # 暫時關閉以避免繪圖錯誤
  pval = TRUE,
  risk.table = TRUE,
  risk.table.height = 0.3,
  xlab = "存活時間（天）",
  ylab = "存活機率",
  title = "顧客存活分析：是否曾買過 Combo",
  legend.title = "曾買 Combo",
  legend.labs = c("No", "Yes"),
  palette = c("#E64B35FF", "#4DBBD5FF"),
  ggtheme = theme_bw(base_size = 12),
  font.family = "HiraginoSans"
)

ggsave(
  file.path(output_dir, "charts", "km_ever_combo.pdf"),
  plot = p_ever_combo$plot,
  width = 10,
  height = 8,
  device = cairo_pdf
)

cat("已儲存：km_ever_combo.pdf\n")

# ============================================================================
# 4. 商品多樣性（Category）----
# ============================================================================
cat("\n=== 分析 4：商品多樣性（Category）===\n")

# 擬合 KM 曲線
fit_diversity_cat <- survfit(Surv(survival_time, status) ~ diversity_category, data = cohort)

# Log-rank 檢定
survdiff_diversity_cat <- survdiff(Surv(survival_time, status) ~ diversity_category, data = cohort)
pval_diversity_cat <- pchisq(survdiff_diversity_cat$chisq, 
                              length(survdiff_diversity_cat$n) - 1, 
                              lower.tail = FALSE)
cat("Log-rank 檢定 p 值：", pval_diversity_cat, "\n")

# Pairwise 比較
pairwise_diversity_cat <- pairwise_survdiff(
  Surv(survival_time, status) ~ diversity_category, 
  data = cohort,
  p.adjust.method = "holm"
)

cat("Pairwise 比較（Holm 校正）：\n")
print(pairwise_diversity_cat$p.value)

# 儲存統計結果
logrank_results$diversity_category <- list(
  overall_pvalue = pval_diversity_cat,
  pairwise = pairwise_diversity_cat$p.value
)

# 視覺化
p_diversity_cat <- ggsurvplot(
  fit_diversity_cat,
  data = cohort,
  conf.int = FALSE,  # 暫時關閉以避免繪圖錯誤
  pval = TRUE,
  risk.table = TRUE,
  risk.table.height = 0.3,
  xlab = "存活時間（天）",
  ylab = "存活機率",
  title = "顧客存活分析：商品多樣性（Category）",
  legend.title = "商品類別數",
  palette = "jco",
  ggtheme = theme_bw(base_size = 12),
  font.family = "HiraginoSans"
)

ggsave(
  file.path(output_dir, "charts", "km_diversity_category.pdf"),
  plot = p_diversity_cat$plot,
  width = 10,
  height = 8,
  device = cairo_pdf
)

cat("已儲存：km_diversity_category.pdf\n")

# ============================================================================
# 5. 商品多樣性（Item）----
# ============================================================================
cat("\n=== 分析 5：商品多樣性（Item）===\n")

# 擬合 KM 曲線
fit_diversity_item <- survfit(Surv(survival_time, status) ~ diversity_item, data = cohort)

# Log-rank 檢定
survdiff_diversity_item <- survdiff(Surv(survival_time, status) ~ diversity_item, data = cohort)
pval_diversity_item <- pchisq(survdiff_diversity_item$chisq, 
                               length(survdiff_diversity_item$n) - 1, 
                               lower.tail = FALSE)
cat("Log-rank 檢定 p 值：", pval_diversity_item, "\n")

# Pairwise 比較
pairwise_diversity_item <- pairwise_survdiff(
  Surv(survival_time, status) ~ diversity_item, 
  data = cohort,
  p.adjust.method = "holm"
)

cat("Pairwise 比較（Holm 校正）：\n")
print(pairwise_diversity_item$p.value)

# 儲存統計結果
logrank_results$diversity_item <- list(
  overall_pvalue = pval_diversity_item,
  pairwise = pairwise_diversity_item$p.value
)

# 視覺化
p_diversity_item <- ggsurvplot(
  fit_diversity_item,
  data = cohort,
  conf.int = FALSE,  # 暫時關閉以避免繪圖錯誤
  pval = TRUE,
  risk.table = TRUE,
  risk.table.height = 0.3,
  xlab = "存活時間（天）",
  ylab = "存活機率",
  title = "顧客存活分析：商品多樣性（Item）",
  legend.title = "商品種類數",
  palette = "jco",
  ggtheme = theme_bw(base_size = 12),
  font.family = "HiraginoSans"
)

ggsave(
  file.path(output_dir, "charts", "km_diversity_item.pdf"),
  plot = p_diversity_item$plot,
  width = 10,
  height = 8,
  device = cairo_pdf
)

cat("已儲存：km_diversity_item.pdf\n")

# ============================================================================
# 儲存統計結果 ----
# ============================================================================
cat("\n正在儲存統計結果...\n")

# 整理成 data frame
logrank_df <- tibble(
  analysis = c(
    "用餐方式",
    "首購是否 Combo",
    "是否曾買過 Combo",
    "商品多樣性（Category）",
    "商品多樣性（Item）"
  ),
  overall_pvalue = c(
    logrank_results$dining_option$overall_pvalue,
    logrank_results$first_purchase_combo$pvalue,
    logrank_results$ever_bought_combo$pvalue,
    logrank_results$diversity_category$overall_pvalue,
    logrank_results$diversity_item$overall_pvalue
  ),
  significance = case_when(
    overall_pvalue < 0.001 ~ "***",
    overall_pvalue < 0.01 ~ "**",
    overall_pvalue < 0.05 ~ "*",
    TRUE ~ "ns"
  )
)

write_csv(logrank_df, file.path(output_dir, "statistics", "logrank_results.csv"))

cat("Log-rank 檢定結果已儲存至：statistics/logrank_results.csv\n")

# 儲存 pairwise 比較結果
pairwise_results <- list(
  dining_option = logrank_results$dining_option$pairwise,
  diversity_category = logrank_results$diversity_category$pairwise,
  diversity_item = logrank_results$diversity_item$pairwise
)

saveRDS(pairwise_results, file.path(output_dir, "statistics", "pairwise_comparisons.rds"))

cat("Pairwise 比較結果已儲存至：statistics/pairwise_comparisons.rds\n")

cat("\n=== 存活分析完成！===\n")
cat("已生成 5 張 KM 曲線圖於 charts/ 目錄\n")
cat("統計檢定結果已儲存至 statistics/ 目錄\n")

