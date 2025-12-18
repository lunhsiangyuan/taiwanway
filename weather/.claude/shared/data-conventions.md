# Data Conventions - 數據慣例

本文件定義天氣預測系統的數據格式和命名慣例，所有 Subagent 共享使用。

## 檔案命名慣例

### 數據檔案
```yaml
naming_conventions:
  raw_data:
    weather_history: "weather_history.csv"
    weather_forecast: "weather_forecast.csv"
    holidays: "holidays.csv"
    daily_sales: "daily_sales.csv"

  processed_data:
    merged_data: "raw_merged.csv"
    feature_matrix: "feature_matrix.csv"
    scaled_features: "feature_matrix_scaled.csv"

  audit_data:
    audit_report: "audit_report.csv"
    data_quality: "data_quality.md"
    schema_validation: "schema_validation.json"

  predictions:
    format: "predictions_YYYYMMDD.csv"
    example: "predictions_20251214.csv"

  models:
    local: "{target}_model.pkl"
    examples:
      - "visitor_model.pkl"
      - "revenue_model.pkl"
      - "bento_model.pkl"

  reports:
    weekly_forecast_md: "weekly_forecast.md"
    weekly_forecast_json: "weekly_forecast.json"
```

## 日期格式

### 標準日期格式
```yaml
date_formats:
  standard: "YYYY-MM-DD"
  examples:
    - "2025-12-14"
    - "2024-04-01"

  datetime: "YYYY-MM-DD HH:MM:SS"
  examples:
    - "2025-12-14 14:30:00"

  timestamp_iso: "YYYY-MM-DDTHH:MM:SSZ"
  examples:
    - "2025-12-14T14:30:00Z"
```

### 時區處理
```yaml
timezone:
  source: "UTC"
  target: "America/New_York"
  conversion: "Always convert UTC to NY timezone"
  library: "pytz"
```

## 數值格式

### 貨幣
```yaml
currency:
  format: "float with 2 decimal places"
  unit: "USD"
  examples:
    - 750.50
    - 1234.00
  storage: "原始值（美元），不含千分位"
```

### 溫度
```yaml
temperature:
  unit: "Fahrenheit (°F)"
  format: "float with 1 decimal place"
  examples:
    - 68.5
    - 32.0
```

### 降水量
```yaml
precipitation:
  unit: "inches"
  format: "float with 2 decimal places"
  examples:
    - 0.15
    - 1.25
```

### 百分比
```yaml
percentage:
  format: "decimal (0-1) not percent"
  examples:
    - 0.15  # 15%, not 15
    - 0.875 # 87.5%
```

## 欄位命名慣例

### 命名規則
```yaml
naming_style:
  format: "snake_case"
  language: "English"
  examples:
    good:
      - "total_revenue"
      - "visitor_count"
      - "is_holiday"
    bad:
      - "TotalRevenue"  # camelCase
      - "total-revenue" # kebab-case
      - "總營收"        # Chinese
```

### 布林欄位
```yaml
boolean_columns:
  prefix: "is_" or "has_"
  examples:
    - "is_holiday"
    - "is_weekend"
    - "is_rainy"
    - "has_school_break"
  values: [true, false] or [1, 0]
```

### 日期相關欄位
```yaml
date_columns:
  date: "date"
  day_of_week: "day_of_week"  # 0-6
  day_name: "day_name"        # Monday, etc.
  month: "month"              # 1-12
  year: "year"                # 2025
  year_month: "year_month"    # "2025-12"
  season: "season"            # Spring, Summer, Fall, Winter
```

## 數據類型對照

### Python/Pandas 類型
```yaml
data_types:
  date:
    pandas: "datetime64[ns, America/New_York]"
    python: "datetime.date"

  integer:
    pandas: "int64"
    python: "int"

  float:
    pandas: "float64"
    python: "float"

  boolean:
    pandas: "bool"
    python: "bool"

  string:
    pandas: "object" or "string"
    python: "str"

  category:
    pandas: "category"
    python: "str"
```

## 缺失值處理

### 缺失值表示
```yaml
missing_values:
  standard: null or NaN
  csv_representation: ""  # 空字串
  json_representation: null
```

### 預設填充策略
```yaml
fill_strategies:
  numeric_weather:
    method: "interpolate"
    description: "使用前後天平均值"

  boolean:
    method: "fill_false"
    description: "填入 False"

  categorical:
    method: "fill_mode"
    description: "填入最常見值"

  target_variables:
    method: "leave_null"
    description: "保留 NULL，表示需要預測"
```

## CSV 檔案規範

### 編碼
```yaml
csv_encoding:
  encoding: "utf-8"
  line_ending: "LF" or "CRLF"
  delimiter: ","
  quoting: "minimal"  # 僅在需要時使用引號
```

### 標頭
```yaml
csv_header:
  include: true
  row: 1
  style: "snake_case"
```

## JSON 檔案規範

### 格式
```yaml
json_format:
  indent: 2
  ensure_ascii: false  # 允許非 ASCII 字符
  sort_keys: false
```

### 結構範例
```json
{
  "metadata": {
    "generated_at": "2025-12-14T12:00:00",
    "version": "1.0"
  },
  "data": {
    ...
  }
}
```

## 目錄結構

```yaml
directory_structure:
  weather/
    ├── .claude/
    │   ├── agents/          # Subagent 定義
    │   ├── commands/        # Slash 命令
    │   └── shared/          # 共享配置
    ├── tools/               # Python 工具
    ├── data/
    │   ├── raw/             # 原始數據
    │   ├── processed/       # 處理後數據
    │   └── audit/           # Audit 輸出
    │       └── charts/      # EDA 圖表
    ├── models/
    │   ├── local/           # 本地模型
    │   └── gcp/             # GCP 模型配置
    ├── predictions/         # 預測結果
    ├── reports/             # 報告輸出
    │   └── charts/          # 報告圖表
    └── scripts/             # 執行腳本
```

## 版本控制

### 忽略檔案
```yaml
gitignore:
  - "*.pkl"           # 模型檔案
  - "data/raw/*.csv"  # 原始數據
  - "predictions/"    # 預測結果
  - "__pycache__/"
  - ".env"
```

### 追蹤檔案
```yaml
tracked_files:
  - ".claude/**/*.md"     # Agent 定義
  - "tools/**/*.py"       # 工具代碼
  - "config.yaml"         # 配置
  - "README.md"           # 說明
```

## 更新記錄

| 日期 | 更新內容 | 更新者 |
|------|----------|--------|
| 2025-12-14 | 初始版本 | System |
