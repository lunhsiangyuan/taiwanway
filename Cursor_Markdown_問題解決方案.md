# Cursor Markdown 檔案無法開啟問題解決方案

## 🔍 問題描述

Cursor 2.0 更新後，許多使用者遇到 Markdown (.md) 檔案無法開啟的問題，錯誤訊息為：
- **"Unable to open: Assertion Failed: Argument is 'undefined' or 'null'"**
- **"Unable to retrieve document from URI"**

這個問題主要發生在：
- AI 工具（write, search_replace）創建或修改的 Markdown 檔案
- 程式化創建的 .md 檔案
- 更新到 Cursor 2.0 之後

## ✅ 解決方案（按優先順序）

### 方案 1：禁用 Office Viewer 擴展 ⭐ **最有效**

根據社群回報，**Office Viewer 擴展**是主要原因之一：

1. 打開 Cursor
2. 前往 **Extensions** (擴展)
3. 搜尋 **"Office Viewer"**
4. **禁用**該擴展
5. **重新載入** Cursor (Reload Window)
6. 嘗試打開 Markdown 檔案

**如果成功**：可以重新啟用 Office Viewer（如果需要該功能）

**來源**：多位使用者回報此方法有效

---

### 方案 2：清除 Cursor 緩存

這可以解決檔案系統監視器的緩存問題：

#### macOS:
```bash
# 關閉 Cursor 後執行
rm -rf ~/Library/Application\ Support/Cursor/Cache*
rm -rf ~/Library/Application\ Support/Cursor/*Cache
rm -f ~/.cursor.json
```

#### Windows:
```cmd
# 關閉 Cursor 後執行
rd /s /q "%USERPROFILE%\AppData\Local\Cursor"
rd /s /q "%USERPROFILE%\AppData\Roaming\Cursor"
del /f /q "%USERPROFILE%\.cursor*"
```

#### Linux:
```bash
rm -rf ~/.cursor ~/.config/Cursor/
```

**注意**：清除緩存會刪除擴展設定，可能需要重新配置

---

### 方案 3：使用文字編輯器模式打開

臨時解決方案，可以正常編輯檔案：

1. 在檔案總管中**右鍵點擊** .md 檔案
2. 選擇 **"Open With"** (使用...開啟)
3. 選擇 **"Text Editor"** (文字編輯器)
4. 檔案會以原始 Markdown 模式打開（非預覽模式）

---

### 方案 4：禁用所有擴展測試

確認是否為擴展衝突：

1. 關閉 Cursor
2. 從終端機執行：
   ```bash
   cursor --disable-extensions
   ```
3. 如果檔案可以打開，則問題在擴展
4. 逐一啟用擴展找出問題擴展

---

### 方案 5：手動創建檔案

如果 AI 創建的檔案有問題，可以：

1. 手動創建空白 .md 檔案（File > New File）
2. 讓 AI 使用 `search_replace` 工具填充內容
3. 這樣創建的檔案通常可以正常打開

---

### 方案 6：重啟 Cursor

簡單但有效：

1. 完全關閉 Cursor
2. 重新開啟
3. 檔案系統會重新掃描，可能解決問題

---

### 方案 7：切換編輯器模式

如果檔案已經打開但顯示錯誤：

1. 點擊檔案標籤上的 **"Switch to Markdown Editor"** 按鈕
2. 關閉檔案
3. 重新打開檔案
4. 應該可以正常顯示

---

## 🔧 進階診斷

### 檢查開發者工具錯誤

1. 打開 **Help > Toggle Developer Tools**
2. 查看 **Console** 標籤
3. 尋找錯誤訊息，特別是：
   - `ERR Unable to retrieve document from URI`
   - `Assertion Failed: Argument is 'undefined' or 'null'`

### 檢查檔案路徑

問題可能與檔案路徑有關：
- 避免特殊字元
- 避免過長的路徑
- 確認檔案權限正確

### 檢查檔案編碼

確保檔案使用 UTF-8 編碼：
```bash
# macOS/Linux
file -I filename.md

# 應該顯示 charset=utf-8
```

---

## 📋 已知問題

### Cursor 2.0 回歸問題

這是 Cursor 2.0 更新後引入的已知 bug：
- **影響範圍**：所有平台（Windows, macOS, Linux）
- **觸發條件**：AI 工具創建/修改 Markdown 檔案
- **狀態**：已回報給 Cursor 團隊，等待修復

### 檔案系統監視器問題

根據分析，問題可能出在：
- Cursor 的 Electron 檔案系統監視器
- Windows 上程式化創建的檔案未被正確註冊
- 重啟後強制重新掃描可以解決

---

## 🛠️ 臨時工作流程建議

在官方修復之前，建議：

1. **手動創建檔案**：先手動創建空白 .md 檔案
2. **使用 search_replace**：讓 AI 使用 `search_replace` 而非 `write` 工具
3. **定期重啟**：如果問題頻繁出現，定期重啟 Cursor
4. **使用文字編輯器模式**：暫時關閉 Markdown 預覽功能

---

## 📞 回報問題

如果以上方法都無效，請到 [Cursor 論壇](https://forum.cursor.com/) 回報：

1. **系統資訊**：Help > About Cursor > Copy
2. **錯誤訊息**：Developer Tools > Console 的錯誤
3. **重現步驟**：詳細描述如何觸發問題
4. **已嘗試的解決方案**：列出已試過的方法

---

## 🔗 相關資源

- [Cursor 官方論壇討論](https://forum.cursor.com/t/create-update-md-files-unable-to-open-assertion-failed-argument-is-undefined-or-null/140018)
- [Cursor 故障排除指南](https://cursor.com/docs/troubleshooting/troubleshooting-guide)
- [GitHub Issue #3241](https://github.com/cursor/cursor/issues/3241)

---

## 📝 更新記錄

- **2025-12-17**：整理解決方案文件
- **已知問題**：Cursor 2.0.38+ 版本存在此問題
- **最佳解決方案**：禁用 Office Viewer 擴展（多數使用者有效）

---

**提示**：如果問題持續，建議暫時使用其他編輯器（如 VS Code）編輯 Markdown 檔案，等待 Cursor 官方修復。


