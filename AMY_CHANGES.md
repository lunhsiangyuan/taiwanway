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
