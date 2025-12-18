#!/usr/bin/env python3
"""
自動下載所有 cursor 並合併數據
如果遇到問題會記錄到 log 文件
"""
import json
import sys
import time
from pathlib import Path
from datetime import datetime

# 讀取 cursor 列表
cursors_file = Path(__file__).parent / 'cursors_to_download.json'
log_file = Path(__file__).parent / 'download_progress.log'

def log_message(message):
    """記錄日誌"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def main():
    if not cursors_file.exists():
        log_message(f"❌ 找不到 cursor 列表文件: {cursors_file}")
        sys.exit(1)
    
    with open(cursors_file, 'r', encoding='utf-8') as f:
        all_cursors = json.load(f)
    
    log_message("=" * 80)
    log_message(f"開始下載所有 cursor，總共 {len(all_cursors)} 個")
    log_message("=" * 80)
    
    # 檢查已下載的文件
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    downloaded_count = 0
    
    if mcp_tools_dir.exists():
        downloaded_files = list(mcp_tools_dir.glob("*.txt"))
        downloaded_count = len(downloaded_files)
        log_message(f"目前已有 {downloaded_count} 個下載文件")
    
    log_message(f"需要下載 {len(all_cursors)} 個 cursor")
    log_message("")
    log_message("注意：此腳本會生成 MCP Square 命令，需要手動執行")
    log_message("或使用 MCP Square API 工具批量下載")
    log_message("")
    
    # 生成下載命令
    LOCATION_ID = "LMDN6Z5DKNJ2P"
    commands_file = Path(__file__).parent / 'all_cursor_commands.txt'
    
    with open(commands_file, 'w', encoding='utf-8') as f:
        for i, item in enumerate(all_cursors, 1):
            f.write(f"# ───────────────────────────────────────────────────────\n")
            f.write(f"# Cursor #{i}/{len(all_cursors)}: {item['file']}\n")
            f.write(f"# ───────────────────────────────────────────────────────\n")
            f.write("\n")
            f.write("service: payments\n")
            f.write("method: list\n")
            f.write("request: {\n")
            f.write(f'    "location_id": "{LOCATION_ID}",\n')
            f.write(f'    "cursor": "{item["cursor"]}",\n')
            f.write('    "limit": 100,\n')
            f.write('    "sort_order": "ASC"\n')
            f.write("}\n")
            f.write("\n")
            f.write("\n")
    
    log_message(f"✅ 所有下載命令已生成至: {commands_file}")
    log_message(f"   總共 {len(all_cursors)} 個命令")
    log_message("")
    log_message("下一步：")
    log_message("1. 使用 MCP Square API 工具批量下載這些 cursor")
    log_message("2. 下載完成後運行: python3 scripts/download_all_payments_mcp.py")
    log_message("3. 檢查 log 文件了解進度")

if __name__ == "__main__":
    main()




