#!/usr/bin/env python3
"""
獲取所有 cursor 的詳細信息，用於後續下載
"""
import json
from pathlib import Path
from typing import List, Dict

def get_all_cursors_with_info() -> List[Dict]:
    """獲取所有有 cursor 的文件信息"""
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    
    if not mcp_tools_dir.exists():
        print(f"❌ MCP tools 目錄不存在: {mcp_tools_dir}")
        return []
    
    json_files = list(mcp_tools_dir.glob("*.txt"))
    cursors_info = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cursor = data.get('cursor', '')
            if cursor:
                payments = data.get('payments', [])
                if payments:
                    # 取得日期範圍
                    dates = [p.get('created_at', '')[:10] for p in payments if p.get('created_at')]
                    min_date = min(dates) if dates else None
                    max_date = max(dates) if dates else None
                    
                    # 從第一個 payment 獲取 location_id
                    location_id = payments[0].get('location_id', 'LMDN6Z5DKNJ2P') if payments else 'LMDN6Z5DKNJ2P'
                    
                    cursors_info.append({
                        'file': json_file.name,
                        'file_path': str(json_file),
                        'cursor': cursor,
                        'count': len(payments),
                        'min_date': min_date,
                        'max_date': max_date,
                        'location_id': location_id
                    })
        except Exception as e:
            print(f"⚠️  無法讀取 {json_file.name}: {e}")
            continue
    
    return cursors_info

def save_cursors_info(cursors_info: List[Dict], output_file: Path):
    """保存 cursor 信息到 JSON 文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cursors_info, f, indent=2, ensure_ascii=False)
    print(f"✅ 已保存 {len(cursors_info)} 個 cursor 信息到 {output_file}")

if __name__ == "__main__":
    print("=" * 80)
    print("獲取所有 cursor 信息")
    print("=" * 80)
    
    cursors_info = get_all_cursors_with_info()
    
    if cursors_info:
        print(f"\n找到 {len(cursors_info)} 個文件還有 cursor：")
        for i, c in enumerate(cursors_info[:10], 1):
            print(f"{i}. {c['file']}: {c['count']} 筆, {c['min_date']} to {c['max_date']}")
        if len(cursors_info) > 10:
            print(f"... 還有 {len(cursors_info) - 10} 個文件有 cursor")
        
        # 保存到文件
        output_file = Path(__file__).parent.parent / 'data' / 'all_payments' / 'cursors_info.json'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        save_cursors_info(cursors_info, output_file)
    else:
        print("✅ 沒有找到 cursor，數據應該已完整下載")






