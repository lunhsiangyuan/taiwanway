# /analyze - 完整數據分析命令

執行完整的數據分析管線，使用 Orchestrator 協調多個 Subagent 執行。

## 使用方式

```
/analyze [數據檔案路徑] [--mode 模式] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
```

## 參數說明

- `數據檔案路徑`：數據檔案路徑（預設：`data/all_payments/all_payments.csv`）
- `--mode`：分析模式
  - `full`：完整分析（預設）- 執行所有 Subagent
  - `quick`：快速 EDA - 只執行 DataIngestion → EDA → Viz
  - `analysis-only`：僅分析 - 跳過視覺化
- `--start-date`：分析開始日期（可選）
- `--end-date`：分析結束日期（可選）

## 管線架構

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ORCHESTRATOR                                    │
│  負責：Sequential Thinking → Research → Subagent 調度 → 重試/降級 → 彙總    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
┌───────────────┐           ┌───────────────┐            ┌───────────────┐
│   Phase 0     │           │   Phase 1     │            │   Phase 2+    │
│   Sequential  │     →     │   Research    │      →     │   Subagent    │
│   Thinking    │           │               │            │   Pipeline    │
│               │           │ • Context7    │            │               │
│ • 深度推理    │           │ • WebSearch   │            │ DataIngestion │
│ • 任務分析    │           │ • Firecrawl   │            │   → EDA       │
│ • 策略規劃    │           │ • 行業基準    │            │   → Analysis  │
│               │           │               │            │   → Viz       │
│               │           │               │            │   → Export    │
└───────────────┘           └───────────────┘            └───────────────┘
```

## 執行流程

### Step 1: 調用 Orchestrator

使用 Task Tool 調用 Orchestrator，傳入任務參數：

```json
{
  "task": "完整分析數據",
  "data_source": "data/all_payments/all_payments.csv",
  "options": {
    "mode": "full",
    "date_range": {"start": "2025-09-01", "end": "2025-11-30"},
    "analysis_types": ["growth_rate", "clustering", "trends"],
    "chart_priority": "high",
    "output_format": ["markdown", "json"]
  }
}
```

### Step 2: Orchestrator 調度 Subagents

Orchestrator 自動執行以下流程：

#### Phase 0: Sequential Thinking（深度推理）

在執行任何分析之前，Orchestrator 先進行結構化思考：

- **理解任務**：解析用戶的分析需求和隱含目標
- **識別挑戰**：預判數據問題和分析難點
- **規劃策略**：決定最佳的分析路徑
- **驗證計劃**：確保計劃完整且可行
- **確認順序**：決定 Subagent 執行順序和依賴關係

#### Phase 1: Research（背景研究）

透過 MCP 工具查詢相關資料：

- **Context7 查詢**：查詢 pandas、matplotlib、scikit-learn 最新用法
  ```python
  # 範例：查詢 pandas groupby 文檔
  library_id = resolve-library-id("pandas")  # → /pandas/pandas
  docs = get-library-docs("/pandas/pandas", topic="groupby", mode="code")
  ```
- **WebSearch/Firecrawl**：搜尋行業基準和最佳實踐
  ```python
  # 範例：搜尋餐飲業指標
  results = firecrawl_search("restaurant revenue metrics NYC 2025", limit=5)
  ```
- **背景脈絡包**：整合為 `context_package` JSON，傳遞給後續 Subagent

輸出：`context_package` 包含 library_references、industry_benchmarks、recommendations

#### 2a. DataIngestion（數據攝取）

- 載入數據檔案（支援 CSV/JSON/Parquet）
- 格式偵測和 Schema 驗證
- 時間標準化（UTC → America/New_York）
- 套用業務規則過濾：
  - 營業日：週一(0)、二(1)、五(4)、六(5)
  - 營業時間：10:00-20:00
  - 排除關閉月份：六月(6)、七月(7)
- 輸出：預處理後的 DataFrame + 元資料

#### 2b. EDA（探索性分析）

- 計算摘要統計（mean, median, std, quartiles）
- 分佈分析（skewness, kurtosis）
- 相關性分析（correlation matrix）
- 離群值偵測（IQR method）
- **生成圖表需求列表**（傳給 Viz）
- 輸出：EDA 結果 + `chart_requirements[]`

#### 2c. Analysis（統計/ML 分析）

- 成長率分析（日/週/月）
- 客戶分群（K-means, RFM）
- 時間序列分析（季節性分解、ARIMA）
- Pareto 分析（80/20 法則）
- 輸出：分析結果 JSON

#### 2d. Viz（視覺化）

根據 EDA 的 `chart_requirements` 生成圖表：

| 圖表類型 | 用途 |
|----------|------|
| bar | 每小時營收分布 |
| heatmap | 營收熱力圖（小時 × 星期） |
| line | 月度營收趨勢 |
| boxplot | 各星期營收分布 |
| histogram | 交易金額分布 |
| pie | 營收佔比 |

輸出：圖表檔案路徑列表

#### 2e. Export（報告輸出）

整合所有結果，輸出：
- `report.md`：Markdown 格式報告
- `report.json`：結構化數據
- `charts/`：所有圖表
- `data/`：處理後的數據 CSV

### Step 3: 接收結果

Orchestrator 返回彙總結果：

```json
{
  "task_id": "task_20251206_001",
  "status": "completed",
  "pipeline": {
    "DataIngestion": {"status": "success", "duration_ms": 1200},
    "EDA": {"status": "success", "duration_ms": 800},
    "Analysis": {"status": "success", "duration_ms": 1500},
    "Viz": {"status": "success", "duration_ms": 2000},
    "Export": {"status": "success", "duration_ms": 500}
  },
  "outputs": {
    "report": "agents/output/reports/20251206_143000/report.md",
    "data": "agents/output/reports/20251206_143000/report.json",
    "charts": ["chart_001.png", "chart_002.png", ...]
  },
  "summary": "分析完成，共生成 6 張圖表，發現 3 個關鍵洞察。"
}
```

## 重試與降級策略

Orchestrator 內建重試機制：

| Subagent | 重試次數 | 降級行為 |
|----------|----------|----------|
| DataIngestion | 3 | 使用快取數據 |
| EDA | 3 | 使用基本統計 |
| Analysis | 3 | 跳過進階分析（ARIMA） |
| Viz | 3 | 跳過失敗的圖表 |
| Export | 3 | 輸出部分報告 |

## 輸出結構

```
agents/output/reports/{timestamp}/
├── report.md                    # 主報告
├── report.json                  # 結構化數據
├── charts/
│   ├── chart_001_hourly_revenue.png
│   ├── chart_002_heatmap.png
│   ├── chart_003_monthly_trend.png
│   └── ...
├── data/
│   ├── processed_data.csv
│   └── summary_stats.csv
└── metadata.json                # 執行元資料
```

## 輸出範例

```markdown
# 數據分析報告

**生成時間**：2025-12-06 14:30:00
**數據範圍**：2025-09-01 ~ 2025-11-30
**數據筆數**：8,500 筆交易

---

## 執行摘要

### 關鍵指標

| 指標 | 數值 | 趨勢 |
|-----|------|------|
| 總營收 | $33,885.50 | - |
| 日均營收 | $753.01 | ↓ 8.2% |
| 平均客單價 | $18.50 | ↑ 3.5% |
| 交易筆數 | 1,832 | ↓ 5.1% |

### 重要發現

1. 🔴 **營收下滑**：11 月營收較 9 月下滑 22%
2. 🟡 **尖峰時段**：12:00-13:00 貢獻 25% 營收
3. 🟢 **VIP 客戶**：15% 客戶貢獻 45% 營收

### 優先建議

- 🔴 **緊急**：調查 11 月營收下滑原因
- 🟡 **重要**：優化午餐時段服務效率
- 🟢 **建議**：推動 VIP 會員計劃

---

## 圖表

### 每小時平均營收分布
![圖表](charts/chart_001_hourly_revenue.png)

### 營收熱力圖
![圖表](charts/chart_002_heatmap.png)

---

*報告生成：Claude Code Agent System*
```

## 分析模式對照

| 模式 | 執行的 Subagents | 預期時間 | 用途 |
|------|------------------|----------|------|
| `full` | Sequential Thinking → Research → 全部 6 個 Subagent | ~45 秒 | 完整分析報告（含背景研究） |
| `quick` | DataIngestion → EDA → Viz | ~15 秒 | 快速探索數據（跳過研究） |
| `analysis-only` | Research → DataIngestion → EDA → Analysis → Export | ~30 秒 | 不需要圖表時 |

## 錯誤處理

- **檔案不存在**：提示用戶確認路徑
- **格式不支援**：列出支援的格式（CSV/JSON/Parquet）
- **Schema 驗證失敗**：顯示缺失欄位
- **Subagent 失敗**：執行降級策略，繼續其他 Subagent
- **全部失敗**：返回錯誤報告，列出所有失敗原因

## 相關命令

- `/break-even`：損益平衡分析
- `/report`：報告生成（使用已有結果）

## 相關 Subagent 文檔

- [orchestrator.md](../agents/orchestrator.md) - 主協調器
- [research.md](../agents/research.md) - 背景研究（Context7 + WebSearch）
- [data-ingestion.md](../agents/data-ingestion.md) - 數據攝取
- [eda.md](../agents/eda.md) - 探索性分析
- [analysis.md](../agents/analysis.md) - 統計/ML 分析
- [viz.md](../agents/viz.md) - 視覺化
- [export.md](../agents/export.md) - 報告輸出
