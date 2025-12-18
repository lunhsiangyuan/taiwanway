# ============================================================================
# install_packages.R
# 安裝所有必要的 R 套件
# ============================================================================

cat("======================================================================\n")
cat("  安裝 Kaplan-Meier 存活分析所需的 R 套件\n")
cat("======================================================================\n\n")

# 檢查 R 版本 ----
r_version <- as.numeric(paste0(R.version$major, ".", R.version$minor))
if (r_version < 4.0) {
  warning("建議使用 R 版本 4.0 或更新版本。當前版本：", R.version.string)
}

# 必要套件清單 ----
packages <- c(
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
)

cat("將安裝以下套件：\n")
cat(paste("-", packages, collapse = "\n"), "\n\n")

# 檢查並安裝套件 ----
installed <- installed.packages()[, "Package"]
to_install <- packages[!packages %in% installed]

if (length(to_install) > 0) {
  cat("需要安裝的套件：", paste(to_install, collapse = ", "), "\n\n")
  
  for (pkg in to_install) {
    cat("正在安裝", pkg, "...\n")
    tryCatch({
      install.packages(pkg, dependencies = TRUE, repos = "https://cloud.r-project.org/")
      cat("✓", pkg, "安裝成功\n")
    }, error = function(e) {
      cat("✗", pkg, "安裝失敗：", e$message, "\n")
    })
  }
} else {
  cat("所有套件已安裝完成！\n")
}

# 載入測試 ----
cat("\n正在測試套件載入...\n")

success_count <- 0
fail_count <- 0

for (pkg in packages) {
  result <- tryCatch({
    library(pkg, character.only = TRUE)
    cat("✓", pkg, "\n")
    success_count <- success_count + 1
    TRUE
  }, error = function(e) {
    cat("✗", pkg, "- 載入失敗：", e$message, "\n")
    fail_count <- fail_count + 1
    FALSE
  })
}

# 測試中文字型 ----
cat("\n正在測試中文字型...\n")

tryCatch({
  library(showtext)
  showtext_auto()
  
  font_paths <- c(
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
  )
  
  font_found <- FALSE
  for (fp in font_paths) {
    if (file.exists(fp)) {
      cat("✓ 找到中文字型：", fp, "\n")
      font_found <- TRUE
      break
    }
  }
  
  if (!font_found) {
    cat("✗ 警告：未找到中文字型，圖表可能無法正確顯示中文\n")
  }
}, error = function(e) {
  cat("✗ 字型測試失敗：", e$message, "\n")
})

# 摘要 ----
cat("\n======================================================================\n")
cat("  安裝摘要\n")
cat("======================================================================\n")
cat("成功載入：", success_count, "個套件\n")
cat("載入失敗：", fail_count, "個套件\n")

if (fail_count == 0) {
  cat("\n✓ 所有套件已就緒！可以執行 run_all.R 開始分析。\n")
} else {
  cat("\n✗ 部分套件安裝或載入失敗，請檢查錯誤訊息並手動安裝。\n")
}

cat("======================================================================\n")



