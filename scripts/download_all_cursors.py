#!/usr/bin/env python3
"""
自動下載所有剩餘的 cursor 數據
讀取 cursors_info.json，然後使用 MCP Square 工具下載
注意：此腳本需要手動調用 MCP Square 工具，這裡只是生成下載指令
"""
import json
from pathlib import Path

def load_cursors_info():
    """載入所有 cursor 信息"""
    info_file = Path(__file__).parent.parent / 'data' / 'all_payments' / 'cursors_info.json'
    if not info_file.exists():
        print(f"❌ 找不到 cursor 信息文件: {info_file}")
        return []
    
    with open(info_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_download_commands(cursors_info):
    """生成下載命令（用於參考）"""
    print("=" * 80)
    print("Cursor 下載指令（使用 MCP Square 工具）")
    print("=" * 80)
    print(f"\n總共有 {len(cursors_info)} 個 cursor 需要下載\n")
    
    for i, cursor_info in enumerate(cursors_info, 1):
        print(f"{i}. {cursor_info['file']}")
        print(f"   Date: {cursor_info['min_date']} to {cursor_info['max_date']}")
        print(f"   Cursor: {cursor_info['cursor'][:60]}...")
        print(f"   MCP Command:")
        print(f"   service: payments")
        print(f"   method: list")
        print(f"   request: {{")
        print(f"     'location_id': '{cursor_info['location_id']}',")
        print(f"     'cursor': '{cursor_info['cursor']}',")
        print(f"     'limit': 100,")
        print(f"     'sort_order': 'ASC'")
        print(f"   }}")
        print()

if __name__ == "__main__":
    cursors_info = load_cursors_info()
    if cursors_info:
        generate_download_commands(cursors_info)
    else:
        print("沒有找到 cursor 信息")






