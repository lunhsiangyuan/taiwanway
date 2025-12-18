#!/usr/bin/env python3
"""
顯示下載狀態
"""
import json
from pathlib import Path

def show_status():
    """顯示當前下載狀態"""
    # 檢查 cursor 數量
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    json_files = list(mcp_tools_dir.glob("*.txt"))
    
    cursor_count = 0
    total_files = len(json_files)
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get('cursor', ''):
                cursor_count += 1
        except:
            pass
    
    # 檢查已合併記錄數
    merged_file = Path(__file__).parent.parent / 'data' / 'all_payments' / 'all_payments.json'
    merged_count = 0
    if merged_file.exists():
        try:
            with open(merged_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                merged_count = data.get('total_count', 0)
        except:
            pass
    
    print("=" * 60)
    print("📊 下載狀態")
    print("=" * 60)
    print(f"總文件數: {total_files}")
    print(f"剩餘 cursor: {cursor_count} 個文件")
    print(f"已完成: {total_files - cursor_count} 個文件")
    print(f"已合併記錄: {merged_count:,} 筆")
    print("=" * 60)
    
    return cursor_count, merged_count

if __name__ == "__main__":
    show_status()






