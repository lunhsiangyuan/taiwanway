# ============================================================================
# 01_data_preprocessing.R
# 資料前處理：時間合併、平移、時區轉換、清理
# ============================================================================

# 載入套件 ----
library(tidyverse)
library(lubridate)
library(showtext)

# 設定中文字型 ----
showtext_auto()
font_add("HiraginoSans", "/System/Library/Fonts/Hiragino Sans GB.ttc")
theme_set(theme_bw(base_size = 12, base_family = "HiraginoSans"))

# 設定路徑 ----
input_file <- "/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv"
output_dir <- "/Users/lunhsiangyuan/Desktop/square/km-analysis"
dir.create(file.path(output_dir, "data"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(output_dir, "charts"), showWarnings = FALSE, recursive = TRUE)

# 讀取原始資料 ----
cat("正在讀取原始資料...\n")
raw_data <- read_csv(input_file, show_col_types = FALSE)

cat("原始資料筆數：", nrow(raw_data), "\n")
cat("原始資料欄位：", ncol(raw_data), "\n")

# 1. 合併 Date + Time 為 DateTime ----
cat("\n步驟 1：合併日期與時間...\n")

# 處理 Date 和 Time 欄位
data <- raw_data %>%
  mutate(
    # 合併 Date 和 Time，假設為 Taipei 時區 (Asia/Taipei)
    DateTime_Taipei = ymd_hms(paste(Date, Time), tz = "Asia/Taipei")
  )

# 檢查是否有解析失敗的記錄
failed_parse <- sum(is.na(data$DateTime_Taipei))
cat("解析失敗的記錄數：", failed_parse, "\n")

# 2. 時間平移 +12 小時 ----
cat("\n步驟 2：時間平移 +12 小時...\n")

data <- data %>%
  mutate(
    DateTime_Shifted = DateTime_Taipei + hours(12)
  )

# 3. 轉換為紐約時區（考慮 DST）----
cat("\n步驟 3：轉換為紐約時區...\n")

# 2025 年美國冬令時間開始：11月2日
# EDT (UTC-4): 2025-03-09 02:00 至 2025-11-02 02:00
# EST (UTC-5): 2025-11-02 02:00 之後

data <- data %>%
  mutate(
    # 使用 lubridate 的 with_tz 自動處理 DST
    DateTime_NY = with_tz(DateTime_Shifted, tzone = "America/New_York")
  )

# 4. 資料清理 ----
cat("\n步驟 4：資料清理...\n")

# 4a. 只保留 Event Type = "Payment"
cat("移除 Event Type ≠ Payment 的記錄...\n")
before_event <- nrow(data)
data <- data %>%
  filter(`Event Type` == "Payment")
after_event <- nrow(data)
cat("  移除了", before_event - after_event, "筆記錄\n")

# 4b. 移除 Price Point Name 為空（Custom Amount）
cat("移除 Custom Amount（Price Point Name 為空）...\n")
before_custom <- nrow(data)
data <- data %>%
  filter(!is.na(`Price Point Name`), `Price Point Name` != "")
after_custom <- nrow(data)
cat("  移除了", before_custom - after_custom, "筆記錄\n")

# 4c. 移除 SKU 缺失的記錄
cat("移除 SKU 缺失的記錄...\n")
before_sku <- nrow(data)
data <- data %>%
  filter(!is.na(SKU), SKU != "")
after_sku <- nrow(data)
cat("  移除了", before_sku - after_sku, "筆記錄\n")

# 5. 觀察終點 ----
observation_end <- max(data$DateTime_NY, na.rm = TRUE)
cat("\n觀察終點：", as.character(observation_end), "\n")

# 6. 提取時間相關欄位 ----
data <- data %>%
  mutate(
    Hour = hour(DateTime_NY),
    Date_NY = as.Date(DateTime_NY),
    YearMonth = floor_date(DateTime_NY, "month")
  )

# 7. 整理欄位名稱（移除空格）----
data <- data %>%
  rename(
    Event_Type = `Event Type`,
    Price_Point_Name = `Price Point Name`,
    Gross_Sales = `Gross Sales`,
    Net_Sales = `Net Sales`,
    Transaction_ID = `Transaction ID`,
    Payment_ID = `Payment ID`,
    Device_Name = `Device Name`,
    Dining_Option = `Dining Option`,
    Customer_ID = `Customer ID`,
    Customer_Name = `Customer Name`,
    Customer_Reference_ID = `Customer Reference ID`,
    Itemization_Type = `Itemization Type`,
    Fulfillment_Note = `Fulfillment Note`,
    Card_Brand = `Card Brand`,
    PAN_Suffix = `PAN Suffix`,
    Modifiers_Applied = `Modifiers Applied`,
    Time_Zone = `Time Zone`
  )

# 8. 儲存清理後的資料 ----
output_file <- file.path(output_dir, "data", "cleaned_data.csv")
cat("\n正在儲存清理後的資料...\n")
write_csv(data, output_file)

cat("清理後的資料已儲存至：", output_file, "\n")
cat("最終資料筆數：", nrow(data), "\n")

# 9. 資料摘要 ----
cat("\n=== 資料摘要 ===\n")
cat("日期範圍（紐約時間）：", 
    as.character(min(data$Date_NY)), "至", 
    as.character(max(data$Date_NY)), "\n")
cat("總交易筆數：", nrow(data), "\n")
cat("不重複交易 ID 數：", n_distinct(data$Transaction_ID), "\n")
cat("不重複顧客數：", n_distinct(data$Customer_ID[data$Customer_ID != ""]), "\n")
cat("不重複 SKU 數：", n_distinct(data$SKU), "\n")

# 10. 測試中文字型顯示 ----
cat("\n正在測試中文字型顯示...\n")

test_data <- data.frame(
  x = 1:3,
  label = c("內用", "外帶", "外送")
)

p <- ggplot(test_data, aes(x = x, y = x, label = label)) +
  geom_text(family = "HiraginoSans", size = 10) +
  labs(
    title = "中文字型測試",
    x = "X 軸",
    y = "Y 軸"
  ) +
  theme_bw(base_family = "HiraginoSans") +
  theme(
    text = element_text(family = "HiraginoSans"),
    plot.title = element_text(family = "HiraginoSans", size = 16, face = "bold"),
    axis.title = element_text(family = "HiraginoSans", size = 12)
  )

ggsave(
  file.path(output_dir, "charts", "font_test.pdf"),
  plot = p,
  width = 6,
  height = 4,
  device = cairo_pdf
)

cat("中文字型測試圖已儲存至：km-analysis/charts/font_test.pdf\n")

cat("\n資料前處理完成！\n")

