# ============================================================================
# 04_product_association.R
# 產品關聯分析：計算 support、confidence、lift，統計檢定，視覺化
# ============================================================================

# 載入套件 ----
library(tidyverse)
library(pheatmap)
library(showtext)
library(gridExtra)
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
# 1. 建構購物籃資料 ----
# ============================================================================
cat("\n步驟 1：建構購物籃資料...\n")

# 以 Transaction_ID 為單位，聚合 SKU
transactions_list <- data %>%
  filter(!is.na(SKU), SKU != "") %>%
  group_by(Transaction_ID) %>%
  summarise(
    items = list(unique(SKU)),
    n_items = n_distinct(SKU),
    .groups = "drop"
  )

cat("交易籃數：", nrow(transactions_list), "\n")
cat("平均每筆交易 SKU 數：", sprintf("%.2f", mean(transactions_list$n_items)), "\n")

# ============================================================================
# 2. 手動計算 SKU 配對統計 ----
# ============================================================================
cat("\n步驟 2：計算 SKU 配對統計...\n")

# 獲取所有 SKU
all_skus <- unique(data$SKU[!is.na(data$SKU) & data$SKU != ""])
cat("不重複 SKU 數：", length(all_skus), "\n")

# 計算每個 SKU 出現的交易數
sku_counts <- data %>%
  filter(!is.na(SKU), SKU != "") %>%
  group_by(Transaction_ID, SKU) %>%
  summarise(.groups = "drop") %>%
  count(SKU, name = "sku_count")

  # 計算 SKU 配對的共現次數
cat("計算 SKU 配對共現...\n")

sku_pairs <- data %>%
  filter(!is.na(SKU), SKU != "") %>%
  select(Transaction_ID, SKU) %>%
  distinct() %>%
  inner_join(., ., by = "Transaction_ID", suffix = c("_A", "_B"), relationship = "many-to-many") %>%
  filter(SKU_A < SKU_B) %>%  # 避免重複配對
  count(SKU_A, SKU_B, name = "co_occur") %>%
  filter(co_occur >= 10)  # 篩選共現 >= 10

cat("符合條件的 SKU 配對數：", nrow(sku_pairs), "\n")

# 計算 support, confidence, lift
total_transactions <- n_distinct(data$Transaction_ID)

association_stats <- sku_pairs %>%
  left_join(sku_counts %>% rename(SKU_A = SKU, count_A = sku_count), by = "SKU_A") %>%
  left_join(sku_counts %>% rename(SKU_B = SKU, count_B = sku_count), by = "SKU_B") %>%
  mutate(
    support = co_occur / total_transactions,
    confidence_A_to_B = co_occur / count_A,  # P(B|A)
    confidence_B_to_A = co_occur / count_B,  # P(A|B)
    lift = (co_occur / total_transactions) / ((count_A / total_transactions) * (count_B / total_transactions))
  ) %>%
  arrange(desc(lift))

# 取 Top 30
association_top30 <- association_stats %>%
  head(30)

cat("Top 30 lift 配對已計算\n")

# ============================================================================
# 3. 統計檢定（卡方或 Fisher's exact test）----
# ============================================================================
cat("\n步驟 3：統計檢定...\n")

# 對每個配對進行檢定
association_with_test <- association_top30 %>%
  rowwise() %>%
  mutate(
    # 建立 2x2 列聯表
    # 有 A 有 B, 有 A 無 B, 無 A 有 B, 無 A 無 B
    n_AB = co_occur,
    n_A_notB = count_A - co_occur,
    n_notA_B = count_B - co_occur,
    n_notA_notB = total_transactions - count_A - count_B + co_occur,
    
    # 檢定選擇
    expected_min = min(
      n_AB * (n_AB + n_A_notB) / total_transactions,
      n_AB * (n_AB + n_notA_B) / total_transactions
    ),
    
    # 執行檢定
    p_value = if (expected_min >= 5) {
      # 卡方檢定
      contingency <- matrix(c(n_AB, n_A_notB, n_notA_B, n_notA_notB), nrow = 2)
      tryCatch(chisq.test(contingency)$p.value, error = function(e) NA_real_)
    } else {
      # Fisher's exact test
      contingency <- matrix(c(n_AB, n_A_notB, n_notA_B, n_notA_notB), nrow = 2)
      tryCatch(fisher.test(contingency)$p.value, error = function(e) NA_real_)
    },
    
    test_method = ifelse(expected_min >= 5, "Chi-square", "Fisher")
  ) %>%
  ungroup() %>%
  mutate(
    # Holm-Bonferroni 校正
    p_adjusted = p.adjust(p_value, method = "holm"),
    significance = case_when(
      p_adjusted < 0.001 ~ "***",
      p_adjusted < 0.01 ~ "**",
      p_adjusted < 0.05 ~ "*",
      TRUE ~ "ns"
    )
  )

cat("統計檢定完成\n")

# ============================================================================
# 4. 儲存結果 ----
# ============================================================================
cat("\n步驟 4：儲存結果...\n")

# 整理輸出欄位
association_output <- association_with_test %>%
  select(
    SKU_A, SKU_B,
    co_occur,
    confidence_A_to_B, confidence_B_to_A,
    lift,
    p_value, p_adjusted,
    significance,
    test_method
  ) %>%
  mutate(
    confidence_A_to_B = sprintf("%.2f%%", confidence_A_to_B * 100),
    confidence_B_to_A = sprintf("%.2f%%", confidence_B_to_A * 100),
    lift = round(lift, 3)
  )

write_csv(
  association_output,
  file.path(output_dir, "statistics", "product_association.csv")
)

cat("產品關聯統計已儲存至：statistics/product_association.csv\n")

# ============================================================================
# 5. 視覺化：關聯表格 ----
# ============================================================================
cat("\n步驟 5：視覺化關聯表格...\n")

# 準備表格資料（取前 20 條以便顯示）
table_data <- association_with_test %>%
  head(20) %>%
  mutate(
    `A→B%` = sprintf("%.1f%%", confidence_A_to_B * 100),
    `B→A%` = sprintf("%.1f%%", confidence_B_to_A * 100),
    Lift = sprintf("%.2f", lift),
    `p值` = ifelse(p_adjusted < 0.001, "<0.001", sprintf("%.3f", p_adjusted))
  ) %>%
  select(SKU_A, SKU_B, co_occur, `A→B%`, `B→A%`, Lift, `p值`, significance)

# 使用 ggpubr::ggtexttable 生成表格
table_plot <- ggtexttable(
  table_data,
  rows = NULL,
  theme = ttheme(
    base_style = "default",
    base_size = 8,
    padding = unit(c(2, 2), "mm")
  )
)

ggsave(
  file.path(output_dir, "charts", "product_association_table.pdf"),
  plot = table_plot,
  width = 12,
  height = 10,
  device = cairo_pdf
)

cat("產品關聯表格已儲存至：charts/product_association_table.pdf\n")

# ============================================================================
# 6. 視覺化：熱力圖 ----
# ============================================================================
cat("\n步驟 6：視覺化熱力圖...\n")

# 選擇 lift > 1 的配對，限制為前 10 個
heatmap_data <- association_with_test %>%
  filter(lift > 1) %>%
  head(10)  # 限制前 10 個配對

if (nrow(heatmap_data) > 0) {
  # 獲取所有涉及的 SKU
  skus_in_heatmap <- unique(c(heatmap_data$SKU_A, heatmap_data$SKU_B))
  
  # 建立 SKU 到品項名稱的對應
  sku_to_item <- data %>%
    filter(SKU %in% skus_in_heatmap) %>%
    select(SKU, Item) %>%
    distinct() %>%
    group_by(SKU) %>%
    slice(1) %>%
    ungroup()
  
  # 使用品項名稱作為標籤
  item_names <- sku_to_item$Item
  names(item_names) <- sku_to_item$SKU
  
  # 建立 lift 矩陣（使用品項名稱）
  lift_matrix <- matrix(1, nrow = length(skus_in_heatmap), ncol = length(skus_in_heatmap))
  rownames(lift_matrix) <- item_names[skus_in_heatmap]
  colnames(lift_matrix) <- item_names[skus_in_heatmap]
  
  # 建立顯著性矩陣（使用品項名稱）
  sig_matrix <- matrix("", nrow = length(skus_in_heatmap), ncol = length(skus_in_heatmap))
  rownames(sig_matrix) <- item_names[skus_in_heatmap]
  colnames(sig_matrix) <- item_names[skus_in_heatmap]
  
  # 填入數值
  for (i in 1:nrow(heatmap_data)) {
    sku_a <- heatmap_data$SKU_A[i]
    sku_b <- heatmap_data$SKU_B[i]
    item_a <- item_names[sku_a]
    item_b <- item_names[sku_b]
    lift_val <- heatmap_data$lift[i]
    sig_val <- heatmap_data$significance[i]
    
    # 對稱填入
    lift_matrix[item_a, item_b] <- lift_val
    lift_matrix[item_b, item_a] <- lift_val
    
    sig_matrix[item_a, item_b] <- ifelse(sig_val != "ns", sig_val, "")
    sig_matrix[item_b, item_a] <- ifelse(sig_val != "ns", sig_val, "")
  }
  
  # 繪製熱力圖
  pdf(
    file.path(output_dir, "charts", "product_heatmap.pdf"),
    width = 14,
    height = 12
  )
  
  pheatmap(
    lift_matrix,
    color = colorRampPalette(c("blue", "white", "red"))(100),
    display_numbers = sig_matrix,
    number_color = "black",
    fontsize = 10,
    fontsize_row = 8,
    fontsize_col = 8,
    cluster_rows = TRUE,
    cluster_cols = TRUE,
    main = "產品關聯 Lift 熱力圖\n(* p<0.05, ** p<0.01, *** p<0.001)",
    border_color = "grey60"
  )
  
  dev.off()
  
  cat("產品關聯熱力圖已儲存至：charts/product_heatmap.pdf\n")
} else {
  cat("警告：沒有 lift > 1 的配對，跳過熱力圖\n")
}

cat("\n=== 產品關聯分析完成！===\n")
cat("統計結果已儲存至 statistics/product_association.csv\n")
cat("視覺化圖表已儲存至 charts/ 目錄\n")

