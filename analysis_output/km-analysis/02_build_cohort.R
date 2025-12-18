# ============================================================================
# 02_build_cohort.R
# 建構顧客世代：計算首購日、末購日、存活時間、流失狀態、分組變數
# ============================================================================

# 載入套件 ----
library(tidyverse)
library(lubridate)
library(survival)

# 設定路徑 ----
output_dir <- "/Users/lunhsiangyuan/Desktop/square/km-analysis"
input_file <- file.path(output_dir, "data", "cleaned_data.csv")

# 讀取清理後的資料 ----
cat("正在讀取清理後的資料...\n")
data <- read_csv(input_file, show_col_types = FALSE)

cat("資料筆數：", nrow(data), "\n")

# 觀察終點 ----
observation_end <- max(data$DateTime_NY, na.rm = TRUE)
cat("觀察終點：", as.character(observation_end), "\n")

# 1. 顧客層級資料建構 ----
cat("\n步驟 1：建構顧客層級資料...\n")

# 只處理有 Customer_ID 的記錄
customer_data <- data %>%
  filter(!is.na(Customer_ID), Customer_ID != "")

cat("有 Customer_ID 的交易筆數：", nrow(customer_data), "\n")

# 2. 計算首購日和末購日 ----
cat("\n步驟 2：計算首購日和末購日...\n")

customer_timeline <- customer_data %>%
  group_by(Customer_ID) %>%
  summarise(
    first_purchase_date = min(DateTime_NY, na.rm = TRUE),
    last_purchase_date = max(DateTime_NY, na.rm = TRUE),
    total_transactions = n_distinct(Transaction_ID),
    total_purchases = n(),
    .groups = "drop"
  )

cat("顧客數：", nrow(customer_timeline), "\n")

# 3. 計算存活時間和流失狀態 ----
cat("\n步驟 3：計算存活時間和流失狀態...\n")

cohort <- customer_timeline %>%
  mutate(
    # 存活時間（以天為單位）
    survival_time = as.numeric(difftime(last_purchase_date, first_purchase_date, units = "days")),
    
    # 流失定義：末購日 + 60 天 < 觀察終點
    days_since_last = as.numeric(difftime(observation_end, last_purchase_date, units = "days")),
    
    # status: 1 = 流失（event occurred）, 0 = censored（仍活躍或觀察期內）
    status = ifelse(days_since_last > 60, 1, 0)
  )

cat("流失顧客數：", sum(cohort$status == 1), "\n")
cat("Censored 顧客數：", sum(cohort$status == 0), "\n")
cat("流失率：", sprintf("%.2f%%", 100 * mean(cohort$status)), "\n")

# 4. 建構分組變數 ----
cat("\n步驟 4：建構分組變數...\n")

# 4a. 用餐方式（首購時的 Dining Option）----
cat("  4a. 用餐方式...\n")
first_dining <- customer_data %>%
  group_by(Customer_ID) %>%
  arrange(DateTime_NY) %>%
  slice(1) %>%
  ungroup() %>%
  select(Customer_ID, Dining_Option)

cohort <- cohort %>%
  left_join(first_dining, by = "Customer_ID") %>%
  mutate(
    dining_group = case_when(
      Dining_Option == "For Here" ~ "內用",
      Dining_Option == "To Go" ~ "外帶",
      Dining_Option == "Delivery" ~ "外送",
      is.na(Dining_Option) | Dining_Option == "" ~ "Unknown",
      TRUE ~ "Unknown"
    )
  )

cat("    用餐方式分佈：\n")
print(table(cohort$dining_group))

# 4b. 首購是否 Combo ----
cat("  4b. 首購是否 Combo...\n")
first_purchase_items <- customer_data %>%
  group_by(Customer_ID) %>%
  arrange(DateTime_NY) %>%
  slice(1) %>%
  ungroup() %>%
  select(Customer_ID, Category)

cohort <- cohort %>%
  left_join(first_purchase_items, by = "Customer_ID") %>%
  mutate(
    first_purchase_combo = ifelse(
      str_detect(Category, regex("combo", ignore_case = TRUE)),
      "Yes",
      "No"
    )
  )

cat("    首購 Combo 分佈：\n")
print(table(cohort$first_purchase_combo))

# 4c. 是否曾買過 Combo ----
cat("  4c. 是否曾買過 Combo...\n")
ever_combo <- customer_data %>%
  group_by(Customer_ID) %>%
  summarise(
    has_combo = any(str_detect(Category, regex("combo", ignore_case = TRUE))),
    .groups = "drop"
  )

cohort <- cohort %>%
  left_join(ever_combo, by = "Customer_ID") %>%
  mutate(
    ever_bought_combo = ifelse(has_combo, "Yes", "No")
  )

cat("    曾買過 Combo 分佈：\n")
print(table(cohort$ever_bought_combo))

# 4d. 商品多樣性（Category 層級）----
cat("  4d. 商品多樣性（Category）...\n")
category_diversity <- customer_data %>%
  group_by(Customer_ID) %>%
  summarise(
    unique_categories = n_distinct(Category),
    .groups = "drop"
  )

cohort <- cohort %>%
  left_join(category_diversity, by = "Customer_ID") %>%
  mutate(
    diversity_category = case_when(
      unique_categories == 1 ~ "1種",
      unique_categories >= 2 & unique_categories <= 3 ~ "2-3種",
      unique_categories >= 4 ~ "4種以上",
      TRUE ~ "Unknown"
    ),
    diversity_category = factor(diversity_category, levels = c("1種", "2-3種", "4種以上", "Unknown"))
  )

cat("    商品多樣性（Category）分佈：\n")
print(table(cohort$diversity_category))

# 4e. 商品多樣性（Item 層級）----
cat("  4e. 商品多樣性（Item）...\n")
item_diversity <- customer_data %>%
  group_by(Customer_ID) %>%
  summarise(
    unique_items = n_distinct(Item),
    .groups = "drop"
  )

cohort <- cohort %>%
  left_join(item_diversity, by = "Customer_ID") %>%
  mutate(
    diversity_item = case_when(
      unique_items == 1 ~ "1種",
      unique_items >= 2 & unique_items <= 3 ~ "2-3種",
      unique_items >= 4 ~ "4種以上",
      TRUE ~ "Unknown"
    ),
    diversity_item = factor(diversity_item, levels = c("1種", "2-3種", "4種以上", "Unknown"))
  )

cat("    商品多樣性（Item）分佈：\n")
print(table(cohort$diversity_item))

# 5. 儲存顧客世代資料 ----
output_file <- file.path(output_dir, "data", "customer_cohort.csv")
cat("\n正在儲存顧客世代資料...\n")

# 選擇需要的欄位
cohort_output <- cohort %>%
  select(
    Customer_ID,
    first_purchase_date,
    last_purchase_date,
    survival_time,
    status,
    total_transactions,
    total_purchases,
    dining_group,
    first_purchase_combo,
    ever_bought_combo,
    diversity_category,
    unique_categories,
    diversity_item,
    unique_items
  )

write_csv(cohort_output, output_file)

cat("顧客世代資料已儲存至：", output_file, "\n")
cat("顧客總數：", nrow(cohort_output), "\n")

# 6. 資料摘要 ----
cat("\n=== 顧客世代資料摘要 ===\n")
cat("顧客總數：", nrow(cohort), "\n")
cat("流失顧客：", sum(cohort$status == 1), 
    sprintf("（%.2f%%）", 100 * mean(cohort$status)), "\n")
cat("Censored 顧客：", sum(cohort$status == 0), 
    sprintf("（%.2f%%）", 100 * (1 - mean(cohort$status))), "\n")

cat("\n平均存活時間：", sprintf("%.2f", mean(cohort$survival_time)), "天\n")
cat("中位數存活時間：", sprintf("%.2f", median(cohort$survival_time)), "天\n")

cat("\n平均交易次數：", sprintf("%.2f", mean(cohort$total_transactions)), "\n")
cat("平均購買件數：", sprintf("%.2f", mean(cohort$total_purchases)), "\n")

cat("\n顧客世代建構完成！\n")



