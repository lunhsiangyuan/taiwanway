# ============================================================================
# 05_time_product_analysis.R
# 時段產品分析：劃分時段、計算 lift、卡方檢定、視覺化
# ============================================================================

# 載入套件 ----
library(tidyverse)
library(pheatmap)
library(showtext)
library(ggpubr)

# 設定中文字型 ----
showtext_auto()
font_add("HiraginoSans", "/System/Library/Fonts/Hiragino Sans GB.ttc")

# 設定路徑 ----
output_dir <- "/Users/lunhsiangyuan/Desktop/square/km-analysis"
input_file <- file.path(output_dir, "data", "cleaned_data.csv")

# 讀取清理後的資料 ----
cat("正在讀取清理後的資料...\n")
data <- read_csv(input_file, show_col_types = FALSE)

cat("資料筆數：", nrow(data), "\n")

# ============================================================================
# 1. 時段劃分 ----
# ============================================================================
cat("\n步驟 1：時段劃分...\n")

# 時間平移 +12 小時後，11-19 變成 23-7（跨日）
# 調整時段定義以符合實際資料
data <- data %>%
  mutate(
    time_period = case_when(
      (Hour >= 23 | Hour <= 1) ~ "午餐",      # 原 11-13，平移後 23-1
      Hour >= 2 & Hour <= 4 ~ "下午茶",       # 原 14-16，平移後 2-4
      Hour >= 5 & Hour <= 6 ~ "晚餐",         # 原 17-18，平移後 5-6
      TRUE ~ "其他"
    )
  ) %>%
  filter(time_period != "其他")  # 移除不在營業時段的記錄

cat("時段分佈：\n")
print(table(data$time_period))

cat("篩選後資料筆數：", nrow(data), "\n")

# ============================================================================
# 2. 計算時段 × SKU 共現 ----
# ============================================================================
cat("\n步驟 2：計算時段 × SKU 共現...\n")

# 計算每個時段 × SKU 的出現次數
time_sku_counts <- data %>%
  count(time_period, SKU) %>%
  filter(n >= 10)  # 篩選共現 >= 10

cat("符合條件的時段×SKU 組合數：", nrow(time_sku_counts), "\n")

# 計算各時段總交易數
period_totals <- data %>%
  count(time_period, name = "period_total")

# 計算各 SKU 總出現次數
sku_totals <- data %>%
  count(SKU, name = "sku_total")

# 總交易數
overall_total <- nrow(data)

# 計算 lift
time_sku_lift <- time_sku_counts %>%
  left_join(period_totals, by = "time_period") %>%
  left_join(sku_totals, by = "SKU") %>%
  mutate(
    # 期望值：如果時段和 SKU 獨立，期望共現次數
    expected = (period_total * sku_total) / overall_total,
    # Lift = 觀察值 / 期望值
    lift = n / expected,
    # Support
    support = n / overall_total
  )

cat("Lift 計算完成\n")

# 統計摘要
cat("\n時段 × SKU Lift 統計：\n")
cat("平均 Lift：", sprintf("%.3f", mean(time_sku_lift$lift)), "\n")
cat("中位數 Lift：", sprintf("%.3f", median(time_sku_lift$lift)), "\n")
cat("Lift > 1 的組合數：", sum(time_sku_lift$lift > 1), "\n")
cat("Lift < 1 的組合數：", sum(time_sku_lift$lift < 1), "\n")

# ============================================================================
# 3. 卡方檢定（每個 SKU）----
# ============================================================================
cat("\n步驟 3：卡方檢定...\n")

# 對每個 SKU 進行卡方檢定，檢驗時段分佈是否顯著偏離期望
sku_list <- unique(time_sku_lift$SKU)

chi_results <- map_dfr(sku_list, function(sku) {
  # 獲取該 SKU 在各時段的實際出現次數
  sku_data <- data %>%
    filter(SKU == !!sku) %>%
    count(time_period)
  
  # 如果該 SKU 總數 < 10，跳過
  if (sum(sku_data$n) < 10) {
    return(tibble(SKU = sku, p_value = NA_real_, test_method = "Skipped"))
  }
  
  # 期望值：基於各時段的整體分佈
  period_props <- period_totals %>%
    mutate(prop = period_total / sum(period_total))
  
  expected_counts <- period_props %>%
    mutate(expected = prop * sum(sku_data$n)) %>%
    select(time_period, expected)
  
  # 合併實際值和期望值
  test_data <- full_join(sku_data, expected_counts, by = "time_period") %>%
    replace_na(list(n = 0))
  
  # 卡方檢定
  if (min(test_data$expected) >= 5 && nrow(test_data) >= 2) {
    chi_test <- tryCatch(
      chisq.test(test_data$n, p = test_data$expected / sum(test_data$expected)),
      error = function(e) NULL
    )
    
    if (!is.null(chi_test)) {
      return(tibble(
        SKU = sku,
        p_value = chi_test$p.value,
        test_method = "Chi-square"
      ))
    }
  }
  
  return(tibble(SKU = sku, p_value = NA_real_, test_method = "Not tested"))
})

# Holm-Bonferroni 校正（只對非 NA 的 p 值進行校正）
valid_p <- chi_results$p_value[!is.na(chi_results$p_value)]
if (length(valid_p) > 0) {
  adjusted_valid <- p.adjust(valid_p, method = "holm")
  chi_results$p_adjusted <- NA_real_
  chi_results$p_adjusted[!is.na(chi_results$p_value)] <- adjusted_valid
} else {
  chi_results$p_adjusted <- NA_real_
}

chi_results <- chi_results %>%
  mutate(
    significance = case_when(
      !is.na(p_adjusted) & p_adjusted < 0.001 ~ "***",
      !is.na(p_adjusted) & p_adjusted < 0.01 ~ "**",
      !is.na(p_adjusted) & p_adjusted < 0.05 ~ "*",
      is.na(p_adjusted) ~ "NA",
      TRUE ~ "ns"
    )
  )

cat("卡方檢定完成\n")
cat("顯著 SKU 數（p < 0.05）：", sum(chi_results$significance %in% c("*", "**", "***"), na.rm = TRUE), "\n")

# ============================================================================
# 4. 儲存結果 ----
# ============================================================================
cat("\n步驟 4：儲存結果...\n")

# 合併 lift 和檢定結果
if (nrow(time_sku_lift) > 0 && nrow(chi_results) > 0) {
  time_product_stats <- time_sku_lift %>%
    left_join(chi_results, by = "SKU") %>%
    select(
      time_period, SKU, n, support, lift,
      p_value, p_adjusted, significance
    ) %>%
    arrange(time_period, desc(lift))
} else {
  # 如果沒有資料，建立空資料框
  time_product_stats <- tibble(
    time_period = character(),
    SKU = character(),
    n = integer(),
    support = numeric(),
    lift = numeric(),
    p_value = numeric(),
    p_adjusted = numeric(),
    significance = character()
  )
}

write_csv(
  time_product_stats,
  file.path(output_dir, "statistics", "time_product_stats.csv")
)

cat("時段產品統計已儲存至：statistics/time_product_stats.csv\n")

# ============================================================================
# 5. 視覺化：熱力圖 ----
# ============================================================================
cat("\n步驟 5：視覺化熱力圖...\n")

# 選擇有顯著差異或 lift 極端的 SKU（最多取 10 個）
top_skus <- time_product_stats %>%
  group_by(SKU) %>%
  summarise(
    max_lift = max(lift),
    min_lift = min(lift),
    lift_range = max_lift - min_lift,
    is_sig = any(significance %in% c("*", "**", "***")),
    .groups = "drop"
  ) %>%
  filter(is_sig | lift_range > 0.5) %>%
  arrange(desc(lift_range)) %>%
  head(10) %>%  # 限制前 10 個
  pull(SKU)

cat("選擇繪製熱力圖的 SKU 數：", length(top_skus), "\n")

if (length(top_skus) > 0) {
  # 建立 SKU 到品項名稱的對應
  sku_to_item <- data %>%
    filter(SKU %in% top_skus) %>%
    select(SKU, Item) %>%
    distinct() %>%
    group_by(SKU) %>%
    slice(1) %>%
    ungroup()
  
  # 篩選資料
  heatmap_data <- time_sku_lift %>%
    filter(SKU %in% top_skus) %>%
    left_join(sku_to_item, by = "SKU") %>%
    select(Item, time_period, lift) %>%
    ungroup() %>%
    # 確保每個 Item-time_period 組合只有一個值
    group_by(Item, time_period) %>%
    summarise(lift = mean(lift, na.rm = TRUE), .groups = "drop")
  
  # 轉為寬格式（使用品項名稱）
  lift_wide <- heatmap_data %>%
    pivot_wider(
      names_from = time_period,
      values_from = lift
    ) %>%
    replace(is.na(.), 1) %>%
    column_to_rownames("Item")
  
  # 確保時段順序正確（檢查哪些時段存在）
  available_periods <- intersect(c("午餐", "下午茶", "晚餐"), colnames(lift_wide))
  if (length(available_periods) > 0) {
    lift_wide <- lift_wide[, available_periods, drop = FALSE]
  }
  
  # 準備顯著性標註矩陣
  sig_data <- chi_results %>%
    filter(SKU %in% top_skus) %>%
    select(SKU, significance)
  
  sig_matrix <- matrix(
    "",
    nrow = nrow(lift_wide),
    ncol = ncol(lift_wide)
  )
  rownames(sig_matrix) <- rownames(lift_wide)
  colnames(sig_matrix) <- colnames(lift_wide)
  
  # 填入顯著性標記（針對整個 SKU 的檢定結果）
  for (i in 1:nrow(sig_matrix)) {
    sku <- rownames(sig_matrix)[i]
    sig_val <- sig_data$significance[sig_data$SKU == sku]
    if (length(sig_val) > 0 && sig_val != "ns" && sig_val != "NA") {
      sig_matrix[i, ] <- sig_val
    }
  }
  
  # 繪製熱力圖
  pdf(
    file.path(output_dir, "charts", "time_product_heatmap.pdf"),
    width = 10,
    height = max(8, nrow(lift_wide) * 0.4)
  )
  
  pheatmap(
    as.matrix(lift_wide),
    color = colorRampPalette(c("#3B4992FF", "white", "#EE0000FF"))(100),
    breaks = seq(0.5, 2, length.out = 101),
    display_numbers = sig_matrix,
    number_color = "black",
    fontsize = 10,
    fontsize_row = 8,
    fontsize_col = 10,
    cluster_rows = TRUE,
    cluster_cols = FALSE,
    main = "時段 × 產品 Lift 熱力圖\n(* p<0.05, ** p<0.01, *** p<0.001)",
    legend_breaks = c(0.5, 1, 1.5, 2),
    legend_labels = c("0.5", "1.0", "1.5", "2.0"),
    border_color = "grey60"
  )
  
  dev.off()
  
  cat("時段產品熱力圖已儲存至：charts/time_product_heatmap.pdf\n")
} else {
  cat("警告：沒有符合條件的 SKU，跳過熱力圖\n")
}

# ============================================================================
# 6. 額外視覺化：時段偏好前 10 名 SKU ----
# ============================================================================
cat("\n步驟 6：生成時段偏好前 10 名圖表...\n")

# 找出每個時段 lift 最高的 SKU
top_by_period <- time_sku_lift %>%
  group_by(time_period) %>%
  arrange(desc(lift)) %>%
  slice_head(n = 10) %>%
  ungroup()

# 繪製條形圖
p_top_period <- ggplot(top_by_period, aes(x = reorder(SKU, lift), y = lift, fill = time_period)) +
  geom_col() +
  coord_flip() +
  facet_wrap(~ time_period, scales = "free_y", ncol = 1) +
  geom_hline(yintercept = 1, linetype = "dashed", color = "red", alpha = 0.7) +
  labs(
    title = "各時段 Lift 前 10 名產品",
    x = "產品 SKU",
    y = "Lift 值",
    caption = "Lift > 1 表示該時段偏好購買該產品"
  ) +
  scale_fill_manual(values = c("午餐" = "#00A087FF", "下午茶" = "#3C5488FF", "晚餐" = "#F39B7FFF")) +
  theme_bw(base_family = "HiraginoSans", base_size = 12) +
  theme(
    text = element_text(family = "HiraginoSans"),
    plot.title = element_text(family = "HiraginoSans", face = "bold", hjust = 0.5),
    legend.position = "none",
    strip.text = element_text(family = "HiraginoSans", face = "bold")
  )

ggsave(
  file.path(output_dir, "charts", "time_period_top10.pdf"),
  plot = p_top_period,
  width = 10,
  height = 12,
  device = cairo_pdf
)

cat("時段偏好前 10 名圖表已儲存至：charts/time_period_top10.pdf\n")

cat("\n=== 時段產品分析完成！===\n")
cat("統計結果已儲存至 statistics/time_product_stats.csv\n")
cat("視覺化圖表已儲存至 charts/ 目錄\n")

