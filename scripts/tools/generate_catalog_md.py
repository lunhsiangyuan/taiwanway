#!/usr/bin/env python3
"""
從 Square API 數據生成分類目錄 Markdown 文件
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

def load_catalog_data(file_path):
    """載入 Square API 返回的目錄數據"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"讀取文件時發生錯誤: {e}")
        return None

def organize_items_by_category(data):
    """按照分類組織品項"""
    if not data or 'objects' not in data:
        return {}, {}
    
    objects = data.get('objects', [])
    
    # 提取分類資訊（如果 API 有提供）
    categories = {}
    for obj in objects:
        if obj.get('type') == 'CATEGORY':
            cat_data = obj.get('category_data', {})
            cat_id = obj.get('id')
            cat_name = cat_data.get('name', '未分類')
            categories[cat_id] = {
                'name': cat_name,
                'id': cat_id
            }
    
    # 組織品項
    items_by_category = defaultdict(list)
    uncategorized_items = []
    
    for obj in objects:
        if obj.get('type') == 'ITEM':
            item_data = obj.get('item_data', {})
            category_ids = item_data.get('category_id', [])
            item_name = item_data.get('name', '未命名')
            
            item_info = {
                'id': obj.get('id'),
                'name': item_name,
                'description': item_data.get('description', ''),
                'variations': []
            }
            
            # 獲取變體資訊
            variations = item_data.get('variations', [])
            for var in variations:
                var_data = var.get('item_variation_data', {})
                var_name = var_data.get('name', '')
                price_money = var_data.get('price_money', {})
                amount = price_money.get('amount', 0)
                currency = price_money.get('currency', 'USD')
                price = amount / 100 if amount else 0
                
                item_info['variations'].append({
                    'name': var_name,
                    'price': price,
                    'currency': currency
                })
            
            # 如果有 API 提供的分類，使用它；否則使用自動分類
            if category_ids:
                for cat_id in category_ids:
                    if cat_id in categories:
                        items_by_category[cat_id].append(item_info)
                    else:
                        # 分類 ID 存在但找不到分類資訊，使用自動分類
                        auto_category = categorize_item_by_name(item_name)
                        items_by_category[auto_category].append(item_info)
            else:
                # 使用自動分類
                auto_category = categorize_item_by_name(item_name)
                items_by_category[auto_category].append(item_info)
    
    return categories, items_by_category, uncategorized_items

def categorize_item_by_name(item_name):
    """根據品項名稱自動分類"""
    name_lower = item_name.lower()
    
    # 定義分類關鍵字（按優先順序，越前面的優先級越高）
    category_keywords = [
        ('茶包禮盒', ['茶包', 'tea bag', '禮盒', 'box']),
        ('杯具', ['杯', 'mug', '馬克杯', '玻璃杯', '蝴蝶杯', '壺', '提樑']),
        ('主食', ['麵', 'noodle', 'rice', '飯', 'beef', 'pork', 'chicken', 'shrimp', 'combo', '牛肉', '豬肉', '雞肉', '蝦']),
        ('飲品', ['latte', '拿鐵', 'coffee', '咖啡', '奶茶', 'milk tea', 'bubble', '珍珠', '鮮奶', 'lemonade', 'jade dew', '玉露', '薑汁', 'americano', 'drip', 'matcha latte']),
        ('梅子類', ['梅', '甘梅', '香梅', '紫蘇梅', '茶梅', '脆梅', '無籽梅', '宋梅', '甘宋梅']),
        ('果乾類', ['芒果乾', '芭樂乾', '蜜柑', '水蜜桃', '洛神花', '果乾', '雪花李']),
        ('零食', ['豆乾', '爆米花', 'popcorn', '魚', '魷魚', '鱈魚', '虱目魚', '酥', '片', '條', 'flossy bun', '蜜沙茶', '香菇燒', '蜂梨糖', '糖']),
        ('甜點', ['蛋糕', 'cake', '布丁', 'panna cotta', '奶酪', '泡芙', 'puff', '起司', 'cheese', '生乳捲', 'swiss roll', '酥粒', 'crumble', 'marshmallow', 'cookie', 'cookies', 'matcha', 'strawberry']),
        ('茶類', ['茶', 'tea', '烏龍', '紅茶', '綠茶', '金萱', '鐵觀音', '包種', '碧螺春', '龍井', '四季春', '茉莉', '春茶', '冬片', '蜜香', 'oolong', 'jasmine', 'tieguanyin', 'geisha']),
    ]
    
    # 檢查每個分類（按優先順序）
    for category, keywords in category_keywords:
        for keyword in keywords:
            if keyword in name_lower:
                return category
    
    return '其他'

def generate_markdown(categories, items_by_category, uncategorized_items, total_items):
    """生成 Markdown 格式的目錄"""
    md_lines = []
    
    # 標題
    md_lines.append("# Square 商品目錄")
    md_lines.append("")
    md_lines.append(f"**總品項數：{total_items}**")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # 定義分類顯示順序
    category_order = [
        '主食', '茶類', '茶包禮盒', '飲品', '梅子類', '果乾類', 
        '零食', '甜點', '杯具', '其他'
    ]
    
    # 收集所有分類名稱（包括自動分類）
    all_category_names = set()
    
    # 添加 API 提供的分類
    for cat_id, cat_info in categories.items():
        all_category_names.add(cat_info['name'])
    
    # 添加自動分類
    for cat_name in items_by_category.keys():
        if isinstance(cat_name, str):  # 自動分類使用字符串
            all_category_names.add(cat_name)
    
    # 按順序顯示分類
    displayed_categories = []
    for cat_name in category_order:
        if cat_name in all_category_names:
            displayed_categories.append(cat_name)
            all_category_names.remove(cat_name)
    
    # 添加剩餘的分類（按字母順序）
    displayed_categories.extend(sorted(all_category_names))
    
    # 按分類列出品項
    for cat_name in displayed_categories:
        items = []
        
        # 查找該分類的品項（可能是 API 分類或自動分類）
        if cat_name in [cat_info['name'] for cat_info in categories.values()]:
            # API 提供的分類
            for cat_id, cat_info in categories.items():
                if cat_info['name'] == cat_name:
                    items.extend(items_by_category.get(cat_id, []))
        else:
            # 自動分類
            items.extend(items_by_category.get(cat_name, []))
        
        if items:
            md_lines.append(f"## {cat_name}")
            md_lines.append("")
            md_lines.append(f"*共 {len(items)} 個品項*")
            md_lines.append("")
            
            # 按照品項名稱排序
            sorted_items = sorted(items, key=lambda x: x['name'])
            
            for item in sorted_items:
                md_lines.append(f"### {item['name']}")
                
                if item['description']:
                    md_lines.append(f"*{item['description']}*")
                    md_lines.append("")
                
                md_lines.append(f"**ID:** `{item['id']}`")
                md_lines.append("")
                
                if item['variations']:
                    md_lines.append("**價格：**")
                    for var in item['variations']:
                        var_name = var['name'] if var['name'] else "標準"
                        price_str = f"{var['currency']} {var['price']:,.2f}"
                        md_lines.append(f"- {var_name}: {price_str}")
                
                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")
    
    # 未分類的品項
    if uncategorized_items:
        md_lines.append("## 未分類")
        md_lines.append("")
        md_lines.append(f"*共 {len(uncategorized_items)} 個品項*")
        md_lines.append("")
        
        sorted_uncategorized = sorted(uncategorized_items, key=lambda x: x['name'])
        
        for item in sorted_uncategorized:
            md_lines.append(f"### {item['name']}")
            
            if item['description']:
                md_lines.append(f"*{item['description']}*")
                md_lines.append("")
            
            md_lines.append(f"**ID:** `{item['id']}`")
            md_lines.append("")
            
            if item['variations']:
                md_lines.append("**價格：**")
                for var in item['variations']:
                    var_name = var['name'] if var['name'] else "標準"
                    price_str = f"{var['currency']} {var['price']:,.2f}"
                    md_lines.append(f"- {var_name}: {price_str}")
            
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
    
    return "\n".join(md_lines)

def merge_data(data1, data2):
    """合併兩個數據對象"""
    if not data1:
        return data2
    if not data2:
        return data1
    
    merged = {
        'objects': data1.get('objects', []) + data2.get('objects', []),
        'cursor': data2.get('cursor')  # 使用第二個的 cursor（如果有的話）
    }
    
    return merged

def main():
    # 預設文件路徑（多個頁面）
    base_path = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    file1 = base_path / "11a25f4f-64ea-42fc-a2b2-2d90ea93259e.txt"  # 第一頁
    file2 = base_path / "a8a06eb7-eace-4c18-8ced-af369246e0e8.txt"  # 第二頁
    
    all_data = None
    
    # 讀取第一頁
    if file1.exists():
        print(f"正在讀取第一頁: {file1.name}")
        data1 = load_catalog_data(file1)
        if data1:
            all_data = data1
            print(f"  找到 {len(data1.get('objects', []))} 個物件")
    
    # 讀取第二頁
    if file2.exists():
        print(f"正在讀取第二頁: {file2.name}")
        data2 = load_catalog_data(file2)
        if data2:
            if all_data:
                all_data = merge_data(all_data, data2)
            else:
                all_data = data2
            print(f"  找到 {len(data2.get('objects', []))} 個物件")
    
    if not all_data:
        print("無法載入數據")
        return
    
    # 組織品項
    categories, items_by_category, uncategorized_items = organize_items_by_category(all_data)
    
    # 計算總品項數
    total_items = sum(len(items) for items in items_by_category.values()) + len(uncategorized_items)
    
    print(f"\n找到 {len(categories)} 個 API 分類")
    print(f"找到 {total_items} 個品項")
    
    # 生成 Markdown
    markdown_content = generate_markdown(categories, items_by_category, uncategorized_items, total_items)
    
    # 寫入文件
    output_file = Path(__file__).parent.parent / "catalog.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n目錄已生成: {output_file}")

if __name__ == "__main__":
    main()

