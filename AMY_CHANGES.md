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

## [2026-04-19 14:40] Product card「點餐」按鈕改指向 Uber Eats

**檔案：**
- `components/product-card.tsx`（改）— Grid 版與 List 版兩處「點餐 / Order」按鈕

**改動：**
兩個「點餐」按鈕的 `href` 從停用的 `https://order.taiwanwayny.com/order`（自家訂餐子網域）改為 Uber Eats 店家頁：
`https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A`

同時加上 `target="_blank" rel="noopener noreferrer"`（外站連結安全 attr），並補上西班牙文版按鈕文字 "Pedir"（原本只有 zh `'點餐'` / en `'Order'`）。

**原因：**
Amy 表示線上訂餐頁已關閉，但 `/products` 頁上每張商品卡片的「點餐」按鈕還指向那個無效子網域。改指向 Uber Eats，讓客人點擊後能直接進入外送流程；與 Header 現有的「🛵 Delivery (Uber Eats)」CTA 對齊。

**測試：**
`bun dev` 於 `http://localhost:3000/products` 驗證：
- `www.ubereats.com/store/taiwanway-middletown` 在 HTML 中出現 ✓
- `order.taiwanwayny.com` 已不存在 ✓
- HTTP 200

**設計備註：**
- 按鈕樣式（terracotta 圓角 pill + ShoppingBag icon）維持不變
- 語言切換時文字自動切 zh/en/es

**後續可考慮：**
- `app/faq/faqs.ts` 有兩題 FAQ 答案仍提到「可在 order.taiwanwayny.com 線上訂餐」— 訂餐頁關閉後這些答案也需更新（等 Amy 指示再處理）
- `components/order-banner.tsx` 與 `components/floating-order-cta.tsx` 檔案仍存在但已被 upstream commit 49c154b 從 layout 拔掉使用，屬 dead code（可另開 cleanup PR）

**PR：** 進行中。

---
