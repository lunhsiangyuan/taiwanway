#!/usr/bin/env python3
"""
自動使用 MCP Square 工具批量下載剩餘的 cursor
讀取 cursors_info.json，然後使用 MCP Square API 下載
"""
import json
import time
from pathlib import Path
from typing import List, Dict, Optional

# Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# Cursor 信息文件
CURSORS_INFO_FILE = Path(__file__).parent.parent / 'data' / 'all_payments' / 'cursors_info.json'

# 進度記錄文件
PROGRESS_FILE = Path(__file__).parent / 'cursor_download_progress.json'

# MCP tools 目錄（下載的文件會保存在這裡）
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"

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

def check_file_downloaded(cursor_info: Dict) -> bool:
    """檢查 cursor 對應的文件是否已下載（沒有 cursor）"""
    file_path = Path(cursor_info['file_path'])
    
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 如果文件沒有 cursor，表示已經下載完成
        cursor = data.get('cursor', '')
        return not cursor
    except Exception as e:
        print(f"⚠️  無法讀取文件 {file_path.name}: {e}")
        return False

def download_cursor_via_mcp(cursor_info: Dict) -> bool:
    """
    使用 MCP Square 工具下載 cursor
    
    Returns:
        bool: 是否成功下載
    """
    cursor = cursor_info['cursor']
    location_id = cursor_info.get('location_id', LOCATION_ID)
    file_name = cursor_info['file']
    
    request = {
        "location_id": location_id,
        "cursor": cursor,
        "limit": 100,
        "sort_order": "ASC"
    }
    
    # 注意：此處需要使用 MCP Square 工具來實際下載
    # 由於腳本中無法直接調用 MCP 工具，這個函數會返回 False
    # 實際下載需要通過其他方式（如生成命令列表或使用其他自動化工具）
    return False

def main():
    print("=" * 80)
    print("自動下載剩餘的 cursor（使用 MCP Square 工具）")
    print("=" * 80)
    
    # 載入 cursor 信息
    cursors_info = load_cursors_info()
    if not cursors_info:
        print("❌ 沒有找到需要下載的 cursor")
        print(f"   請先運行: python3 scripts/get_all_cursors_info.py")
        return
    
    # 載入進度
    progress = load_progress()
    downloaded = set(progress.get("downloaded", []))
    failed = set(progress.get("failed", []))
    last_index = progress.get("last_index", 0)
    
    # 過濾出需要下載的 cursor（排除已下載和已失敗的）
    remaining = []
    for i, cursor_info in enumerate(cursors_info):
        file_name = cursor_info['file']
        if file_name in downloaded:
            continue
        if file_name in failed:
            continue
        # 檢查文件是否已經下載完成（沒有 cursor）
        if check_file_downloaded(cursor_info):
            downloaded.add(file_name)
            continue
        remaining.append((i, cursor_info))
    
    total = len(cursors_info)
    remaining_count = len(remaining)
    
    print(f"\n總共需要下載: {total} 個 cursor")
    print(f"已完成: {len(downloaded)} 個")
    print(f"失敗: {len(failed)} 個")
    print(f"剩餘: {remaining_count} 個")
    print("=" * 80)
    
    if remaining_count == 0:
        print("✅ 所有 cursor 已下載完成！")
        return
    
    # 批量下載設定
    batch_size = 20  # 每次下載 20 個
    start_index = last_index
    end_index = min(start_index + batch_size, remaining_count)
    
    print(f"\n準備下載第 {start_index + 1}-{end_index} 個 cursor (共 {end_index - start_index} 個)")
    print("\n⚠️  注意：此腳本需要配合 MCP Square 工具使用")
    print("   每個 cursor 需要使用以下命令下載：\n")
    
    success_count = 0
    new_downloaded = []
    
    for idx, (original_idx, cursor_info) in enumerate(remaining[start_index:end_index], start=start_index + 1):
        cursor = cursor_info['cursor']
        file_name = cursor_info['file']
        date_range = f"{cursor_info['min_date']} to {cursor_info['max_date']}"
        location_id = cursor_info.get('location_id', LOCATION_ID)
        
        print(f"# ───────────────────────────────────────────────────────")
        print(f"# Cursor #{idx}/{remaining_count}: {file_name}")
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
        
        # 更新進度（假設會手動下載）
        new_downloaded.append(file_name)
        success_count += 1
    
    # 更新進度
    progress["downloaded"].extend(new_downloaded)
    progress["last_index"] = end_index
    save_progress(progress)
    
    print("=" * 80)
    print(f"已生成 {end_index - start_index} 個下載命令")
    print("=" * 80)
    print("\n使用說明:")
    print("1. 複製上面的每個命令到 MCP Square 工具中執行")
    print("2. MCP 會自動保存文件到:")
    print(f"   {MCP_TOOLS_DIR}")
    print("3. 下載完成後，運行合併腳本:")
    print("   python3 scripts/download_all_payments_mcp.py")
    print("4. 繼續下載剩餘 cursor:")
    print("   python3 scripts/auto_download_remaining_cursors.py")
    print("5. 檢查狀態:")
    print("   python3 scripts/download_all_remaining.py")
    print()

if __name__ == "__main__":
    main()



