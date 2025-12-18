#!/usr/bin/env python3
"""
生成所有 cursor 的下載命令
"""
import json
from pathlib import Path

# Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# MCP tools 目錄
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
# 儲存所有待下載 cursor 的文件
ALL_CURSORS_FILE = Path.home() / "Desktop/square/scripts/all_new_cursors.json"
# 輸出命令文件
COMMANDS_FILE = Path.home() / "Desktop/square/scripts/all_download_commands.txt"

def main():
    # 讀取所有 cursor
    with open(ALL_CURSORS_FILE, 'r', encoding='utf-8') as f:
        all_cursors = json.load(f)
    
    print(f"總共 {len(all_cursors)} 個 cursor")
    
    # 生成命令
    commands = []
    for i, cursor in enumerate(all_cursors):
        # 跳過無效的 cursor（如 "CAASGgoS..." 開頭的）
        if cursor.startswith("CAASGgoS"):
            print(f"跳過無效 cursor #{i+1}: {cursor[:30]}...")
            continue
        
        file_name = f"cursor_batch_{i+1:04d}.txt"
        command = f'make_api_request service: payments method: list request: {{ "location_id": "{LOCATION_ID}", "cursor": "{cursor}", "limit": 100, "sort_order": "ASC" }} > {MCP_TOOLS_DIR / file_name}'
        commands.append(command)
    
    # 寫入文件
    with open(COMMANDS_FILE, 'w', encoding='utf-8') as f:
        for cmd in commands:
            f.write(cmd + "\n")
    
    print(f"✅ 已生成 {len(commands)} 個下載命令至: {COMMANDS_FILE}")
    print(f"   無效 cursor: {len(all_cursors) - len(commands)} 個")

if __name__ == "__main__":
    main()




