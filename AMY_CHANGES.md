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
