# 下载 2025 年 Payments 数据指南

**日期范围**: 2025-01-01 至 2025-11-15

## 快速开始

### 步骤 1: 生成下载命令

```bash
python3 scripts/download_2025_only.py
```

这将生成 11 个月的 MCP Square 下载命令。

### 步骤 2: 使用 MCP Square 下载数据

将生成的命令逐个复制到 MCP Square 中执行。

**示例命令（2025-01）**:
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

### 步骤 3: 处理 Cursor（如有）

如果 MCP Square 返回结果中包含 `cursor` 字段，表示还有更多数据需要下载。

**Cursor 命令格式**:
```
service: payments
method: list
request: {
    "location_id": "LMDN6Z5DKNJ2P",
    "cursor": "<从上次响应中获取的 cursor>",
    "limit": 100,
    "sort_order": "ASC"
}
```

重复使用返回的 cursor 继续下载，直到没有 cursor 返回为止。

### 步骤 4: 合并所有下载的数据

```bash
python3 scripts/download_all_payments_mcp.py
```

这个脚本会：
- 自动扫描 `~/.cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/` 目录
- 读取所有 MCP 下载的 `.txt` 文件
- 自动去重（根据 payment ID）
- **过滤日期**: 只保留 2025-01-01 至 2025-11-15 的数据
- 显示按月份的统计信息
- 输出到 `data/all_payments/all_payments.json`

**预期输出**:
```
总共找到 XXX 筆記錄
去重後: XXX 筆唯一記錄

⏳ 過濾日期範圍: 2025-01-01 至 2025-11-15
過濾前: XXX 筆
過濾後: XXX 筆 (2025 年數據)

📊 按月份統計 (2025 年):
------------------------------------------------------------
  2025-01:  XXX 筆
  2025-02:  XXX 筆
  ...
------------------------------------------------------------
  總計:   XXX 筆

✅ 已合併並儲存至 data/all_payments/all_payments.json
```

### 步骤 5: 转换为 CSV

```bash
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json
```

这个脚本会：
- 将 JSON 转换为 CSV 格式
- **验证日期范围**: 确保所有数据都在 2025-01-01 至 2025-11-15 范围内
- 检查营业日规则（周一、二、五、六）
- 检查六七月数据（应该为空）
- 输出到 `data/all_payments/all_payments.csv`

### 步骤 6: 生成报告

```bash
# HTML 报告
python3 scripts/generate_html_report.py data/all_payments/all_payments.csv

# 月度统计报告
python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv

# 完整数据检查报告
python3 scripts/generate_data_report.py
```

---

## 文件说明

### 新增脚本

- **`scripts/download_2025_only.py`**: 生成 2025 年下载命令
  - 输出 11 个月的 MCP Square 命令
  - 包含 cursor 处理说明
  - 标注暑期休息月份（六、七月）

### 修改脚本

1. **`scripts/download_all_payments_mcp.py`**
   - ✅ 添加日期过滤: 只保留 2025-01-01 至 2025-11-15
   - ✅ 显示按月份统计
   - ✅ 自动排除 2024 年及之前的数据

2. **`scripts/convert_mcp_json_to_csv.py`**
   - ✅ 添加日期范围验证
   - ✅ 检测非 2025 年数据并报警

3. **`scripts/generate_html_report.py`**
   - ✅ 更新为 2025 年数据标题

4. **`scripts/generate_monthly_report.py`**
   - ✅ 更新为 2025 年数据标题

5. **`scripts/generate_data_report.py`**
   - ✅ 更新为 2025 年数据标题

---

## 数据清理

所有旧数据已清空：
- ✅ `data/all_payments/` 目录已清空
- ✅ 准备接收 2025 年新数据

---

## 营业规则

- **营业日**: 周一、周二、周五、周六（每周四天）
- **不营业月份**: 六月、七月（暑期休息）
- **特殊假期**: 圣诞节（12月25日）
- **Location ID**: LMDN6Z5DKNJ2P

---

## 月份摘要

| 月份 | 日期范围 | 状态 |
|------|---------|------|
| 2025-01 | 2025-01-01 至 2025-01-31 | 冬季营业 |
| 2025-02 | 2025-02-01 至 2025-02-28 | 冬季营业 |
| 2025-03 | 2025-03-01 至 2025-03-31 | 春季营业 |
| 2025-04 | 2025-04-01 至 2025-04-30 | 春季营业 |
| 2025-05 | 2025-05-01 至 2025-05-31 | 春季营业 |
| 2025-06 | 2025-06-01 至 2025-06-30 | ⚠️ 暑期休息，应该无数据 |
| 2025-07 | 2025-07-01 至 2025-07-31 | ⚠️ 暑期休息，应该无数据 |
| 2025-08 | 2025-08-01 至 2025-08-31 | 秋季营业 |
| 2025-09 | 2025-09-01 至 2025-09-30 | 秋季营业 |
| 2025-10 | 2025-10-01 至 2025-10-31 | 秋季营业 |
| 2025-11 | 2025-11-01 至 2025-11-15 | 秋季营业（前15天）|

---

## 注意事项

1. **分页下载**: Square API 每页最多返回 100 笔记录
   - 如果某个月有 >100 笔交易，会返回 cursor
   - 必须使用 cursor 继续下载，直到没有 cursor 为止

2. **数据去重**: 合并时会根据 payment ID 自动去重
   - 即使重复下载同一时间段，也不会产生重复记录

3. **时区转换**: 所有时间自动转换
   - API 使用 UTC 时间
   - 脚本会自动转换为纽约时区（America/New_York）
   - 自动处理夏令时（DST）

4. **日期过滤**: 系统会严格过滤日期
   - 只保留 2025-01-01 00:00:00 至 2025-11-15 23:59:59 (UTC)
   - 2024 年或更早的数据会被自动排除

5. **营业日验证**: CSV 转换时会检查
   - 非营业日的记录会被标记
   - 六七月的记录会被标记（应该为空）

---

## 疑难排解

### 问题 1: 找不到 MCP 下载的文件

**解决方案**:
- 确认 MCP Square 已成功执行命令
- 检查目录: `~/.cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/`
- 文件格式应该是 `.txt`，内容是 JSON 格式

### 问题 2: 合并后数据为空

**可能原因**:
1. MCP 文件目录路径不正确
2. 下载的数据不在 2025-01-01 至 2025-11-15 范围内
3. JSON 格式不正确

**解决方案**:
- 检查脚本输出的错误信息
- 手动查看 MCP 下载的文件内容
- 确认日期范围正确

### 问题 3: CSV 转换失败

**可能原因**:
- JSON 文件格式不正确
- 缺少必要的字段

**解决方案**:
- 检查 `all_payments.json` 文件格式
- 确认文件不为空
- 查看脚本错误信息

---

## 完整工作流程示意图

```
┌─────────────────────────────────────────────┐
│ 1. 生成下载命令                              │
│    python3 scripts/download_2025_only.py    │
└──────────────┬──────────────────────────────┘
               │
               v
┌─────────────────────────────────────────────┐
│ 2. 使用 MCP Square 下载                      │
│    - 复制命令到 MCP Square                    │
│    - 逐月下载数据                            │
│    - 处理所有 cursor                         │
└──────────────┬──────────────────────────────┘
               │
               v
┌─────────────────────────────────────────────┐
│ 3. 合并数据 (自动去重 + 日期过滤)            │
│    python3 scripts/download_all_payments_   │
│    mcp.py                                   │
│    → data/all_payments/all_payments.json    │
└──────────────┬──────────────────────────────┘
               │
               v
┌─────────────────────────────────────────────┐
│ 4. 转换为 CSV (日期验证 + 营业日检查)         │
│    python3 scripts/convert_mcp_json_to_     │
│    csv.py ...                               │
│    → data/all_payments/all_payments.csv     │
└──────────────┬──────────────────────────────┘
               │
               v
┌─────────────────────────────────────────────┐
│ 5. 生成报告                                  │
│    - HTML 报告                               │
│    - 月度统计报告                            │
│    - 数据检查报告                            │
└─────────────────────────────────────────────┘
```

---

## 下一步

下载完成后，可以继续进行：

1. **流量分析**: `python3 scripts/analysis/analyze_hourly_traffic.py`
2. **周间日分析**: `python3 scripts/analysis/analyze_weekday_revenue.py`
3. **总营收计算**: `python3 scripts/analysis/calculate_total_revenue.py`
4. **成本分析**: `python3 scripts/analysis/analyze_cost_structure.py`

---

**创建日期**: 2025-11-15
**数据范围**: 2025-01-01 至 2025-11-15
**Location**: Taiwanway (LMDN6Z5DKNJ2P)
