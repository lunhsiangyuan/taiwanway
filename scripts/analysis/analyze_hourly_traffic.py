#!/usr/bin/env python3
"""
分析 Taiwanway 店鋪每小時的來客數（流量）和金流
按月分開統計，只包含營業日（週一、週二、週五、週六）
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import pytz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 設定
DATA_DIR = "../data/2025_08_11"
PAYMENTS_FILE = os.path.join(DATA_DIR, "taiwanway_payments.csv")
OUTPUT_DIR = "../analysis_output"
DATA_DIR_HOURLY = os.path.join(OUTPUT_DIR, "data", "hourly")
CHARTS_DIR_HOURLY = os.path.join(OUTPUT_DIR, "charts", "hourly")
CHARTS_DIR_OTHER = os.path.join(OUTPUT_DIR, "charts", "other")

# 營業日：週一、週二、週五、週六
BUSINESS_DAYS = [0, 1, 4, 5]  # Monday=0, Tuesday=1, Friday=4, Saturday=5

# 紐約時區
NY_TZ = pytz.timezone('America/New_York')

def ensure_output_dir():
    """確保輸出目錄存在"""
    os.makedirs(DATA_DIR_HOURLY, exist_ok=True)
    os.makedirs(CHARTS_DIR_HOURLY, exist_ok=True)
    os.makedirs(CHARTS_DIR_OTHER, exist_ok=True)

def load_payments():
    """載入 payments 資料（從 CSV）"""
    print(f"載入 payments 資料: {PAYMENTS_FILE}")
    df = pd.read_csv(PAYMENTS_FILE, encoding='utf-8-sig')
    
    # 轉換為字典列表格式以保持兼容性
    payments = df.to_dict('records')
    
    print(f"✓ 載入 {len(payments)} 筆 payments")
    return payments

def convert_timezone(dt_str):
    """
    將 UTC 時間轉換為紐約時區（America/New_York）
    
    注意事項：
    - pytz 會自動處理夏令時（DST）和冬令時（標準時間）的轉換
    - 夏令時（EDT）：3月第二個星期日 ~ 11月第一個星期日，UTC-4
    - 冬令時（EST）：11月第一個星期日 ~ 3月第二個星期日，UTC-5
    - 2025年：夏令時 3月9日開始，11月2日結束
    """
    if pd.isna(dt_str) or dt_str == '':
        return None
    if isinstance(dt_str, str):
        dt_utc = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        dt_ny = dt_utc.astimezone(NY_TZ)
        return dt_ny
    return dt_str

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

def analyze_hourly_data(payments):
    """分析每小時的來客數和金流（按月）"""
    # 結構：month -> hour -> {customers, revenue, dates}
    monthly_hourly = defaultdict(lambda: defaultdict(lambda: {
        'customers': 0,
        'revenue': 0.0,
        'dates': set()
    }))
    
    for payment in payments:
        dt_ny = convert_timezone(payment.get('created_at', ''))
        if dt_ny is None:
            continue
        
        month = dt_ny.month
        hour = dt_ny.hour
        date = dt_ny.date()
        
        # 金額：CSV 中已經是美元
        amount = payment.get('total_amount', 0)
        
        monthly_hourly[month][hour]['customers'] += 1
        monthly_hourly[month][hour]['revenue'] += amount
        monthly_hourly[month][hour]['dates'].add(date)
    
    return monthly_hourly

def create_dataframe(monthly_hourly):
    """建立 DataFrame"""
    results = []
    for month in sorted(monthly_hourly.keys()):
        for hour in range(24):
            if hour in monthly_hourly[month]:
                stats = monthly_hourly[month][hour]
                dates_count = len(stats['dates'])
                customers = stats['customers']
                revenue = stats['revenue']
                
                # 計算每日平均值
                avg_customers = customers / dates_count if dates_count > 0 else 0
                avg_revenue = revenue / dates_count if dates_count > 0 else 0
                avg_order_value = revenue / customers if customers > 0 else 0
                
                results.append({
                    'month': f"2025-{month:02d}",
                    'hour': hour,
                    'customers': avg_customers,
                    'revenue': avg_revenue,
                    'avg_order_value': avg_order_value
                })
            else:
                results.append({
                    'month': f"2025-{month:02d}",
                    'hour': hour,
                    'customers': 0.0,
                    'revenue': 0.0,
                    'avg_order_value': 0.0
                })
    
    return pd.DataFrame(results)

def save_json_csv(df):
    """儲存 JSON 和 CSV（按月分開）"""
    months = sorted(df['month'].unique())
    
    for month in months:
        month_df = df[df['month'] == month].sort_values('hour')
        
        # JSON
        json_file = os.path.join(DATA_DIR_HOURLY, f'hourly_analysis_{month}.json')
        json_data = month_df.to_dict('records')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"✓ 儲存 JSON: hourly_analysis_{month}.json")
        
        # CSV
        csv_file = os.path.join(DATA_DIR_HOURLY, f'hourly_analysis_{month}.csv')
        month_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✓ 儲存 CSV: hourly_analysis_{month}.csv")

def print_statistics(df, payments):
    """列印統計資訊"""
    print("\n" + "=" * 60)
    print("統計資訊")
    print("=" * 60)
    
    months = sorted(df['month'].unique())
    for month in months:
        month_df = df[df['month'] == month]
        total_customers = month_df['customers'].sum()
        total_revenue = month_df['revenue'].sum()
        
        # 計算該月的實際總來客數和總金流
        month_num = int(month.split('-')[1])
        month_payments = []
        for p in payments:
            dt = convert_timezone(p.get('created_at', ''))
            if dt and dt.month == month_num:
                month_payments.append(p)
        actual_customers = len(month_payments)
        actual_revenue = sum(p.get('total_amount', 0) for p in month_payments)
        
        print(f"\n{month}:")
        print(f"  總來客數: {actual_customers:,} 人")
        print(f"  總金流: ${actual_revenue:,.2f}")
        print(f"  平均客單價: ${actual_revenue / actual_customers:,.2f}" if actual_customers > 0 else "  平均客單價: $0.00")
        print(f"  每小時平均來客數: {total_customers / 24:.2f} 人/小時")
        print(f"  每小時平均金流: ${total_revenue / 24:,.2f} 美元/小時")
    
    print("=" * 60)

def setup_chinese_font():
    """設定中文字體"""
    try:
        import scienceplots
        plt.style.use(['science', 'ieee'])
    except:
        plt.style.use('default')
    plt.rcParams['text.usetex'] = False
    
    font_path = '/System/Library/Fonts/Hiragino Sans GB.ttc'
    chinese_font_prop = None
    if os.path.exists(font_path):
        chinese_font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = [chinese_font_prop.get_name(), 'DejaVu Sans', 'Arial']
        print(f"✓ 使用中文字體: {chinese_font_prop.get_name()}")
    else:
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'STHeiti', 'Arial Unicode MS', 'DejaVu Sans', 'Arial']
    
    plt.rcParams['axes.unicode_minus'] = False
    return chinese_font_prop

def create_visualizations(df, payments=None):
    """創建視覺化圖表"""
    chinese_font_prop = setup_chinese_font()
    
    if len(df) == 0:
        print("⚠ 沒有數據可視覺化")
        return
    
    months = sorted(df['month'].unique())
    hours = range(24)
    
    # 1. 每小時來客數折線圖（按月）
    fig, axes = plt.subplots(len(months), 1, figsize=(14, 5 * len(months)))
    if len(months) == 1:
        axes = [axes]
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        axes[idx].plot(month_df['hour'], month_df['customers'], 
                      marker='o', linewidth=2, markersize=6)
        axes[idx].set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_ylabel('來客數', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_title(f'{month} 每小時來客數', fontsize=14, fontweight='bold',
                           fontproperties=chinese_font_prop)
        axes[idx].set_xticks(hours)
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_customers_by_month.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_customers_by_month.png")
    plt.close()
    
    # 2. 每小時金流折線圖（按月）
    fig, axes = plt.subplots(len(months), 1, figsize=(14, 5 * len(months)))
    if len(months) == 1:
        axes = [axes]
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        axes[idx].plot(month_df['hour'], month_df['revenue'], 
                      marker='o', linewidth=2, markersize=6, color='#2ecc71')
        axes[idx].set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_ylabel('金流 ($)', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_title(f'{month} 每小時金流', fontsize=14, fontweight='bold',
                           fontproperties=chinese_font_prop)
        axes[idx].set_xticks(hours)
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_revenue_by_month.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_revenue_by_month.png")
    plt.close()
    
    # 3. 來客數跨月比較圖
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(months)))
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        ax.plot(month_df['hour'], month_df['customers'], 
               marker='o', linewidth=2, markersize=6, label=month, color=colors[idx])
    
    ax.set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('來客數', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('每小時來客數跨月比較', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop)
    ax.set_xticks(hours)
    ax.legend(fontsize=10, prop=chinese_font_prop)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_customers_comparison.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_customers_comparison.png")
    plt.close()
    
    # 4. 金流跨月比較圖
    fig, ax = plt.subplots(figsize=(14, 6))
    green_colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(months)))
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        ax.plot(month_df['hour'], month_df['revenue'], 
               marker='o', linewidth=2, markersize=6, label=month, color=green_colors[idx])
    
    ax.set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('金流 ($)', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('每小時金流跨月比較', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop)
    ax.set_xticks(hours)
    ax.legend(fontsize=10, prop=chinese_font_prop)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_revenue_comparison.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_revenue_comparison.png")
    plt.close()
    
    # 5. 每小時來客數長條圖（按月）
    fig, axes = plt.subplots(len(months), 1, figsize=(14, 5 * len(months)))
    if len(months) == 1:
        axes = [axes]
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        axes[idx].bar(month_df['hour'], month_df['customers'], 
                     color='#3498db', alpha=0.8, edgecolor='black', linewidth=0.5)
        axes[idx].set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_ylabel('來客數', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_title(f'{month} 每小時來客數', fontsize=14, fontweight='bold',
                           fontproperties=chinese_font_prop)
        axes[idx].set_xticks(hours)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_customers_bar_by_month.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_customers_bar_by_month.png")
    plt.close()
    
    # 6. 每小時金流長條圖（按月）
    fig, axes = plt.subplots(len(months), 1, figsize=(14, 5 * len(months)))
    if len(months) == 1:
        axes = [axes]
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        axes[idx].bar(month_df['hour'], month_df['revenue'], 
                     color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=0.5)
        axes[idx].set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_ylabel('金流 ($)', fontsize=12, fontproperties=chinese_font_prop)
        axes[idx].set_title(f'{month} 每小時金流', fontsize=14, fontweight='bold',
                           fontproperties=chinese_font_prop)
        axes[idx].set_xticks(hours)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_revenue_bar_by_month.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_revenue_bar_by_month.png")
    plt.close()
    
    # 7. 來客數跨月分組長條圖
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(24)
    width = 0.8 / len(months)
    colors_bar = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        ax.bar(x + idx * width, month_df['customers'], width, 
              label=month, color=colors_bar[idx % len(colors_bar)], 
              alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('來客數', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('每小時來客數跨月比較', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop)
    ax.set_xticks(x + width * (len(months) - 1) / 2)
    ax.set_xticklabels(hours)
    ax.legend(fontsize=10, prop=chinese_font_prop)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_customers_bar_comparison.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_customers_bar_comparison.png")
    plt.close()
    
    # 8. 金流跨月分組長條圖
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(24)
    width = 0.8 / len(months)
    colors_bar = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    
    for idx, month in enumerate(months):
        month_df = df[df['month'] == month].sort_values('hour')
        ax.bar(x + idx * width, month_df['revenue'], width, 
              label=month, color=colors_bar[idx % len(colors_bar)], 
              alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('小時', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('金流 ($)', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('每小時金流跨月比較', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop)
    ax.set_xticks(x + width * (len(months) - 1) / 2)
    ax.set_xticklabels(hours)
    ax.legend(fontsize=10, prop=chinese_font_prop)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR_HOURLY, 'hourly_revenue_bar_comparison.png'), 
                dpi=300, bbox_inches='tight')
    print("✓ 儲存圖表: hourly_revenue_bar_comparison.png")
    plt.close()
    
    # 9. 營業日分佈圖
    if payments:
        weekday_counts = defaultdict(int)
        for payment in payments:
            dt_ny = convert_timezone(payment['created_at'])
            weekday = dt_ny.weekday()
            if weekday in BUSINESS_DAYS:
                weekday_counts[weekday] += 1
        
        weekday_names = {0: '週一', 1: '週二', 4: '週五', 5: '週六'}
        weekdays = sorted(weekday_counts.keys())
        counts = [weekday_counts[w] for w in weekdays]
        names = [weekday_names[w] for w in weekdays]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(names, counts, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'], 
              alpha=0.8, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('營業日', fontsize=12, fontproperties=chinese_font_prop)
        ax.set_ylabel('來客數', fontsize=12, fontproperties=chinese_font_prop)
        ax.set_title('營業日來客數分佈', fontsize=14, fontweight='bold',
                    fontproperties=chinese_font_prop)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR_OTHER, 'business_days_distribution.png'), 
                    dpi=300, bbox_inches='tight')
        print("✓ 儲存圖表: business_days_distribution.png")
        plt.close()

def main():
    """主函數"""
    print("=" * 60)
    print("Taiwanway 每小時流量與金流分析")
    print("=" * 60)
    
    ensure_output_dir()
    
    # 載入資料
    payments = load_payments()
    
    # 過濾營業日
    filtered_payments = filter_business_days(payments)
    
    # 按小時統計
    print("\n進行每小時統計...")
    monthly_hourly = analyze_hourly_data(filtered_payments)
    
    # 建立 DataFrame
    df = create_dataframe(monthly_hourly)
    
    # 儲存 JSON 和 CSV
    print("\n儲存分析結果...")
    save_json_csv(df)
    
    # 列印統計資訊
    print_statistics(df, filtered_payments)
    
    # 繪製圖表
    print("\n繪製視覺化圖表...")
    create_visualizations(df, filtered_payments)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print(f"結果儲存在: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)

if __name__ == "__main__":
    main()

