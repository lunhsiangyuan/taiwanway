# /predict - 天氣預測命令

執行天氣+放假預測分析，預測來客數、營收和便當量。

## 使用方式

```
/predict [選項]
```

## 選項

| 選項 | 說明 | 預設值 | 範例 |
|------|------|--------|------|
| `--date` | 預測起始日期 | 明天 | `--date 2025-12-20` |
| `--range` | 預測天數 (1-7) | 7 | `--range 7` |
| `--model` | 模型選擇 | local | `--model local` 或 `--model gcp` |
| `--skip-audit` | 跳過 Audit 確認 | false | `--skip-audit` |
| `--force-retrain` | 強制重新訓練 | false | `--force-retrain` |

## 範例

### 基本用法
```
/predict
```
預測明天起 7 天的營運狀況

### 指定日期
```
/predict --date 2025-12-25 --range 3
```
預測 12/25 起 3 天的營運狀況

### 使用 GCP ML
```
/predict --model gcp
```
使用 Vertex AI AutoML 進行預測

### 快速預測（跳過 Audit）
```
/predict --skip-audit
```
跳過 Audit 確認步驟，直接執行預測

## 執行流程

調用此命令後，Orchestrator 將：

1. **數據收集** (並行)
   - Weather Agent: 獲取天氣數據
   - Holiday Agent: 獲取假日資訊
   - Historical Agent: 提取歷史銷售

2. **Audit 檢查** (並行)
   - Data Ingestion Agent: Schema 驗證
   - EDA Agent: 探索性分析

3. **人工確認** ⏸️
   - 顯示 Audit 報告
   - 等待確認 (confirm/reject/modify)
   - 可用 `--skip-audit` 跳過

4. **特徵工程**
   - Feature Agent: 生成 feature_matrix.csv

5. **預測**
   - Local Forecast Agent (預設)
   - 或 GCP ML Agent (`--model gcp`)

6. **驗證**
   - Validation Agent: 計算 MAPE/RMSE/R²

7. **最終檢查** 🔄
   - Orchestrator 驗證結果

8. **報告生成**
   - Report Agent: Markdown + JSON + 圖表

## 輸出

成功執行後，將生成：

```
weather/
├── data/
│   ├── raw/
│   │   ├── weather_history.csv
│   │   ├── weather_forecast.csv
│   │   ├── holidays.csv
│   │   └── daily_sales.csv
│   ├── processed/
│   │   └── feature_matrix.csv
│   └── audit/
│       ├── audit_report.csv
│       └── data_quality.md
├── predictions/
│   ├── predictions_YYYYMMDD.csv
│   └── validation_metrics.json
└── reports/
    ├── weekly_forecast.md      # 👈 主報告
    ├── weekly_forecast.json
    └── charts/
        ├── weekly_revenue_forecast.png
        ├── weather_impact.png
        └── model_performance.png
```

## 錯誤處理

| 錯誤 | 說明 | 解決方式 |
|------|------|----------|
| `No historical data` | 找不到歷史銷售數據 | 確認 Square 數據存在 |
| `Weather API error` | 天氣 API 失敗 | 檢查 API Key 設定 |
| `Model validation failed` | 模型驗證不通過 | 查看驗證報告 |
| `GCP authentication failed` | GCP 認證失敗 | 設定 service account |

## 相關命令

- `/analyze` - 完整營收分析
- `/break-even` - 損益平衡分析
- `/report` - 報告生成

## 技術細節

此命令調用 `orchestrator` Subagent，並依序執行 11 個 Subagent：

```
① orchestrator → ② weather → ③ holiday → ④ historical
       ↓
⑤ data-ingestion + ⑥ eda (並行)
       ↓
   [人工確認]
       ↓
⑦ feature → ⑧ local-forecast 或 ⑨ gcp-ml
       ↓
⑩ validation → [orchestrator 檢查] → ⑪ report
```
