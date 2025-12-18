# 數據處理慣例

本文檔定義了 Square 支付數據的欄位規範和處理方法。

## 數據來源

### 主要數據檔案
- **位置**：`data/all_payments/all_payments.csv`
- **格式**：CSV（UTF-8 編碼）
- **來源**：Square Payments API

### 備用數據檔案
- `data/all_payments/all_payments.json`（原始 JSON）
- `data/all_payments/payments_2025_*.csv`（按月份）
- `data/all_payments/payments_2024_full.csv`（歷史數據）

---

## 欄位定義

### 時間欄位

| 欄位名稱 | 格式 | 說明 |
|---------|------|------|
| `created_at` | ISO 8601 (UTC) | 交易創建時間 |
| `Date` | YYYY-MM-DD | 日期（可能已轉換時區） |
| `Time` | HH:MM:SS | 時間（可能已轉換時區） |

#### 衍生欄位（預處理後）
| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| `DateTime` | datetime64[ns, America/New_York] | 完整時間戳 |
| `Year` | int | 年份 |
| `Month` | int | 月份 (1-12) |
| `Day` | int | 日期 (1-31) |
| `Hour` | int | 小時 (0-23) |
| `DayOfWeek` | int | 星期幾 (0=週一, 6=週日) |
| `DayName` | str | 星期名稱 |
| `YearMonth` | Period[M] | 年月 (e.g., 2025-09) |

### 金額欄位

| 欄位名稱 | 原始格式 | 處理後格式 | 說明 |
|---------|---------|-----------|------|
| `amount` | int (cents) | float (dollars) | 總金額（含稅） |
| `total_amount` | int (cents) | float (dollars) | 總金額（含稅） |
| `Gross Sales` | "$X.XX" | float | 總銷售額 |
| `Net Sales` | "$X.XX" | float | 淨銷售額 |
| `Tax` | "$X.XX" | float | 稅金 |
| `Discounts` | "$X.XX" | float | 折扣金額 |
| `Tip` | "$X.XX" | float | 小費 |

#### 金額解析規則
```python
# 從字串解析
df['Net Sales'] = df['Net Sales'].replace('[\$,]', '', regex=True).astype(float)

# 從 cents 轉換
df['amount_dollars'] = df['amount'] / 100

# 計算淨銷售額（扣稅）
NYC_TAX_RATE = 0.08875
df['Net Sales'] = df['amount'] / (1 + NYC_TAX_RATE)
```

### 交易欄位

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| `id` / `payment_id` | str | 唯一交易 ID |
| `Transaction ID` | str | 交易 ID（CSV 格式） |
| `status` | str | 交易狀態 |
| `source_type` | str | 來源類型 |
| `card_brand` | str | 信用卡品牌 |

#### 有效交易狀態
- `COMPLETED`：已完成（**只處理此狀態**）
- `FAILED`：失敗（排除）
- `CANCELED`：取消（排除）

### 商品欄位

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| `Category` | str | 商品類別 |
| `Item` | str | 商品名稱 |
| `Qty` | int | 數量 |
| `Price` | float | 單價 |
| `Modifiers Applied` | str | 客製化選項 |

### 用餐偏好欄位

| 欄位名稱 | 可能值 | 說明 |
|---------|-------|------|
| `Dining Option` | `For Here`, `To Go`, `Delivery` | 用餐方式 |

---

## 預處理流程

### 步驟 1：載入數據
```python
df = pd.read_csv(file_path)
```

### 步驟 2：時區轉換
```python
import pytz

ny_tz = pytz.timezone('America/New_York')

# 若時間為 UTC
df['DateTime'] = pd.to_datetime(df['created_at'])
if df['DateTime'].dt.tz is None:
    df['DateTime'] = df['DateTime'].dt.tz_localize('UTC')
df['DateTime'] = df['DateTime'].dt.tz_convert(ny_tz)
```

### 步驟 3：提取時間組件
```python
df['Year'] = df['DateTime'].dt.year
df['Month'] = df['DateTime'].dt.month
df['Day'] = df['DateTime'].dt.day
df['Hour'] = df['DateTime'].dt.hour
df['DayOfWeek'] = df['DateTime'].dt.dayofweek
df['DayName'] = df['DateTime'].dt.day_name()
df['YearMonth'] = df['DateTime'].dt.to_period('M')
```

### 步驟 4：金額解析
```python
# 字串格式
for col in ['Gross Sales', 'Net Sales', 'Tax', 'Discounts']:
    if col in df.columns:
        df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

# Cents 格式
if 'amount' in df.columns:
    df['amount_dollars'] = df['amount'] / 100
```

### 步驟 5：狀態過濾
```python
df = df[df['status'] == 'COMPLETED']
```

### 步驟 6：營業日過濾
```python
OPERATING_DAYS = [0, 1, 4, 5]  # 週一、二、五、六
df = df[df['DayOfWeek'].isin(OPERATING_DAYS)]
```

### 步驟 7：月份過濾
```python
CLOSED_MONTHS = [6, 7]  # 6月、7月
df = df[~df['Month'].isin(CLOSED_MONTHS)]
```

### 步驟 8：去重
```python
df = df.drop_duplicates(subset=['id'])  # 或 'payment_id', 'Transaction ID'
```

---

## 常用計算公式

### 每小時平均營收
```python
# 避免營業日數不均的影響
hourly = df.groupby(['YearMonth', 'Hour']).agg({
    'Net Sales': 'sum',
    'DateTime': lambda x: x.dt.date.nunique()  # 營業日數
}).reset_index()

hourly['Avg_Daily_Revenue'] = hourly['Net Sales'] / hourly['DateTime']
```

### 客戶分群
```python
customer_stats = df.groupby('customer_id').agg({
    'id': 'count',           # 造訪次數
    'Net Sales': 'sum'       # 累計消費
}).reset_index()

customer_stats['segment'] = customer_stats.apply(
    lambda x: 'VIP' if (x['id'] > 10 or x['Net Sales'] > 200) else
              'Regular' if x['id'] >= 3 else 'Occasional',
    axis=1
)
```

### AOV（平均訂單價值）
```python
aov = df['Net Sales'].sum() / df['id'].nunique()
```

---

## 輸出格式

### JSON 報告
```json
{
  "analysis_type": "full_analysis",
  "timestamp": "2025-01-15T10:30:00",
  "data_info": {
    "total_records": 9347,
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-11-15"
    }
  },
  "results": { ... },
  "insights": [ ... ],
  "recommendations": [ ... ]
}
```

### Markdown 報告
```markdown
# 營收分析報告

## 數據概述
- 總記錄數：9,347
- 時間範圍：2025-01-01 ~ 2025-11-15

## 銷售分析
...

## 關鍵洞察
1. ...
2. ...

## 建議
1. ...
2. ...
```

### CSV 匯出
- 欄位：保持原始欄位名稱
- 編碼：UTF-8 with BOM（Excel 相容）
- 日期格式：ISO 8601
