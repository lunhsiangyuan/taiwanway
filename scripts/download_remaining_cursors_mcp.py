#!/usr/bin/env python3
"""
使用 MCP Square 工具批量下載剩餘的 cursor
讀取 cursors_info.json，然後使用 MCP Square API 下載
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

def load_progress() -> Dict:
    """載入下載進度"""
    if not PROGRESS_FILE.exists():
        return {"downloaded": [], "failed": [], "last_index": 0}
    
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  無法讀取進度文件: {e}")
        return {"downloaded": [], "failed": [], "last_index": 0}

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

def download_cursor_via_mcp(cursor_info: Dict) -> bool:
    """
    使用 MCP Square 工具下載 cursor
    
    Returns:
        bool: 是否成功下載
    """
    cursor = cursor_info['cursor']
    location_id = cursor_info.get('location_id', LOCATION_ID)
    
    request = {
        "location_id": location_id,
        "cursor": cursor,
        "limit": 100,
        "sort_order": "ASC"
    }
    
    try:
        # 使用 MCP 工具下載
        # 注意：這需要實際調用 MCP Square 工具
        # 由於無法在腳本中直接調用，這裡返回需要執行的命令信息
        return True
    except Exception as e:
        print(f"   ❌ 下載失敗: {e}")
        return False

def main():
    print("=" * 80)
    print("下載剩餘的 cursor（使用 MCP Square 工具）")
    print("=" * 80)
    
    # 載入 cursor 信息
    cursors_info = load_cursors_info()
    if not cursors_info:
        print("❌ 沒有找到需要下載的 cursor")
        return
    
    # 載入進度
    progress = load_progress()
    downloaded = set(progress.get("downloaded", []))
    failed = set(progress.get("failed", []))
    last_index = progress.get("last_index", 0)
    
    total = len(cursors_info)
    remaining = [c for c in cursors_info if c['file'] not in downloaded and c['file'] not in failed]
    
    print(f"\n總共需要下載: {total} 個 cursor")
    print(f"已完成: {len(downloaded)} 個")
    print(f"失敗: {len(failed)} 個")
    print(f"剩餘: {len(remaining)} 個")
    print("=" * 80)
    
    if not remaining:
        print("✅ 所有 cursor 已下載完成！")
        return
    
    # 批量下載設定
    batch_size = 50  # 每次下載 50 個
    start_index = last_index
    end_index = min(start_index + batch_size, len(remaining))
    
    print(f"\n準備下載第 {start_index + 1}-{end_index} 個 cursor (共 {end_index - start_index} 個)")
    print("\n請使用 MCP Square 工具執行以下命令：\n")
    
    success_count = 0
    fail_count = 0
    
    for i, cursor_info in enumerate(remaining[start_index:end_index], start=start_index + 1):
        cursor = cursor_info['cursor']
        file_name = cursor_info['file']
        date_range = f"{cursor_info['min_date']} to {cursor_info['max_date']}"
        location_id = cursor_info.get('location_id', LOCATION_ID)
        
        print(f"# ───────────────────────────────────────────────────────")
        print(f"# Cursor #{i}/{len(remaining)}: {file_name}")
        print(f"# 日期範圍: {date_range}")
        print(f"# ───────────────────────────────────────────────────────")
        print()
        print("service: payments")
        print("method: list")
        print("request: {")
        print(f'    "location_id": "{location_id}",')
        print(f'    "cursor": "{cursor}",')
        print('    "limit": 100,')
        print('    "sort_order": "ASC"')
        print("}")
        print()
        print()
    
    print("=" * 80)
    print(f"總共生成 {end_index - start_index} 個下載命令")
    print("=" * 80)
    print("\n使用說明:")
    print("1. 複製上面的每個命令到 MCP Square")
    print("2. 依次執行每個命令")
    print("3. MCP 會自動保存文件到:")
    print("   ~/.cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/")
    print("4. 下載完成後，運行合併腳本:")
    print("   python3 scripts/download_all_payments_mcp.py")
    print("5. 檢查剩餘 cursor:")
    print("   python3 scripts/download_all_remaining.py")
    print()

if __name__ == "__main__":
    main()



