#!/usr/bin/env python3
"""
生成完整的數據檢查報告

修改記錄:
- 2025-11-15: 更新為 2025 年數據 (2025-01-01 至 2025-11-15)
"""
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def check_data_integrity():
    """檢查數據完整性"""
    json_file = Path(__file__).parent.parent / 'data' / 'all_payments' / 'all_payments.json'
    csv_file = Path(__file__).parent.parent / 'data' / 'all_payments' / 'all_payments.csv'
    
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'files': {},
        'data_stats': {},
        'date_range': {},
        'months': {},
        'issues': []
    }
    
    # 檢查文件
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            report['files']['json'] = {
                'exists': True,
                'size_mb': round(json_file.stat().st_size / 1024 / 1024, 2),
                'record_count': data.get('total_count', 0)
            }
    else:
        report['files']['json'] = {'exists': False}
        report['issues'].append('JSON 文件不存在')
    
    if csv_file.exists():
        report['files']['csv'] = {
            'exists': True,
            'size_mb': round(csv_file.stat().st_size / 1024 / 1024, 2)
        }
    else:
        report['files']['csv'] = {'exists': False}
        report['issues'].append('CSV 文件不存在')
    
    # 檢查數據統計
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            payments = data.get('payments', [])
            
            if payments:
                # 日期範圍
                dates = [p.get('created_at', '')[:10] for p in payments if p.get('created_at')]
                if dates:
                    report['date_range'] = {
                        'earliest': min(dates),
                        'latest': max(dates)
                    }
                
                # 月份統計
                months = defaultdict(int)
                for p in payments:
                    date_str = p.get('created_at', '')
                    if date_str:
                        month = date_str[:7]  # YYYY-MM
                        months[month] += 1
                
                report['months'] = dict(sorted(months.items()))
                
                # 數據統計
                total_amount = sum(
                    p.get('total_money', {}).get('amount', 0) / 100 
                    for p in payments 
                    if p.get('status') == 'COMPLETED'
                )
                
                completed_count = sum(1 for p in payments if p.get('status') == 'COMPLETED')
                
                report['data_stats'] = {
                    'total_records': len(payments),
                    'completed_payments': completed_count,
                    'total_revenue_usd': round(total_amount, 2),
                    'avg_order_value': round(total_amount / completed_count, 2) if completed_count > 0 else 0
                }
    
    return report

def check_cursor_status():
    """檢查 cursor 狀態"""
    mcp_tools_dir = Path.home() / ".cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools"
    json_files = list(mcp_tools_dir.glob("*.txt"))
    
    cursor_count = 0
    completed_count = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get('cursor', ''):
                cursor_count += 1
            else:
                completed_count += 1
        except:
            pass
    
    return {
        'total_files': len(json_files),
        'files_with_cursor': cursor_count,
        'files_completed': completed_count,
        'completion_rate': round(completed_count / len(json_files) * 100, 2) if json_files else 0
    }

def generate_report():
    """生成完整報告"""
    print("=" * 80)
    print("📊 Taiwanway Payment Histories 數據檢查報告")
    print("=" * 80)
    print()
    
    # 數據完整性檢查
    print("1. 數據完整性檢查")
    print("-" * 80)
    integrity = check_data_integrity()
    
    if integrity['files']['json']['exists']:
        print(f"✅ JSON 文件存在: {integrity['files']['json']['size_mb']} MB")
        print(f"   記錄數: {integrity['files']['json']['record_count']:,} 筆")
    else:
        print("❌ JSON 文件不存在")
    
    if integrity['files']['csv']['exists']:
        print(f"✅ CSV 文件存在: {integrity['files']['csv']['size_mb']} MB")
    else:
        print("❌ CSV 文件不存在")
    
    print()
    
    # 數據統計
    if integrity['data_stats']:
        print("2. 數據統計")
        print("-" * 80)
        stats = integrity['data_stats']
        print(f"總記錄數: {stats['total_records']:,} 筆")
        print(f"已完成交易: {stats['completed_payments']:,} 筆")
        print(f"總營收: ${stats['total_revenue_usd']:,.2f}")
        print(f"平均客單價: ${stats['avg_order_value']:.2f}")
        print()
    
    # 日期範圍
    if integrity['date_range']:
        print("3. 日期範圍")
        print("-" * 80)
        print(f"最早記錄: {integrity['date_range']['earliest']}")
        print(f"最新記錄: {integrity['date_range']['latest']}")
        print()
    
    # 月份覆蓋
    if integrity['months']:
        print("4. 月份覆蓋")
        print("-" * 80)
        print(f"有數據的月份: {len(integrity['months'])} 個")
        for month, count in integrity['months'].items():
            print(f"  {month}: {count:,} 筆")
        print()
    
    # Cursor 狀態
    print("5. 下載狀態")
    print("-" * 80)
    cursor_status = check_cursor_status()
    print(f"總文件數: {cursor_status['total_files']}")
    print(f"有 cursor (待下載): {cursor_status['files_with_cursor']} 個")
    print(f"已完成: {cursor_status['files_completed']} 個")
    print(f"完成率: {cursor_status['completion_rate']:.2f}%")
    print()
    
    # 問題檢查
    if integrity['issues']:
        print("6. 發現的問題")
        print("-" * 80)
        for issue in integrity['issues']:
            print(f"⚠️  {issue}")
        print()
    
    # 缺失月份檢查
    print("7. 缺失月份檢查")
    print("-" * 80)
    expected_months = [
        '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08',
        '2024-09', '2024-10', '2024-11', '2024-12',
        '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07',
        '2025-08', '2025-09', '2025-10', '2025-11'
    ]
    existing_months = set(integrity['months'].keys()) if integrity['months'] else set()
    missing_months = [m for m in expected_months if m not in existing_months]
    
    if missing_months:
        print(f"⚠️  缺失月份 ({len(missing_months)} 個):")
        for month in missing_months:
            print(f"  - {month}")
    else:
        print("✅ 所有預期月份都有數據")
    print()
    
    print("=" * 80)
    print(f"報告生成時間: {integrity['timestamp']}")
    print("=" * 80)

if __name__ == "__main__":
    generate_report()






