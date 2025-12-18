#!/usr/bin/env python3
"""
自動下載所有 2025 年 payments 數據的 cursor 頁面
"""
import json
import os
from pathlib import Path

# Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# MCP tools 目錄
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"

def get_cursor_from_file(file_path: Path) -> str:
    """從文件中讀取 cursor"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cursor', '')
    except Exception as e:
        print(f"⚠️  無法讀取 {file_path.name}: {e}")
        return ''

def download_with_cursor(cursor: str) -> dict:
    """使用 cursor 下載數據（需要手動調用 MCP Square）"""
    return {
        "location_id": LOCATION_ID,
        "cursor": cursor,
        "limit": 100,
        "sort_order": "ASC"
    }

def main():
    """生成所有 cursor 下載命令"""
    if not MCP_TOOLS_DIR.exists():
        print(f"❌ MCP tools 目錄不存在: {MCP_TOOLS_DIR}")
        return
    
    # 查找所有 .txt 文件
    txt_files = sorted(MCP_TOOLS_DIR.glob("*.txt"))
    
    if not txt_files:
        print(f"❌ 在 {MCP_TOOLS_DIR} 中找不到 .txt 文件")
        return
    
    print("=" * 80)
    print("檢查需要下載的 cursor")
    print("=" * 80)
    print()
    
    cursors_to_download = []
    
    for txt_file in txt_files:
        cursor = get_cursor_from_file(txt_file)
        if cursor:
            payments_count = len(json.load(open(txt_file)).get('payments', []))
            cursors_to_download.append({
                'file': txt_file.name,
                'cursor': cursor,
                'payments': payments_count
            })
            print(f"✅ {txt_file.name}: {payments_count} 筆記錄，有 cursor")
    
    print()
    print(f"總共找到 {len(cursors_to_download)} 個需要下載的 cursor")
    print()
    print("=" * 80)
    print("Cursor 下載命令（請在 MCP Square 中執行）")
    print("=" * 80)
    print()
    
    for i, item in enumerate(cursors_to_download, 1):
        print(f"# ───────────────────────────────────────────────────────")
        print(f"# Cursor #{i}: {item['file']}")
        print(f"# 前一頁: {item['payments']} 筆記錄")
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
    print("說明:")
    print("1. 複製上面的每個命令到 MCP Square 執行")
    print("2. 如果返回的結果還有 cursor，需要繼續下載")
    print("3. 重複直到沒有 cursor 為止")
    print("=" * 80)

if __name__ == "__main__":
    main()




