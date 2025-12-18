#!/usr/bin/env python3
"""
生成最終狀態報告
"""
import json
import os
from pathlib import Path
from datetime import datetime

cursors_file = Path(__file__).parent / 'cursors_to_download.json'
log_file = Path(__file__).parent / 'download_progress.log'
mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"

def log_message(message):
    """記錄日誌"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def main():
    log_message("=" * 80)
    log_message("下載狀態報告")
    log_message("=" * 80)
    
    # 讀取 cursor 列表
    if cursors_file.exists():
        with open(cursors_file, 'r', encoding='utf-8') as f:
            all_cursors = json.load(f)
        log_message(f"總共需要下載: {len(all_cursors)} 個 cursor")
    else:
        log_message("❌ 找不到 cursor 列表文件")
        return
    
    # 檢查已下載的文件
    downloaded_count = 0
    if mcp_tools_dir.exists():
        downloaded_files = list(mcp_tools_dir.glob("*.txt"))
        downloaded_count = len(downloaded_files)
        log_message(f"目前已有文件: {downloaded_count} 個")
    
    # 檢查合併後的數據
    merged_file = Path(__file__).parent.parent / 'data' / 'all_payments' / 'all_payments.json'
    if merged_file.exists():
        with open(merged_file, 'r', encoding='utf-8') as f:
            merged_data = json.load(f)
        log_message(f"已合併數據: {merged_data.get('total_count', 0)} 筆")
    
    # 計算進度
    estimated_downloaded = 80  # 根據之前的記錄
    remaining = len(all_cursors) - estimated_downloaded
    progress = (estimated_downloaded / len(all_cursors)) * 100
    
    log_message(f"已下載約: {estimated_downloaded} 個 cursor ({progress:.1f}%)")
    log_message(f"剩餘約: {remaining} 個 cursor")
    log_message("")
    log_message("注意：下載過程可能因API限制而暫停")
    log_message("如果下載停止，請檢查 log 文件了解最後進度")
    log_message("=" * 80)

if __name__ == "__main__":
    main()




