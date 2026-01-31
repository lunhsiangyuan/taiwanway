## 1. 環境與專案初始化

- [x] 1.1 確認 `taiwanway` 專案已在本地複製並設定開發環境。
- [x] 1.2 檢查 `package.json`，確認所有開發依賴項已安裝。
- [ ] 1.3 確保已配置 Google Sheets API 的服務帳戶憑證（`.env` 或其他安全配置）。

## 2. 後端數據同步服務 (`group-buy-google-sync-integration`)

- [ ] 2.1 實作 Google Sheets API 連接工具函數，用於讀取指定 Google Sheet ID 和工作表名稱的數據。
- [ ] 2.2 開發數據轉換邏輯，將 Google Sheets 讀取到的原始數據映射到網站數據庫的團購數據模型。
- [ ] 2.3 實作數據庫更新邏輯，將轉換後的團購數據寫入或更新到數據庫中（處理新增、更新、刪除）。
- [ ] 2.4 建立定時任務 (Cron Job)，配置其定期觸發數據同步服務（例如，每 30 分鐘）。
- [ ] 2.5 開發手動觸發同步的 API 端點或後台介面。
- [ ] 2.6 實作錯誤日誌記錄和警報機制，監控同步過程中的錯誤（例如，API 連接失敗、數據結構不匹配）。

## 3. 後端 API 開發 (`group-buy-listing` - Optimized for Homepage)

- [ ] 3.1 建立新的後端 API 端點，例如 `/api/homepage/group-buys/active`，用於提供首頁所需的精簡團購數據。
- [ ] 3.2 實作該 API 端點的邏輯，從數據庫中高效查詢當前活躍的團購活動。
- [ ] 3.3 確保 API 響應只包含首頁展示所需的關鍵字段（例如，ID, 名稱, 圖片 URL, 進度, 截止日期, 詳情頁 URL）。
- [ ] 3.4 為該 API 端點實作數據緩存機制（例如，使用 Redis 或內存緩存），以減少數據庫負載和提高響應速度。

## 4. 前端組件開發 (`homepage-group-buy-display`)

- [x] 4.1 創建新的 React 組件 `HomepageGroupBuySection.js`，作為首頁團購展示區塊的容器。(對應現有 `components/GroupBuy.tsx` 基礎)
- [x] 4.2 在 `HomepageGroupBuySection.js` 中實作數據獲取邏輯，調用步驟 3.1 中建立的後端 API 端點。(使用 mock data，預留 API 接口)
- [x] 4.3 設計並實作 `GroupBuyCard.js` 組件，用於展示單個團購活動的資訊（名稱、圖片、進度等）。
- [x] 4.4 在 `HomepageGroupBuySection.js` 中渲染 `GroupBuyCard` 組件列表。
- [x] 4.5 實作響應式設計，確保 `HomepageGroupBuySection` 在不同設備上良好顯示。(基於 Tailwind CSS 假設)
- [x] 4.6 實作加載狀態 (Loading State) 和錯誤狀態 (Error State)，提升用戶體驗。
- [x] 4.7 若無活躍團購，顯示友善提示訊息或隱藏區塊。

## 5. 首頁整合

- [x] 5.1 修改 `src/pages/Homepage.js` 或主頁面的相關模板文件。(已修改 `app/page.tsx`)
- [x] 5.2 在首頁的適當位置，整合並渲染 `HomepageGroupBuySection` 組件。(已整合 `GroupBuy` 組件)
- [x] 5.3 調整首頁的 CSS/SCSS 樣式，確保團購區塊與整體頁面風格協調一致。(基於 Tailwind CSS 假設)

## 6. 測試與部署

- [ ] 6.1 為後端數據同步服務撰寫單元測試和整合測試。
- [ ] 6.2 為新的後端 API 端點撰寫單元測試和整合測試。
- [ ] 6.3 為 `HomepageGroupBuySection` 和 `GroupBuyCard` 組件撰寫單元測試和 UI 測試。
- [ ] 6.4 執行端對端測試，驗證從 Google Sheets 到首頁展示的整個流程。
- [ ] 6.5 更新部署腳本，包含新的後端服務和前端組件。
- [ ] 6.6 實作持續監控機制，特別是數據同步狀態和首頁性能。