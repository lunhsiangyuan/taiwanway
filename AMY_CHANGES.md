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
