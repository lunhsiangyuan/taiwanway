#!/usr/bin/env python3
"""
自動下載所有 cursor 的資料
讀取所有現有文件的 cursor，然後使用 MCP Square API 下載
"""
import json
import os
from pathlib import Path

# Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# MCP tools 目錄
MCP_TOOLS_DIR = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"

def get_all_cursors():
    """獲取所有需要下載的 cursor"""
    if not MCP_TOOLS_DIR.exists():
        print(f"❌ MCP tools 目錄不存在: {MCP_TOOLS_DIR}")
        return []
    
    txt_files = sorted(MCP_TOOLS_DIR.glob("*.txt"))
    cursors = []
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cursor = data.get('cursor', '')
                if cursor:
                    cursors.append({
                        'file': txt_file.name,
                        'cursor': cursor,
                        'payments': len(data.get('payments', []))
                    })
        except Exception as e:
            print(f"⚠️  無法讀取 {txt_file.name}: {e}")
            continue
    
    return cursors

def main():
    """生成所有 cursor 列表供下載"""
    cursors = get_all_cursors()
    
    print("=" * 80)
    print(f"找到 {len(cursors)} 個 cursor 需要下載")
    print("=" * 80)
    print()
    
    # 將 cursor 資訊保存到文件，供其他腳本使用
    output_file = Path(__file__).parent / 'cursors_to_download.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cursors, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cursor 列表已保存至: {output_file}")
    print(f"   總共 {len(cursors)} 個 cursor")
    print()
    print("前 10 個 cursor 示例:")
    for i, item in enumerate(cursors[:10], 1):
        print(f"  {i}. {item['file']}: {item['payments']} 筆記錄")
    
    if len(cursors) > 10:
        print(f"  ... 還有 {len(cursors) - 10} 個")

if __name__ == "__main__":
    main()




