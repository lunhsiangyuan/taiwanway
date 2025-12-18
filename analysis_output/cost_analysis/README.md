# Taiwanway 成本結構與人力配置分析

本目錄包含所有成本結構與人力配置分析的相關內容。

## 目錄結構

```
cost_analysis/
├── README.md                    # 本說明文件
├── charts/                      # 圖表目錄
│   ├── labor_schedule_chart.png          # 人力配置時段圖
│   ├── cost_structure_chart.png          # 成本結構堆疊圖
│   ├── cost_pie_chart.png               # 成本佔比餅圖
│   ├── profit_trend_chart.png           # 利潤趨勢圖
│   └── break_even_analysis.png          # 損益平衡分析圖
├── data/                        # 數據目錄
│   ├── cost_structure_analysis.csv      # 成本結構分析數據（CSV）
│   ├── cost_structure_analysis.json     # 成本結構分析數據（JSON）
│   └── labor_schedule.json              # 人力配置數據
└── reports/                     # 報告目錄
    └── cost_analysis_summary.txt        # 文字摘要報告
```

## 成本參數設定

- **每小時人力成本**: $15
- **房租保險水電**: $4,000/月
- **食材包材成本率**: 35%
- **人力配置預算**: $3,300/月（13.5人時/天）

## 圖表說明

### 1. 人力配置時段圖 (labor_schedule_chart.png)
展示每日各時段的人力配置，區分全職與兼職員工，並標註每時段的總人數和成本。

### 2. 成本結構堆疊圖 (cost_structure_chart.png)
各月份成本結構對比，包含食材包材、人力成本、房租水電和淨利潤，並顯示總營收參考線。

### 3. 成本佔比餅圖 (cost_pie_chart.png)
- 左圖：成本結構餅圖（顯示各項成本佔比）
- 右圖：營收分配餅圖（顯示營收如何分配）

### 4. 利潤趨勢圖 (profit_trend_chart.png)
- 營收柱狀圖
- 淨利潤折線圖
- 利潤率折線圖（右軸）
- 標註獲利/虧損區間

### 5. 損益平衡分析圖 (break_even_analysis.png)
展示不同營業日數下的損益平衡點，標註實際數據點，並顯示獲利/虧損區域。

## 數據文件說明

### cost_structure_analysis.csv / .json
包含各月份的成本結構分析數據：
- 月份
- 營業日數
- 總營收
- 食材包材成本
- 人力成本
- 房租保險水電
- 總成本
- 淨利潤
- 利潤率

### labor_schedule.json
包含人力配置相關數據：
- 每日人力配置（人時）
- 每日人力成本
- 月人力預算
- 每小時人力成本
- 詳細時段配置表

## 報告說明

### cost_analysis_summary.txt
文字格式的完整分析摘要，包含：
- 成本參數設定
- 人力配置摘要
- 各月份成本結構分析
- 報告生成時間

## 使用方法

執行分析腳本：
```bash
python3 scripts/analysis/analyze_cost_structure.py
```

所有輸出將自動儲存在本目錄中。

## 更新記錄

- 2025-01-XX: 初始版本，包含所有成本分析圖表和數據






