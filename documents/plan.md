# Square MCP 下載 All Payments 完整計畫
## 2025 年度數據下載與驗證指南（2025-01-01 至 2025-11-15）

**文件版本**: 2.0
**建立日期**: 2025-11-15
**狀態**: 進行中（98% 待完成）
**上次更新**: 2025-11-15

---

## 📋 目錄

1. [系統概覽](#系統概覽)
2. [當前下載狀態](#當前下載狀態)
3. [完整下載檢查清單](#完整下載檢查清單)
4. [核心腳本使用說明](#核心腳本使用說明)
5. [驗證項目](#驗證項目)
6. [已識別問題與解決方案](#已識別問題與解決方案)
7. [執行命令參考](#執行命令參考)
8. [數據完整性驗證](#數據完整性驗證)

---

## 系統概覽

### 數據流程架構圖

```
Square API (Payments Endpoint)
    Location: LMDN6Z5DKNJ2P (Taiwanway)
            │
            ▼
┌───────────────────────────────────────────────┐
│ 階段 1: MCP Square 手動下載                    │
│   • 使用 Cursor 的 MCP Square Server          │
│   • Cursor-based 分頁（每頁 100 筆）           │
│   • 日期範圍: 2025-01-01 → 2025-11-15         │
└──────────────┬────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────┐
│ 儲存位置: MCP Tools 目錄                       │
│   ~/.cursor/projects/.../agent-tools/         │
│   • 710 個 .txt 文件（JSON 格式）              │
│   • 總大小約 140MB                             │
└──────────────┬────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────┐
│ 階段 2: 自動合併與去重                         │
│   腳本: download_all_payments_mcp.py          │
│   • 掃描所有 .txt 文件                         │
│   • 根據 payment ID 去重                       │
│   • 日期過濾: 2025-01-01 至 2025-11-15        │
│   ↓                                            │
│   輸出: data/all_payments/all_payments.json   │
│   （3,686 筆記錄，9.5 MB）                     │
└──────────────┬────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────┐
│ 階段 3: 格式轉換與驗證                         │
│   腳本: convert_mcp_json_to_csv.py            │
│   • JSON → CSV 扁平化                          │
│   • 時區轉換 (UTC → America/New_York)         │
│   • 營業日驗證                                 │
│   • 閉店月份檢查                               │
│   ↓                                            │
│   輸出: data/all_payments/all_payments.csv    │
│   （1.1 MB）                                   │
└──────────────┬────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────┐
│ 階段 4: 報告生成                               │
│   • HTML 報告                                  │
│   • 月度統計報告                               │
│   • 數據檢查報告                               │
└───────────────────────────────────────────────┘
```

### MCP Square API 調用機制

```
使用者 (Cursor IDE)
    │
    ├─→ 複製 MCP 命令
    │   service: payments
    │   method: list
    │   request: {
    │     "location_id": "LMDN6Z5DKNJ2P",
    │     "begin_time": "2025-01-01T00:00:00Z",
    │     "end_time": "2025-01-31T23:59:59Z",
    │     "limit": 100,
    │     "sort_order": "ASC"
    │   }
    │
    ▼
MCP Square Server
    │
    ├─→ 調用 Square Payments API
    │
    ▼
Square API 返回
    {
      "payments": [...100 筆...],
      "cursor": "eyJjcmVhdGVkQXQ..."  ← 如果還有更多數據
    }
    │
    ▼
自動儲存到
~/.cursor/projects/.../agent-tools/[UUID].txt
```

### 關鍵配置參數

| 參數 | 值 | 說明 |
|------|---|------|
| **Location ID** | `LMDN6Z5DKNJ2P` | Taiwanway 餐廳 |
| **日期範圍** | `2025-01-01` ~ `2025-11-15` | 2025 年度數據 |
| **時區** | `America/New_York` | EST/EDT 自動轉換 |
| **每頁記錄數** | `100` | Square API 限制 |
| **排序方式** | `ASC` | 按 created_at 升序 |
| **營業日** | `[0, 1, 4, 5]` | 週一、二、五、六 |
| **閉店月份** | `[6, 7]` | 六月、七月（暑期休息） |
| **營業時間** | `10:00 - 20:00` | 每日營業時段 |

---

## 當前下載狀態

### 📊 整體進度

```
總體完成度: ████░░░░░░░░░░░░░░░░ 2%

下載狀態統計:
├─ 總文件數:     710 個
├─ 剩餘 cursor:  694 個 (98%)
├─ 已完成:       16 個 (2%)
└─ 已合併記錄:   3,686 筆
```

### 📅 月度數據分佈

| 月份 | 日期範圍 | 營業狀態 | 已合併記錄數 | 狀態 |
|------|---------|---------|-------------|------|
| 2025-01 | 01-01 ~ 01-31 | 🟢 冬季營業 | 407 筆 | ✅ 部分下載 |
| 2025-02 | 02-01 ~ 02-28 | 🟢 冬季營業 | 291 筆 | ✅ 部分下載 |
| 2025-03 | 03-01 ~ 03-31 | 🟢 春季營業 | 399 筆 | ✅ 部分下載 |
| 2025-04 | 04-01 ~ 04-30 | 🟢 春季營業 | 200 筆 | ✅ 部分下載 |
| 2025-05 | 05-01 ~ 05-31 | 🟢 春季營業 | 200 筆 | ✅ 部分下載 |
| 2025-06 | 06-01 ~ 06-30 | 🔴 暑期休息 | 0 筆 | ✅ 符合預期 |
| 2025-07 | 07-01 ~ 07-31 | 🔴 暑期休息 | 0 筆 | ✅ 符合預期 |
| 2025-08 | 08-01 ~ 08-31 | 🟢 秋季營業 | 420 筆 | ✅ 部分下載 |
| 2025-09 | 09-01 ~ 09-30 | 🟢 秋季營業 | 790 筆 | ✅ 部分下載 |
| 2025-10 | 10-01 ~ 10-31 | 🟢 秋季營業 | 683 筆 | ✅ 部分下載 |
| 2025-11 | 11-01 ~ 11-15 | 🟢 秋季營業 | 296 筆 | ✅ 部分下載 |
| **總計** | | | **3,686 筆** | ⚠️ 未完成 |

### ⚠️ 關鍵發現

1. **下載未完成警告**
   - 694 個文件仍有 cursor，表示每個文件至少還有 1 頁未下載
   - 估計剩餘數據量：694 × 100 = **約 69,400 筆**（保守估計）
   - 當前 3,686 筆可能僅佔總數據的 **5% 左右**

2. **數據完整性疑慮**
   - 六月、七月數據為 0 筆 ✅（符合暑期休息規則）
   - 其他月份數據量偏低，需要完成剩餘 cursor 下載

3. **時區轉換正確性**
   - 已使用 `pytz.timezone('America/New_York')`
   - 自動處理 DST 轉換：
     - EDT (UTC-4): 2025-03-09 02:00 開始
     - EST (UTC-5): 2025-11-02 02:00 開始

---

## 完整下載檢查清單

### 階段 A: 準備與狀態檢查 ✅

- [x] **A1. 確認腳本配置**
  - [x] 日期範圍設定: 2025-01-01 至 2025-11-15
  - [x] Location ID: LMDN6Z5DKNJ2P
  - [x] MCP tools 目錄路徑正確

- [x] **A2. 檢查當前狀態**
  ```bash
  python3 scripts/show_status.py
  ```
  - [x] 確認總文件數: 710
  - [x] 確認剩餘 cursor: 694
  - [x] 確認已合併記錄: 3,686

### 階段 B: Cursor 追蹤與批次下載 ⚠️

- [ ] **B1. 更新 cursor 資訊**
  ```bash
  python3 scripts/get_all_cursors_info.py
  ```
  - [ ] 生成 `data/all_payments/cursors_info.json`
  - [ ] 確認剩餘 cursor 數量
  - [ ] 檢查 cursor 日期分佈

- [ ] **B2. 批次生成下載命令**
  ```bash
  python3 scripts/batch_download_with_mcp.py
  ```
  - [ ] 設定批次大小: 20-50 個 cursor
  - [ ] 生成待執行命令列表
  - [ ] 保存到 `pending_cursor_commands.json`

- [ ] **B3. 執行 MCP Square 命令**（手動步驟）
  - [ ] 複製命令到 Cursor IDE
  - [ ] 在 MCP Square 中執行
  - [ ] 等待所有命令完成
  - [ ] 記錄執行批次編號: ___

- [ ] **B4. 驗證下載結果**
  ```bash
  python3 scripts/show_status.py
  ```
  - [ ] 確認新增文件數
  - [ ] 確認剩餘 cursor 減少
  - [ ] 記錄新的剩餘 cursor 數: ___

- [ ] **B5. 重複 B2-B4**
  - [ ] 批次 1: ___ cursor 處理 (日期: ___)
  - [ ] 批次 2: ___ cursor 處理 (日期: ___)
  - [ ] 批次 3: ___ cursor 處理 (日期: ___)
  - [ ] ... 繼續直到剩餘 cursor = 0

### 階段 C: 數據合併與去重 ⚠️

- [ ] **C1. 合併所有下載數據**
  ```bash
  python3 scripts/download_all_payments_mcp.py
  ```
  - [ ] 確認掃描文件數: ___ 個
  - [ ] 確認合併前總記錄: ___ 筆
  - [ ] 確認去重後記錄: ___ 筆
  - [ ] 確認日期範圍: 2025-01-01 至 2025-11-15

- [ ] **C2. 檢查月度統計**
  - [ ] 一月記錄數: ___
  - [ ] 二月記錄數: ___
  - [ ] 三月記錄數: ___
  - [ ] 四月記錄數: ___
  - [ ] 五月記錄數: ___
  - [ ] 六月記錄數: 0（預期）
  - [ ] 七月記錄數: 0（預期）
  - [ ] 八月記錄數: ___
  - [ ] 九月記錄數: ___
  - [ ] 十月記錄數: ___
  - [ ] 十一月記錄數: ___

### 階段 D: 格式轉換與驗證 ⚠️

- [ ] **D1. 轉換為 CSV 格式**
  ```bash
  python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json
  ```
  - [ ] 確認 CSV 生成成功
  - [ ] 確認記錄數與 JSON 一致: ___ 筆

- [ ] **D2. 營業日驗證**
  - [ ] 檢查非營業日記錄數: ___ 筆
  - [ ] 確認週日 (Sunday) 記錄數: ___
  - [ ] 確認週三 (Wednesday) 記錄數: ___
  - [ ] 確認週四 (Thursday) 記錄數: ___

- [ ] **D3. 閉店月份驗證**
  - [ ] 六月記錄數: 0（必須）
  - [ ] 七月記錄數: 0（必須）

- [ ] **D4. 特殊假期驗證**
  - [ ] 聖誕節 (12-25) 記錄數: 0（預期）

- [ ] **D5. 時區轉換驗證**
  - [ ] 檢查 EDT 期間 (03-09 至 11-02) 時間正確性
  - [ ] 檢查 EST 期間時間正確性
  - [ ] 隨機抽查 10 筆記錄的時區轉換

### 階段 E: 報告生成 ⚠️

- [ ] **E1. HTML 報告**
  ```bash
  python3 scripts/generate_html_report.py data/all_payments/all_payments.csv
  ```
  - [ ] 確認報告生成: `all_payments_report.html`
  - [ ] 檢查報告內容完整性

- [ ] **E2. 月度統計報告**
  ```bash
  python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv
  ```
  - [ ] 確認月度報告生成
  - [ ] 檢查月度趨勢圖表

- [ ] **E3. 完整數據檢查報告**
  ```bash
  python3 scripts/generate_data_report.py
  ```
  - [ ] 確認數據檢查報告生成
  - [ ] 審查異常記錄（如有）

### 階段 F: 最終驗證 ⚠️

- [ ] **F1. 數據完整性最終檢查**
  - [ ] 總記錄數合理性: ___ 筆
  - [ ] 日期範圍完整: 2025-01-01 至 2025-11-15
  - [ ] 無重複記錄（payment ID 唯一）
  - [ ] 所有 cursor 已處理完畢（剩餘 = 0）

- [ ] **F2. 業務邏輯驗證**
  - [ ] 營業日記錄占比: ___% (預期 > 95%)
  - [ ] 營業時間 (10:00-20:00) 記錄占比: ___%
  - [ ] COMPLETED 狀態記錄占比: ___%

- [ ] **F3. 文檔更新**
  - [ ] 更新 README.md 數據統計
  - [ ] 記錄最終下載日期
  - [ ] 記錄總記錄數和日期範圍

---

## 核心腳本使用說明

### 1. `download_all_payments_mcp.py` - 合併與去重

**檔案路徑**: [scripts/download_all_payments_mcp.py](scripts/download_all_payments_mcp.py)

**用途**: 掃描 MCP tools 目錄，合併所有下載的 JSON 文件

**執行命令**:
```bash
python3 scripts/download_all_payments_mcp.py
```

**功能說明**:
- 自動掃描 `~/.cursor/projects/.../agent-tools/` 目錄
- 讀取所有 `.txt` 文件（JSON 格式）
- 根據 `payment ID` 去重
- 按 `created_at` 日期過濾（2025-01-01 至 2025-11-15）
- 生成月度統計報告

**輸出檔案**:
- `data/all_payments/all_payments.json` - 合併後的 JSON
- 控制台輸出月度統計

**關鍵參數**:
```python
START_DATE = "2025-01-01"
END_DATE = "2025-11-15"
LOCATION_ID = "LMDN6Z5DKNJ2P"
```

---

### 2. `get_all_cursors_info.py` - Cursor 追蹤

**檔案路徑**: [scripts/get_all_cursors_info.py](scripts/get_all_cursors_info.py)

**用途**: 識別所有仍有 cursor 的文件，提取元數據

**執行命令**:
```bash
python3 scripts/get_all_cursors_info.py
```

**功能說明**:
- 掃描所有已下載的 JSON 文件
- 識別包含 `cursor` 欄位的文件
- 提取每個 cursor 的元數據：
  - 文件路徑
  - cursor 字串
  - 記錄數 (count)
  - 日期範圍 (min_date, max_date)
  - location_id

**輸出檔案**:
- `data/all_payments/cursors_info.json` - Cursor 元數據列表

**輸出格式**:
```json
[
  {
    "file": "697f9895-ffcf-4264-a8a1-4e5fa58273b8.txt",
    "file_path": "/Users/.../.../697f9895-....txt",
    "cursor": "eyJjcmVhdGVkQXQ...",
    "count": 100,
    "min_date": "2025-09-27",
    "max_date": "2025-09-30",
    "location_id": "LMDN6Z5DKNJ2P"
  }
]
```

---

### 3. `batch_download_with_mcp.py` - 批次下載助手

**檔案路徑**: [scripts/batch_download_with_mcp.py](scripts/batch_download_with_mcp.py)

**用途**: 生成批次下載命令，追蹤下載進度

**執行命令**:
```bash
python3 scripts/batch_download_with_mcp.py
```

**功能說明**:
- 讀取 `cursors_info.json`
- 過濾已下載的 cursor
- 批次生成 MCP Square 命令（每次 20 個）
- 保存待執行命令到文件

**輸出檔案**:
- `data/all_payments/pending_cursor_commands.json` - 待執行命令列表

**批次大小配置**:
```python
BATCH_SIZE = 20  # 每次處理 20 個 cursor
```

**生成的命令格式**:
```
service: payments
method: list
request: {
    "location_id": "LMDN6Z5DKNJ2P",
    "cursor": "eyJjcmVhdGVkQXQ...",
    "limit": 100,
    "sort_order": "ASC"
}
```

---

### 4. `show_status.py` - 快速狀態檢查

**檔案路徑**: [scripts/show_status.py](scripts/show_status.py)

**用途**: 快速顯示當前下載狀態

**執行命令**:
```bash
python3 scripts/show_status.py
```

**功能說明**:
- 統計總文件數
- 計算剩餘 cursor 數量
- 顯示已合併記錄數
- 顯示最新的 cursor 信息（可選）

**輸出範例**:
```
============================================================
📊 下載狀態
============================================================
總文件數: 710
剩餘 cursor: 694 個文件
已完成: 16 個文件
已合併記錄: 3,686 筆
============================================================
```

---

### 5. `convert_mcp_json_to_csv.py` - 格式轉換與驗證

**檔案路徑**: [scripts/convert_mcp_json_to_csv.py](scripts/convert_mcp_json_to_csv.py)

**用途**: 將 JSON 轉換為 CSV，並執行業務邏輯驗證

**執行命令**:
```bash
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json
```

**功能說明**:
- JSON 扁平化為 CSV 格式
- 時區轉換（UTC → America/New_York）
- 營業日驗證（週一、二、五、六）
- 閉店月份檢查（六月、七月）
- 特殊假期檢查（聖誕節）
- 生成驗證報告

**輸出檔案**:
- `data/all_payments/all_payments.csv` - CSV 格式數據
- 控制台輸出驗證報告

**CSV 欄位**:
```
id, created_at, status, location_id, order_id, customer_id,
amount, tip, total_amount, approved_amount, refunded_amount,
card_brand, card_last_4, card_type, entry_method,
device_id, device_name
```

**驗證規則**:
```python
BUSINESS_DAYS = {0, 1, 4, 5}  # Monday, Tuesday, Friday, Saturday
CLOSED_MONTHS = {6, 7}  # June, July
CHRISTMAS_DAY = 25
```

---

### 6. `download_2025_only.py` - 命令生成器

**檔案路徑**: [scripts/download_2025_only.py](scripts/download_2025_only.py)

**用途**: 生成 2025 年每月的初始下載命令

**執行命令**:
```bash
python3 scripts/download_2025_only.py
```

**功能說明**:
- 自動計算每個月的日期範圍
- 生成 11 個月的初始下載命令（2025-01 至 2025-11）
- 提供 cursor 繼續下載的命令模板

**輸出**:
- 控制台輸出 11 個月的 MCP 命令
- 包含 cursor 繼續下載說明

---

## 驗證項目

### 🔍 日期範圍驗證

**檢查項目**:
- [ ] 最早記錄日期 ≥ 2025-01-01 00:00:00
- [ ] 最晚記錄日期 ≤ 2025-11-15 23:59:59
- [ ] 無 2024 年或更早的記錄
- [ ] 無 2025-11-16 或更晚的記錄

**驗證方法**:
```python
# 在 CSV 中檢查
df = pd.read_csv('data/all_payments/all_payments.csv')
df['created_at'] = pd.to_datetime(df['created_at'])
print(f"最早記錄: {df['created_at'].min()}")
print(f"最晚記錄: {df['created_at'].max()}")
```

---

### 🏢 Location ID 驗證

**檢查項目**:
- [ ] 所有記錄的 location_id = "LMDN6Z5DKNJ2P"
- [ ] 無其他 location 的記錄混入

**驗證方法**:
```python
unique_locations = df['location_id'].unique()
assert len(unique_locations) == 1
assert unique_locations[0] == "LMDN6Z5DKNJ2P"
```

---

### 📅 營業日規則驗證

**營業日定義**:
- 週一 (Monday, 0)
- 週二 (Tuesday, 1)
- 週五 (Friday, 4)
- 週六 (Saturday, 5)

**檢查項目**:
- [ ] 統計非營業日記錄數（週日、三、四）
- [ ] 非營業日記錄應 < 5%（可能有特殊情況）

**決策樹**:
```
交易記錄
    │
    ├─ 星期幾？
    │   ├─ 週一 (0) ──────────┐
    │   ├─ 週二 (1) ──────────┤
    │   ├─ 週三 (2) → ⚠️ 警告  │
    │   ├─ 週四 (3) → ⚠️ 警告  │
    │   ├─ 週五 (4) ──────────┤ → ✅ 正常營業日
    │   ├─ 週六 (5) ──────────┤
    │   └─ 週日 (6) → ⚠️ 警告  │
    │                          │
    └──────────────────────────┘
```

---

### 🏖️ 閉店月份驗證

**閉店月份定義**:
- 六月 (June, 6)
- 七月 (July, 7)

**檢查項目**:
- [ ] 六月記錄數 = 0
- [ ] 七月記錄數 = 0

**驗證方法**:
```python
june_records = df[df['created_at'].dt.month == 6]
july_records = df[df['created_at'].dt.month == 7]
assert len(june_records) == 0, "六月應無營業記錄"
assert len(july_records) == 0, "七月應無營業記錄"
```

---

### 🌐 時區轉換驗證

**時區規則**:
- 來源: UTC
- 目標: America/New_York
- DST 自動處理（pytz）

**DST 轉換日期**:
- EDT 開始 (UTC-4): 2025-03-09 02:00
- EST 開始 (UTC-5): 2025-11-02 02:00

**檢查項目**:
- [ ] 三月 9 日前使用 EST (UTC-5)
- [ ] 三月 9 日後至十一月 2 日前使用 EDT (UTC-4)
- [ ] 十一月 2 日後使用 EST (UTC-5)

---

## 已識別問題與解決方案

### 🔴 問題 1: 下載未完成（694 個 cursor 待處理）

**問題描述**:
- 當前狀態: 710 個文件中，694 個仍有 cursor
- 完成度: 僅 2%（16/710）
- 估計剩餘數據: 約 69,400 筆（694 × 100）

**影響**:
- 當前合併的 3,686 筆可能只佔總數據的 5%
- 數據分析結果不完整
- 月度統計可能失真

**解決方案 - 批次處理（推薦）**:
```bash
# 步驟 1: 生成待處理 cursor 列表
python3 scripts/get_all_cursors_info.py

# 步驟 2: 批次生成命令（每次 20-50 個）
python3 scripts/batch_download_with_mcp.py

# 步驟 3: 複製命令到 Cursor MCP 執行（手動步驟）

# 步驟 4: 檢查進度
python3 scripts/show_status.py

# 重複步驟 2-4，直到剩餘 cursor = 0
```

**預期工作量**:
- 批次大小: 20 cursor/次
- 總批次數: 694 ÷ 20 = 35 批次
- 每批次執行時間: 約 5-10 分鐘
- 總預估時間: 3-6 小時

---

### 🟡 問題 2: 無法自動調用 MCP

**問題描述**:
- Python 腳本無法直接調用 MCP Square Server
- 所有 MCP 命令需要手動複製到 Cursor 執行
- 無法實現完全自動化

**短期方案**: 優化手動流程
1. 使用批次命令生成腳本減少手動工作
2. 建立標準操作流程（SOP）
3. 使用進度追蹤避免遺漏

**長期方案**: 直接使用 Square API SDK
```python
from square.client import Client

client = Client(
    access_token='YOUR_ACCESS_TOKEN',
    environment='production'
)

result = client.payments.list_payments(
    location_id='LMDN6Z5DKNJ2P',
    begin_time='2025-01-01T00:00:00Z',
    end_time='2025-01-31T23:59:59Z',
    limit=100
)
```

---

## 執行命令參考

### 📋 完整下載流程命令集

**步驟 1: 檢查當前狀態**
```bash
# 快速狀態檢查
python3 scripts/show_status.py

# 詳細 cursor 資訊
python3 scripts/get_all_cursors_info.py
```

**步驟 2: 批次下載 cursor**
```bash
# 生成批次命令（每次 20 個）
python3 scripts/batch_download_with_mcp.py

# 輸出: pending_cursor_commands.json
# 手動複製命令到 Cursor MCP Square 執行
```

**步驟 3: 合併數據**
```bash
# 合併所有下載的 JSON 文件
python3 scripts/download_all_payments_mcp.py

# 輸出:
# - data/all_payments/all_payments.json
# - 控制台顯示月度統計
```

**步驟 4: 轉換為 CSV**
```bash
# JSON → CSV 並驗證
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json

# 輸出:
# - data/all_payments/all_payments.csv
# - 控制台顯示驗證報告
```

**步驟 5: 生成報告**
```bash
# HTML 報告
python3 scripts/generate_html_report.py data/all_payments/all_payments.csv

# 月度統計報告
python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv

# 完整數據檢查報告
python3 scripts/generate_data_report.py
```

---

### 🎯 MCP Square 命令範例

**初始月度下載**
```
service: payments
method: list
request: {
    "location_id": "LMDN6Z5DKNJ2P",
    "begin_time": "2025-01-01T00:00:00Z",
    "end_time": "2025-01-31T23:59:59Z",
    "sort_order": "ASC",
    "limit": 100
}
```

**Cursor 繼續下載**
```
service: payments
method: list
request: {
    "location_id": "LMDN6Z5DKNJ2P",
    "cursor": "eyJjcmVhdGVkQXQiOjE3NTkyNjc1ODM5MTYsImlkIjoicjdkVHZNOUU5cExPMmJOc29NVjJoYUlEYmdXWlkifQ==",
    "limit": 100,
    "sort_order": "ASC"
}
```

**注意事項**:
- `cursor` 值從上一次 API 響應中獲取
- 不需要再指定 `begin_time` 和 `end_time`
- `location_id` 和 `sort_order` 必須與初始請求一致

---

## 數據完整性驗證

### ✅ 完整性檢查清單

**基本統計**:
```python
import pandas as pd

df = pd.read_csv('data/all_payments/all_payments.csv')

print("=== 基本統計 ===")
print(f"總記錄數: {len(df):,}")
print(f"唯一 Payment ID: {df['id'].nunique():,}")
print(f"日期範圍: {df['created_at'].min()} ~ {df['created_at'].max()}")
print(f"唯一 Location: {df['location_id'].nunique()}")
```

**月度分佈**:
```python
df['created_at'] = pd.to_datetime(df['created_at'])
df['month'] = df['created_at'].dt.month

monthly = df.groupby('month').size()
print("\n=== 月度分佈 ===")
for month, count in monthly.items():
    print(f"{month:02d} 月: {count:,} 筆")
```

**營業日分佈**:
```python
df['dayofweek'] = df['created_at'].dt.dayofweek
dayofweek_names = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']

print("\n=== 星期分佈 ===")
for day in range(7):
    count = len(df[df['dayofweek'] == day])
    pct = count / len(df) * 100
    print(f"{dayofweek_names[day]}: {count:,} 筆 ({pct:.1f}%)")
```

---

## 📊 進度追蹤表

### 下載進度記錄

| 批次 | 執行日期 | Cursor 數 | 新增記錄 | 剩餘 Cursor | 累計記錄 | 執行人 | 備註 |
|------|---------|----------|---------|------------|---------|-------|------|
| 初始 | 2025-11-15 | - | 3,686 | 694 | 3,686 | - | 初始狀態 |
| 1 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| 2 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| 3 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |

### 完成標準

- [ ] 剩餘 cursor = 0
- [ ] 所有文件都無 cursor 欄位
- [ ] 總記錄數穩定（重複執行合併結果一致）
- [ ] 月度統計合理（符合營業規律）
- [ ] 通過所有驗證項目

---

## 🎯 快速參考

### 立即執行（優先級最高）

```bash
# 1. 檢查當前狀態
python3 scripts/show_status.py

# 2. 更新 cursor 列表
python3 scripts/get_all_cursors_info.py

# 3. 生成批次命令
python3 scripts/batch_download_with_mcp.py

# 4. 執行 MCP 命令（手動）
# 複製 pending_cursor_commands.json 中的命令到 Cursor MCP Square

# 5. 重複步驟 1-4，直到剩餘 cursor = 0
```

### 完成後驗證

```bash
# 合併數據
python3 scripts/download_all_payments_mcp.py

# 轉換為 CSV
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json

# 生成報告
python3 scripts/generate_html_report.py data/all_payments/all_payments.csv
python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv
python3 scripts/generate_data_report.py
```

---

## 📝 相關文檔

- [README.md](README.md) - 專案完整文檔
- [agents/README.md](agents/README.md) - 多代理分析系統說明
- [CLAUDE.md](CLAUDE.md) - Claude Code 專案指引
- [Square API 文檔](https://developer.squareup.com/reference/square/payments-api) - Payments API 官方文檔

---

**文件結束**

✅ 已建立完整的 2025 年度 Square Payments 下載計畫
⚠️ 當前進度: 2% 完成（694 個 cursor 待處理）
🎯 下一步: 執行批次下載流程
