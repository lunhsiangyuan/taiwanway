#!/usr/bin/env python3
"""
檢查所有包含 combo 的品項
"""
import json
from pathlib import Path

def load_json_file(file_path):
    """載入 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"讀取文件時發生錯誤: {e}")
        return None

def extract_combo_items(data):
    """提取所有包含 combo 的品項"""
    if not data or 'objects' not in data:
        return []
    
    combo_items = []
    for obj in data.get('objects', []):
        if obj.get('type') == 'ITEM':
            item_data = obj.get('item_data', {})
            name = item_data.get('name', '')
            if 'combo' in name.lower():
                item_id = obj.get('id', '')
                variations = item_data.get('variations', [])
                combo_items.append({
                    'name': name,
                    'id': item_id,
                    'variations': len(variations)
                })
    
    return combo_items

def main():
    base_path = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    file1 = base_path / "11a25f4f-64ea-42fc-a2b2-2d90ea93259e.txt"
    file2 = base_path / "a8a06eb7-eace-4c18-8ced-af369246e0e8.txt"
    
    all_combo_items = []
    
    # 讀取第一頁
    if file1.exists():
        data1 = load_json_file(file1)
        if data1:
            items1 = extract_combo_items(data1)
            all_combo_items.extend(items1)
            print(f"第一頁找到 {len(items1)} 個 combo 品項")
    
    # 讀取第二頁
    if file2.exists():
        data2 = load_json_file(file2)
        if data2:
            items2 = extract_combo_items(data2)
            all_combo_items.extend(items2)
            print(f"第二頁找到 {len(items2)} 個 combo 品項")
    
    print(f"\n總共找到 {len(all_combo_items)} 個 combo 品項：\n")
    
    # 去重（根據 ID）
    unique_items = {}
    for item in all_combo_items:
        item_id = item['id']
        if item_id not in unique_items:
            unique_items[item_id] = item
        else:
            print(f"⚠️  發現重複品項: {item['name']} (ID: {item_id})")
    
    print(f"去重後共有 {len(unique_items)} 個獨特的 combo 品項：\n")
    
    for idx, (item_id, item) in enumerate(sorted(unique_items.items(), key=lambda x: x[1]['name']), 1):
        print(f"{idx}. {item['name']}")
        print(f"   ID: {item_id}")
        print(f"   變體數: {item['variations']}")
        print()

if __name__ == "__main__":
    main()

