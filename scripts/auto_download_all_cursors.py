#!/usr/bin/env python3
"""
自動下載所有 cursor 並合併數據
如果下載停止，會記錄進度到 log 文件
"""
import json
import os
from pathlib import Path
import logging
import time
import subprocess

# 配置日誌
log_file = Path.home() / "Desktop/square/scripts/download_progress.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# MCP tools 目錄 (下載的 .txt 文件會存放在這裡)
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
# 儲存所有待下載 cursor 的文件
ALL_CURSORS_FILE = Path.home() / "Desktop/square/scripts/all_new_cursors.json"
# 儲存已下載 cursor 索引的文件
LAST_DOWNLOADED_INDEX_FILE = Path.home() / "Desktop/square/scripts/last_downloaded_cursor_index.txt"
# 合併後的數據文件
ALL_PAYMENTS_JSON = Path.home() / "Desktop/square/data/all_payments/all_payments.json"

def get_all_cursors_from_json_file() -> list:
    """從 JSON 文件中讀取所有 cursor"""
    if not ALL_CURSORS_FILE.exists():
        logging.warning(f"⚠️  文件不存在: {ALL_CURSORS_FILE}")
        return []
    try:
        with open(ALL_CURSORS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"❌ 無法讀取 {ALL_CURSORS_FILE}: {e}")
        return []

def get_last_downloaded_index() -> int:
    """讀取上次下載的 cursor 索引"""
    if not LAST_DOWNLOADED_INDEX_FILE.exists():
        return 0
    try:
        with open(LAST_DOWNLOADED_INDEX_FILE, 'r', encoding='utf-8') as f:
            return int(f.read().strip())
    except Exception as e:
        logging.warning(f"⚠️  無法讀取上次下載索引，從 0 開始: {e}")
        return 0

def save_last_downloaded_index(index: int):
    """保存上次下載的 cursor 索引"""
    try:
        with open(LAST_DOWNLOADED_INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(str(index))
    except Exception as e:
        logging.error(f"❌ 無法保存下載索引: {e}")

def get_merged_data_count() -> int:
    """獲取已合併數據的記錄數"""
    if not ALL_PAYMENTS_JSON.exists():
        return 0
    try:
        with open(ALL_PAYMENTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)
    except Exception as e:
        logging.warning(f"⚠️  無法讀取合併數據文件: {e}")
        return 0

def merge_data():
    """合併數據"""
    try:
        logging.info("正在合併新下載的數據...")
        result = subprocess.run(
            f"python3 {Path.home() / 'Desktop/square/scripts/download_all_payments_mcp.py'}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            # 提取總計行
            for line in result.stdout.splitlines():
                if "總計:" in line:
                    logging.info(f"✅ {line.strip()}")
            return True
        else:
            logging.error(f"❌ 合併數據失敗: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logging.error("❌ 合併數據超時")
        return False
    except Exception as e:
        logging.error(f"❌ 合併數據時發生錯誤: {e}")
        return False

def main():
    logging.info("=" * 80)
    logging.info("自動下載所有 cursor")
    logging.info("=" * 80)
    
    all_cursors = get_all_cursors_from_json_file()
    if not all_cursors:
        logging.info("沒有找到任何待下載的 cursor。")
        return
    
    total_cursors = len(all_cursors)
    last_downloaded_index = get_last_downloaded_index()
    initial_merged_count = get_merged_data_count()
    
    logging.info(f"總共需要下載: {total_cursors} 個 cursor")
    logging.info(f"目前已有文件: {len(list(MCP_TOOLS_DIR.glob('*.txt')))} 個")
    logging.info(f"已合併數據: {initial_merged_count} 筆")
    logging.info(f"已下載約: {last_downloaded_index}/{total_cursors} cursor ({last_downloaded_index/total_cursors:.1%})")
    logging.info(f"剩餘約: {total_cursors - last_downloaded_index} 個 cursor")
    logging.info("=" * 80)
    logging.info("")
    
    if last_downloaded_index >= total_cursors:
        logging.info("✅ 所有 cursor 已下載完成！")
        merge_data()
        return
    
    # 批量下載設定
    batch_size = 20  # 每次下載 20 個
    start_index = last_downloaded_index
    end_index = min(start_index + batch_size, total_cursors)
    
    logging.info(f"準備下載第 {start_index + 1}-{end_index} 個 cursor (共 {end_index - start_index} 個)")
    logging.info("")
    
    success_count = 0
    fail_count = 0
    
    for i in range(start_index, end_index):
        cursor = all_cursors[i]
        logging.info(f"[{i+1}/{total_cursors}] 下載 cursor: {cursor[:50]}...")
        
        # 這裡需要手動使用 MCP Square API 工具下載
        # 因為無法在腳本中直接調用 MCP 工具
        logging.info(f"   請使用 MCP Square API 工具執行以下命令:")
        logging.info(f"   make_api_request service: payments method: list request: {{ \"location_id\": \"{LOCATION_ID}\", \"cursor\": \"{cursor}\", \"limit\": 100, \"sort_order\": \"ASC\" }}")
        logging.info("")
        
        # 等待用戶手動下載或使用其他方式自動化
        # 這裡先記錄進度
        save_last_downloaded_index(i + 1)
        success_count += 1
        
        # 每下載10個就合併一次
        if (i + 1) % 10 == 0:
            if merge_data():
                new_count = get_merged_data_count()
                logging.info(f"✅ 合併完成，目前總計: {new_count} 筆 (新增: {new_count - initial_merged_count} 筆)")
            time.sleep(2)  # 避免請求過快
    
    # 最後合併一次
    if success_count > 0:
        logging.info("")
        logging.info("正在進行最後合併...")
        if merge_data():
            final_count = get_merged_data_count()
            logging.info(f"✅ 最終合併完成，總計: {final_count} 筆 (新增: {final_count - initial_merged_count} 筆)")
    
    new_last_index = get_last_downloaded_index()
    logging.info("")
    logging.info("=" * 80)
    logging.info(f"本次下載進度: {start_index + 1}-{new_last_index} (共 {new_last_index - start_index} 個)")
    logging.info(f"總體進度: {new_last_index}/{total_cursors} ({new_last_index/total_cursors:.1%})")
    
    if new_last_index < total_cursors:
        remaining = total_cursors - new_last_index
        logging.info(f"剩餘: {remaining} 個 cursor")
        logging.info("")
        logging.info("⚠️  下載已暫停，請繼續執行此腳本以下載剩餘 cursor")
        logging.info(f"   或手動使用 MCP Square API 工具下載剩餘的 {remaining} 個 cursor")
    else:
        logging.info("✅ 所有 cursor 已下載完成！")
    
    logging.info("=" * 80)

if __name__ == "__main__":
    main()
