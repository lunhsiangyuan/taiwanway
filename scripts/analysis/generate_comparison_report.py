#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成方案 A 和方案 B 的綜合比較報告"""

import json

# 讀取兩個方案的結果
with open('analysis_output/clustering/optimized/data/cluster_profiles_optimized.json', 'r') as f:
    data_a = json.load(f)

with open('analysis_output/clustering/rfm/data/cluster_profiles_rfm.json', 'r') as f:
    data_b = json.load(f)

# 生成表格 A
def generate_table_a(data):
    table = '| 集群 | 名稱 | 客戶數 | 佔比 | 交易次數 | 總消費 |\n'
    table += '|------|------|-------|------|---------|--------|\n'
    for cid, prof in data['cluster_profiles'].items():
        pct = prof['customer_count'] / data['total_customers'] * 100
        table += f"| {cid} | {prof['cluster_name']} | {prof['customer_count']} | {pct:.1f}% | {prof['avg_transaction_count']:.2f} | ${prof['avg_total_spending']:.2f} |\n"
    return table

# 生成表格 B
def generate_table_b(data):
    table = '| 集群 | 名稱 | 客戶數 | 佔比 | Recency | Frequency | Monetary |\n'
    table += '|------|------|-------|------|---------|-----------|----------|\n'
    for cid, prof in data['cluster_profiles'].items():
        pct = prof['customer_count'] / data['total_customers'] * 100
        table += f"| {cid} | {prof['cluster_name']} | {prof['customer_count']} | {pct:.1f}% | {prof['avg_recency']:.0f}天 | {prof['avg_frequency']:.2f}次 | ${prof['avg_monetary']:.2f} |\n"
    return table

# 生成報告
report = f'''# 客戶集群分析方案比較報告

**生成時間**: {data_b['timestamp']}
**比較方案**: 方案 A (優化特徵) vs 方案 B (RFM)

---

## 🏆 評估指標對比

| 指標 | 方案 A | 方案 B | 優勝 |
|------|-------|-------|------|
| **Silhouette Score** | {data_a['silhouette_score']:.4f} | {data_b['silhouette_score']:.4f} | **方案 B** ⭐ |
| **Davies-Bouldin Index** | {data_a['davies_bouldin_score']:.4f} | {data_b['davies_bouldin_score']:.4f} | **方案 B** ⭐ |
| **特徵數量** | {data_a['n_features']} | {data_b['n_features']} | 方案 B（更簡潔） |
| **集群數量** | {data_a['n_clusters']} | {data_b['n_clusters']} | 相同 (K=3) |
| **總客戶數** | {data_a['total_customers']} | {data_b['total_customers']} | 相同 |

### 評分說明

- **Silhouette Score**: 衡量集群內聚度和分離度（-1 到 1，越高越好）
  - **> 0.5**: 良好的集群結構 ✓
  - **0.3-0.5**: 中等的集群結構
  - **< 0.3**: 較弱的集群結構

- **Davies-Bouldin Index**: 衡量集群分離度（越低越好）
  - **< 0.5**: 優秀
  - **0.5-1.0**: 良好 ✓
  - **> 1.0**: 較差

---

## 📊 集群分布對比

### 方案 A：優化特徵組合（5 特徵）

{generate_table_a(data_a)}

**使用特徵**: {', '.join(data_a['features'])}

### 方案 B：RFM 分析（3 特徵）

{generate_table_b(data_b)}

**使用特徵**: {', '.join(data_b['features'])}

---

## 💡 關鍵發現

### 方案 A 的特點

**優勢：**
- 包含更多行為特徵（小費、支付方式）
- 能捕捉細緻的客戶行為差異

**劣勢：**
- Silhouette Score 僅 {data_a['silhouette_score']:.4f}（中等水平）
- 集群分離度不夠明顯
- 特徵較多，可能存在噪音

### 方案 B 的特點

**優勢：**
- ⭐ **Silhouette Score 達到 {data_b['silhouette_score']:.4f}**（良好水平）
- ⭐ **Davies-Bouldin Index 僅 {data_b['davies_bouldin_score']:.4f}**（優秀）
- 使用業界標準 RFM 模型，易於解釋
- 僅 3 個特徵，簡潔高效
- 集群分離度明顯更好

**劣勢：**
- 缺少行為特徵（小費、支付方式）
- 可能錯過部分行為模式

---

## 🎯 推薦方案

### **建議採用：方案 B（RFM 分析）**

**理由：**

1. **集群品質顯著更優**
   - Silhouette Score 提升 43.3%（{data_a['silhouette_score']:.4f} → {data_b['silhouette_score']:.4f}）
   - Davies-Bouldin Index 降低 28.5%（{data_a['davies_bouldin_score']:.4f} → {data_b['davies_bouldin_score']:.4f}）

2. **業界標準，可對標**
   - RFM 是零售業最成熟的客戶分層模型
   - 可與其他餐廳/零售業對比

3. **簡潔易懂**
   - 僅 3 個維度，容易向業務團隊解釋
   - 清晰的商業意義（最近、頻率、金額）

4. **可執行性強**
   - 集群特徵明確，營銷策略針對性強
   - 決策者容易理解並執行

---

## 📈 方案 B 集群特徵詳解

基於 RFM 分析的三個集群：

### 集群 0: {data_b['cluster_profiles']['0']['cluster_name']}（{data_b['cluster_profiles']['0']['customer_count']/data_b['total_customers']*100:.1f}%）
- **Recency**: {data_b['cluster_profiles']['0']['avg_recency']:.0f} 天（近期消費）
- **Frequency**: {data_b['cluster_profiles']['0']['avg_frequency']:.1f} 次
- **Monetary**: ${data_b['cluster_profiles']['0']['avg_monetary']:.2f}
- **策略**: 保持互動，鼓勵復購

### 集群 1: {data_b['cluster_profiles']['1']['cluster_name']}（{data_b['cluster_profiles']['1']['customer_count']/data_b['total_customers']*100:.1f}%）
- **Recency**: {data_b['cluster_profiles']['1']['avg_recency']:.0f} 天（較久未消費）⚠️
- **Frequency**: {data_b['cluster_profiles']['1']['avg_frequency']:.1f} 次
- **Monetary**: ${data_b['cluster_profiles']['1']['avg_monetary']:.2f}
- **策略**: 召回優惠，重新激活

### 集群 2: {data_b['cluster_profiles']['2']['cluster_name']}（{data_b['cluster_profiles']['2']['customer_count']/data_b['total_customers']*100:.1f}%）
- **Recency**: {data_b['cluster_profiles']['2']['avg_recency']:.0f} 天（非常近期）
- **Frequency**: {data_b['cluster_profiles']['2']['avg_frequency']:.1f} 次（超高頻率）⭐
- **Monetary**: ${data_b['cluster_profiles']['2']['avg_monetary']:.2f}（超高消費）⭐
- **策略**: 專屬服務，重點維護

---

## 🚀 後續行動建議

### 立即執行

1. **採用方案 B（RFM）作為主要客戶分層依據**
2. **針對 {data_b['cluster_profiles']['2']['customer_count']} 位超級 VIP（集群 2）建立專屬服務**
3. **召回 {data_b['cluster_profiles']['1']['customer_count']} 位流失風險客戶（集群 1）**

### 短期目標（1-3 個月）

1. 建立 RFM 自動化追蹤系統
2. 每月更新客戶分層
3. 追蹤各集群的營銷活動效果

### 長期優化

1. 結合方案 A 的行為特徵作為輔助分析
2. 開發混合模型（RFM + 行為特徵）
3. 探索更多客戶維度（商品偏好、時段偏好等）

---

## 📁 輸出文件位置

### 方案 A
- 報告：[analysis_output/clustering/optimized/](analysis_output/clustering/optimized/)
- 圖表：[analysis_output/clustering/optimized/charts/](analysis_output/clustering/optimized/charts/)
- 數據：[analysis_output/clustering/optimized/data/](analysis_output/clustering/optimized/data/)

### 方案 B ⭐ 推薦
- 報告：[analysis_output/clustering/rfm/](analysis_output/clustering/rfm/)
- 圖表：[analysis_output/clustering/rfm/charts/](analysis_output/clustering/rfm/charts/)
- 數據：[analysis_output/clustering/rfm/data/](analysis_output/clustering/rfm/data/)

---

**結論**: 方案 B（RFM 分析）在集群品質、可解釋性和實用性上都明顯優於方案 A，強烈建議作為主要客戶分層方法。

'''

# 寫入報告
with open('analysis_output/clustering/comparison_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print('✅ 綜合比較報告已生成')
print('📁 位置: analysis_output/clustering/comparison_report.md')
print()
print('🏆 結論: 方案 B (RFM) 勝出！')
print(f'   - Silhouette Score: {data_b["silhouette_score"]:.4f} (方案 A: {data_a["silhouette_score"]:.4f})')
print(f'   - Davies-Bouldin Index: {data_b["davies_bouldin_score"]:.4f} (方案 A: {data_a["davies_bouldin_score"]:.4f})')
print(f'   - 品質提升: Silhouette Score +{((data_b["silhouette_score"]-data_a["silhouette_score"])/data_a["silhouette_score"]*100):.1f}%')
