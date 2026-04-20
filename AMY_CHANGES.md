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

## [2026-04-19 13:10] FAQ 字型從 Playfair Display SC 改為 Karla 無襯線

**檔案：**
- `app/faq/faq-client.tsx`（改）— h1 / h2 / 內文段落的 `font-heading` 改為 `font-body`；新增 `leading-snug` 與 `flex-shrink-0` 等微調

**改動：**
FAQ 頁的 `<h1>Frequently Asked Questions</h1>` 與每題 `<h2>` 原本用 `font-heading`（Playfair Display SC — serif 字型且為 small-caps 樣式），長句如 "Where is TaiwanWay located?" 閱讀困難。改用 `font-body`（Karla — 無襯線易讀字型），並把 H1 尺寸略縮（`text-4xl sm:text-5xl` → `text-3xl sm:text-4xl`）避免視覺過大、加上 `tracking-tight` 保留品牌感。

**原因：**
Amy 在實際瀏覽 `/faq` 時反映「字體字型不容易閱讀」。Playfair Display SC 適合短標題與裝飾性 hero，但不適合長問句。保留 logo 與首頁 hero 的 `font-heading` 使用不動，僅針對 FAQ 頁的閱讀體驗做調整。

**測試：**
1. `bun dev` 啟動於 `http://localhost:3000/faq`
2. 確認 H1、每題 summary、內文皆改為 Karla 字型
3. 切換中 / 英 / 西三語，長句換行與粗體皆正常
4. Screenshot 對比：改前 serif-caps 難讀 → 改後 sans-serif 清晰

**PR：** 進行中 — 由此條目觸發。

---

## [2026-04-19 13:05] Repo 重啟為 fork，改用 PR-based 工作流

**檔案：**
- `AMY_CHANGES.md`（重建）
- Local git remotes 重設（origin → `amyheish-prog/taiwanway-website` 新 fork；新增 `upstream` → `lunhsiangyuan/taiwanway`）
- Local main branch 重設為 `upstream/main`（HEAD = `49c154b`）

**改動：**
1. 刪除舊的 `amyheish-prog/taiwanway-website`（非 fork 版本）
2. 從 `lunhsiangyuan/taiwanway` 重新 fork，維持 repo 名稱 `taiwanway-website`
3. 本機 `Taiwanway 網站設計/` 資料夾 remotes 改為 origin=fork、upstream=Lun-Hsiang
4. 本機 main 硬重設為 `upstream/main`

**原因：**
舊的 repo 是直接 push 的獨立分支，無法與 Lun-Hsiang 的主線同步、也沒有 PR review 機制。改為 fork + PR 流程後：
- Amy 改動會走 feature branch → PR → Lun-Hsiang review → merge 上 Vercel
- 本機可以定期 `git fetch upstream && git merge --ff-only` 追最新
- Vercel 會自動為每個 PR 產 preview URL

**舊版本保存：**
之前 Amy 分支的兩個 commit（`3f3bcc6` SEO + GEO overhaul、`e57af2c` FAQ 字型修正）已匯出為 patch 檔保存於：
- `~/Desktop/taiwanway-patches/0001-SEO-GEO-overhaul-6-items.patch`
- `~/Desktop/taiwanway-patches/0002-FAQ-switch-to-sans-serif-body-font-for-readability.patch`

Lun-Hsiang 的 upstream `30c0b14 feat(amy-collab): SEO + GEO overhaul (round 2, 2026-04-19 12:30)` 已包含大部分 SEO/GEO 功能（含 `/faq` 頁、`/llms.txt`、動態 `<html lang>`、LocalBusiness schema 等），因此 patch `0001` 大概率冗餘；但 patch `0002`（FAQ 字型從 Playfair Display SC serif-caps 改為 Karla sans-serif）upstream 還沒做，之後會以 PR 形式送回去。

**測試：**
- `git log --oneline -5` → HEAD 為 `49c154b`，與 `upstream/main` 一致
- `git remote -v` → origin 指向新 fork、upstream 指向 Lun-Hsiang
- `bun dev` dev server 已在執行，`/`、`/faq`、`/menu`、`/products`、`/llms.txt`、`/sitemap.xml` 全部 200 OK

**後續：**
之後 Amy 每次改動一律走此流程：
1. `git fetch upstream && git merge upstream/main --ff-only`
2. `git checkout -b feature/<描述>`
3. 改檔案 + append 本檔案
4. `git commit` + `git push -u origin feature/<描述>`
5. `gh pr create` 開 PR 給 Lun-Hsiang

**PR：** (無 — 此變更為 local 環境設定，不走 PR)

---
