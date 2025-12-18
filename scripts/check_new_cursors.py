#!/usr/bin/env python3
"""
檢查所有已下載文件中的 cursor，找出新的 cursor 需要下載
"""
import json
from pathlib import Path

# MCP tools 目錄
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
# 儲存所有待下載 cursor 的文件
ALL_CURSORS_FILE = Path.home() / "Desktop/square/scripts/all_new_cursors.json"

def get_all_cursors_from_downloaded_files() -> set:
    """從所有已下載的文件中提取所有 cursor"""
    all_cursors = set()
    
    if not MCP_TOOLS_DIR.exists():
        return all_cursors
    
    for txt_file in MCP_TOOLS_DIR.glob("*.txt"):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'cursor' in data and data['cursor']:
                    # 跳過無效的 cursor
                    cursor = data['cursor']
                    if not cursor.startswith("CAASGgoS") and len(cursor) > 10:
                        all_cursors.add(cursor)
        except json.JSONDecodeError:
            continue
        except Exception as e:
            continue
    
    return all_cursors

def get_cursors_from_list_file() -> set:
    """從 cursor 列表文件中讀取所有 cursor"""
    if not ALL_CURSORS_FILE.exists():
        return set()
    try:
        with open(ALL_CURSORS_FILE, 'r', encoding='utf-8') as f:
            cursors = json.load(f)
            # 過濾無效的 cursor
            return {c for c in cursors if not c.startswith("CAASGgoS") and len(c) > 10}
    except Exception as e:
        print(f"⚠️  無法讀取 cursor 列表文件: {e}")
        return set()

def main():
    print("=" * 80)
    print("檢查新的 cursor")
    print("=" * 80)
    print()
    
    # 從已下載文件中提取 cursor
    downloaded_cursors = get_all_cursors_from_downloaded_files()
    print(f"從已下載文件中找到: {len(downloaded_cursors)} 個 cursor")
    
    # 從列表中讀取 cursor
    list_cursors = get_cursors_from_list_file()
    print(f"從列表中讀取: {len(list_cursors)} 個 cursor")
    print()
    
    # 找出需要下載的新 cursor（在列表中但不在已下載文件中）
    new_cursors = list_cursors - downloaded_cursors
    
    print("=" * 80)
    if new_cursors:
        print(f"發現 {len(new_cursors)} 個新的 cursor 需要下載:")
        print()
        for i, cursor in enumerate(list(new_cursors)[:10], 1):
            print(f"{i}. {cursor[:60]}...")
        if len(new_cursors) > 10:
            print(f"... 還有 {len(new_cursors) - 10} 個")
        
        # 保存新的 cursor 列表
        output_file = Path.home() / "Desktop/square/scripts/new_cursors_to_download.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(list(new_cursors), f, indent=2)
        print()
        print(f"✅ 已保存新的 cursor 列表至: {output_file}")
    else:
        print("✅ 沒有發現新的 cursor，所有 cursor 都已下載！")
    
    print("=" * 80)

if __name__ == "__main__":
    main()




