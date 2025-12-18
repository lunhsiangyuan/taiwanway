#!/usr/bin/env python3
"""
生成每月統計報告：營業日數、營收等

修改記錄:
- 2025-11-15: 更新為 2025 年數據 (2025-01-01 至 2025-11-15)
"""
import json
import csv
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List
import pytz

# 營業日設定：週一、週二、週五、週六
BUSINESS_DAYS = {0, 1, 4, 5}  # Monday=0, Tuesday=1, Friday=4, Saturday=5

# 不營業的月份：六月、七月
CLOSED_MONTHS = {6, 7}  # June=6, July=7


def load_payments_from_csv(csv_file: Path) -> List[Dict]:
    """從 CSV 檔案載入 payments"""
    payments = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            payments.append(row)
    return payments


def load_payments_from_json(json_file: Path) -> List[Dict]:
    """從 JSON 檔案載入 payments"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        if 'payments' in data:
            return data['payments']
        elif 'objects' in data:
            return data['objects']
    elif isinstance(data, list):
        return data
    
    return []


def parse_date(date_str: str) -> datetime:
    """解析日期字串為 datetime 物件（紐約時區）"""
    dt_utc = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    ny_tz = pytz.timezone('America/New_York')
    return dt_utc.astimezone(ny_tz)


def is_business_day(dt: datetime) -> bool:
    """檢查是否為營業日"""
    # 檢查星期幾
    if dt.weekday() not in BUSINESS_DAYS:
        return False
    
    # 檢查月份（六月、七月不營業）
    if dt.month in CLOSED_MONTHS:
        return False
    
    # 檢查聖誕節
    if dt.month == 12 and dt.day == 25:
        return False
    
    return True


def calculate_monthly_stats(payments: List[Dict]) -> Dict:
    """計算每月統計"""
    monthly_stats = defaultdict(lambda: {
        'total_revenue': 0,
        'total_transactions': 0,
        'business_days': set(),
        'total_days': 0,
        'avg_daily_revenue': 0,
        'avg_transaction_value': 0,
        'transactions_by_day': defaultdict(int),
        'revenue_by_day': defaultdict(float)
    })
    
    for payment in payments:
        created_at = payment.get('created_at', '')
        if not created_at:
            continue
        
        try:
            dt_ny = parse_date(created_at)
            month_key = dt_ny.strftime('%Y-%m')
            date_key = dt_ny.strftime('%Y-%m-%d')
            
            # 只統計營業日的記錄
            if not is_business_day(dt_ny):
                continue
            
            # 取得金額（從 CSV 或 JSON）
            if isinstance(payment, dict):
                if 'total_amount' in payment:
                    # CSV 格式
                    amount = float(payment.get('total_amount', 0)) / 100  # 轉換為美元
                else:
                    # JSON 格式
                    total_money = payment.get('total_money', {})
                    amount = float(total_money.get('amount', 0)) / 100
            else:
                amount = 0
            
            # 更新統計
            stats = monthly_stats[month_key]
            stats['total_revenue'] += amount
            stats['total_transactions'] += 1
            stats['business_days'].add(date_key)
            stats['transactions_by_day'][date_key] += 1
            stats['revenue_by_day'][date_key] += amount
            
        except Exception as e:
            print(f"⚠️  處理記錄時發生錯誤: {e}")
            continue
    
    # 計算平均值
    for month_key, stats in monthly_stats.items():
        stats['total_days'] = len(stats['business_days'])
        if stats['total_days'] > 0:
            stats['avg_daily_revenue'] = stats['total_revenue'] / stats['total_days']
        if stats['total_transactions'] > 0:
            stats['avg_transaction_value'] = stats['total_revenue'] / stats['total_transactions']
    
    return dict(sorted(monthly_stats.items()))


def print_monthly_report(stats: Dict):
    """列印每月統計報告"""
    print("\n" + "="*100)
    print("每月營業統計報告")
    print("="*100)
    print(f"{'月份':<12} {'營業日數':<10} {'總交易數':<12} {'總營收 (USD)':<15} {'日均營收':<15} {'平均客單價':<15}")
    print("-"*100)
    
    total_revenue_all = 0
    total_transactions_all = 0
    total_days_all = 0
    
    for month_key, month_stats in stats.items():
        revenue = month_stats['total_revenue']
        transactions = month_stats['total_transactions']
        days = month_stats['total_days']
        avg_daily = month_stats['avg_daily_revenue']
        avg_transaction = month_stats['avg_transaction_value']
        
        print(f"{month_key:<12} {days:<10} {transactions:<12} ${revenue:>13,.2f} ${avg_daily:>13,.2f} ${avg_transaction:>13,.2f}")
        
        total_revenue_all += revenue
        total_transactions_all += transactions
        total_days_all += days
    
    print("-"*100)
    avg_daily_all = total_revenue_all / total_days_all if total_days_all > 0 else 0
    avg_transaction_all = total_revenue_all / total_transactions_all if total_transactions_all > 0 else 0
    print(f"{'總計':<12} {total_days_all:<10} {total_transactions_all:<12} ${total_revenue_all:>13,.2f} ${avg_daily_all:>13,.2f} ${avg_transaction_all:>13,.2f}")
    print("="*100)


def save_monthly_report_csv(stats: Dict, output_file: Path):
    """儲存每月統計為 CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['月份', '營業日數', '總交易數', '總營收 (USD)', '日均營收 (USD)', '平均客單價 (USD)'])
        
        for month_key, month_stats in stats.items():
            writer.writerow([
                month_key,
                month_stats['total_days'],
                month_stats['total_transactions'],
                f"{month_stats['total_revenue']:.2f}",
                f"{month_stats['avg_daily_revenue']:.2f}",
                f"{month_stats['avg_transaction_value']:.2f}"
            ])
    
    print(f"\n✅ 統計報告已儲存至 {output_file}")


def main():
    if len(sys.argv) < 2:
        print("使用方法: python generate_monthly_report.py <csv_or_json_file> [output_csv]")
        print("\n範例:")
        print("  python generate_monthly_report.py taiwanway_all_payments.csv")
        print("  python generate_monthly_report.py all_payments.json monthly_report.csv")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"❌ 檔案不存在: {input_file}")
        sys.exit(1)
    
    # 輸出檔案
    if len(sys.argv) >= 3:
        output_csv = Path(sys.argv[2])
    else:
        output_csv = input_file.parent / f"{input_file.stem}_monthly_report.csv"
    
    print("="*100)
    print("每月營業統計報告生成工具")
    print("="*100)
    print(f"輸入檔案: {input_file}")
    print(f"輸出檔案: {output_csv}")
    print("="*100)
    
    # 載入數據
    print("\n正在載入數據...")
    if input_file.suffix.lower() == '.csv':
        payments = load_payments_from_csv(input_file)
    else:
        payments = load_payments_from_json(input_file)
    
    print(f"✅ 載入 {len(payments)} 筆記錄")
    
    # 計算統計
    print("\n正在計算統計...")
    stats = calculate_monthly_stats(payments)
    
    # 列印報告
    print_monthly_report(stats)
    
    # 儲存 CSV
    save_monthly_report_csv(stats, output_csv)
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()






