#!/usr/bin/env python3
"""
自動下載所有剩餘的 payment 數據
持續下載直到沒有 cursor
"""
import json
from pathlib import Path

def get_latest_cursor():
    """找出最新的 cursor"""
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    json_files = list(mcp_tools_dir.glob("*.txt"))
    
    latest_cursor = None
    latest_file = None
    
    for json_file in sorted(json_files, key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cursor = data.get('cursor', '')
            if cursor:
                latest_cursor = cursor
                latest_file = json_file.name
                break
        except:
            pass
    
    return latest_cursor, latest_file

def check_all_cursors():
    """檢查所有文件中的 cursor"""
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    json_files = list(mcp_tools_dir.glob("*.txt"))
    
    cursors = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cursor = data.get('cursor', '')
            if cursor:
                payments = data.get('payments', [])
                if payments:
                    # 取得日期範圍
                    dates = [p.get('created_at', '')[:10] for p in payments if p.get('created_at')]
                    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
                    cursors.append({
                        'file': json_file.name,
                        'cursor': cursor,
                        'count': len(payments),
                        'date_range': date_range
                    })
        except:
            pass
    
    return cursors

if __name__ == "__main__":
    print("檢查所有 cursor...")
    print("=" * 80)
    
    cursors = check_all_cursors()
    if cursors:
        print(f"找到 {len(cursors)} 個文件還有 cursor：")
        for i, c in enumerate(cursors[:10], 1):
            print(f"{i}. {c['file']}: {c['count']} 筆, {c['date_range']}")
        if len(cursors) > 10:
            print(f"... 還有 {len(cursors) - 10} 個文件有 cursor")
    else:
        print("✅ 沒有找到 cursor，數據應該已完整下載")
    
    print("\n" + "=" * 80)
    latest_cursor, latest_file = get_latest_cursor()
    if latest_cursor:
        print(f"最新 cursor 在: {latest_file}")
        print(f"Cursor: {latest_cursor[:80]}...")
    else:
        print("沒有找到 cursor")






