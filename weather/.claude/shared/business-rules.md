# Business Rules - 業務規則

本文件定義天氣預測系統的業務規則，所有 Subagent 共享使用。

## 營業時間規則

### 營業日
```yaml
operating_days:
  - monday     # 0
  - tuesday    # 1
  - friday     # 4
  - saturday   # 5

closed_days:
  - wednesday  # 2
  - thursday   # 3
  - sunday     # 6
```

### 營業時間
```yaml
operating_hours:
  open: "10:00"
  close: "20:00"
  timezone: "America/New_York"
```

### 休息月份
```yaml
closed_months:
  - 6  # June
  - 7  # July
  reason: "Summer break"
```

### 特殊休息日
```yaml
special_closed_days:
  - date: "12-25"
    name: "Christmas Day"
  - date: "01-01"
    name: "New Year's Day"
```

## 地理位置

```yaml
location:
  city: "New York"
  state: "NY"
  country: "US"
  coordinates:
    lat: 40.7128
    lon: -74.0060
  timezone: "America/New_York"
```

## 稅率設定

```yaml
tax_rates:
  nyc_sales_tax: 0.08875  # 8.875%
  breakdown:
    ny_state: 0.04        # 4%
    nyc: 0.045            # 4.5%
    mta: 0.00375          # 0.375%
```

## 營收計算規則

### 稅前營收
```python
# Net Sales = Gross Sales / (1 + tax_rate)
net_sales = gross_sales / (1 + 0.08875)
```

### 來客數定義
```yaml
visitor_count:
  definition: "unique transactions per day"
  note: "一筆交易 = 一位來客"
```

### 便當識別
```yaml
bento_identification:
  patterns:
    - "Bento"
    - "便當"
    - "Lunch Box"
    - "Combo"
  category: "Bento"
```

## 天氣影響規則

### 降雨影響
```yaml
rain_impact:
  light:  # < 0.1 inch
    revenue_impact: -0.05  # -5%
  moderate:  # 0.1-0.3 inch
    revenue_impact: -0.15  # -15%
  heavy:  # > 0.3 inch
    revenue_impact: -0.25  # -25%
```

### 溫度影響
```yaml
temperature_impact:
  cold:  # < 40°F
    revenue_impact: -0.10  # -10%
  mild:  # 40-70°F
    revenue_impact: 0      # 基準
  hot:   # > 70°F
    revenue_impact: -0.05  # -5% (但紐約夏天餐廳休息)
```

### 極端天氣
```yaml
extreme_weather:
  snow_day:
    revenue_impact: -0.40  # -40%
  storm:
    revenue_impact: -0.50  # -50%
```

## 假日影響規則

### 假日類型影響
```yaml
holiday_impact:
  very_high:  # Chinese New Year
    revenue_impact: +0.50  # +50%
    examples: ["Chinese New Year"]

  high:  # Major holidays
    revenue_impact: +0.30  # +30%
    examples: ["Thanksgiving", "Christmas"]

  medium:  # Regular holidays
    revenue_impact: +0.15  # +15%
    examples: ["Labor Day", "Memorial Day"]

  low:  # Minor holidays
    revenue_impact: +0.05  # +5%
    examples: ["Columbus Day", "Veterans Day"]
```

### 連假影響
```yaml
long_weekend_impact:
  3_day_weekend: +0.20  # +20%
  4_day_weekend: +0.30  # +30%
```

### 假日前夕
```yaml
pre_holiday_impact:
  day_before: +0.15  # +15%
```

## 星期影響規則

```yaml
day_of_week_impact:
  monday:    0       # 基準
  tuesday:   -0.05   # -5%
  friday:    +0.08   # +8%
  saturday:  +0.15   # +15%
```

## 季節性規則

```yaml
seasonal_impact:
  spring:  # 3-5 月
    revenue_impact: +0.05
  fall:    # 9-11 月
    revenue_impact: +0.15  # 最旺
  winter:  # 12-2 月
    revenue_impact: +0.10
  summer:  # 6-8 月
    note: "餐廳休息，無營業"
```

## 便當預測規則

### 便當比例
```yaml
bento_ratio:
  average: 0.33  # 來客數的 33%
  factors:
    rain_day: +0.05      # 下雨天多外帶
    holiday: -0.03       # 假日少外帶
    weekday_lunch: +0.10 # 平日午餐多外帶
```

## 備料規則

### 安全庫存
```yaml
preparation_buffer:
  default: 0.15  # 15% 安全庫存
  holiday_week: 0.20  # 假日週 20%
  uncertain_weather: 0.25  # 天氣不確定 25%
```

### 材料換算
```yaml
material_per_bento:
  rice_cups: 0.32
  meat_lbs: 0.10
  vegetables_lbs: 0.20
  eggs: 1.0
  containers: 1.1  # 10% 備用
```

## 模型驗證規則

### 可接受閾值
```yaml
model_thresholds:
  mape:
    excellent: 10
    good: 15
    acceptable: 20
    warning: 30
    fail: 30

  r2:
    excellent: 0.85
    good: 0.75
    acceptable: 0.60
    warning: 0.50
    fail: 0.50
```

### 預測合理性檢查
```yaml
prediction_bounds:
  visitors:
    min: 0
    max: 200
    typical_range: [20, 100]

  revenue:
    min: 0
    max: 5000
    typical_range: [300, 1500]

  bento:
    min: 0
    max: 100
    max_ratio_to_visitors: 0.6
```

## 更新記錄

| 日期 | 更新內容 | 更新者 |
|------|----------|--------|
| 2025-12-14 | 初始版本 | System |
