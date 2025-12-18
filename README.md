# Taiwanway 店鋪數據分析系統

這是一個完整的 Taiwanway 店鋪數據分析專案，用於從 Square API 下載支付數據、分析店鋪營運表現、產生可視化報表。系統涵蓋資料下載、數據處理、流量分析、金流統計、成本結構分析等多個面向。

## 功能特色

### 🔄 數據下載與管理
- 📥 **Square API 整合**：自動從 Square API 下載 payments 數據
- 🔄 **批次下載**：支援分頁下載（cursor-based pagination）
- 🗂️ **數據合併與去重**：自動合併多個來源並去除重複記錄
- 💾 **多格式匯出**：支援 JSON、CSV、HTML 格式

### 📊 流量與金流分析
- 📊 **每小時流量分析**：統計每小時的來客數
- 💰 **每小時金流分析**：統計每小時的營業額
- 📅 **營業日過濾**：自動過濾只保留營業日（週一、週二、週五、週六）
- 🌍 **時區轉換**：自動將 UTC 時間轉換為紐約時區（America/New_York），處理夏令時（DST）
- 📈 **視覺化圖表**：使用 seaborn、matplotlib 和 scienceplot 繪製專業圖表
- 📁 **多格式輸出**：支援 JSON 和 CSV 格式輸出

### 💵 成本與利潤分析
- 💼 **成本結構分析**：計算固定成本、變動成本、員工成本
- 📊 **人力排班分析**：分析不同時段的人力配置
- 📈 **利潤趨勢追蹤**：追蹤月度利潤變化
- ⚖️ **損益平衡分析**：計算損益平衡點

### 🤖 智能代理系統（新功能！）
- 🎯 **多代理架構**：Orchestrator-Subagent 設計模式
- 🔍 **銷售分析代理**：自動分析銷售趨勢、高峰時段、成長率
- 👥 **客戶行為代理**：客戶分群、用餐偏好、付款方式分析
- 💰 **財務分析代理**：營收指標、交易統計、AOV 趨勢
- 📊 **報告生成代理**：自動生成 JSON、Markdown、CSV 報告
- ⚡ **快速執行**：分析 9,000+ 筆資料僅需 0.16 秒
- 🔧 **高度可擴展**：模組化設計，易於新增自定義代理

## 專案結構

```
square/
├── agents/                           # 智能代理系統（新！）
│   ├── base_agent.py                 # 基礎代理類別
│   ├── orchestrator.py              # 主協調器
│   ├── data_agent.py                # 資料代理
│   ├── sales_analysis_agent.py      # 銷售分析代理
│   ├── customer_behavior_agent.py   # 客戶行為代理
│   ├── financial_agent.py           # 財務分析代理
│   ├── report_agent.py              # 報告生成代理
│   ├── config.yaml                  # 配置檔案
│   ├── README.md                    # 代理系統文檔
│   ├── QUICKSTART.md                # 快速入門指南
│   ├── ARCHITECTURE.md              # 架構文檔
│   └── output/                      # 分析結果輸出
│
├── scripts/                          # 腳本目錄
│   ├── analysis/                     # 分析腳本
│   │   ├── analyze_hourly_traffic.py           # 每小時流量與金流分析
│   │   ├── analyze_weekday_revenue.py          # 週間日收入分析
│   │   ├── calculate_total_revenue.py          # 計算總營收和總來客數
│   │   ├── create_hourly_revenue_heatmap.py    # 產生營業時間熱力圖
│   │   ├── analyze_cost_structure.py           # 成本結構分析
│   │   └── generate_business_insights_report.py # 商業洞察報告
│   │
│   ├── tools/                        # 工具腳本
│   │   ├── check_all_items.py                  # 檢查所有品項
│   │   ├── check_combo_items.py                # 檢查 combo 品項
│   │   ├── compare_with_square_api.py          # 與 Square API 比對
│   │   ├── generate_catalog_md.py              # 生成目錄 Markdown
│   │   └── list_catalog_items.py               # 查詢 Square 目錄品項
│   │
│   ├── download_all_payments_mcp.py  # 合併 MCP 下載的數據
│   ├── convert_mcp_json_to_csv.py    # JSON 轉 CSV
│   ├── generate_html_report.py       # 生成 HTML 報告
│   ├── generate_monthly_report.py    # 生成每月統計報告
│   ├── generate_data_report.py       # 生成數據檢查報告
│   ├── show_status.py                # 顯示下載狀態
│   ├── download_all_remaining.py     # 檢查剩餘 cursor
│   ├── analyze_november_revenue.py   # 11月營收分析（紐約時間）
│   ├── analyze_fall_revenue.py       # 9-11月秋季營收比較分析
│   └── generate_pdf_report.py        # 生成秋季營收 PDF 報告
│
├── data/                             # 資料目錄
│   ├── all_payments/                 # 合併後的所有支付數據
│   │   ├── all_payments.json         # 合併的 JSON 數據（10.36 MB）
│   │   ├── all_payments.csv          # 轉換後的 CSV 數據（1.32 MB）
│   │   ├── all_payments_report.html  # HTML 報告
│   │   └── all_payments_monthly_report.csv # 每月統計報告
│   └── 2025_08_11/                   # 按日期分類的資料
│       └── taiwanway_payments.csv    # 歷史 CSV 資料
│
├── analysis_output/                  # 分析結果輸出目錄
│   ├── data/                         # 數據文件
│   │   ├── hourly/                   # 每小時分析數據
│   │   │   ├── hourly_analysis_2025_MM.json  # JSON 格式分析結果
│   │   │   └── hourly_analysis_2025_MM.csv   # CSV 格式分析結果
│   │   └── weekday/                  # 週間日分析數據
│   │       ├── weekday_revenue_by_month.json # JSON 格式週間日收入
│   │       └── weekday_revenue_by_month.csv  # CSV 格式週間日收入
│   │
│   ├── charts/                       # 圖表文件
│   │   ├── hourly/                   # 每小時相關圖表
│   │   │   ├── hourly_customers_by_month.png        # 每小時來客數折線圖
│   │   │   ├── hourly_revenue_by_month.png          # 每小時金流折線圖
│   │   │   ├── hourly_customers_comparison.png      # 來客數跨月比較
│   │   │   ├── hourly_revenue_comparison.png        # 金流跨月比較
│   │   │   ├── hourly_customers_bar_by_month.png    # 每小時來客數長條圖
│   │   │   ├── hourly_revenue_bar_by_month.png      # 每小時金流長條圖
│   │   │   ├── hourly_customers_bar_comparison.png  # 來客數分組長條圖
│   │   │   ├── hourly_revenue_bar_comparison.png    # 金流分組長條圖
│   │   │   └── hourly_revenue_heatmap_by_month.png  # 每小時金流熱力圖
│   │   ├── weekday/                  # 週間日相關圖表
│   │   │   ├── weekday_revenue_by_month.png         # 週間日收入圖表
│   │   │   ├── weekday_revenue_heatmap.png          # 週間日收入熱力圖
│   │   │   └── weekday_revenue_trend.png            # 週間日收入趨勢圖
│   │   └── other/                    # 其他圖表
│   │       └── business_days_distribution.png       # 營業日分佈圖
│   │
│   └── cost_analysis/                # 成本分析輸出
│       ├── data/                     # 成本數據
│       │   ├── cost_structure_analysis.json         # 成本結構 JSON
│       │   ├── cost_structure_analysis.csv          # 成本結構 CSV
│       │   └── labor_schedule.json                  # 人力排班數據
│       ├── charts/                   # 成本分析圖表
│       │   ├── cost_structure_chart.png             # 成本結構圖
│       │   ├── labor_schedule_chart.png             # 人力排班圖
│       │   ├── profit_trend_chart.png               # 利潤趨勢圖
│       │   ├── cost_pie_chart.png                   # 成本圓餅圖
│       │   └── break_even_analysis.png              # 損益平衡分析圖
│       ├── reports/                  # 報告文件
│       │   ├── cost_analysis_tables.md              # 成本分析表格
│       │   └── cost_analysis_summary.txt            # 成本分析摘要
│       └── README.md                 # 成本分析說明
│
│   └── break_even_q4/               # Q4 2025 損益平衡分析（新！）
│       ├── README.md                # 分析說明文件
│       ├── break_even_report.md     # 完整分析報告
│       ├── data/
│       │   └── monthly_stats.csv    # 月度統計數據
│       └── charts/
│           ├── break_even_days.png          # 三種日營收情境損益平衡天數
│           ├── sensitivity_3d_heatmap.png   # 三維敏感度熱力圖
│           ├── labor_sensitivity_table.png  # 人力成本敏感度表
│           └── ...                          # 其他圖表
│
├── documents/                        # 文件目錄
│   └── catalog.md                    # 商品目錄
│
├── README.md                         # 專案說明（本文件）
├── DATA_REPORT.md                    # 數據檢查報告
└── plan.md                           # 下載計劃文件
```

## 安裝需求

### Python 套件

```bash
pip install pandas matplotlib seaborn scienceplots pytz
```

### 系統需求

- Python 3.7+
- macOS（已內建中文字體）
- 或 Windows/Linux（需安裝中文字體）

## 使用方法

### 1. 資料下載與合併

#### 下載 Square API 數據
使用 MCP Square 工具下載 payments 數據（需要 Square API 訪問權限）：

```bash
# 檢查下載狀態
python3 scripts/show_status.py

# 檢查剩餘待下載的 cursor
python3 scripts/download_all_remaining.py
```

#### 合併與轉換數據
```bash
# 合併所有 MCP 下載的數據
python3 scripts/download_all_payments_mcp.py

# 轉換 JSON 為 CSV
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json

# 生成 HTML 報告
python3 scripts/generate_html_report.py data/all_payments/all_payments.csv

# 生成每月統計報告
python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv

# 生成完整的數據檢查報告
python3 scripts/generate_data_report.py
```

### 2. 流量與金流分析

從專案根目錄執行：

```bash
# 每小時流量與金流分析（主要分析）
python3 scripts/analysis/analyze_hourly_traffic.py

# 週間日收入分析
python3 scripts/analysis/analyze_weekday_revenue.py

# 計算總營收和總來客數
python3 scripts/analysis/calculate_total_revenue.py

# 產生營業時間熱力圖
python3 scripts/analysis/create_hourly_revenue_heatmap.py
```

### 3. 成本與利潤分析

```bash
# 成本結構分析
python3 scripts/analysis/analyze_cost_structure.py

# 生成商業洞察報告
python3 scripts/analysis/generate_business_insights_report.py
```

### 4. 智能代理系統（新功能！）

使用 AI 代理系統進行自動化分析：

```bash
# 完整分析（所有代理）
python3 agents/orchestrator.py \
  --task full_analysis \
  --data data/items-2025-01-01-2025-11-16.csv

# 銷售分析
python3 agents/orchestrator.py \
  --task sales_analysis \
  --data data/items-2025-01-01-2025-11-16.csv

# 客戶行為分析
python3 agents/orchestrator.py \
  --task customer_analysis \
  --data data/items-2025-01-01-2025-11-16.csv

# 財務指標分析
python3 agents/orchestrator.py \
  --task financial_analysis \
  --data data/items-2025-01-01-2025-11-16.csv

# 指定日期範圍
python3 agents/orchestrator.py \
  --task full_analysis \
  --data data/items-2025-01-01-2025-11-16.csv \
  --start-date 2025-09-01 \
  --end-date 2025-09-30

# 運行測試
python3 agents/test_agents.py

# 查看使用範例
./agents/examples.sh
```

**輸出位置**：
- JSON 報告：`agents/output/reports/*.json`
- Markdown 摘要：`agents/output/reports/*.md`
- CSV 數據：`agents/output/data/*.csv`
- 完整結果：`agents/output/results/*.json`

**詳細文檔**：
- [agents/README.md](agents/README.md) - 系統概覽
- [agents/QUICKSTART.md](agents/QUICKSTART.md) - 快速入門
- [agents/ARCHITECTURE.md](agents/ARCHITECTURE.md) - 架構設計
- [agents/SUMMARY.md](agents/SUMMARY.md) - 功能總覽

### 5. 秋季營收分析 (Q4 2025)

針對 2025 年 9月、10月、11月 的特別分析：

```bash
# 11月單月營收分析 (紐約時間)
python3 scripts/analyze_november_revenue.py

# 9-11月秋季營收比較 (含中位數分析)
python3 scripts/analyze_fall_revenue.py

# 生成 PDF 報告
python3 scripts/generate_pdf_report.py

# 損益平衡分析
python3 scripts/analysis/analyze_break_even_q4.py
```

#### 損益平衡分析功能

`analyze_break_even_q4.py` 腳本提供完整的多維度損益平衡分析：

**成本參數設定**：
- 固定成本：$3,800/月（房租 $3,100 + 水電 $700）
- 人力成本：$100 / $160 / $200 / $250/天（四種情境分析）
- 食材成本率：30% / 35% / 40%（三種情境分析）
- NYC 銷售稅：8.875%

**日營收情境（三種）**：
- 淡季：$640（11月實際日均）
- 平均：$753（Q4 平均）
- 旺季：$820（9月實際日均）

**營收計算方式**：
- 數據來源：Payments CSV (`payments_2025_XX.csv`)
- 篩選條件：僅計算 `status == 'COMPLETED'` 的交易
- Net Sales 計算：`amount / (1 + 0.08875)` - 從含稅金額轉換為稅前淨銷售額
- 驗證：計算結果與 Square Summary Report 誤差 < 1%

**分析功能**：
1. 計算各月實際營收和營業天數（使用 Net Sales）
2. 計算不同食材成本率 × 人力成本的損益情況
3. 計算不同營業天數（2-7天/週）的損益平衡點
4. 三維敏感度分析矩陣（營業天數 × 食材成本 × 人力成本）
5. 三種日營收情境下的損益平衡天數比較

**輸出內容**（詳見 `analysis_output/break_even_q4/README.md`）：
- `break_even_report.md` - 完整分析報告
- `charts/break_even_days.png` - **三種日營收情境損益平衡天數（4×3 子圖）**
- `charts/sensitivity_3d_heatmap.png` - **三維敏感度熱力圖（2×2 子圖）**
- `charts/labor_sensitivity_table.png` - 人力成本敏感度比較表
- `charts/break_even_analysis.png` - 損益平衡點分析
- `charts/cost_breakdown.png` - 成本結構分解圖
- `charts/sensitivity_heatmap.png` - 基本敏感度熱力圖
- `charts/monthly_pnl_comparison.png` - 月度損益比較

### 6. 查看結果

#### 數據文件
- **合併數據**：`data/all_payments/`
  - `all_payments.json`：合併的 JSON 數據
  - `all_payments.csv`：轉換後的 CSV 數據
  - `all_payments_report.html`：HTML 報告
  - `all_payments_monthly_report.csv`：每月統計

#### 分析結果
- **流量分析**：`analysis_output/data/hourly/`
- **週間日分析**：`analysis_output/data/weekday/`
- **成本分析**：`analysis_output/cost_analysis/data/`

#### 圖表文件
- **每小時圖表**：`analysis_output/charts/hourly/`
- **週間日圖表**：`analysis_output/charts/weekday/`
- **成本圖表**：`analysis_output/cost_analysis/charts/`
- **其他圖表**：`analysis_output/charts/other/`

## 輸出格式說明

### JSON 格式

```json
[
  {
    "month": "2025-09",
    "hour": 11,
    "customers": 86,
    "revenue": 1110.15,
    "avg_order_value": 12.91
  },
  ...
]
```

### CSV 格式

| month | hour | customers | revenue | avg_order_value |
|-------|------|-----------|---------|-----------------|
| 2025-09 | 11 | 86 | 1110.15 | 12.91 |
| ... | ... | ... | ... | ... |

## 中文顯示解決方案

### 問題說明

在 macOS 上使用 matplotlib 繪製包含中文的圖表時，可能會遇到中文字符無法正確顯示的問題（顯示為方框或亂碼）。

### 解決方案

本專案已實作完整的中文顯示解決方案：

#### 1. 停用 LaTeX 渲染

```python
plt.rcParams['text.usetex'] = False
```

LaTeX 渲染不支援中文字符，必須停用。

#### 2. 明確指定中文字體文件路徑

腳本會自動尋找 macOS 系統內建的中文字體：

```python
chinese_font_paths = [
    '/System/Library/Fonts/Hiragino Sans GB.ttc',  # macOS 常用中文字體
    '/System/Library/Fonts/STHeiti Medium.ttc',     # 華文黑體
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',  # Arial Unicode
    '/Library/Fonts/Arial Unicode.ttf',              # Arial Unicode（備用路徑）
]
```

#### 3. 使用 FontProperties 明確指定字體

在所有中文文字元素上明確指定字體屬性：

```python
ax.set_title('每小時來客數', fontproperties=chinese_font_prop)
ax.set_xlabel('小時', fontproperties=chinese_font_prop)
ax.set_ylabel('來客數', fontproperties=chinese_font_prop)
```

#### 4. 清除字體快取（如需要）

如果字體仍然無法正確顯示，可以清除 matplotlib 的字體快取：

```bash
rm -rf ~/.matplotlib/fontlist-*.json
```

然後重新執行腳本。

### 其他作業系統

#### Windows

在 Windows 系統上，可以使用以下字體：

```python
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
```

#### Linux

在 Linux 系統上，需要安裝中文字體：

```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei

# 然後設定
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei']
```

## 資料說明

### 資料來源

- **Payments 資料**：來自 Square API 的 payments 端點
- **時間範圍**：2025年8月至11月11日
- **時區**：UTC（自動轉換為紐約時區）

### 時區與夏令時（DST）處理

本專案使用 `pytz` 庫自動處理夏令時（Daylight Saving Time, DST）轉換：

- **夏令時（EDT）**：3月第二個星期日 ~ 11月第一個星期日，UTC-4
- **冬令時（EST）**：11月第一個星期日 ~ 3月第二個星期日，UTC-5
- **2025年 DST 時間**：
  - 夏令時開始：2025年3月9日
  - 夏令時結束：2025年11月2日

`pytz` 會根據日期自動判斷並應用正確的時區偏移，無需手動處理。例如：
- 2025年8月（夏令時期間）：UTC-4
- 2025年11月2日之後（冬令時期間）：UTC-5

這確保了時間統計的準確性，不會因為 DST 轉換而產生錯誤。

### 資料欄位

- `created_at`: 支付建立時間（UTC）
- `status`: 支付狀態（只統計 COMPLETED）
- `total_money.amount`: 總金額（單位：分，需除以100轉換為美元）

### 營業日設定

- **週一**（Monday）
- **週二**（Tuesday）
- **週五**（Friday）
- **週六**（Saturday）

## 統計指標

分析腳本會計算以下統計指標：

- **總來客數**：每個月的總來客數
- **總金流**：每個月的總營業額
- **每小時平均來客數**：平均每小時的來客數
- **每小時平均金流（每日平均）**：每日每小時的平均營業額（該小時的總金流 / 該小時出現的天數）
- **平均客單價**：總金流 / 總來客數

**注意**：金流統計採用「每日每小時的平均值」，即該小時的總金流除以該小時出現的天數，這樣可以更準確地反映每個時段的平均營收表現，不受該月營業天數差異的影響。

## 圖表說明

### 折線圖

#### 1. 每小時來客數圖表（按月）

顯示每個月每小時的來客數趨勢，幫助了解客流高峰時段。

- `hourly_customers_by_month.png` - 按月分開顯示

#### 2. 每小時金流圖表（按月）

顯示每個月每小時的營業額趨勢（每日每小時的平均值），幫助了解營收高峰時段。

- `hourly_revenue_by_month.png` - 按月分開顯示
- **計算方式**：該小時的總金流 / 該小時出現的天數（每日平均）
- **顏色**：使用高對比度的綠色系（深綠到亮綠）

#### 3. 來客數跨月比較圖

比較不同月份的每小時來客數，識別季節性趨勢。

- `hourly_customers_comparison.png` - 跨月折線比較圖

#### 4. 金流跨月比較圖

比較不同月份的每小時營業額（每日每小時的平均值），識別營收變化趨勢。

- `hourly_revenue_comparison.png` - 跨月折線比較圖
- **計算方式**：每日每小時的平均值
- **顏色**：使用高對比度的綠色系（深綠到亮綠）

### 長條圖

#### 5. 每小時來客數長條圖（按月）

以長條圖形式顯示每個月每小時的來客數，更直觀地比較不同時段的客流差異。

- `hourly_customers_bar_by_month.png` - 按月分開顯示

#### 6. 每小時金流長條圖（按月）

以長條圖形式顯示每個月每小時的營業額（每日每小時的平均值），更直觀地比較不同時段的營收差異。

- `hourly_revenue_bar_by_month.png` - 按月分開顯示
- **計算方式**：每日每小時的平均值
- **顏色**：使用高對比度的綠色系（深綠到亮綠）

#### 7. 來客數跨月分組長條圖

使用分組長條圖比較不同月份的每小時來客數，方便並排比較。

- `hourly_customers_bar_comparison.png` - 跨月分組長條圖

#### 8. 金流跨月分組長條圖

使用分組長條圖比較不同月份的每小時營業額（每日每小時的平均值），方便並排比較。

- `hourly_revenue_bar_comparison.png` - 跨月分組長條圖
- **計算方式**：每日每小時的平均值
- **顏色**：使用高對比度的不同顏色（藍、紅、橙、紫）

### 其他圖表

#### 9. 營業日分佈圖

顯示各營業日（週一、週二、週五、週六）的來客數分佈。

- `business_days_distribution.png` - 營業日分佈長條圖

## 腳本說明

### 資料下載與處理腳本（scripts/）

- **`download_all_payments_mcp.py`**：合併 MCP 下載的所有 payments 數據
  - 自動去重（根據 payment ID）
  - 支援時區轉換（UTC → America/New_York）
  - 輸出：`data/all_payments/all_payments.json`

- **`convert_mcp_json_to_csv.py`**：將 JSON 格式轉換為 CSV
  - 用途：方便在 Excel 或其他工具中查看數據
  - 輸出：`data/all_payments/all_payments.csv`

- **`generate_html_report.py`**：生成 HTML 格式的月度報告
  - 包含每月統計表格、圖表
  - 輸出：`data/all_payments/all_payments_report.html`

- **`generate_monthly_report.py`**：生成每月統計 CSV 報告
  - 包含：營業日數、總交易數、總營收、日均營收、平均客單價
  - 輸出：`data/all_payments/all_payments_monthly_report.csv`

- **`generate_data_report.py`**：生成完整的數據檢查報告
  - 數據完整性檢查、異常記錄檢測
  - 輸出：`DATA_REPORT.md`

- **`show_status.py`**：顯示當前下載狀態

- **`download_all_remaining.py`**：檢查剩餘待下載的 cursor

### 分析腳本（scripts/analysis/）

- **`analyze_hourly_traffic.py`**：每小時流量與金流分析（主要分析腳本）
  - 輸出：每小時流量與金流的折線圖、長條圖、跨月比較圖等
  - 數據格式：JSON 和 CSV
  - 輸出位置：`analysis_output/data/hourly/` 和 `analysis_output/charts/hourly/`

- **`analyze_weekday_revenue.py`**：週間日收入分析
  - 分析週一、週二、週五、週六每個月的平均消費金額
  - 輸出：週間日收入圖表、熱力圖、趨勢圖
  - 輸出位置：`analysis_output/data/weekday/` 和 `analysis_output/charts/weekday/`

- **`calculate_total_revenue.py`**：計算總營收統計
  - 輸出：控制台統計資訊
  - 包含：總來客數、總營收、平均客單價、平均每日來客數等

- **`create_hourly_revenue_heatmap.py`**：產生營業時間熱力圖
  - 熱力圖範圍：10:00-20:00
  - 輸出位置：`analysis_output/charts/hourly/`

- **`analyze_cost_structure.py`**：成本結構分析
  - 計算固定成本、變動成本、員工成本
  - 分析利潤率和損益平衡點
  - 輸出位置：`analysis_output/cost_analysis/`

- **`generate_business_insights_report.py`**：商業洞察報告
  - 綜合分析營運表現
  - 提供改善建議

### 工具腳本（scripts/tools/）

- **`list_catalog_items.py`**：查詢 Square 目錄品項
  - 用途：查看店鋪商品目錄
  - 需要：Square API 訪問權限

- **`check_all_items.py`**：檢查所有品項
  - 檢查所有 Square API 返回的品項，包括分頁數據

- **`check_combo_items.py`**：檢查 combo 品項
  - 檢查所有包含 combo 的品項

- **`compare_with_square_api.py`**：API 數據比對
  - 從 Square API 查詢所有品項，並與 catalog.md 比對

- **`generate_catalog_md.py`**：生成目錄文件
  - 從 Square API 數據生成分類目錄 Markdown 文件
  - 輸出：`documents/catalog.md`

## 疑難排解

### 問題：中文字顯示為方框

**解決方案**：
1. 確認已停用 LaTeX 渲染：`plt.rcParams['text.usetex'] = False`
2. 清除字體快取：`rm -rf ~/.matplotlib/fontlist-*.json`
3. 確認系統已安裝中文字體

### 問題：找不到字體文件

**解決方案**：
1. 確認字體文件路徑正確
2. 檢查檔案權限
3. 使用備用字體名稱列表

### 問題：資料為空

**解決方案**：
1. 確認資料檔案路徑正確
2. 檢查資料格式是否正確
3. 確認營業日設定是否正確

### 問題：時區轉換不正確

**解決方案**：
1. 確認使用 `pytz.timezone('America/New_York')` 而非固定時區偏移
2. `pytz` 會自動處理 DST，無需手動調整
3. 如需驗證 DST 轉換，可以執行：
   ```python
   import pytz
   from datetime import datetime
   
   ny_tz = pytz.timezone('America/New_York')
   dt = datetime.fromisoformat('2025-03-10T12:00:00+00:00')
   dt_ny = dt.astimezone(ny_tz)
   print(dt_ny)  # 應該顯示 EDT (UTC-4)
   ```

## 數據概況（截至 2025-11-12）

### 資料統計
- **總記錄數**: 4,329 筆
- **已完成交易**: 4,261 筆（98.4%）
- **總營收**: $85,136.90
- **平均客單價**: $19.98
- **日期範圍**: 2024-02-08 至 2025-11-11

### 營業日統計（僅營業日）
- **總營業日數**: 116 天
- **總交易數**: 3,714 筆
- **總營收**: $77,267.58
- **日均營收**: $666.10
- **平均客單價**: $20.80

### 月份覆蓋
有數據的月份（13 個）：
- 2024: 02, 03, 04, 05, 06, 09
- 2025: 01, 02, 03, 08, 09, 10, 11

缺失月份（9 個）：
- 2024: 07, 08, 10, 11, 12
- 2025: 04, 05, 06, 07

### 最佳表現
- **最佳月份**: 2025-09（18 營業日，$17,094.44）
- **最高日均營收**: 2025-08（$992.70/天）
- **最高客單價**: 2025-08（$23.64）

## 重要檔案

### 報告文件
- [README.md](README.md) - 專案說明（本文件）
- [DATA_REPORT.md](DATA_REPORT.md) - 數據檢查報告
- [plan.md](plan.md) - 下載計劃文件

### 數據文件
- [data/all_payments/all_payments.json](data/all_payments/all_payments.json) - 合併數據
- [data/all_payments/all_payments.csv](data/all_payments/all_payments.csv) - CSV 格式
- [data/all_payments/all_payments_report.html](data/all_payments/all_payments_report.html) - HTML 報告

### 成本分析
- [analysis_output/cost_analysis/README.md](analysis_output/cost_analysis/README.md) - 成本分析說明

## 快速啟動指南

### 完整數據處理流程
```bash
# 1. 下載並合併數據
python3 scripts/download_all_payments_mcp.py

# 2. 轉換為 CSV
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json

# 3. 生成報告
python3 scripts/generate_html_report.py data/all_payments/all_payments.csv
python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv
python3 scripts/generate_data_report.py

# 4. 執行分析
python3 scripts/analysis/analyze_hourly_traffic.py
python3 scripts/analysis/analyze_weekday_revenue.py
python3 scripts/analysis/calculate_total_revenue.py
python3 scripts/analysis/create_hourly_revenue_heatmap.py
python3 scripts/analysis/analyze_cost_structure.py
```

### 檢查狀態
```bash
# 檢查下載狀態
python3 scripts/show_status.py

# 檢查剩餘待下載的 cursor
python3 scripts/download_all_remaining.py
```

## 營業規則

### 營業時間
- **營業日**: 週一、週二、週五、週六（每週四天）
- **營業時段**: 10:00-20:00（部分時段）

### 特殊規則
- **不營業月份**: 六月、七月（暑期休息）
- **特殊假期**: 聖誕節（12月25日）不營業

### Location ID
- **Taiwanway Location ID**: `LMDN6Z5DKNJ2P`

## 技術細節

### Square API
- **API 版本**: Square Payments API
- **分頁機制**: Cursor-based pagination
- **每頁限制**: 100 筆記錄
- **數據一致性**: 最終一致性（eventual consistency）

### 時區處理
- **原始時區**: UTC
- **目標時區**: America/New_York
- **DST 處理**: 自動處理夏令時轉換（使用 pytz）
  - 夏令時（EDT）: UTC-4（3月第二個星期日 ~ 11月第一個星期日）
  - 冬令時（EST）: UTC-5（11月第一個星期日 ~ 3月第二個星期日）

### 數據處理
- **去重機制**: 根據 payment ID 自動去重
- **數據過濾**: 自動過濾非營業日、非營業月份
- **狀態過濾**: 只統計 COMPLETED 狀態的交易

## 授權

本專案僅供內部使用。

## 聯絡資訊

如有問題或建議，請聯絡專案維護者。

---

**最後更新**: 2025-11-15
