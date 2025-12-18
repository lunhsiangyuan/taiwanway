#!/usr/bin/env python3
"""
從 Square API 查詢所有品項，並與 catalog.md 比對
"""
import json
import re
from pathlib import Path
from collections import defaultdict

def load_json_file(file_path):
    """載入 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"讀取文件時發生錯誤: {e}")
        return None

def extract_items_from_api(data):
    """從 API 數據中提取所有品項"""
    items = {}
    if not data or 'objects' not in data:
        return items
    
    for obj in data.get('objects', []):
        if obj.get('type') == 'ITEM':
            item_data = obj.get('item_data', {})
            item_id = obj.get('id', '')
            name = item_data.get('name', '未命名')
            items[item_id] = {
                'name': name,
                'description': item_data.get('description', ''),
                'is_deleted': obj.get('is_deleted', False)
            }
    
    return items

def extract_items_from_catalog_md(file_path):
    """從 catalog.md 中提取所有品項 ID"""
    items = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正則表達式提取品項名稱和 ID
        # 先提取所有 ID
        id_pattern = r'\*\*ID:\*\* `([A-Z0-9]+)`'
        all_ids = re.findall(id_pattern, content)
        
        # 然後為每個 ID 找到對應的品項名稱
        # 格式: ### 品項名稱\n...\n**ID:** `ID`
        lines = content.split('\n')
        current_name = None
        
        for i, line in enumerate(lines):
            # 檢查是否是品項名稱行
            if line.startswith('### '):
                current_name = line[4:].strip()
            # 檢查是否是 ID 行
            elif '**ID:**' in line and current_name:
                id_match = re.search(id_pattern, line)
                if id_match:
                    item_id = id_match.group(1)
                    items[item_id] = {
                        'name': current_name,
                        'source': 'catalog.md'
                    }
                    current_name = None  # 重置，避免重複使用
    
    except Exception as e:
        print(f"讀取 catalog.md 時發生錯誤: {e}")
    
    return items

def main():
    # 讀取最新的 API 數據
    api_file = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/69caa956-c4f9-4097-bc5a-054e9cabbb4d.txt"
    
    print("正在從 Square API 讀取數據...")
    api_data = load_json_file(api_file)
    
    if not api_data:
        print("無法載入 API 數據")
        return
    
    # 檢查是否有 cursor（分頁）
    cursor = api_data.get('cursor')
    if cursor:
        print(f"發現分頁 cursor，需要查詢更多數據...")
        print(f"Cursor: {cursor[:50]}...")
    
    # 提取 API 中的品項
    api_items = extract_items_from_api(api_data)
    print(f"\n從 API 第一頁找到 {len(api_items)} 個品項")
    
    # 如果有分頁，需要查詢更多（這裡先處理第一頁）
    # 同時讀取之前保存的兩頁數據
    base_path = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    file1 = base_path / "11a25f4f-64ea-42fc-a2b2-2d90ea93259e.txt"
    file2 = base_path / "a8a06eb7-eace-4c18-8ced-af369246e0e8.txt"
    
    all_api_items = {}
    
    # 讀取第一頁（舊數據）
    if file1.exists():
        data1 = load_json_file(file1)
        if data1:
            items1 = extract_items_from_api(data1)
            all_api_items.update(items1)
            print(f"從舊數據第一頁找到 {len(items1)} 個品項")
    
    # 讀取第二頁（舊數據）
    if file2.exists():
        data2 = load_json_file(file2)
        if data2:
            items2 = extract_items_from_api(data2)
            all_api_items.update(items2)
            print(f"從舊數據第二頁找到 {len(items2)} 個品項")
    
    # 也加入最新的 API 數據
    all_api_items.update(api_items)
    
    print(f"\n總共從 API 數據中找到 {len(all_api_items)} 個獨特品項")
    
    # 讀取 catalog.md
    catalog_file = Path(__file__).parent.parent / "catalog.md"
    if not catalog_file.exists():
        # 嘗試在 documents 目錄下尋找
        catalog_file = Path(__file__).parent.parent / "documents" / "catalog.md"
    if not catalog_file.exists():
        # 嘗試在根目錄尋找
        catalog_file = Path(__file__).parent.parent.parent / "catalog.md"
    print(f"\n正在讀取 catalog.md...")
    catalog_items = extract_items_from_catalog_md(catalog_file)
    print(f"從 catalog.md 中找到 {len(catalog_items)} 個品項")
    
    # 比對
    print("\n" + "="*80)
    print("比對結果：")
    print("="*80)
    
    # 找出在 API 中但不在 catalog.md 中的品項
    missing_in_catalog = {}
    for item_id, item_info in all_api_items.items():
        if item_id not in catalog_items and not item_info.get('is_deleted', False):
            missing_in_catalog[item_id] = item_info
    
    # 找出在 catalog.md 中但不在 API 中的品項
    missing_in_api = {}
    for item_id, item_info in catalog_items.items():
        if item_id not in all_api_items:
            missing_in_api[item_id] = item_info
    
    # 顯示結果
    if missing_in_catalog:
        print(f"\n⚠️  在 Square API 中但不在 catalog.md 中的品項 ({len(missing_in_catalog)} 個):")
        print("-" * 80)
        for idx, (item_id, item_info) in enumerate(sorted(missing_in_catalog.items(), key=lambda x: x[1]['name']), 1):
            print(f"{idx}. {item_info['name']}")
            print(f"   ID: {item_id}")
            if item_info.get('description'):
                print(f"   描述: {item_info['description']}")
            print()
    else:
        print("\n✅ catalog.md 包含所有 Square API 中的品項")
    
    if missing_in_api:
        print(f"\n⚠️  在 catalog.md 中但不在 Square API 中的品項 ({len(missing_in_api)} 個):")
        print("-" * 80)
        for idx, (item_id, item_info) in enumerate(sorted(missing_in_api.items(), key=lambda x: x[1]['name']), 1):
            print(f"{idx}. {item_info['name']}")
            print(f"   ID: {item_id}")
            print()
    else:
        print("\n✅ 所有 catalog.md 中的品項都在 Square API 中")
    
    # 統計已刪除的品項
    deleted_items = {item_id: item_info for item_id, item_info in all_api_items.items() 
                     if item_info.get('is_deleted', False)}
    if deleted_items:
        print(f"\n📝 已刪除的品項 ({len(deleted_items)} 個):")
        print("-" * 80)
        for idx, (item_id, item_info) in enumerate(sorted(deleted_items.items(), key=lambda x: x[1]['name']), 1):
            print(f"{idx}. {item_info['name']} (ID: {item_id})")
    
    # 總結
    print("\n" + "="*80)
    print("總結：")
    print(f"  Square API 總品項數: {len(all_api_items)}")
    print(f"  catalog.md 品項數: {len(catalog_items)}")
    print(f"  遺漏在 catalog.md 中的品項: {len(missing_in_catalog)}")
    print(f"  在 catalog.md 中但不在 API 中的品項: {len(missing_in_api)}")
    print(f"  已刪除的品項: {len(deleted_items)}")
    print("="*80)

if __name__ == "__main__":
    main()

