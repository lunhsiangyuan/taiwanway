#!/usr/bin/env python3
"""
檢查所有 Square API 返回的品項，包括分頁數據
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

def extract_item_names(data):
    """提取所有品項名稱"""
    if not data or 'objects' not in data:
        return []
    
    items = []
    for obj in data.get('objects', []):
        if obj.get('type') == 'ITEM':
            item_data = obj.get('item_data', {})
            name = item_data.get('name', '未命名')
            items.append(name)
    
    return items

def main():
    # 第一頁
    file1 = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/11a25f4f-64ea-42fc-a2b2-2d90ea93259e.txt"
    # 第二頁
    file2 = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/a8a06eb7-eace-4c18-8ced-af369246e0e8.txt"
    
    all_items = []
    
    # 讀取第一頁
    if file1.exists():
        data1 = load_json_file(file1)
        if data1:
            items1 = extract_item_names(data1)
            all_items.extend(items1)
            print(f"第一頁: {len(items1)} 個品項")
            if 'cursor' in data1:
                print(f"  有 cursor: {data1['cursor'][:50]}...")
    
    # 讀取第二頁
    if file2.exists():
        data2 = load_json_file(file2)
        if data2:
            items2 = extract_item_names(data2)
            all_items.extend(items2)
            print(f"第二頁: {len(items2)} 個品項")
    
    print(f"\n總共: {len(all_items)} 個品項")
    
    # 搜索牛肉、麵、飯相關的品項
    keywords = ['牛肉', '麵', '飯', 'beef', 'noodle', 'rice']
    found_items = []
    
    for item in all_items:
        item_lower = item.lower()
        for keyword in keywords:
            if keyword in item_lower:
                found_items.append(item)
                break
    
    if found_items:
        print(f"\n找到相關品項 ({len(found_items)} 個):")
        for item in found_items:
            print(f"  - {item}")
    else:
        print("\n未找到牛肉、麵、飯相關的品項")
    
    # 列出所有品項名稱（前20個）
    print(f"\n所有品項（前20個）:")
    for i, item in enumerate(all_items[:20], 1):
        print(f"  {i}. {item}")

if __name__ == "__main__":
    main()

