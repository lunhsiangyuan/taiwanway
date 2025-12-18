#!/usr/bin/env python3
"""
批量下載所有 cursor 的資料
讀取 cursor 列表，然後使用 MCP Square API 下載
"""
import json
import sys
from pathlib import Path

# 讀取 cursor 列表
cursors_file = Path(__file__).parent / 'cursors_to_download.json'

if not cursors_file.exists():
    print(f"❌ 找不到 cursor 列表文件: {cursors_file}")
    sys.exit(1)

with open(cursors_file, 'r', encoding='utf-8') as f:
    all_cursors = json.load(f)

print(f"總共需要下載 {len(all_cursors)} 個 cursor")
print("=" * 80)
print("請手動執行以下 MCP Square 命令來下載所有 cursor")
print("=" * 80)
print()

LOCATION_ID = "LMDN6Z5DKNJ2P"

# 生成所有下載命令
for i, item in enumerate(all_cursors, 1):
    print(f"# ───────────────────────────────────────────────────────")
    print(f"# Cursor #{i}/{len(all_cursors)}: {item['file']}")
    print(f"# ───────────────────────────────────────────────────────")
    print()
    print("service: payments")
    print("method: list")
    print("request: {")
    print(f'    "location_id": "{LOCATION_ID}",')
    print(f'    "cursor": "{item["cursor"]}",')
    print('    "limit": 100,')
    print('    "sort_order": "ASC"')
    print("}")
    print()
    print()

print("=" * 80)
print(f"總共 {len(all_cursors)} 個命令")
print("=" * 80)




