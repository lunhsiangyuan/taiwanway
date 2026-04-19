# Amy 的修改日誌

> 這個檔案由 Claude Code 自動維護。每次幫 Amy 改完任何檔案，會立即 append 一筆到這裡，方便 Lun-Hsiang 後續合併時對照。
>
> **請勿手動刪除或修改過去的紀錄**。

---

## 📖 格式範例

```markdown
## [YYYY-MM-DD HH:MM] 變更標題
**檔案：**
- `path/to/file.tsx`（改／新增／移除）

**改動：**
具體改了什麼（1–3 句話）。

**原因：**
為什麼要改（Amy 的需求是什麼）。

**測試：**
本地確認方式（開哪個頁面、點哪裡）。

**PR：** #N（如有）
```

---

## 🗓️ 變更紀錄（由新到舊）

<!-- Claude Code: 每次修改完 含內容調整 append 新紀錄在下面這條線之下 -->

---

## [2026-04-19 14:55] Menu ProductsShowcase 加「主餐」分類 + 支援雙尺寸定價

**檔案：**
- `lib/menu-data.ts`（改）— Product 介面新增 `priceRange?: { regular, large }`；PRODUCTS 陣列最前面加入 5 道主餐
- `components/product-card.tsx`（改）— 兩個 variant（list + grid）的價格顯示支援 priceRange；同時把「點餐」按鈕改指向 Uber Eats

**改動：**
`/menu` 頁下半段的 ProductsShowcase（春水堂風格的 tab + 卡片清單）原本只有飲料和甜點，主餐 tab 存在但 PRODUCTS 陣列沒對應品項，因而被 `products.length === 0` 自動隱藏。本次補齊：

五道主餐，對照 Amy 提供的菜單板，照實價格：
| # | 品項 | 英文 | 價格 | 圖片 |
|---|---|---|---|---|
| 1 | 紅燒牛肉麵 | Braised Beef Noodle Soup | $13.99 / $15.99 | `products/beef-noodle-soup-*.webp` |
| 2 | 麻醬牛肉乾麵 | Sesame Beef Noodles | $13.99 / $15.99 | `/images/sesame-beef-noodles.jpg` |
| 3 | 古早味滷肉飯 | Braised Pork Rice | $10.99 / $12.99 | `products/braised-pork-rice-*.webp` |
| 4 | 嘉義雞肉飯 | Chiayi Chicken Rice | $10.99 / $12.99 | `/images/chicken-rice.png` |
| 5 | 櫻花蝦米糕 | Sakura Shrimp Sticky Rice | $12.99 | `/images/sakura-shrimp-rice.jpg` |

每道菜三語描述全新寫（非延續菜單板原文），語氣對齊其他飲料品項的敘事風格。

**為了支援雙尺寸定價：**
Product 介面加 `priceRange?: { regular, large }`。product-card 顯示邏輯：
1. 有 `priceRange` → 顯示 `$13.99 / $15.99`
2. 否則有 `price` → 顯示 `$13.99`
3. 兩者都無 → 不顯示價格（避免 crash）

向後相容（既有品項都只用 `price`，不受影響）。

**為什麼同時改點餐按鈕 URL：**
product-card.tsx 的點餐按鈕原本指向停用的 `order.taiwanwayny.com`，同一檔案 PR #8 已在修。為了讓本 branch 的本地 preview 在新主餐卡片上能實際測試點餐流程，一併改為 Uber Eats URL。git 層面與 PR #8 變更相同行，若 PR #8 先 merge 本 PR 會是 no-op；若本 PR 先 merge 則 PR #8 變冗餘。

**原因：**
Amy 請求：「加上主餐的標籤、對應的圖片，還有點餐按鈕（一樣要連結到 Uber Eats）」。並附官方菜單板圖片確認品項與價格（刈包不賣了、tab 放最前面、描述三語新寫）。

**設計備註：**
- `CATEGORIES.MAIN_DISHES` 為物件第一個 key，`Object.values(CATEGORIES)` 保留插入順序，因此主餐 tab 自動排在第一
- MenuCarousel（頁面上半段）本來就有主餐分類，本次不動
- 過敏原依品項標註（麩質、大豆、芝麻、甲殼類）

**測試：**
- `bun dev` 於 `http://localhost:3000/menu`
- Fetch HTML 驗證：`主餐` / `Main Dishes` / `紅燒牛肉麵` / `Braised Beef Noodle Soup` / `櫻花蝦米糕` / `Sakura Shrimp` / `13.99` / `15.99` / `www.ubereats.com/store/taiwanway` 全部存在；`order.taiwanwayny.com` 不存在

**PR：** 進行中。

---
