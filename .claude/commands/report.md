# /report - 報告生成命令

根據已有的分析結果生成格式化報告，支援多種輸出格式。

## 使用方式

```
/report [報告類型] [--format 格式] [--output 輸出路徑]
```

## 參數說明

- `報告類型`：
  - `full`：完整分析報告（預設）
  - `sales`：銷售分析報告
  - `customer`：客戶分析報告
  - `financial`：財務分析報告
  - `break-even`：損益平衡報告
- `--format`：輸出格式（`json`、`markdown`、`csv`、`all`）
- `--output`：自訂輸出路徑

## 報告類型詳情

### 完整分析報告 (full)

整合所有分析模組的結果：

```markdown
# Taiwanway 營收分析完整報告

## 1. 執行摘要
- 關鍵指標總覽
- 重要發現
- 優先建議

## 2. 銷售趨勢分析
- 時間維度分析
- 產品類別分析
- 成長趨勢

## 3. 客戶行為分析
- 客戶分群
- 消費模式
- 價值分布

## 4. 財務指標分析
- 營收指標
- 交易指標
- 稅務分析

## 5. 營運建議
- 短期行動
- 中期規劃
- 長期策略

## 附錄
- 數據來源
- 計算方法
- 術語說明
```

### 銷售分析報告 (sales)

專注於銷售趨勢和模式：

- 每小時營收分布
- 每日營收趨勢
- 月度營收統計
- 熱門產品排行
- 類別銷售佔比

### 客戶分析報告 (customer)

專注於客戶行為洞察：

- 客戶分群分析
- RFM 指標
- 用餐偏好
- 消費頻率分布
- VIP 客戶特徵

### 財務分析報告 (financial)

專注於財務健康指標：

- 營收分析
- 平均客單價趨勢
- 交易量分析
- 稅務統計
- Pareto 分析

### 損益平衡報告 (break-even)

專注於成本和盈虧分析：

- 損益平衡點
- 敏感度分析
- 利潤目標
- 情境比較
- 風險評估

## 執行流程

### Step 1: 檢查分析結果

確認是否有可用的分析結果：

```
agents/output/results/
├── sales_analysis_*.json
├── customer_analysis_*.json
├── financial_analysis_*.json
└── break_even_*.json
```

### Step 2: 載入結果

讀取最新的分析結果檔案。

### Step 3: 格式化報告

根據指定格式生成報告：

#### JSON 格式
- 完整數據結構
- 便於程式化讀取
- 包含所有計算結果

#### Markdown 格式
- 人類可讀
- 包含圖表連結
- 適合分享和展示

#### CSV 格式
- 表格數據
- 便於 Excel 開啟
- 適合進一步分析

### Step 4: 輸出檔案

預設輸出位置：
```
agents/output/reports/
├── full_analysis_report_{timestamp}.json
├── full_analysis_summary_{timestamp}.md
└── data/
    ├── hourly_sales_{timestamp}.csv
    ├── monthly_sales_{timestamp}.csv
    └── customer_segments_{timestamp}.csv
```

## 輸出範例

### JSON 格式

```json
{
  "report_type": "full",
  "generated_at": "2025-11-16T10:30:00",
  "data_range": {
    "start": "2025-09-01",
    "end": "2025-11-15"
  },
  "executive_summary": {
    "total_revenue": 33885.50,
    "total_transactions": 1832,
    "avg_daily_revenue": 753.01,
    "key_findings": [...],
    "recommendations": [...]
  },
  "detailed_analysis": {
    "sales": {...},
    "customer": {...},
    "financial": {...}
  }
}
```

### Markdown 格式

```markdown
# Taiwanway 營收分析報告

**報告生成時間**：2025-11-16 10:30:00
**數據範圍**：2025-09-01 ~ 2025-11-15

---

## 執行摘要

### 關鍵指標

| 指標 | 數值 | 說明 |
|-----|------|------|
| 總營收 | $33,885.50 | 稅後淨額 |
| 交易筆數 | 1,832 | 已完成交易 |
| 日均營收 | $753.01 | 45 營業日平均 |
| 平均客單價 | $18.50 | 穩定成長中 |

### 重要發現

1. 午餐尖峰（12:00-13:00）貢獻 25% 營收
2. VIP 客戶（15%）貢獻 45% 營收
3. 11 月營收較 9 月下滑 22%

### 優先建議

- 🔴 **緊急**：關注 11 月營收下滑
- 🟡 **重要**：推動 VIP 會員計劃
- 🟢 **建議**：優化午餐時段出餐效率

---

[完整分析內容...]

---

*報告生成：Claude Code Agent System*
```

## 進階選項

### 指定時間範圍

```
/report full --from 2025-09-01 --to 2025-09-30
```

### 包含圖表

```
/report full --include-charts
```

### 多語言輸出

```
/report full --lang en  # 英文報告
/report full --lang zh  # 中文報告（預設）
```

### 比較報告

```
/report compare --periods "2025-09,2025-10,2025-11"
```

## 錯誤處理

- **無分析結果**：提示先執行 `/analyze` 命令
- **結果過期**：提示結果已超過 7 天，建議重新分析
- **格式不支援**：列出支援的格式選項
- **輸出路徑無效**：使用預設路徑並提示

## 相關命令

- `/analyze`：執行完整分析
- `/break-even`：損益平衡分析
