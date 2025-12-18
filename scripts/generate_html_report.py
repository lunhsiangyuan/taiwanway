#!/usr/bin/env python3
"""
生成 HTML 格式的每月統計報告

修改記錄:
- 2025-11-15: 更新為 2025 年數據 (2025-01-01 至 2025-11-15)
"""
import csv
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import pytz

# 營業日設定：週一、週二、週五、週六
BUSINESS_DAYS = {0, 1, 4, 5}  # Monday=0, Tuesday=1, Friday=4, Saturday=5

# 不營業的月份：六月、七月
CLOSED_MONTHS = {6, 7}  # June=6, July=7

# 聖誕節日期
CHRISTMAS_DAY = 25


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


def calculate_monthly_stats(payments: list) -> dict:
    """計算每月統計"""
    monthly_stats = defaultdict(lambda: {
        'total_records': 0,
        'unique_dates': set(),
        'total_amount': 0,
        'business_days': set(),
        'business_transactions': 0,
        'business_revenue': 0,
    })
    
    for payment in payments:
        created_at = payment.get('created_at', '')
        if not created_at:
            continue
        
        try:
            dt_ny = parse_date(created_at)
            month_key = dt_ny.strftime('%Y-%m')
            date_key = dt_ny.strftime('%Y-%m-%d')
            
            # 取得金額
            if isinstance(payment, dict):
                if 'total_amount' in payment:
                    # CSV 格式
                    amount = float(payment.get('total_amount', 0)) / 100
                else:
                    # JSON 格式
                    total_money = payment.get('total_money', {})
                    amount = float(total_money.get('amount', 0)) / 100
            else:
                amount = 0
            
            # 更新統計
            stats = monthly_stats[month_key]
            stats['total_records'] += 1
            stats['unique_dates'].add(date_key)
            stats['total_amount'] += amount
            
            # 只統計營業日的記錄
            if is_business_day(dt_ny):
                stats['business_days'].add(date_key)
                stats['business_transactions'] += 1
                stats['business_revenue'] += amount
            
        except Exception as e:
            continue
    
    # 轉換為可序列化的格式
    result = {}
    for month_key, stats in sorted(monthly_stats.items()):
        result[month_key] = {
            'total_records': stats['total_records'],
            'unique_dates': len(stats['unique_dates']),
            'total_amount': stats['total_amount'],
            'business_days': len(stats['business_days']),
            'business_transactions': stats['business_transactions'],
            'business_revenue': stats['business_revenue'],
        }
    
    return result


def load_payments_from_csv(csv_file: Path) -> list:
    """從 CSV 檔案載入 payments"""
    payments = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            payments.append(row)
    return payments


def generate_html_report(stats: dict, output_file: Path):
    """生成 HTML 報告"""
    html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taiwanway 每月營業統計報告</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", "Hiragino Sans GB", sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background-color: #4a90e2;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #357abd;
        }
        td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: right;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f0f7ff;
        }
        .month {
            text-align: left;
            font-weight: 500;
        }
        .highlight {
            font-weight: bold;
        }
        .summary {
            margin-top: 30px;
            padding: 20px;
            background-color: #f0f7ff;
            border-radius: 6px;
            border-left: 4px solid #4a90e2;
        }
        .summary h2 {
            margin-top: 0;
            color: #333;
        }
        .summary-item {
            margin: 10px 0;
            font-size: 16px;
        }
        .summary-label {
            font-weight: 600;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>目前下載進度</h1>
        <p class="subtitle">已下載的數據</p>
        <table>
            <thead>
                <tr>
                    <th>月份</th>
                    <th>總記錄數</th>
                    <th>不同日期數</th>
                    <th>總金額 (USD)</th>
                    <th>營業日數</th>
                    <th>營業日交易數</th>
                    <th>營業日營收</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # 生成表格行
    for month_key in sorted(stats.keys()):
        month_stats = stats[month_key]
        month_display = month_key.replace('-', '/')
        
        # 判斷是否為新發現的數據（2024-05 和 2025-01）
        is_new = month_key in ['2024-05', '2025-01']
        highlight_class = ' class="highlight"' if is_new else ''
        
        business_days = month_stats['business_days'] if month_stats['business_days'] > 0 else '-'
        business_transactions = month_stats['business_transactions'] if month_stats['business_transactions'] > 0 else '-'
        business_revenue = f"${month_stats['business_revenue']:,.2f}" if month_stats['business_revenue'] > 0 else '-'
        
        html += f"""                <tr{highlight_class}>
                    <td class="month">{month_display}</td>
                    <td>{month_stats['total_records']}</td>
                    <td>{month_stats['unique_dates']}</td>
                    <td>${month_stats['total_amount']:,.2f}</td>
                    <td>{business_days}</td>
                    <td>{business_transactions}</td>
                    <td>{business_revenue}</td>
                </tr>
"""
    
    # 計算總計
    total_records = sum(s['total_records'] for s in stats.values())
    total_amount = sum(s['total_amount'] for s in stats.values())
    total_business_days = sum(s['business_days'] for s in stats.values() if s['business_days'] > 0)
    total_business_transactions = sum(s['business_transactions'] for s in stats.values())
    total_business_revenue = sum(s['business_revenue'] for s in stats.values())
    
    html += f"""            </tbody>
        </table>
        
        <div class="summary">
            <h2>總計</h2>
            <div class="summary-item">
                <span class="summary-label">總記錄數：</span>{total_records} 筆
            </div>
            <div class="summary-item">
                <span class="summary-label">總金額：</span>${total_amount:,.2f}
            </div>
            <div class="summary-item">
                <span class="summary-label">總營業日數：</span>{total_business_days} 天
            </div>
            <div class="summary-item">
                <span class="summary-label">總營業日交易數：</span>{total_business_transactions} 筆
            </div>
            <div class="summary-item">
                <span class="summary-label">總營業日營收：</span>${total_business_revenue:,.2f}
            </div>
            <div class="summary-item">
                <span class="summary-label">平均每日營收：</span>${total_business_revenue/total_business_days:,.2f} (營業日)
            </div>
            <div class="summary-item">
                <span class="summary-label">平均客單價：</span>${total_business_revenue/total_business_transactions:,.2f}
            </div>
        </div>
        
        <p style="margin-top: 30px; color: #666; font-size: 14px;">
            報告生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML 報告已生成: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("使用方法: python generate_html_report.py <csv_file> [output_html]")
        print("\n範例:")
        print("  python generate_html_report.py data/all_payments/all_payments.csv")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"❌ 檔案不存在: {input_file}")
        sys.exit(1)
    
    # 輸出檔案
    if len(sys.argv) >= 3:
        output_html = Path(sys.argv[2])
    else:
        output_html = input_file.parent / f"{input_file.stem}_report.html"
    
    print("="*80)
    print("生成 HTML 報告")
    print("="*80)
    print(f"輸入檔案: {input_file}")
    print(f"輸出檔案: {output_html}")
    print("="*80)
    
    # 載入數據
    print("\n正在載入數據...")
    payments = load_payments_from_csv(input_file)
    print(f"✅ 載入 {len(payments)} 筆記錄")
    
    # 計算統計
    print("\n正在計算統計...")
    stats = calculate_monthly_stats(payments)
    
    # 生成 HTML
    print("\n正在生成 HTML 報告...")
    generate_html_report(stats, output_html)
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()






