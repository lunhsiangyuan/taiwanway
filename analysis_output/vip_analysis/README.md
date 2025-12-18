# VIP 和高消費客戶分析系統文檔

## 系統概述

本分析系統專門用於深入分析 VIP 客戶和高單筆消費客戶的消費型態、時間偏好、場景選擇和商品組合。

## 執行方式

```bash
python3 scripts/analysis/analyze_vip_high_spenders.py
```

## 分析架構

```
數據載入
  │
  ├─ 讀取商品明細數據 (items CSV)
  ├─ 時區轉換 (Taipei → New York)
  └─ 提取時間特徵
  │
  ▼
客戶與交易分群
  │
  ├─ VIP 客戶識別
  │   ├─ 按 Customer ID 聚合
  │   ├─ 計算造訪次數與總消費
  │   └─ 應用 VIP 規則
  │
  └─ 高消費交易識別
      ├─ 按 Transaction ID 聚合
      └─ 篩選單筆 ≥ $50 的交易
  │
  ▼
深度分析
  │
  ├─ VIP 客戶分析
  │   ├─ 商品偏好分析
  │   ├─ 時間型態分析
  │   └─ 場景偏好分析
  │
  └─ 高消費交易分析
      ├─ 商品組合分析
      ├─ 時間分布分析
      └─ 場景特徵分析
  │
  ▼
輸出結果
  │
  ├─ JSON 報告
  ├─ CSV 數據
  ├─ Markdown 摘要
  └─ 視覺化圖表
```

---

## 核心函數文檔

### 函數：`load_and_preprocess_data()`

#### 功能說明
載入商品明細 CSV 數據並進行預處理,包含時區轉換和時間特徵提取。

#### 計算邏輯
1. 讀取 CSV 檔案
2. 解析 Date 和 Time 欄位為 DateTime
3. 從 Taipei 時區轉換到 New York 時區(自動處理 DST)
4. 提取時間特徵:Hour, DayOfWeek, DayName, Month, YearMonth
5. 解析貨幣欄位(移除 $ 符號並轉為浮點數)

#### 輸入變量
- `items_csv_path`: str - 商品明細 CSV 檔案路徑
  - 必需欄位: Date, Time, Item, Category, Net Sales, Transaction ID, Customer ID, Dining Option

#### 輸出變量
- `df`: pandas.DataFrame
  - 新增欄位:
    - `DateTime`: datetime64[ns, America/New_York] - 轉換後的時間戳
    - `Hour`: int - 小時 (0-23)
    - `DayOfWeek`: int - 星期 (0=週一, 6=週日)
    - `DayName`: str - 星期名稱
    - `Month`: int - 月份 (1-12)
    - `YearMonth`: Period - 年月
    - `Date`: date - 日期

---

### 函數：`identify_vip_customers()`

#### 功能說明
識別符合 VIP 標準的客戶,標準為:造訪次數 > 10 次 **或** 總消費 > $200。

#### 計算邏輯
```
1. 篩選有 Customer ID 的記錄
2. 按 Customer ID 分組統計:
   - VisitCount = nunique(Transaction ID)
   - TotalSpent = sum(Net Sales)
   - CustomerName = first(Customer Name)
3. 計算 AvgSpent = TotalSpent / VisitCount
4. 應用 VIP 規則(OR 邏輯):
   IF VisitCount > 10 OR TotalSpent > 200
   THEN 標記為 VIP
5. 按 TotalSpent 降序排序
```

#### 決策樹
```
開始
  │
  ▼
客戶有記錄? ──NO──► 跳過
  │
 YES
  │
  ▼
計算統計指標
  │
  ▼
VisitCount > 10 ──YES──► VIP 客戶
  │
 NO
  │
  ▼
TotalSpent > $200 ──YES──► VIP 客戶
  │
 NO
  │
  ▼
非 VIP 客戶
```

#### 輸入變量
- `df`: pandas.DataFrame - 預處理後的商品數據
  - 必需欄位: Customer ID, Transaction ID, Net Sales, Customer Name

#### 輸出變量
- `vip_customers`: pandas.DataFrame
  - 欄位:
    - `CustomerID`: str - 客戶 ID
    - `VisitCount`: int - 造訪次數(唯一交易數)
    - `TotalSpent`: float - 總消費金額($)
    - `CustomerName`: str - 客戶名稱
    - `AvgSpent`: float - 平均每次消費($)

---

### 函數：`identify_high_transactions()`

#### 功能說明
識別單筆消費金額 ≥ $50 的高消費交易。

#### 計算邏輯
```
1. 按 Transaction ID 分組統計:
   - TotalAmount = sum(Net Sales)
   - ItemCount = count(Item)
   - 其他欄位 = first(...)
2. 篩選 TotalAmount >= 50
3. 按 TotalAmount 降序排序
```

#### 輸入變量
- `df`: pandas.DataFrame - 預處理後的商品數據
- `high_transaction_threshold`: float - 高消費閾值(預設 $50)

#### 輸出變量
- `high_transactions`: pandas.DataFrame
  - 欄位:
    - `TransactionID`: str - 交易 ID
    - `TotalAmount`: float - 交易總金額($)
    - `ItemCount`: int - 商品數量
    - `CustomerID`: str - 客戶 ID
    - `CustomerName`: str - 客戶名稱
    - `DateTime`: datetime - 交易時間
    - `DiningOption`: str - 用餐選項

---

### 函數：`analyze_vip_product_preferences()`

#### 功能說明
分析 VIP 客戶的商品偏好,包含最愛商品、類別和商品組合。

#### 計算邏輯
1. **Top 商品分析**:
   - 篩選 VIP 客戶的所有交易
   - 按 Item 分組統計購買次數(Qty)、營收(Net Sales)、交易數
   - 按購買次數降序排序,取 Top 20

2. **Top 類別分析**:
   - 按 Category 分組統計
   - 按營收降序排序

3. **商品組合分析**:
   - 識別同一交易中購買的多個商品
   - 計算兩兩組合出現的頻率
   - 返回最常見的 Top 15 組合

4. **客製化率**:
   - 計算有 Modifiers Applied 的記錄比例

#### 輸入變量
- `vip_customers`: DataFrame - VIP 客戶列表
- `df`: DataFrame - 完整商品數據

#### 輸出變量
- `results`: dict
  - `top_items`: list[dict] - Top 商品
  - `top_categories`: list[dict] - Top 類別
  - `common_combinations`: list[dict] - 常見組合
  - `customization_rate`: str - 客製化比例

---

### 函數：`analyze_vip_temporal_patterns()`

#### 功能說明
分析 VIP 客戶的時間消費型態,包含小時、星期、月份分布。

#### 計算邏輯
1. **小時分布**:
   - 按 Hour 分組統計交易數和營收
   - 範圍: 0-23

2. **星期分布**:
   - 按 DayName 分組統計
   - 保留星期順序

3. **月份分布**:
   - 按 Month 分組統計
   - 範圍: 1-12

公式:
```
TransactionCount(時段) = nunique(Transaction ID)
Revenue(時段) = sum(Net Sales)
```

#### 輸入變量
- `vip_transactions`: DataFrame - VIP 客戶的所有交易記錄

#### 輸出變量
- `results`: dict
  - `hourly_distribution`: list[dict] - 每小時統計
  - `weekday_distribution`: list[dict] - 每星期統計
  - `monthly_distribution`: list[dict] - 每月統計

---

### 函數：`analyze_vip_dining_preferences()`

#### 功能說明
分析 VIP 客戶的用餐場景偏好(For Here vs To Go)。

#### 計算邏輯
```
1. 按 Dining Option 分組統計:
   - TransactionCount = nunique(Transaction ID)
   - Revenue = sum(Net Sales)
2. 計算百分比:
   Percentage = (TransactionCount / TotalTransactionCount) × 100
```

#### 輸入變量
- `vip_transactions`: DataFrame - VIP 客戶的交易記錄

#### 輸出變量
- `results`: list[dict]
  - 每個 dict 包含:
    - `DiningOption`: str - For Here/To Go
    - `TransactionCount`: int - 交易次數
    - `Revenue`: float - 營收
    - `Percentage`: float - 百分比

---

### 函數：`analyze_high_transaction_patterns()`

#### 功能說明
分析高單筆消費交易的特徵,包含商品組合、時間分布和場景。

#### 計算邏輯
1. **商品組合**: 同 `_analyze_product_combinations()`
2. **類別分布**: 按 Category 統計數量和營收
3. **平均商品數**: mean(ItemCount)
4. **時間分布**: 按 Hour 統計交易數,找出尖峰時段
5. **場景分布**: 按 Dining Option 統計

#### 輸入變量
- `high_transactions`: DataFrame - 高消費交易列表
- `df`: DataFrame - 完整商品數據

#### 輸出變量
- `results`: dict
  - `common_combinations`: list[dict] - 常見組合
  - `category_distribution`: list[dict] - 類別分布
  - `avg_items_per_transaction`: float - 平均商品數
  - `peak_hour`: int - 尖峰時段
  - `dining_distribution`: dict - 場景分布

---

### 函數：`_analyze_product_combinations()`

#### 功能說明
分析同一交易中的商品兩兩組合,找出最常一起購買的商品。

#### 計算邏輯
```
1. 按 Transaction ID 分組,收集每筆交易的商品列表
2. 篩選出包含多個商品的交易(ItemCount > 1)
3. 對每筆交易:
   a. 去重並排序商品列表
   b. 生成所有可能的兩兩組合 C(n,2)
   c. 組合名稱格式: "商品A + 商品B"
4. 統計所有組合的出現次數
5. 返回 Top N 最常見組合
```

#### 演算法範例
```
交易 1: [麵, 飯, 飲料]
  組合: [麵 + 飯, 麵 + 飲料, 飯 + 飲料]

交易 2: [麵, 飯]
  組合: [麵 + 飯]

合併統計:
  麵 + 飯: 2次
  麵 + 飲料: 1次
  飯 + 飲料: 1次
```

#### 輸入變量
- `df`: DataFrame - 交易商品數據
- `top_n`: int - 返回前 N 個組合(預設 10)

#### 輸出變量
- `top_combos`: list[dict]
  - 每個 dict 包含:
    - `combination`: str - 商品組合名稱
    - `count`: int - 出現次數

---

## 視覺化圖表

### 1. `vip_top_items.png`
- **類型**: 橫向條形圖
- **內容**: VIP 客戶最常購買的 Top 15 商品
- **Y軸**: 商品名稱
- **X軸**: 購買次數

### 2. `vip_temporal_patterns.png`
- **類型**: 雙子圖
- **左圖**: 小時分布條形圖
  - X軸: 小時 (0-23)
  - Y軸: 交易次數
- **右圖**: 星期分布條形圖
  - X軸: 星期 (一~日)
  - Y軸: 交易次數

### 3. `vip_comparison.png`
- **類型**: 雙子圖
- **左圖**: VIP vs 非VIP 交易次數餅圖
- **右圖**: VIP vs 非VIP 平均交易額條形圖

### 4. `high_transaction_analysis.png`
- **類型**: 雙子圖
- **左圖**: 高消費交易 Top 類別(按營收)橫向條形圖
- **右圖**: 高消費交易時段分布條形圖

---

## 輸出檔案結構

```
analysis_output/vip_analysis/
├── charts/                                    # 視覺化圖表
│   ├── vip_top_items.png
│   ├── vip_temporal_patterns.png
│   ├── vip_comparison.png
│   └── high_transaction_analysis.png
│
├── data/                                      # 數據檔案
│   ├── vip_customers.csv                     # VIP 客戶明細
│   ├── high_transactions.csv                 # 高消費交易明細
│   └── vip_analysis_report_YYYYMMDD_HHMMSS.json  # 完整 JSON 報告
│
├── VIP_Analysis_Summary_YYYYMMDD.md          # Markdown 摘要報告
└── README.md                                  # 本文檔
```

---

## 配置參數

### 可調整參數

```python
VIPHighSpenderAnalyzer(
    items_csv_path='...',               # 商品明細 CSV 路徑
    vip_visit_threshold=10,             # VIP 最低造訪次數
    vip_spending_threshold=200,         # VIP 最低總消費($)
    high_transaction_threshold=50       # 高消費交易閾值($)
)
```

### VIP 判斷邏輯

```
VIP 客戶 = (造訪次數 > vip_visit_threshold) OR (總消費 > vip_spending_threshold)
```

**注意**: 使用 **OR** 邏輯,滿足任一條件即可成為 VIP。

---

## 使用範例

### 基本使用

```python
from analyze_vip_high_spenders import VIPHighSpenderAnalyzer

# 初始化分析器
analyzer = VIPHighSpenderAnalyzer(
    items_csv_path='data/items-2025-01-01-2025-11-16.csv',
    vip_visit_threshold=10,
    vip_spending_threshold=200,
    high_transaction_threshold=50
)

# 執行完整分析
report = analyzer.run_full_analysis()
```

### 自訂參數

```python
# 更嚴格的 VIP 標準
analyzer = VIPHighSpenderAnalyzer(
    items_csv_path='data/items.csv',
    vip_visit_threshold=20,          # 提高到 20 次
    vip_spending_threshold=500,      # 提高到 $500
    high_transaction_threshold=100   # 提高到 $100
)
```

### 單獨執行特定分析

```python
# 載入數據
analyzer.load_and_preprocess_data()

# 識別 VIP
analyzer.identify_vip_customers()

# 只分析商品偏好
product_prefs = analyzer.analyze_vip_product_preferences()
print(product_prefs['top_items'])
```

---

## 分析結果摘要(實際執行結果)

### VIP 客戶概況

- **VIP 客戶數量**: 46 位
- **VIP 總營收**: $15,713.53
- **平均造訪次數**: 15.5 次
- **平均總消費**: $341.60

### VIP 客戶最愛商品 Top 5

1. **麵 Noodles** - 購買 137 次,營收 $2,200.96
2. **飯 Rice** - 購買 110 次,營收 $1,519.40
3. **滷肉飯Pork Rice** - 購買 108 次,營收 $1,173.86
4. **Custom Amount** - 購買 93 次,營收 $1,249.99
5. **牛肉麵 Beef Noodles** - 購買 76 次,營收 $1,084.20

### VIP 客戶時間偏好

- **尖峰時段**: 18:00
- **偏好星期**: Friday
- **場景偏好**: For Here (52.5%)

### 高消費交易概況

- **交易數量**: 223 筆
- **總金額**: $15,404.42
- **平均交易額**: $69.08
- **平均商品數**: 4.3 個

### 高消費常見組合 Top 5

1. 飯 Rice + 麵 Noodles (54 次)
2. Custom Amount + 麵 Noodles (17 次)
3. 滷肉飯Pork Rice + 牛肉麵 Beef Noodles (13 次)
4. Combo--- Pork Rice + Bubble Tea + Combo--- noodles + Bubble Tea (9 次)
5. Custom Amount + 飯 Rice (9 次)

---

## 技術細節

### 時區處理

- **原始數據時區**: Asia/Taipei
- **目標時區**: America/New_York
- **處理方式**: 使用 `pytz` 自動處理夏令時(DST)切換

### 數據過濾

目前分析**不過濾**營業時間,以獲得完整客戶行為視角。如需過濾:

```python
# 在 load_and_preprocess_data() 中加入:
df = df[df['DayOfWeek'].isin([0, 1, 4, 5])]  # 只保留營業日
df = df[(df['Hour'] >= 10) & (df['Hour'] <= 20)]  # 只保留營業時間
df = df[~df['Month'].isin([6, 7])]  # 排除休業月份
```

### 性能特徵

對於 ~9,000 筆記錄:
- 數據載入: ~1 秒
- 分析執行: ~2 秒
- 視覺化生成: ~3 秒
- **總執行時間**: ~6 秒

---

## 疑難排解

### 問題: 中文字體顯示為方框

**解決方案**:
```bash
# 清除 matplotlib 字體快取
rm -rf ~/.matplotlib/fontlist-*.json
```

### 問題: 時區轉換不正確

**檢查**:
- 確認原始數據的時區是否為 Taipei
- 檢查 DST 切換時期的數據

### 問題: 記憶體不足

**解決方案**:
- 分批處理數據
- 減少視覺化圖表的 DPI(預設 300)

---

## 未來擴展方向

1. **RFM 分析**: 加入 Recency, Frequency, Monetary 模型
2. **客戶生命週期**: 追蹤客戶從首次到最近消費的變化
3. **預測模型**: 預測客戶流失風險
4. **市場籃分析**: 更深入的關聯規則挖掘(Apriori/FP-Growth)
5. **時間序列**: 分析客戶消費趨勢變化

---

## 參考文獻

- [VIP_ANALYSIS_LOGIC.txt](../../agents/VIP_ANALYSIS_LOGIC.txt) - VIP 分群邏輯圖解
- [agents/customer_behavior_agent.py](../../agents/customer_behavior_agent.py) - 原始客戶分析代理

---

**最後更新**: 2025-11-15
**維護者**: Claude Code
**版本**: 1.0.0
