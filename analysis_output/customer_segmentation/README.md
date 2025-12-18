# 客戶分群比較分析報告

**生成時間**: 2025-12-03 22:13:16

---

## 執行摘要

本報告比較 Taiwanway 餐廳兩個時間段的客戶分群差異：
- **春季**: 2025-01-01 至 2025-05-31
- **秋季**: 2025-08-01 至 2025-12-01

### 核心發現

1. **客戶留存率**: 27.8%（253 位回頭客）
2. **新客戶**: 秋季新增 584 位新客戶
3. **流失客戶**: 656 位客戶未在秋季消費
4. **總客戶變化**: -72 人

---

## 分群概覽

### 春季分群（2025-01-01 - 2025-05-31）

| 分群 | 人數 | 占比 |
|------|------|------|
| 活躍客戶 | 471 | 51.8% |
| 潛在流失客戶 | 366 | 40.3% |
| VIP 忠誠客戶 | 72 | 7.9% |

**評估指標**:
- Silhouette Score: 0.2206
- Davies-Bouldin Index: 1.4965

### 秋季分群（2025-08-01 - 2025-12-01）

| 分群 | 人數 | 占比 |
|------|------|------|
| 活躍客戶 | 389 | 46.5% |
| 潛在流失客戶 | 363 | 43.4% |
| VIP 忠誠客戶 | 85 | 10.2% |

**評估指標**:
- Silhouette Score: 0.2218
- Davies-Bouldin Index: 1.4878

---

## RFM 指標變化

| 指標 | 春季平均 | 秋季平均 | 變化 | 變化率 |
|------|----------|----------|------|--------|
| Recency (天) | 55.41 | 60.30 | +4.89 | +8.8% |
| Frequency (次) | 2.41 | 2.11 | -0.30 | -12.3% |
| Monetary ($) | 47.81 | 44.94 | -2.87 | -6.0% |
| AOV ($) | 20.58 | 21.87 | +1.30 | +6.3% |
| Category Diversity | 2.65 | 2.48 | -0.17 | -6.3% |


---

## 客戶留存分析

| 指標 | 數值 |
|------|------|
| 春季總客戶 | 909 |
| 秋季總客戶 | 837 |
| 回頭客 | 253 |
| 新客戶（秋季） | 584 |
| 流失客戶 | 656 |
| **留存率** | **27.8%** |

---

## 消費時段偏好變化

| 時段 | 春季 | 秋季 | 變化 |
|------|------|------|------|
| 上午 (10-14) | 40.6% | 41.9% | +1.3% |
| 下午 (14-18) | 45.7% | 46.7% | +1.1% |
| 晚間 (18-21) | 13.8% | 11.4% | -2.4% |


---

## 分群人數變化

| 分群 | 春季 | 秋季 | 變化 |
|------|------|------|------|
| 活躍客戶 | 471 (51.8%) | 389 (46.5%) | -82 (-5.3%) |
| VIP 忠誠客戶 | 72 (7.9%) | 85 (10.2%) | +13 (+2.2%) |
| 潛在流失客戶 | 366 (40.3%) | 363 (43.4%) | -3 (+3.1%) |


---

## 分析方法

- **客戶識別**: Card Brand + PAN Suffix 代理 ID
- **特徵維度**: 擴展 RFM（6 維）
  - Recency: 最近購買距今天數
  - Frequency: 交易次數
  - Monetary: 總消費金額
  - Avg Order Value: 平均單次消費
  - Hour Preference: 最常消費時段
  - Category Diversity: 品項多樣性
- **分群算法**: K-means (K=3)
- **標準化**: StandardScaler

---

## 輸出檔案

### 數據檔案 (`analysis_output/customer_segmentation/data/`)
- `comparison_results.json` - 完整比較結果
- `spring_rfm_features.csv` - 春季客戶特徵
- `fall_rfm_features.csv` - 秋季客戶特徵
- `customer_transition.csv` - 分群轉移矩陣

### 視覺化圖表 (`analysis_output/customer_segmentation/charts/`)
1. `fig01_cluster_distribution.png` - 分群分布對比
2. `fig02_cluster_size_change.png` - 分群人數變化
3. `fig03_rfm_radar.png` - RFM 雷達圖
4. `fig04_retention_analysis.png` - 客戶留存分析
5. `fig05_hour_preference.png` - 時段偏好變化
6. `fig06_frequency_distribution.png` - 頻率分布
7. `fig07_monetary_distribution.png` - 消費金額分布
8. `fig08_aov_comparison.png` - AOV 對比
9. `fig09_category_diversity.png` - 品項多樣性
10. `fig10_cluster_heatmap.png` - 分群熱力圖
11. `fig11_transition_matrix.png` - 轉移矩陣
12. `fig12_dashboard.png` - 綜合儀表板

---

**分析完成時間**: 2025-12-03 22:13:16
