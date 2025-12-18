# 客戶集群分析方案比較報告

**生成時間**: 20251115_230403
**比較方案**: 方案 A (優化特徵) vs 方案 B (RFM)

---

## 🏆 評估指標對比

| 指標 | 方案 A | 方案 B | 優勝 |
|------|-------|-------|------|
| **Silhouette Score** | 0.4351 | 0.6234 | **方案 B** ⭐ |
| **Davies-Bouldin Index** | 0.8811 | 0.6297 | **方案 B** ⭐ |
| **特徵數量** | 5 | 3 | 方案 B（更簡潔） |
| **集群數量** | 3 | 3 | 相同 (K=3) |
| **總客戶數** | 1281 | 1281 | 相同 |

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

| 集群 | 名稱 | 客戶數 | 佔比 | 交易次數 | 總消費 |
|------|------|-------|------|---------|--------|
| 0 | 活躍客戶 | 845 | 66.0% | 1.16 | $26.94 |
| 1 | 活躍客戶 | 5 | 0.4% | 1.20 | $22.14 |
| 2 | VIP 忠誠客戶 | 431 | 33.6% | 4.65 | $104.03 |


**使用特徵**: transaction_count, total_spending, purchase_frequency, tip_frequency, card_usage_ratio

### 方案 B：RFM 分析（3 特徵）

| 集群 | 名稱 | 客戶數 | 佔比 | Recency | Frequency | Monetary |
|------|------|-------|------|---------|-----------|----------|
| 0 | VIP 忠誠客戶 | 787 | 61.4% | 47天 | 1.96次 | $43.60 |
| 1 | VIP 忠誠客戶 | 434 | 33.9% | 251天 | 1.58次 | $34.49 |
| 2 | VIP 忠誠客戶 | 60 | 4.7% | 34天 | 12.68次 | $307.22 |


**使用特徵**: recency, frequency, monetary

---

## 💡 關鍵發現

### 方案 A 的特點

**優勢：**
- 包含更多行為特徵（小費、支付方式）
- 能捕捉細緻的客戶行為差異

**劣勢：**
- Silhouette Score 僅 0.4351（中等水平）
- 集群分離度不夠明顯
- 特徵較多，可能存在噪音

### 方案 B 的特點

**優勢：**
- ⭐ **Silhouette Score 達到 0.6234**（良好水平）
- ⭐ **Davies-Bouldin Index 僅 0.6297**（優秀）
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
   - Silhouette Score 提升 43.3%（0.4351 → 0.6234）
   - Davies-Bouldin Index 降低 28.5%（0.8811 → 0.6297）

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

### 集群 0: VIP 忠誠客戶（61.4%）
- **Recency**: 47 天（近期消費）
- **Frequency**: 2.0 次
- **Monetary**: $43.60
- **策略**: 保持互動，鼓勵復購

### 集群 1: VIP 忠誠客戶（33.9%）
- **Recency**: 251 天（較久未消費）⚠️
- **Frequency**: 1.6 次
- **Monetary**: $34.49
- **策略**: 召回優惠，重新激活

### 集群 2: VIP 忠誠客戶（4.7%）
- **Recency**: 34 天（非常近期）
- **Frequency**: 12.7 次（超高頻率）⭐
- **Monetary**: $307.22（超高消費）⭐
- **策略**: 專屬服務，重點維護

---

## 🚀 後續行動建議

### 立即執行

1. **採用方案 B（RFM）作為主要客戶分層依據**
2. **針對 60 位超級 VIP（集群 2）建立專屬服務**
3. **召回 434 位流失風險客戶（集群 1）**

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

