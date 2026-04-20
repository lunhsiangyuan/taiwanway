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

## [2026-04-19 20:30] 新增 Blog 區 + 第一篇文章（鳳梨酥內餡三語深度文）

**檔案：**
- `app/blog/page.tsx`（新增）— Blog 列表頁，內含 Blog JSON-LD schema
- `app/blog/blog-index-client.tsx`（新增）— 列表頁的三語客戶端組件
- `app/blog/posts.ts`（新增）— 文章資料陣列（目前 1 篇）
- `app/blog/why-our-pineapple-cake-uses-winter-melon/page.tsx`（新增）— 第一篇文章，含 BlogPosting + Breadcrumb schema
- `app/blog/why-our-pineapple-cake-uses-winter-melon/post-client.tsx`（新增）— 三語內文（zh/en/es）
- `app/sitemap.ts`（改）— 加入 `/blog` index 與各篇文章 URL

**改動：**
建立 `/blog` 區塊（純 Next.js App Router，不動 `next.config.js`、不加套件）。
第一篇文章：「為什麼我們的鳳梨酥用台灣空運土鳳梨 + 冬瓜餡」，約 800–1200 字、三語。主題：
1. 土鳳梨 vs 金鑽鳳梨的風味差異
2. 傳統鳳梨酥為什麼用冬瓜餡（70% 冬瓜 + 30% 鳳梨）
3. 為什麼堅持從台灣空運而非美國本地製作
4. 一顆 $3.25 的成本拆解

**原因：**
Amy 要求寫 blog 文章做長尾 SEO + GEO 加分。第一個主題是鳳梨酥內餡的工藝故事——AI 引擎（ChatGPT / Perplexity / Gemini）在被問到「authentic Taiwanese pineapple cake」、「why winter melon in pineapple cake」等問題時很可能引用。

**SEO 保障：**
- Metadata：title / description / keywords / OpenGraph / canonical
- JSON-LD：`BlogPosting`（文章）+ `Blog`（列表）+ `BreadcrumbList`（導覽）
- Sitemap：`/blog` + `/blog/why-our-pineapple-cake-uses-winter-melon` 已納入
- Keywords 涵蓋 `Taiwanese pineapple cake` / `winter melon filling` / `土鳳梨酥` 等長尾

**測試：**
- `bun dev` 於 `http://localhost:3000/blog` 與 `http://localhost:3000/blog/why-our-pineapple-cake-uses-winter-melon`
- 兩路由皆 HTTP 200
- HTML 含 `鳳梨酥`（zh）、`winter melon`（en）、`BlogPosting` schema、文章 slug
- Sitemap 已含 blog 路由

**設計備註：**
- 文章主標預設以 cover 圖放大呈現，標題尺寸與 About 頁對齊（`text-3xl md:text-4xl`）
- 三語內文分別寫在 `<PostBodyZh>` / `<PostBodyEn>` / `<PostBodyEs>` 三個子組件，依 `useLanguage()` 切換
- 沒有在 Header nav 加 Blog 連結（文章只有 1 篇、暫時不擴張導覽）；將來累積到 3+ 篇可加

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

---

## [2026-04-19 14:25] About 頁字型尺寸校正 + Header logo 縮小

**檔案：**
- `app/about/page.tsx`（改）— h1 / 副標 / 內文尺寸、欄寬、段距
- `components/header.tsx`（改）— 左上 logo 字級縮小

**改動：**
- **Header logo**：`text-2xl`（24px）→ `text-xl`（20px），視覺更輕盈
- **About h1**：`text-4xl md:text-5xl`（桌機 48px）→ `font-heading text-3xl md:text-4xl tracking-tight`（桌機 36px）— 縮 25%
- **About 副標**：`text-xl`（20px）→ `text-base md:text-lg`，與主標拉開層級落差
- **內文段落**：`text-lg`（18px）→ `text-base md:text-[1.0625rem]`（桌機 17px），容器 `max-w-3xl` → `max-w-2xl` 縮窄閱讀欄寬
- **區塊 padding**：`py-12` → `py-16 md:py-20`，搭配欄寬縮窄改善呼吸感
- 移除 `prose prose-lg` 容器，改用 `space-y-5 font-body` 搭配明確 className

**原因：**
Amy 看了新的 About 頁後反映「關於我們那四個字太大了」、Header「logo 也有點太大」。整體需要重新校正字型層級。

**測試：**
- `bun dev` 於 `http://localhost:3000/about`
- `getComputedStyle` 量測：logo 20px ✓、h1 30px（手機 294px）／36px（md+）✓、內文段落 16px（手機）／17px（md+）✓
- 新文案 "TaiwanWay is Middletown's first Taiwanese café..." 正常顯示（與本 PR 的文案重寫一同 deploy）

**設計備註：**
- 本次 commit 與同一 PR 的「文案重寫」commit 合併上 review（Amy 瀏覽時需要同時看到新文案 + 新尺寸才能判斷是否滿意）
- 不碰 hero 圖與其他頁

**PR：** #7（合併進原有 about-page-rewrite PR）

---

## [2026-04-19 14:00] About 頁三語文案重寫：對齊首頁品牌敘事

**檔案：**
- `lib/i18n/translations.ts`（改）— `about.title / story1 / story2 / story3 / closing` 三語版本全部重寫

**改動：**
把 About 頁原本的「一位母親陪小孩來 Middletown 念書、為解鄉愁開店」個人敘事，改成與首頁 `story-section.tsx` 對齊的品牌敘事：
1. 定位：Middletown 第一間台式咖啡廳 × 巴黎咖啡館 × 台灣茶館
2. 產品：招牌手搖珍奶（蜜香紅茶 / 阿里山烏龍 / 一保堂抹茶 / 手煮珍珠）、牛肉麵、滷肉飯、法式深烘焙拿鐵
3. 空間與使用情境：壁爐、吊燈、台灣伴手禮牆；午餐、工作、聚會、帶回家送禮
4. 結尾呼應首頁 quote「門推開，就是台灣的午後」

**原因：**
Amy 希望 About 頁不要再講老闆個人背景（不提她自己、不提陪小孩念書、不提鄉愁），而是強調店的品牌定位，與首頁故事一致。

**Amy 特別指示：**
- ❌ 不提老闆／Amy 本人
- ❌ 拿掉「沒有奶精」一句 — 為乳糖不耐客戶提供奶精仍是服務選項
- ❌ 不強調營業天數（未來會增加）

**測試：**
- `bun dev` 於 `http://localhost:3000/about` 驗證三語 fetch 結果：
  - 沒有 `mother` / `母親` / `madre`（舊敘事全消失）
  - 沒有 `Adams`（舊的食材來源提法消失）
  - 有 `tea house` / `茶館` / `casa de té`（新敘事到位）
  - status 200

---

## [2026-04-19 13:40] 聯絡 email 全站更新：usamyheish@gmail.com → taiwanway10940@gmail.com

**檔案：**（16 處、9 檔）
- `components/contact-section.tsx`（2 處 — mailto + 顯示文字）
- `components/contact.tsx`（2 處）
- `components/contact-info.tsx`（1 處）
- `components/footer.tsx`（2 處）
- `components/catering-page.tsx`（3 處 — 含三語字串）
- `components/json-ld.tsx`（3 處 — Restaurant / LocalBusiness / Organization schema）
- `public/llms.txt`（1 處 — AI 爬蟲指引）
- `README.md`、`CLAUDE.md`（各 1 處 — 店家資訊段落）

**改動：**
將全站聯絡 email 從 `usamyheish@gmail.com` 改為 `taiwanway10940@gmail.com`。包含：前端顯示、`mailto:` 連結、三語字串、JSON-LD 結構化資料、AI 爬蟲指引、專案說明文件。

**原因：**
Amy 啟用新的品牌信箱 `taiwanway10940@gmail.com`（與 IG 帳號 `@taiwanway10940` 一致），作為官方對外聯絡窗口。舊的 `usamyheish@gmail.com` 為老闆個人信箱，不宜對外公開。

**測試：**
- `bun dev` 於 `http://localhost:3000` 驗證 `/`、`/contact`、`/catering` 三個頁面 HTML 包含新 email、不包含舊 email
- `grep -r "usamyheish" .` → 無結果（確認無遺漏）
- JSON-LD 三處 schema email 欄位已同步更新

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
