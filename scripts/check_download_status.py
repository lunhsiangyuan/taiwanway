#!/usr/bin/env python3
"""
檢查下載狀態並生成報告
"""
import json
from pathlib import Path
from datetime import datetime

# MCP tools 目錄
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
# 儲存所有待下載 cursor 的文件
ALL_CURSORS_FILE = Path.home() / "Desktop/square/scripts/all_new_cursors.json"
# 合併後的數據文件
ALL_PAYMENTS_JSON = Path.home() / "Desktop/square/data/all_payments/all_payments.json"
# 進度日誌文件
PROGRESS_LOG = Path.home() / "Desktop/square/scripts/download_progress.log"

def get_all_cursors_count() -> int:
    """獲取所有 cursor 數量"""
    if not ALL_CURSORS_FILE.exists():
        return 0
    try:
        with open(ALL_CURSORS_FILE, 'r', encoding='utf-8') as f:
            return len(json.load(f))
    except Exception as e:
        print(f"⚠️  無法讀取 cursor 文件: {e}")
        return 0

def get_downloaded_files_count() -> int:
    """獲取已下載文件數量"""
    return len(list(MCP_TOOLS_DIR.glob("*.txt")))

def get_merged_data_count() -> int:
    """獲取已合併數據的記錄數"""
    if not ALL_PAYMENTS_JSON.exists():
        return 0
    try:
        with open(ALL_PAYMENTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)
    except Exception as e:
        print(f"⚠️  無法讀取合併數據文件: {e}")
        return 0

def get_latest_progress() -> str:
    """獲取最新的進度日誌"""
    if not PROGRESS_LOG.exists():
        return "無進度記錄"
    try:
        with open(PROGRESS_LOG, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip()
            return "無進度記錄"
    except Exception as e:
        return f"無法讀取進度日誌: {e}"

def main():
    print("=" * 80)
    print("下載狀態報告")
    print("=" * 80)
    print(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    total_cursors = get_all_cursors_count()
    downloaded_files = get_downloaded_files_count()
    merged_count = get_merged_data_count()
    
    print(f"總共需要下載: {total_cursors} 個 cursor")
    print(f"目前已有文件: {downloaded_files} 個")
    print(f"已合併數據: {merged_count} 筆")
    print("")
    
    # 估算進度（基於已下載文件數）
    if total_cursors > 0:
        estimated_progress = min(downloaded_files / total_cursors * 100, 100)
        print(f"估算進度: {estimated_progress:.1f}%")
        print(f"剩餘約: {max(0, total_cursors - downloaded_files)} 個 cursor")
    
    print("")
    print("=" * 80)
    print("最新進度日誌:")
    print("-" * 80)
    latest_progress = get_latest_progress()
    print(latest_progress)
    print("=" * 80)
    
    # 檢查是否有新的 cursor 需要下載
    print("")
    print("下一步建議:")
    if downloaded_files < total_cursors:
        remaining = total_cursors - downloaded_files
        print(f"1. 繼續下載剩餘的 {remaining} 個 cursor")
        print("2. 下載完成後運行: python3 scripts/download_all_payments_mcp.py")
        print("3. 檢查 scripts/download_progress.log 了解詳細進度")
    else:
        print("✅ 所有 cursor 已下載完成！")
        print("請運行: python3 scripts/download_all_payments_mcp.py 進行最後合併")

if __name__ == "__main__":
    main()

