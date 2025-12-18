#!/usr/bin/env python3
"""
計算每個月的實際總營收和總來客數
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import pytz
import pandas as pd

# 設定
DATA_DIR = "../data/2025_08_11"
PAYMENTS_FILE = os.path.join(DATA_DIR, "taiwanway_payments.csv")

# 營業日：週一、週二、週五、週六
BUSINESS_DAYS = [0, 1, 4, 5]  # Monday=0, Tuesday=1, Friday=4, Saturday=5

# 紐約時區
NY_TZ = pytz.timezone('America/New_York')

def convert_timezone(dt_str):
    """將 UTC 時間轉換為紐約時區"""
    if pd.isna(dt_str) or dt_str == '':
        return None
    if isinstance(dt_str, str):
        dt_utc = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        dt_ny = dt_utc.astimezone(NY_TZ)
        return dt_ny
    return dt_str

def load_payments():
    """載入 payments 資料（從 CSV）"""
    print(f"載入 payments 資料: {PAYMENTS_FILE}")
    df = pd.read_csv(PAYMENTS_FILE, encoding='utf-8-sig')
    
    # 轉換為字典列表格式以保持兼容性
    payments = df.to_dict('records')
    
    print(f"✓ 載入 {len(payments)} 筆 payments")
    return payments

def filter_business_days(payments):
    """過濾營業日（週一、週二、週五、週六）"""
    filtered = []
    for payment in payments:
        if payment.get('status') != 'COMPLETED':
            continue
        
        if pd.isna(payment.get('created_at')) or payment.get('created_at') == '':
            continue
        
        dt_ny = convert_timezone(payment['created_at'])
        if dt_ny is None:
            continue
        
        weekday = dt_ny.weekday()  # Monday=0, Sunday=6
        
        if weekday in BUSINESS_DAYS:
            filtered.append(payment)
    
    print(f"✓ 過濾後剩餘 {len(filtered)} 筆（營業日）")
    return filtered

def calculate_total_revenue(payments):
    """計算每個月的實際總營收和總來客數"""
    monthly_stats = defaultdict(lambda: {
        'total_revenue': 0.0,
        'total_customers': 0,
        'dates': set()
    })
    
    for payment in payments:
        dt_ny = convert_timezone(payment.get('created_at', ''))
        if dt_ny is None:
            continue
        
        month = dt_ny.month
        date = dt_ny.date()
        
        # 金額：CSV 中已經是美元
        amount = payment.get('total_amount', 0)
        
        monthly_stats[month]['total_revenue'] += amount
        monthly_stats[month]['total_customers'] += 1
        monthly_stats[month]['dates'].add(date)
    
    return monthly_stats

def main():
    """主函數"""
    print("=" * 60)
    print("計算實際總營收和總來客數")
    print("=" * 60)
    
    # 載入資料
    payments = load_payments()
    
    # 過濾營業日
    filtered_payments = filter_business_days(payments)
    
    # 計算總營收
    print("\n計算每個月的實際總營收...")
    monthly_stats = calculate_total_revenue(filtered_payments)
    
    # 顯示結果
    print("\n" + "=" * 60)
    print("實際總營收和總來客數（營業日）")
    print("=" * 60)
    
    for month in sorted(monthly_stats.keys()):
        stats = monthly_stats[month]
        month_name = f"2025-{month:02d}"
        total_revenue = stats['total_revenue']
        total_customers = stats['total_customers']
        business_days = len(stats['dates'])
        avg_revenue_per_day = total_revenue / business_days if business_days > 0 else 0
        avg_customers_per_day = total_customers / business_days if business_days > 0 else 0
        
        print(f"\n{month_name}:")
        print(f"  營業天數: {business_days} 天")
        print(f"  總來客數: {total_customers:,} 人")
        print(f"  總營收: ${total_revenue:,.2f}")
        print(f"  平均每日來客數: {avg_customers_per_day:.2f} 人/日")
        print(f"  平均每日營收: ${avg_revenue_per_day:,.2f} 美元/日")
        print(f"  平均客單價: ${total_revenue / total_customers:,.2f}" if total_customers > 0 else "  平均客單價: $0.00")
    
    # 比較各月
    print("\n" + "=" * 60)
    print("月份比較")
    print("=" * 60)
    
    months = sorted(monthly_stats.keys())
    if len(months) >= 2:
        for i in range(len(months) - 1):
            month1 = months[i]
            month2 = months[i + 1]
            month1_name = f"2025-{month1:02d}"
            month2_name = f"2025-{month2:02d}"
            
            revenue1 = monthly_stats[month1]['total_revenue']
            revenue2 = monthly_stats[month2]['total_revenue']
            customers1 = monthly_stats[month1]['total_customers']
            customers2 = monthly_stats[month2]['total_customers']
            
            revenue_change = ((revenue2 - revenue1) / revenue1 * 100) if revenue1 > 0 else 0
            customers_change = ((customers2 - customers1) / customers1 * 100) if customers1 > 0 else 0
            
            print(f"\n{month1_name} → {month2_name}:")
            print(f"  營收變化: {revenue_change:+.1f}% (${revenue2 - revenue1:+,.2f})")
            print(f"  來客數變化: {customers_change:+.1f}% ({customers2 - customers1:+,} 人)")
    
    print("\n" + "=" * 60)
    print("計算完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()


