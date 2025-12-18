#!/usr/bin/env python3
"""
繼續下載剩餘的 cursor
自動檢測下載狀態，生成下載命令，並追蹤進度
"""
import json
import time
from pathlib import Path
from typing import List, Dict, Set

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
        print(f"   請先運行: python3 scripts/get_all_cursors_info.py")
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

def get_remaining_cursors(cursors_info: List[Dict], progress: Dict) -> List[Dict]:
    """獲取需要下載的剩餘 cursor"""
    downloaded = set(progress.get("downloaded", []))
    failed = set(progress.get("failed", []))
    
    remaining = []
    for cursor_info in cursors_info:
        file_name = cursor_info['file']
        
        # 跳過已下載的
        if file_name in downloaded:
            continue
        
        # 跳過已失敗的
        if file_name in failed:
            continue
        
        # 檢查文件是否已經下載完成
        if check_file_downloaded(cursor_info):
            downloaded.add(file_name)
            continue
        
        remaining.append(cursor_info)
    
    # 更新已下載列表
    if len(downloaded) > len(progress.get("downloaded", [])):
        progress["downloaded"] = list(downloaded)
        save_progress(progress)
    
    return remaining

def main():
    print("=" * 80)
    print("繼續下載剩餘的 cursor")
    print("=" * 80)
    
    # 載入 cursor 信息
    cursors_info = load_cursors_info()
    if not cursors_info:
        return
    
    # 載入進度
    progress = load_progress()
    
    # 獲取剩餘的 cursor
    remaining = get_remaining_cursors(cursors_info, progress)
    
    total = len(cursors_info)
    remaining_count = len(remaining)
    downloaded_count = len(progress.get("downloaded", []))
    failed_count = len(progress.get("failed", []))
    
    print(f"\n總共需要下載: {total} 個 cursor")
    print(f"已完成: {downloaded_count} 個 ({downloaded_count/total*100:.1f}%)")
    print(f"失敗: {failed_count} 個")
    print(f"剩餘: {remaining_count} 個 ({remaining_count/total*100:.1f}%)")
    print("=" * 80)
    
    if remaining_count == 0:
        print("\n✅ 所有 cursor 已下載完成！")
        print("\n請運行以下命令合併數據：")
        print("   python3 scripts/download_all_payments_mcp.py")
        return
    
    # 批量下載設定
    batch_size = 20  # 每次生成 20 個下載命令
    last_index = progress.get("last_index", 0)
    start_index = last_index
    end_index = min(start_index + batch_size, remaining_count)
    
    print(f"\n準備下載第 {start_index + 1}-{end_index} 個 cursor (共 {end_index - start_index} 個)")
    print(f"進度: {start_index}/{remaining_count} ({start_index/remaining_count*100:.1f}%)")
    print("\n請使用以下命令在 MCP Square 工具中執行：\n")
    
    commands = []
    for idx, cursor_info in enumerate(remaining[start_index:end_index], start=start_index + 1):
        cursor = cursor_info['cursor']
        file_name = cursor_info['file']
        date_range = f"{cursor_info['min_date']} to {cursor_info['max_date']}"
        location_id = cursor_info.get('location_id', LOCATION_ID)
        
        command_info = {
            "index": idx,
            "total": remaining_count,
            "file": file_name,
            "date_range": date_range,
            "location_id": location_id,
            "cursor": cursor
        }
        commands.append(command_info)
        
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
    
    # 更新進度
    progress["last_index"] = end_index
    progress["total"] = total
    save_progress(progress)
    
    # 保存命令到文件
    commands_file = Path(__file__).parent / 'pending_cursor_commands.json'
    try:
        with open(commands_file, 'w', encoding='utf-8') as f:
            json.dump(commands, f, indent=2, ensure_ascii=False)
        print(f"✅ 已保存 {len(commands)} 個命令到: {commands_file}")
    except Exception as e:
        print(f"⚠️  無法保存命令文件: {e}")
    
    print("=" * 80)
    print(f"已生成 {end_index - start_index} 個下載命令")
    print("=" * 80)
    print("\n📋 使用說明:")
    print("1. 複製上面的每個命令到 MCP Square 工具中執行")
    print("2. MCP 會自動保存文件到:")
    print(f"   {MCP_TOOLS_DIR}")
    print("3. 下載完成這批後，重新運行此腳本繼續下載:")
    print("   python3 scripts/continue_download_cursors_mcp.py")
    print("4. 定期合併數據（建議每下載 50-100 個後）:")
    print("   python3 scripts/download_all_payments_mcp.py")
    print("5. 檢查剩餘 cursor 數量:")
    print("   python3 scripts/download_all_remaining.py")
    print()

if __name__ == "__main__":
    main()



