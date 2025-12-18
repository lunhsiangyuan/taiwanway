#!/usr/bin/env python3
"""
自動使用 MCP Square 工具下載剩餘的 cursor
直接調用 MCP 工具進行下載
"""
import json
import time
from pathlib import Path
from typing import List, Dict

# Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# Cursor 信息文件
CURSORS_INFO_FILE = Path(__file__).parent.parent / 'data' / 'all_payments' / 'cursors_info.json'

# 進度記錄文件
PROGRESS_FILE = Path(__file__).parent / 'cursor_download_progress.json'

# MCP tools 目錄
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"

def load_progress() -> Dict:
    """載入下載進度"""
    if not PROGRESS_FILE.exists():
        return {"downloaded": [], "failed": [], "last_index": 0, "total": 0}
    
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  無法讀取進度文件: {e}")
        return {"downloaded": [], "failed": [], "last_index": 0, "total": 0}

def save_progress(progress: Dict):
    """保存下載進度"""
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ 無法保存進度文件: {e}")

def load_cursors_info() -> List[Dict]:
    """載入 cursor 信息"""
    if not CURSORS_INFO_FILE.exists():
        print(f"❌ 找不到 cursor 信息文件: {CURSORS_INFO_FILE}")
        return []
    
    try:
        with open(CURSORS_INFO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 無法讀取 cursor 信息文件: {e}")
        return []

def check_file_downloaded(cursor_info: Dict) -> bool:
    """檢查 cursor 對應的文件是否已下載完成（沒有 cursor）"""
    file_path = Path(cursor_info['file_path'])
    
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 如果文件沒有 cursor，表示已經下載完成
        cursor = data.get('cursor', '')
        if not cursor:
            return True
        
        # 檢查 cursor 是否已變化（表示有新的數據）
        if cursor != cursor_info['cursor']:
            return True
        
        return False
    except Exception as e:
        return False

def main():
    print("=" * 80)
    print("自動下載剩餘的 cursor（使用 MCP Square 工具）")
    print("=" * 80)
    
    # 載入 cursor 信息
    cursors_info = load_cursors_info()
    if not cursors_info:
        return
    
    # 載入進度
    progress = load_progress()
    downloaded = set(progress.get("downloaded", []))
    failed = set(progress.get("failed", []))
    
    # 過濾出需要下載的 cursor
    remaining = []
    for cursor_info in cursors_info:
        file_name = cursor_info['file']
        
        if file_name in downloaded:
            continue
        if file_name in failed:
            continue
        
        if check_file_downloaded(cursor_info):
            downloaded.add(file_name)
            continue
        
        remaining.append(cursor_info)
    
    total = len(cursors_info)
    remaining_count = len(remaining)
    downloaded_count = len(downloaded)
    
    print(f"\n總共需要下載: {total} 個 cursor")
    print(f"已完成: {downloaded_count} 個 ({downloaded_count/total*100:.1f}%)")
    print(f"失敗: {len(failed)} 個")
    print(f"剩餘: {remaining_count} 個 ({remaining_count/total*100:.1f}%)")
    print("=" * 80)
    
    if remaining_count == 0:
        print("\n✅ 所有 cursor 已下載完成！")
        return
    
    # 批量下載設定
    batch_size = 10  # 每次下載 10 個
    last_index = progress.get("last_index", 0)
    start_index = last_index
    end_index = min(start_index + batch_size, remaining_count)
    
    print(f"\n準備下載第 {start_index + 1}-{end_index} 個 cursor (共 {end_index - start_index} 個)")
    print(f"進度: {start_index}/{remaining_count} ({start_index/remaining_count*100:.1f}%)\n")
    
    # 更新進度
    progress["downloaded"] = list(downloaded)
    progress["total"] = total
    
    # 顯示需要下載的 cursor 信息
    for idx, cursor_info in enumerate(remaining[start_index:end_index], start=start_index + 1):
        cursor = cursor_info['cursor']
        file_name = cursor_info['file']
        date_range = f"{cursor_info['min_date']} to {cursor_info['max_date']}"
        location_id = cursor_info.get('location_id', LOCATION_ID)
        
        print(f"[{idx}/{remaining_count}] {file_name} ({date_range})")
        print(f"   Cursor: {cursor[:60]}...")
        
        # 注意：這裡需要實際調用 MCP 工具
        # 由於腳本環境限制，這裡只顯示命令
        print(f"   命令:")
        print(f"   service: payments")
        print(f"   method: list")
        print(f"   request: {{")
        print(f'       "location_id": "{location_id}",')
        print(f'       "cursor": "{cursor}",')
        print(f'       "limit": 100,')
        print(f'       "sort_order": "ASC"')
        print(f"   }}")
        print()
    
    progress["last_index"] = end_index
    save_progress(progress)
    
    print("=" * 80)
    print(f"已準備 {end_index - start_index} 個下載任務")
    print("=" * 80)
    print("\n⚠️  注意：此腳本需要在支持 MCP 工具的環境中運行")
    print("   實際下載需要使用 MCP Square 工具來執行上面的命令")
    print()

if __name__ == "__main__":
    main()



