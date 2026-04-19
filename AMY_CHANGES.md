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
