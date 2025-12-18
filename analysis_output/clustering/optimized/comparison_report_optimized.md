# 客戶集群分析報告 - 方案 A：優化特徵組合

**生成時間**: 20251115_230148
**方法**: 優化特徵組合（移除共線性和低區分度特徵）
**特徵數量**: 5 個
**集群數量**: K=3

---

## 方法說明

### 特徵選擇策略

**保留的 5 個核心特徵：**
1. transaction_count (交易次數 - Frequency)
2. total_spending (總消費 - Monetary)
3. purchase_frequency (購買頻率 - Frequency 變體)
4. tip_frequency (小費給予率 - 行為模式)
5. card_usage_ratio (信用卡使用率 - 支付偏好)

**移除的特徵及原因：**
- avg_spending：變異係數僅 0.164，與 total_spending 高度共線
- weekend_ratio：變異係數僅 0.390，區分度低
- avg_tip：與 tip_frequency 概念重複

---

## 評估指標

**集群品質：**
- **Silhouette Score**: 0.4351 ⚠️ 中等
- **Davies-Bouldin Index**: 0.8811 (越低越好)
- **總客戶數**: 1281 位

---

## 集群概覽


### 集群 0: 活躍客戶

**描述**: 購買頻率較高的穩定客戶

**規模**: 845 人 (66.0%)

**關鍵指標**:
- 平均交易次數: 1.16 次
- 平均總消費: $26.94
- 購買頻率: 1.1319 次/天
- 小費給予率: 35.2%
- 信用卡使用率: 100.0%

---

### 集群 1: 活躍客戶

**描述**: 購買頻率較高的穩定客戶

**規模**: 5 人 (0.4%)

**關鍵指標**:
- 平均交易次數: 1.20 次
- 平均總消費: $22.14
- 購買頻率: 0.8040 次/天
- 小費給予率: 10.0%
- 信用卡使用率: 10.0%

---

### 集群 2: VIP 忠誠客戶

**描述**: 高消費、高頻率的核心客戶群

**規模**: 431 人 (33.6%)

**關鍵指標**:
- 平均交易次數: 4.65 次
- 平均總消費: $104.03
- 購買頻率: 0.1004 次/天
- 小費給予率: 21.2%
- 信用卡使用率: 100.0%

---

## 輸出文件

- **圖表**: `analysis_output/clustering/optimized/charts/`
  - optimized_elbow_curve.png - 評估指標圖
  - optimized_cluster_analysis.png - 綜合分析圖

- **數據**: `analysis_output/clustering/optimized/data/`
  - cluster_profiles_optimized.json - 集群配置
  - cluster_summary_optimized.csv - 統計摘要
  - customer_clusters_optimized.csv - 客戶分配表

---

**分析方法**: K-means Clustering + StandardScaler
**隨機種子**: 42
