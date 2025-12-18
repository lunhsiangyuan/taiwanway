#!/usr/bin/env python3
"""
使用 Square API 查詢並顯示所有品項
"""
import json
import sys
from pathlib import Path

def load_catalog_data(file_path):
    """載入 Square API 返回的目錄數據"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"讀取文件時發生錯誤: {e}")
        return None

def display_items(data):
    """顯示品項資訊"""
    if not data or 'objects' not in data:
        print("未找到品項數據")
        return
    
    objects = data.get('objects', [])
    items = [obj for obj in objects if obj.get('type') == 'ITEM']
    
    if not items:
        print("目前沒有任何品項")
        return
    
    print(f"\n找到 {len(items)} 個品項：\n")
    print("=" * 80)
    
    for idx, item in enumerate(items, 1):
        item_data = item.get('item_data', {})
        name = item_data.get('name', '未命名')
        description = item_data.get('description', '')
        item_id = item.get('id', 'N/A')
        
        # 獲取變體資訊
        variations = item_data.get('variations', [])
        variation_count = len(variations)
        
        print(f"\n[{idx}] {name}")
        print(f"    ID: {item_id}")
        if description:
            print(f"    描述: {description}")
        print(f"    變體數量: {variation_count}")
        
        # 顯示變體資訊
        if variations:
            print("    變體:")
            for var in variations:
                var_data = var.get('item_variation_data', {})
                var_name = var_data.get('name', '未命名變體')
                price_money = var_data.get('price_money', {})
                amount = price_money.get('amount', 0)
                currency = price_money.get('currency', 'TWD')
                
                # 將金額轉換為可讀格式（Square API 使用最小貨幣單位）
                price = amount / 100 if amount else 0
                print(f"      - {var_name}: {currency} {price:,.0f}")
        
        # 顯示分類
        category_ids = item_data.get('category_id', [])
        if category_ids:
            print(f"    分類 ID: {', '.join(category_ids)}")
        
        print("-" * 80)

def main():
    # 預設文件路徑（從 MCP 工具返回的文件）
    default_file = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/11a25f4f-64ea-42fc-a2b2-2d90ea93259e.txt"
    
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    else:
        file_path = default_file
    
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        print("\n使用方法:")
        print("  python list_catalog_items.py [文件路徑]")
        return
    
    print(f"正在讀取文件: {file_path}")
    data = load_catalog_data(file_path)
    
    if data:
        display_items(data)
        
        # 顯示統計資訊
        if 'objects' in data:
            objects = data.get('objects', [])
            items = [obj for obj in objects if obj.get('type') == 'ITEM']
            variations = [obj for obj in objects if obj.get('type') == 'ITEM_VARIATION']
            categories = [obj for obj in objects if obj.get('type') == 'CATEGORY']
            
            print("\n" + "=" * 80)
            print("統計資訊:")
            print(f"  品項總數: {len(items)}")
            print(f"  變體總數: {len(variations)}")
            print(f"  分類總數: {len(categories)}")
            print("=" * 80)

if __name__ == "__main__":
    main()

