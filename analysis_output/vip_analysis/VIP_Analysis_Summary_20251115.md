# VIP 和高消費客戶分析報告

生成時間: 2025-11-15T13:18:29.556580

## 📋 分析參數

- VIP 客戶定義: 造訪次數 > 10 或 總消費 > $200
- 高消費交易定義: 單筆交易 ≥ $50

---

## 🌟 VIP 客戶分析

### 基本統計

- **VIP 客戶數量**: 46 位
- **VIP 總營收**: $15,713.53
- **平均造訪次數**: 15.5 次
- **平均總消費**: $341.60

### 商品偏好

**最受歡迎的商品 Top 5:**

1. **麵 Noodles** - 購買 137 次,營收 $2,200.96
2. **飯 Rice** - 購買 110 次,營收 $1,519.40
3. **滷肉飯Pork Rice** - 購買 108 次,營收 $1,173.86
4. **Custom Amount** - 購買 93 次,營收 $1,249.99
5. **牛肉麵 Beef Noodles** - 購買 76 次,營收 $1,084.20

**最受歡迎的類別:**

1. **餐點** - 營收 $3,267.58
2. **Combo Meals** - 營收 $2,037.35
3. **meals** - 營收 $1,965.52
4. **Rice / Noodles** - 營收 $1,538.29
5. **飲料 Drink** - 營收 $785.98

### 時間型態

**尖峰時段:** 10:00

**偏好星期:** 分布如下圖表

### 用餐場景偏好

- **For Here**: 52.5% (171 筆交易)
- **To Go**: 47.5% (155 筆交易)

---

## 💰 高消費交易分析

### 基本統計

- **高消費交易數量**: 223 筆
- **總金額**: $15,404.42
- **平均交易額**: $69.08
- **平均商品數**: 4.3 個

### 商品組合特徵

**常見組合 Top 10:**

1. 飯 Rice + 麵 Noodles (出現 54 次)
2. Custom Amount + 麵 Noodles (出現 17 次)
3. 滷肉飯Pork Rice + 牛肉麵 Beef Noodles (出現 13 次)
4. Combo--- Pork Rice + Bubble Tea + Combo--- noodles + Bubble Tea (出現 9 次)
5. Custom Amount + 飯 Rice (出現 9 次)
6. Pork Rice + 麵 Noodles (出現 9 次)
7. Apple Jade Dew蘋果玉露青 + 麵 Noodles (出現 9 次)
8. Apple Jade Dew蘋果玉露青 + 飯 Rice (出現 9 次)
9. Combo--- noodles + Bubble Tea + 麵 Noodles (出現 8 次)
10. Pineapple Cake + 麵 Noodles (出現 8 次)

### 時間特徵

**尖峰時段:** 12:00

### 場景分布

- **For Here**: 51 筆交易
- **To Go**: 60 筆交易

---

## 📊 圖表

請查看 `analysis_output/vip_analysis/charts/` 目錄中的視覺化圖表:

- `vip_top_items.png` - VIP 客戶最常購買的商品
- `vip_temporal_patterns.png` - VIP 客戶時間型態分布
- `vip_comparison.png` - VIP vs 非VIP 比較
- `high_transaction_analysis.png` - 高消費交易分析

## 📁 數據檔案

- `vip_customers.csv` - VIP 客戶明細
- `high_transactions.csv` - 高消費交易明細
- `vip_analysis_report_*.json` - 完整 JSON 報告
