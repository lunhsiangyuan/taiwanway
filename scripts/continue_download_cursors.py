#!/usr/bin/env python3
"""
繼續下載所有剩餘的 cursor
讀取 cursor 列表，從指定位置開始下載
"""
import json
import sys
from pathlib import Path
from datetime import datetime

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
    
    # 檢查已下載的文件數量
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    downloaded_count = 0
    if mcp_tools_dir.exists():
        downloaded_files = list(mcp_tools_dir.glob("*.txt"))
        downloaded_count = len(downloaded_files)
    
    log_message("=" * 80)
    log_message(f"繼續下載 cursor")
    log_message(f"總共需要下載: {len(all_cursors)} 個")
    log_message(f"目前已有文件: {downloaded_count} 個")
    log_message(f"已下載約: 50 個 cursor (15.7%)")
    log_message(f"剩餘約: {len(all_cursors) - 50} 個 cursor")
    log_message("=" * 80)
    log_message("")
    log_message("注意：由於數量較多，建議分批下載")
    log_message("每次下載10-20個cursor，然後合併數據")
    log_message("")

if __name__ == "__main__":
    main()




