#!/usr/bin/env python3
"""
使用 MCP Square 工具下載所有 payments 並合併
需要手動調用 MCP Square 工具，然後將結果文件路徑傳入此腳本

修改記錄:
- 2025-11-15: 添加日期過濾，只保留 2025-01-01 至 2025-11-15 的數據
"""
import json
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from collections import defaultdict

def load_payments_from_file(file_path: Path) -> tuple[List[Dict], str]:
    """從 JSON 檔案載入 payments 並返回 cursor"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    payments = data.get('payments', [])
    cursor = data.get('cursor', '')

    return payments, cursor

def filter_payments_by_date(payments: List[Dict], start_date_str: str, end_date_str: str) -> List[Dict]:
    """
    過濾 payments，只保留指定日期範圍內的記錄

    Args:
        payments: payment 記錄列表
        start_date_str: 開始日期 (ISO 格式，如 "2025-01-01")
        end_date_str: 結束日期 (ISO 格式，如 "2025-11-15")

    Returns:
        過濾後的 payment 列表
    """
    from datetime import timezone
    # 使用 UTC 時區，因為 API 返回的時間是 UTC
    start_date = datetime.fromisoformat(start_date_str).replace(tzinfo=timezone.utc)
    end_date = datetime.fromisoformat(end_date_str).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

    filtered_payments = []

    for payment in payments:
        try:
            # 解析 created_at 欄位
            created_at_str = payment.get('created_at', '')
            if not created_at_str:
                continue

            # 處理 ISO 8601 格式（可能有毫秒和時區）
            # 例如: "2025-09-27T18:48:41.573Z"
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))

            # 檢查是否在範圍內
            if start_date <= created_at <= end_date:
                filtered_payments.append(payment)
        except Exception as e:
            # 如果日期解析失敗，跳過該記錄
            continue

    return filtered_payments

def get_monthly_statistics(payments: List[Dict]) -> Dict[str, Dict]:
    """
    計算每月的統計資訊

    Returns:
        字典，key 為月份 (YYYY-MM)，value 為統計資訊
    """
    monthly_stats = defaultdict(lambda: {'count': 0, 'payments': []})

    for payment in payments:
        try:
            created_at_str = payment.get('created_at', '')
            if not created_at_str:
                continue

            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
            month_key = created_at.strftime('%Y-%m')

            monthly_stats[month_key]['count'] += 1
            monthly_stats[month_key]['payments'].append(payment)
        except:
            continue

    return dict(monthly_stats)

def merge_all_payments(base_dir: Path, output_file: Path):
    """合併所有 MCP Square 下載的 JSON 檔案"""
    all_payments = []
    
    # 查找所有相關的 JSON 檔案
    # MCP 工具通常將結果保存在 ~/.cursor/projects/.../agent-tools/ 目錄
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    
    if not mcp_tools_dir.exists():
        print(f"❌ MCP tools 目錄不存在: {mcp_tools_dir}")
        return None
    
    # 查找所有包含 payments 的 JSON 檔案
    json_files = list(mcp_tools_dir.glob("*.txt"))
    
    if not json_files:
        print(f"❌ 在 {mcp_tools_dir} 中找不到 JSON 檔案")
        return None
    
    print(f"找到 {len(json_files)} 個可能的數據檔案")
    
    # 讀取所有檔案並合併
    for json_file in sorted(json_files):
        try:
            payments, cursor = load_payments_from_file(json_file)
            if payments:
                all_payments.extend(payments)
                print(f"  {json_file.name}: {len(payments)} 筆記錄" + (f" (cursor: {cursor[:30]}...)" if cursor else " (最後一頁)"))
        except Exception as e:
            print(f"  ⚠️  無法讀取 {json_file.name}: {e}")
            continue
    
    if not all_payments:
        print("❌ 沒有找到任何 payment 記錄")
        return None
    
    # 去重（根據 payment ID）
    seen_ids = set()
    unique_payments = []
    for payment in all_payments:
        payment_id = payment.get('id', '')
        if payment_id and payment_id not in seen_ids:
            seen_ids.add(payment_id)
            unique_payments.append(payment)

    print(f"\n總共找到 {len(all_payments)} 筆記錄")
    print(f"去重後: {len(unique_payments)} 筆唯一記錄")

    # 日期過濾：只保留 2025-01-01 至 2025-11-15 的數據
    START_DATE = "2025-01-01"
    END_DATE = "2025-11-15"

    print(f"\n⏳ 過濾日期範圍: {START_DATE} 至 {END_DATE}")
    filtered_payments = filter_payments_by_date(unique_payments, START_DATE, END_DATE)

    print(f"過濾前: {len(unique_payments)} 筆")
    print(f"過濾後: {len(filtered_payments)} 筆 (2025 年數據)")

    # 計算月度統計
    monthly_stats = get_monthly_statistics(filtered_payments)

    print(f"\n📊 按月份統計 (2025 年):")
    print("-" * 60)
    for month in sorted(monthly_stats.keys()):
        count = monthly_stats[month]['count']
        print(f"  {month}: {count:4d} 筆")
    print("-" * 60)
    print(f"  總計:  {len(filtered_payments):4d} 筆")
    print()

    # 儲存合併後的數據
    output_data = {
        'payments': filtered_payments,
        'total_count': len(filtered_payments),
        'date_range': {
            'start': START_DATE,
            'end': END_DATE
        },
        'monthly_summary': {month: stats['count'] for month, stats in monthly_stats.items()}
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✅ 已合併並儲存至 {output_file}")

    return output_data

def main():
    if len(sys.argv) > 1:
        # 如果提供了特定的檔案路徑
        input_file = Path(sys.argv[1])
        if input_file.exists():
            payments, _ = load_payments_from_file(input_file)
            output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.parent / "all_payments.json"
            output_data = {'payments': payments, 'total_count': len(payments)}
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"✅ 已儲存 {len(payments)} 筆記錄至 {output_file}")
        else:
            print(f"❌ 檔案不存在: {input_file}")
    else:
        # 自動查找並合併所有 MCP 下載的檔案
        output_dir = Path(__file__).parent.parent / 'data' / 'all_payments'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'all_payments.json'
        
        print("="*80)
        print("合併 MCP Square 下載的 Payment 數據")
        print("="*80)
        
        result = merge_all_payments(None, output_file)
        
        if result:
            print(f"\n✅ 完成！共 {result['total_count']} 筆記錄")

if __name__ == "__main__":
    main()



