# 下載 Taiwanway Payment Histories 使用說明

## 概述

本專案提供兩種方式下載 Taiwanway 所有的 payment histories：

1. **使用 MCP Square 工具**（推薦）- 透過 Cursor 的 MCP Square 工具下載
2. **使用 Square API** - 透過 Python 腳本直接調用 Square API

## 查詢結果

根據 MCP Square 查詢結果：
- **最早的 payment 記錄**: 2024-02-08T02:39:49.373Z
- **最新的 payment 記錄**: 2025-11-11T23:31:46.806Z
- **Location ID**: LMDN6Z5DKNJ2P

## 方法一：使用 MCP Square 工具（推薦）

### 步驟 1: 下載所有 payments

由於 Square API 有分頁限制（每頁最多 100 筆），需要多次調用 MCP Square 工具。

#### 第一次查詢（獲取最早的記錄）

```python
# 使用 MCP Square 工具
service: payments
method: list
request: {
    "location_id": "LMDN6Z5DKNJ2P",
    "begin_time": "2024-02-08T00:00:00Z",
    "sort_order": "ASC",
    "limit": 100
}
```

#### 後續查詢（使用 cursor 分頁）

從第一次查詢的回應中取得 `cursor`，然後：

```python
service: payments
method: list
request: {
    "location_id": "LMDN6Z5DKNJ2P",
    "begin_time": "2024-02-08T00:00:00Z",
    "sort_order": "ASC",
    "limit": 100,
    "cursor": "<從上次回應取得的 cursor>"
}
```

重複此步驟直到回應中沒有 `cursor` 欄位。

### 步驟 2: 合併所有 JSON 數據

將所有查詢結果的 `payments` 陣列合併成一個 JSON 檔案。

### 步驟 3: 轉換為 CSV 並檢核

```bash
python3 scripts/convert_mcp_json_to_csv.py <合併後的_json檔案> [輸出_csv檔案]
```

範例：
```bash
python3 scripts/convert_mcp_json_to_csv.py all_payments.json taiwanway_all_payments.csv
```

## 方法二：使用 Square API（需要 access token）

### 步驟 1: 設定環境變量

```bash
export SQUARE_ACCESS_TOKEN="your_access_token_here"
```

### 步驟 2: 執行下載腳本

```bash
python3 scripts/download_all_payments.py
```

腳本會自動：
- 下載所有 payments（從 2024-02-08 開始）
- 轉換為 CSV 格式
- 檢核數據

## 數據檢核項目

腳本會自動檢核以下項目：

1. **營業日檢查**
   - 只應在週一、週二、週五、週六有記錄
   - 其他日期會被標記為異常

2. **不營業月份檢查**
   - 六月、七月應該沒有營業記錄
   - 如有記錄會被標記

3. **聖誕節檢查**
   - 12月25日應該沒有營業記錄
   - 如有記錄會被標記

## 輸出檔案

- **CSV 檔案**: 包含所有 payment 記錄的詳細資訊
- **檢核報告**: 在終端機顯示數據檢核結果

## CSV 欄位說明

| 欄位 | 說明 |
|------|------|
| id | Payment ID |
| created_at | 建立時間（UTC） |
| updated_at | 更新時間（UTC） |
| status | 狀態（COMPLETED, APPROVED 等） |
| source_type | 付款來源（CARD, CASH 等） |
| location_id | 店鋪位置 ID |
| order_id | 訂單 ID |
| customer_id | 客戶 ID |
| amount | 金額（單位：分） |
| tip | 小費（單位：分） |
| total_amount | 總金額（單位：分） |
| card_brand | 卡片品牌（VISA, MASTERCARD 等） |
| card_last_4 | 卡片後四碼 |
| ... | 其他欄位 |

## 注意事項

1. **時區轉換**: 所有時間都是 UTC 格式，檢核時會自動轉換為紐約時區（America/New_York）
2. **夏令時處理**: 腳本會自動處理夏令時（DST）轉換
3. **分頁限制**: Square API 每頁最多 100 筆記錄，需要多次查詢
4. **數據一致性**: Square API 的數據是「最終一致性」，新記錄可能需要幾秒鐘才會出現

## 疑難排解

### 問題：無法下載數據

**解決方案**:
1. 確認 MCP Square 工具已正確配置
2. 確認 Location ID 正確（LMDN6Z5DKNJ2P）
3. 確認有適當的權限（PAYMENTS_READ）

### 問題：檢核報告顯示異常記錄

**可能原因**:
1. 測試交易或調整記錄
2. 特殊活動日
3. 數據錯誤

**處理方式**: 檢查異常記錄的詳細資訊，確認是否為預期行為

### 問題：六月/七月有記錄

**可能原因**:
1. 特殊活動或測試
2. 數據錯誤

**處理方式**: 檢查這些記錄的詳細資訊，確認是否為預期行為






