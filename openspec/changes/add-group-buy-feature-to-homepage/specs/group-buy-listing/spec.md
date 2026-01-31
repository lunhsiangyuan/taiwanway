## Capability: Group Buy Listing

### Description
此功能負責提供 `taiwanway` 網站上所有團購活動的列表。針對「將團購網站的 feature 呈現在首頁」的需求，此規格將著重於優化團購列表的資料來源和篩選邏輯，以支援首頁展示的性能和資料即時性，同時不影響原有完整團購列表頁的功能。

### Scenarios

#### Scenario: Optimized Data Fetch for Homepage Display
**Given** 首頁的「團購專區」需要展示有限數量（例如，最新 3 個或最熱門的 3 個）的活躍團購活動
**When** 首頁發出團購數據請求
**Then** 數據接口應能提供經過優化、包含必要展示資訊（如名稱、圖片、進度、截止日期）的精簡團購數據
**And** 數據查詢應高效，避免加載所有團購的完整詳細資訊
**And** 數據應僅限於當前活躍的團購活動

#### Scenario: Full Group Buy Listing Page Functionality
**Given** 使用者訪問團購列表頁面 (非首頁)
**When** 團購列表頁面加載
**Then** 頁面應顯示所有符合篩選條件（若有）的團購活動的完整資訊
**And** 頁面應提供分頁、排序和進階篩選等功能 (保持現有行為)

### Inputs
*   `requestParamsForHomepage`: 針對首頁優化數據的請求參數（例如，`limit=3`, `status=active`, `orderBy=startDate`）。
*   `requestParamsForFullListing`: 針對完整列表頁面的請求參數（例如，分頁、篩選條件）。

### Outputs
*   **針對首頁**：精簡的活躍團購活動數據集合，包含首頁展示所需的關鍵資訊。
*   **針對完整列表頁面**：所有符合條件的團購活動的完整數據集合。

### Error Handling
*   **數據接口響應慢**：如果數據接口響應緩慢，應有超時機制，並在前端提供加載狀態或提示。
*   **無可用團購**：如果沒有符合首頁展示條件的團購活動，應返回空數據集或特定狀態，以便前端處理。

### Non-Functional Requirements
*   **API 性能**：團購數據接口應針對首頁和列表頁的請求進行優化，確保快速響應。
*   **數據緩存**：考慮在服務器端或 CDN 上緩存團購數據，以減少數據庫負載和提高響應速度。
*   **靈活性**：數據接口應足夠靈活，以支持未來可能變化的首頁展示需求。