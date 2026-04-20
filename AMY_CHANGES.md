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
