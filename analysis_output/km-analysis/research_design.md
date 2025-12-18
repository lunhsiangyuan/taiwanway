# Kaplan-Meier 存活分析與產品關聯分析研究設計

## 研究背景

在餐飲業經營中，顧客保留（Customer Retention）是決定長期獲利能力的關鍵因素。相較於開發新顧客，維持既有顧客的成本更低且效益更高。本研究旨在透過 Kaplan-Meier 存活分析方法，探討影響顧客保留的關鍵因子，並結合產品關聯分析（Association Rules Mining），識別產品組合策略與交叉銷售機會。

Taiwanway 餐廳提供多元化的台灣美食，包含飯麵類、奶茶飲品、甜點等商品類別，同時提供內用、外帶、外送等多種用餐方式。透過 Square POS 系統收集的交易資料，我們能夠追蹤個別顧客的購買行為與消費歷程，進而分析顧客生命週期與產品偏好。

## 研究目的

本研究的核心目標包括：

1. **識別顧客流失風險因子**：透過存活分析，找出影響顧客保留的關鍵變數（用餐方式、產品多樣性、Combo 購買行為）

2. **量化顧客生命週期**：估計不同顧客群體的平均存活時間與流失率

3. **發現產品交叉銷售機會**：透過關聯規則挖掘，找出具有正向關聯的產品配對

4. **分析時段消費偏好**：識別不同時段（午餐/下午茶/晚餐）的產品偏好差異

5. **提供數據驅動的經營建議**：基於統計分析結果，提出顧客保留策略與產品組合優化方案

## 資料來源與時間範圍

### 資料來源
- **系統**：Square POS (Point of Sale)
- **地點**：Taiwanway 餐廳（Location ID: LMDN6Z5DKNJ2P）
- **時區**：美國紐約時間（America/New_York）
- **時期**：2025 年 1 月 1 日至 2025 年 11 月 16 日

### 資料處理
1. **時間校正**：原始資料為 Taipei 時區，經 +12 小時平移後轉換為紐約時區，並考慮日光節約時間（DST）轉換（2025 年 11 月 2 日起為 EST）

2. **資料清理**：
   - 僅保留 Event Type = "Payment" 的交易
   - 排除 Custom Amount（Price Point Name 為空）
   - 排除 SKU 缺失的記錄

3. **觀察終點**：以最後一筆交易日（2025-11-16）為觀察終點

### 資料結構
- **交易層級資料**：每筆商品購買記錄（Transaction ID + Item）
- **顧客層級資料**：以 Customer ID 聚合的顧客購買歷程

## 變數定義

### 依變數（Dependent Variables）

#### 1. 存活時間（Survival Time）
- **定義**：從顧客首次購買日至末次購買日的天數
- **計算**：`survival_time = last_purchase_date - first_purchase_date`
- **單位**：天（days）
- **範圍**：0 至觀察期總長度

#### 2. 流失狀態（Event Status）
- **定義**：顧客是否在觀察期內流失
- **編碼**：
  - `1`（event occurred）：流失，定義為末購日後 60 天內未再消費，且觀察終點已超過該期限
  - `0`（censored）：未流失或右設限，包含仍活躍顧客或觀察期內無法確認流失者
- **流失定義邏輯**：
  ```
  IF last_purchase_date + 60 days < observation_end:
      status = 1 (流失)
  ELSE:
      status = 0 (censored)
  ```

### 自變數（Independent Variables / Grouping Variables）

#### 1. 用餐方式（Dining Option）
- **來源**：顧客首次購買時的 Dining Option 欄位
- **分類**：
  - 內用（For Here）
  - 外帶（To Go）
  - 外送（Delivery）
  - Unknown（缺失或其他）
- **假設**：用餐方式反映顧客的消費習慣與餐廳體驗，可能影響顧客黏著度

#### 2. 首購是否為 Combo（First Purchase Combo）
- **定義**：顧客首次購買時是否包含 Combo Meals 類別商品
- **分類**：Yes / No
- **假設**：首購選擇 Combo 的顧客可能對餐廳有較高的信任感或價格敏感度

#### 3. 是否曾購買過 Combo（Ever Bought Combo）
- **定義**：顧客在整體購買歷程中是否至少購買過一次 Combo
- **分類**：Yes / No
- **假設**：曾購買 Combo 的顧客可能具有更高的價格意識與產品探索意願

#### 4. 商品多樣性 - Category 層級（Product Diversity - Category）
- **定義**：顧客曾購買的商品大類數量
- **分類**：
  - 1 種：單一類別消費者（專一型）
  - 2-3 種：中度多樣化消費者
  - 4 種以上：高度多樣化消費者（探索型）
- **假設**：商品多樣性高的顧客對餐廳產品有更廣泛的興趣，可能具有更高的保留率

#### 5. 商品多樣性 - Item 層級（Product Diversity - Item）
- **定義**：顧客曾購買的不重複商品（Item）數量
- **分類**：同 Category 層級
- **假設**：提供更細緻的多樣性衡量，補充 Category 層級分析

### 關聯指標（Association Measures）

#### 1. Support（支持度）
- **定義**：某產品配對在所有交易中出現的比例
- **公式**：`Support(A, B) = P(A ∩ B) = N(A ∩ B) / N_total`
- **解釋**：衡量配對的普遍性

#### 2. Confidence（信賴度）
- **定義**：購買 A 的顧客中同時購買 B 的比例
- **公式**：`Confidence(A → B) = P(B | A) = N(A ∩ B) / N(A)`
- **解釋**：衡量規則的可靠性（條件機率）

#### 3. Lift（提升度）
- **定義**：實際共現比例與期望共現比例的比值
- **公式**：`Lift(A, B) = P(A ∩ B) / [P(A) × P(B)]`
- **解釋**：
  - Lift > 1：正向關聯（一起購買的傾向高於隨機期望）
  - Lift = 1：獨立（無關聯）
  - Lift < 1：負向關聯（互斥或替代關係）

## 統計方法

### 1. Kaplan-Meier 估計（Kaplan-Meier Estimator）

#### 理論基礎
Kaplan-Meier 方法是一種非參數的存活分析技術，適用於處理右設限資料（right-censored data）。其核心概念是透過離散時間點的條件機率連乘，估計存活函數。

#### 存活函數
$$\hat{S}(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

其中：
- $t_i$：第 $i$ 個事件發生時間
- $d_i$：在時間 $t_i$ 發生事件的人數
- $n_i$：在時間 $t_i$ 之前仍處於風險中的人數（at risk）

#### 標準誤估計（Greenwood 公式）
$$\text{SE}[\hat{S}(t)] = \hat{S}(t) \sqrt{\sum_{t_i \leq t} \frac{d_i}{n_i(n_i - d_i)}}$$

#### 95% 信賴區間
$$\text{CI}_{95\%} = \hat{S}(t) \pm 1.96 \times \text{SE}[\hat{S}(t)]$$

### 2. Log-rank 檢定（Mantel-Cox Test）

#### 目的
比較兩組或多組存活曲線是否有顯著差異。

#### 檢定統計量
$$\chi^2 = \frac{(O_1 - E_1)^2}{V_1}$$

其中：
- $O_1$：第 1 組觀察到的事件數
- $E_1$：第 1 組期望事件數
- $V_1$：變異數

#### 虛無假設
$H_0$：各組的存活曲線相同（hazard functions 相等）

#### 備擇假設
$H_1$：至少有一組的存活曲線不同

#### 顯著水準
$\alpha = 0.05$

### 3. Pairwise 比較與多重檢定校正

#### Pairwise Log-rank 檢定
當自變數有 3 組以上時，進行所有可能的兩兩比較。

#### Holm-Bonferroni 校正
為控制多重比較的 Family-Wise Error Rate (FWER)，使用 Holm-Bonferroni 方法校正 p 值：

1. 將所有 p 值由小到大排序：$p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(m)}$
2. 對第 $i$ 個 p 值，校正後的 p 值為：
   $$p_{adj,(i)} = \max\{(m - i + 1) \times p_{(i)}, p_{adj,(i-1)}\}$$
3. 若 $p_{adj} < 0.05$，則拒絕虛無假設

### 4. 卡方檢定（Chi-square Test）

#### 應用場景
- 產品配對的獨立性檢定
- 時段與產品的關聯性檢定

#### 2×2 列聯表
|         | 有 B | 無 B | 總計 |
|---------|------|------|------|
| 有 A    | $n_{11}$ | $n_{12}$ | $n_{1\cdot}$ |
| 無 A    | $n_{21}$ | $n_{22}$ | $n_{2\cdot}$ |
| 總計    | $n_{\cdot 1}$ | $n_{\cdot 2}$ | $n$ |

#### 檢定統計量
$$\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

其中：
- $O_{ij}$：觀察值
- $E_{ij} = \frac{n_{i\cdot} \times n_{\cdot j}}{n}$：期望值

#### 適用條件
期望值 $E_{ij} \geq 5$

### 5. Fisher's Exact Test

#### 應用場景
當 2×2 列聯表的期望值 < 5 時，使用 Fisher's exact test 替代卡方檢定。

#### 特點
- 精確檢定（不依賴近似分佈）
- 適用於小樣本

## 分析流程

### 階段 1：資料前處理
1. 讀取原始 CSV 資料
2. 合併 Date 和 Time 為 DateTime
3. 時間平移 +12 小時
4. 轉換為紐約時區（考慮 DST）
5. 資料清理（Event Type, Custom Amount, SKU）
6. 輸出：`cleaned_data.csv`

### 階段 2：顧客世代建構
1. 以 Customer ID 分組
2. 計算首購日、末購日
3. 計算存活時間
4. 定義流失狀態（60 天規則）
5. 建構 5 個分組變數
6. 輸出：`customer_cohort.csv`

### 階段 3：Kaplan-Meier 存活分析
1. 對 5 個分組變數分別擬合 KM 曲線
2. 執行 log-rank 檢定
3. 多組變數進行 pairwise 比較與 Holm 校正
4. 繪製存活曲線（含 95% CI, risk table, p 值）
5. 輸出：5 張 KM 曲線圖 + 統計結果 CSV

### 階段 4：產品關聯分析
1. 建構購物籃資料（Transaction ID × SKU）
2. 使用 apriori 演算法挖掘關聯規則（最小 support = 10 次）
3. 計算 support, confidence, lift
4. 對每對 SKU 執行卡方或 Fisher's exact test
5. Holm-Bonferroni 校正
6. 輸出：關聯統計表 + 熱力圖

### 階段 5：時段產品分析
1. 劃分時段（午餐 11-13, 下午茶 14-16, 晚餐 17-18）
2. 計算時段 × SKU 的 lift 值
3. 對每個 SKU 執行卡方檢定（時段分佈偏離檢定）
4. Holm-Bonferroni 校正
5. 輸出：時段統計表 + 熱力圖

### 階段 6：報告生成
1. 整合所有圖表與統計結果
2. 生成兩份 PDF 報告：
   - `km_association_report.pdf`：完整分析報告
   - `km_heatmap_report.pdf`：詳細報告（含 pairwise 矩陣）
3. 生成文字摘要報告

## 解讀指南

### Kaplan-Meier 曲線解讀

#### Y 軸：存活機率
- 1.0 (100%)：完全保留，無顧客流失
- 0.5 (50%)：半數顧客流失
- 0.0 (0%)：全部流失

#### X 軸：存活時間（天）
- 從首購日起算的天數
- 越往右代表時間越長

#### 曲線特徵
- **階梯狀下降**：每次事件（流失）發生時，曲線向下跳躍
- **平坦區段**：該時段無事件發生
- **陡峭下降**：短時間內大量流失

#### 信賴區間（陰影區域）
- 95% CI 反映估計的不確定性
- 樣本數越大，CI 越窄

#### Risk Table（風險人數表）
- 顯示各時間點仍處於風險中的顧客數
- 人數遞減反映流失與 censoring

### Log-rank 檢定結果解讀

#### p 值（p-value）
- **p < 0.05**：組間存活曲線有顯著差異，拒絕虛無假設
- **p ≥ 0.05**：無顯著差異，無法拒絕虛無假設

#### Pairwise 比較
- 針對多組比較，識別具體哪些組別間存在顯著差異
- 需考慮多重檢定校正後的 p 值

### Hazard Ratio (HR) 解釋
（若進行 Cox 迴歸分析）
- **HR > 1**：風險增加（更容易流失）
- **HR = 1**：風險相同
- **HR < 1**：風險降低（更容易保留）

### Lift 值解讀

#### Lift > 1
- 正向關聯：兩產品一起購買的機率高於隨機期望
- 例如：Lift = 2.5 表示共同購買的機率是獨立情況下的 2.5 倍
- **商業意義**：適合搭配銷售、組合促銷

#### Lift = 1
- 獨立：兩產品的購買行為互不影響
- 無特殊關聯

#### Lift < 1
- 負向關聯：兩產品一起購買的機率低於期望
- **可能原因**：替代品、互斥需求、價格約束
- **商業意義**：避免強制組合，可能需要差異化定位

### 顯著性標記

- ***** (p < 0.001)：極顯著
- **** (p < 0.01)：非常顯著
- *** (p < 0.05)：顯著
- **ns**：not significant (p ≥ 0.05)，無顯著差異

## 研究限制

### 1. 右設限資料（Right Censoring）
- 部分顧客在觀察期結束時仍未流失，無法得知其真實生命週期
- **影響**：低估真實存活時間
- **處理**：使用 Kaplan-Meier 方法適當處理 censored data

### 2. 流失定義的主觀性
- 60 天未消費定義為流失屬於人為設定
- 不同產業或餐廳類型可能需要不同閾值
- **建議**：敏感性分析，測試不同天數閾值（如 30/45/90 天）

### 3. 選擇性偏誤（Selection Bias）
- 僅分析有 Customer ID 的顧客，排除匿名交易
- 可能低估一次性顧客比例
- **影響**：結果僅適用於已識別顧客群體

### 4. 因果推論限制
- 觀察性研究無法建立因果關係
- 僅能識別關聯性（association），不能斷定因果（causation）
- **例如**：高多樣性顧客保留率高，但不能確定是多樣性導致保留，或是高黏著度顧客傾向探索更多產品

### 5. 時間依存性變數（Time-Dependent Covariates）
- 本研究將多樣性等變數視為固定（基於整體購買歷程）
- 實際上，顧客行為隨時間變化
- **改善方向**：使用 Cox 迴歸模型納入時間依存性變數

### 6. 競爭風險（Competing Risks）
- 顧客可能因搬家、改變飲食習慣等非餐廳因素流失
- 當前分析未區分流失原因
- **影響**：可能高估餐廳服務品質對保留的影響

### 7. 外部效度（External Validity）
- 結果基於單一餐廳（Taiwanway）資料
- 推廣至其他餐廳或地區需謹慎
- **建議**：跨店比較或產業基準比對

## 未來研究方向

1. **Cox 比例風險模型**：納入多變數分析，控制混淆因子

2. **機器學習預測模型**：使用 Random Forest 或 XGBoost 預測流失機率

3. **顧客價值分層**：結合 RFM 分析與存活分析，識別高價值顧客

4. **動態推薦系統**：基於關聯規則建構個人化產品推薦

5. **情境感知分析**：納入天氣、節慶、促銷活動等外部變數

6. **質性研究補充**：顧客訪談或問卷調查，探索流失原因

## 參考文獻格式

### 存活分析
- Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association*, 53(282), 457-481.

### 關聯規則
- Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. *Proceedings of the 20th VLDB Conference*, 487-499.

### 多重檢定校正
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65-70.

## 附錄：R 套件版本

建議使用以下 R 套件版本（或更新版本）：

```r
- R version: ≥ 4.0.0
- tidyverse: ≥ 1.3.0
- survival: ≥ 3.2.0
- survminer: ≥ 0.4.9
- arules: ≥ 1.6.0
- pheatmap: ≥ 1.0.12
- showtext: ≥ 0.9.0
- ggpubr: ≥ 0.4.0
```

---

**文件版本**：1.0  
**最後更新**：2025-11-16  
**作者**：Taiwanway Data Analytics Team  
**聯絡方式**：請參考專案 README.md



