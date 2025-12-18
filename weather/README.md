# 天氣+放假預測系統

使用天氣和假日資訊預測餐廳每日來客數、營收和便當量，方便備料規劃。

## 系統概覽

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    天氣+放假預測系統 - 11 Subagent 架構                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌─────────────────────┐                         │
│                              │ ① ORCHESTRATOR     │◄─────────────────────┐  │
│                              │ 預測系統協調器       │                     │  │
│                              └──────────┬──────────┘                     │  │
│                                         │                                │  │
│                  ┌──────────────────────┼──────────────────────┐         │  │
│                  ▼                      ▼                      ▼         │  │
│         ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  │  │
│         │ ② WEATHER      │   │ ③ HOLIDAY      │   │ ④ HISTORICAL   │  │  │
│         │ OpenWeather API │   │ 假日日曆        │   │ Square 銷售數據 │  │  │
│         └────────┬────────┘   └────────┬────────┘   └────────┬────────┘  │  │
│                  └──────────────────────┼──────────────────────┘         │  │
│                                         ▼                                │  │
│         ┌─────────────────────┐                 ┌─────────────────────┐  │  │
│         │ ⑤ DATA INGESTION   │                 │ ⑥ EDA AGENT        │  │  │
│         │ 數據驗證             │                 │ 探索性分析          │  │  │
│         └────────┬────────────┘                 └────────┬────────────┘  │  │
│                  └──────────────────────┬──────────────────┘             │  │
│                                         ▼                                │  │
│                            ⏸️ 人工確認 CHECKPOINT                         │  │
│                                         │                                │  │
│                                         ▼                                │  │
│                              ┌─────────────────────┐                     │  │
│                              │ ⑦ FEATURE          │                     │  │
│                              │ 特徵工程            │                     │  │
│                              └──────────┬──────────┘                     │  │
│                                         │                                │  │
│              ┌──────────────────────────┴──────────────────────────┐     │  │
│              ▼                                                     ▼     │  │
│  ┌───────────────────────┐                         ┌───────────────────────┐│
│  │ ⑧ LOCAL FORECAST     │                         │ ⑨ GCP ML AGENT       ││
│  │ 線性迴歸 (預設)        │                         │ Vertex AI (可選)      ││
│  └───────────┬───────────┘                         └───────────┬───────────┘│
│              └──────────────────────┬──────────────────────────┘            │
│                                     ▼                                       │
│                              ┌─────────────────────┐                        │
│                              │ ⑩ VALIDATION       │                        │
│                              │ MAPE / RMSE / R²    │                        │
│                              └──────────┬──────────┘                        │
│                                         │                                   │
│                    ═══════ 🔄 ORCHESTRATOR CHECK ═══════─────────────────────┘
│                                         │
│                                         ▼
│                              ┌─────────────────────┐                        │
│                              │ ⑪ REPORT AGENT    │                        │
│                              │ Markdown / JSON     │                        │
│                              └─────────────────────┘                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 快速開始

### 1. 環境設定

```bash
# 安裝依賴
pip install pandas numpy scikit-learn matplotlib seaborn pytz pyyaml requests

# 設定 OpenWeather API Key
export OPENWEATHER_API_KEY='your-api-key'

# (可選) 設定 GCP 專案
export GOOGLE_CLOUD_PROJECT='your-project-id'
```

### 2. 執行預測

```bash
# 在 Claude Code 中使用 Slash 命令
/predict

# 指定日期範圍
/predict --date 2025-12-20 --range 7

# 跳過 Audit 確認
/predict --skip-audit
```

### 3. 查看報告

預測完成後，報告位於：
- `weather/reports/weekly_forecast.md` - Markdown 報告
- `weather/reports/weekly_forecast.json` - JSON 數據
- `weather/reports/charts/` - 視覺化圖表

## 目錄結構

```
weather/
├── .claude/                               # Claude Agent SDK 配置
│   ├── agents/                            # 11 個 Subagent 定義
│   │   ├── orchestrator.md               # ① 協調器
│   │   ├── weather-agent.md              # ② 天氣代理
│   │   ├── holiday-agent.md              # ③ 假日代理
│   │   ├── historical-agent.md           # ④ 歷史代理
│   │   ├── data-ingestion-agent.md       # ⑤ 數據驗證
│   │   ├── eda-agent.md                  # ⑥ 探索性分析
│   │   ├── feature-agent.md              # ⑦ 特徵工程
│   │   ├── local-forecast-agent.md       # ⑧ 本地預測
│   │   ├── gcp-ml-agent.md               # ⑨ GCP ML
│   │   ├── validation-agent.md           # ⑩ 模型驗證
│   │   └── report-agent.md               # ⑪ 報告生成
│   ├── commands/                          # Slash 命令
│   │   └── predict.md                    # /predict 命令
│   └── shared/                            # 共享配置
│       ├── business-rules.md             # 業務規則
│       └── data-conventions.md           # 數據慣例
│
├── tools/                                 # Python 工具
│   ├── __init__.py
│   ├── weather_tools.py                  # 天氣 API
│   ├── holiday_tools.py                  # 假日日曆
│   ├── forecast_tools.py                 # 預測模型
│   └── gcp_ml_tools.py                   # GCP ML
│
├── data/
│   ├── raw/                               # 原始數據
│   │   ├── weather_history.csv           # 歷史天氣
│   │   ├── weather_forecast.csv          # 天氣預報
│   │   ├── holidays.csv                  # 假日日曆
│   │   └── daily_sales.csv               # 每日銷售
│   ├── processed/                         # 處理後數據
│   │   └── feature_matrix.csv            # 特徵矩陣 ⭐
│   └── audit/                             # Audit 輸出
│       ├── audit_report.csv
│       ├── data_quality.md
│       └── charts/
│
├── models/
│   ├── local/                             # 本地模型
│   │   ├── visitor_model.pkl
│   │   ├── revenue_model.pkl
│   │   └── bento_model.pkl
│   └── gcp/                               # GCP 模型配置
│
├── predictions/                           # 預測結果
│   ├── predictions_YYYYMMDD.csv
│   └── validation_metrics.json
│
├── reports/                               # 報告輸出
│   ├── weekly_forecast.md                # 週預測報告
│   ├── weekly_forecast.json
│   └── charts/
│       ├── weekly_revenue_forecast.png
│       ├── weather_impact.png
│       └── model_performance.png
│
├── config.yaml                            # 系統配置
└── README.md                              # 本文件
```

## 預測目標

| 目標 | 說明 | 用途 |
|------|------|------|
| **來客數** | 每日預期來客人數 | 人力配置 |
| **營收** | 每日預期營收金額 | 財務規劃 |
| **便當量** | 每日預期便當數量 | 備料準備 |

## 影響因素

### 天氣因素
- 🌡️ 溫度 (Cold/Mild/Hot)
- 🌧️ 降雨 (Light/Moderate/Heavy)
- ❄️ 降雪
- 💨 風速

### 假日因素
- 🎄 聯邦假日 (Christmas, Thanksgiving 等)
- 🧧 華人節日 (春節、中秋等)
- 🏫 學校假期
- 📅 連假

### 時間因素
- 星期幾 (週六最旺)
- 月份/季節
- 是否週末

## 模型架構

### MVP 階段 (線性迴歸)

```python
# 三個獨立模型
來客數 = f(天氣 + 假日 + 時間)
營收   = f(天氣 + 假日 + 時間)
便當量 = f(天氣 + 假日 + 時間 + 預測來客數)
```

### 進階階段 (可選 GCP ML)

當數據量 > 1000 筆時，可切換至：
- Vertex AI AutoML
- BigQuery ML (XGBoost)

## 數據來源

| 來源 | 數據 | 時間範圍 |
|------|------|----------|
| OpenWeather API | 歷史天氣 + 7天預報 | 2024-04 ~ 今天 |
| 假日日曆 | 聯邦/學校/華人假日 | 2024-2026 |
| Square API | 歷史銷售記錄 | 2024-04 ~ 2025-11 |

## 輸出報告範例

```markdown
# 📅 週營運預測報告
═══════════════════════════════════════════════════════════

**預測範圍**: 2025-12-15 ~ 2025-12-21

## 📊 一週總覽

| 指標 | 預測值 | 95% 信賴區間 | 較上週 |
|------|--------|--------------|--------|
| 總來客數 | 385 人 | 340-430 | +12% |
| 總營收 | $5,280 | $4,650-$5,910 | +8% |
| 總便當量 | 126 份 | 105-147 | +15% |

## 👨‍🍳 備料建議

| 食材 | 建議量 |
|------|--------|
| 白飯 | 45 杯 |
| 滷肉 | 14 磅 |
| 青菜 | 28 磅 |

## ⚠️ 風險提醒
- 12/18 降雨機率上升至 40%
- 聖誕節當週人流可能超出預測
```

## 業務規則

- **營業日**: 週一、週二、週五、週六
- **營業時間**: 10:00 - 20:00
- **休息月份**: 6-7 月 (暑假)
- **時區**: America/New_York

## API 使用

### OpenWeather API (免費方案)
- 每日上限: 1000 calls
- 歷史回溯: 1979-01-01 起
- 預報範圍: 未來 7 天

## 驗證指標

| 指標 | 優秀 | 良好 | 可接受 | 警告 |
|------|------|------|--------|------|
| MAPE | <10% | <15% | <20% | <30% |
| R² | >0.85 | >0.75 | >0.60 | >0.50 |

## 常見問題

### Q: 如何更新天氣數據？
```bash
# 天氣數據會自動增量更新
# 或手動執行
python tools/weather_tools.py
```

### Q: 如何使用 GCP ML？
```bash
/predict --model gcp
```
需要先設定 `GOOGLE_CLOUD_PROJECT` 環境變數。

### Q: 如何跳過 Audit 確認？
```bash
/predict --skip-audit
```

## 更新記錄

| 版本 | 日期 | 更新內容 |
|------|------|----------|
| 1.0.0 | 2025-12-14 | 初始版本 |

## 相關文件

- [業務規則](.claude/shared/business-rules.md)
- [數據慣例](.claude/shared/data-conventions.md)
- [系統配置](config.yaml)
