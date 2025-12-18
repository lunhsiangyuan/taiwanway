#!/usr/bin/env python3
"""
分析週一、週二、週五、週六每個月的平均消費金額
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import pytz
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 設定
DATA_DIR = "../data/2025_08_11"
PAYMENTS_FILE = os.path.join(DATA_DIR, "taiwanway_payments.csv")
OUTPUT_DIR = "../analysis_output"
DATA_DIR_WEEKDAY = os.path.join(OUTPUT_DIR, "data", "weekday")
CHARTS_DIR_WEEKDAY = os.path.join(OUTPUT_DIR, "charts", "weekday")

# 要分析的星期：週一、週二、週五、週六
TARGET_WEEKDAYS = [0, 1, 4, 5]  # Monday=0, Tuesday=1, Friday=4, Saturday=5
WEEKDAY_NAMES = {0: '週一', 1: '週二', 4: '週五', 5: '週六'}

# 紐約時區
NY_TZ = pytz.timezone('America/New_York')

def ensure_output_dir():
    """確保輸出目錄存在"""
    os.makedirs(DATA_DIR_WEEKDAY, exist_ok=True)
    os.makedirs(CHARTS_DIR_WEEKDAY, exist_ok=True)

def load_payments():
    """載入 payments 資料（從 CSV）"""
    print(f"載入 payments 資料: {PAYMENTS_FILE}")
    df = pd.read_csv(PAYMENTS_FILE, encoding='utf-8-sig')
    
    # 轉換為字典列表格式以保持兼容性
    payments = df.to_dict('records')
    
    print(f"✓ 載入 {len(payments)} 筆 payments")
    return payments

def convert_timezone(dt_str):
    """將 UTC 時間轉換為紐約時區"""
    if pd.isna(dt_str) or dt_str == '':
        return None
    if isinstance(dt_str, str):
        dt_utc = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        dt_ny = dt_utc.astimezone(NY_TZ)
        return dt_ny
    return dt_str

def analyze_weekday_revenue_by_month(payments):
    """分析每個月、每個星期的平均每日消費金額"""
    # 結構：month -> weekday -> {total_revenue, dates}
    monthly_weekday_stats = defaultdict(lambda: defaultdict(lambda: {
        'total_revenue': 0.0,
        'dates': set()
    }))
    
    for payment in payments:
        if payment.get('status') != 'COMPLETED':
            continue
        if pd.isna(payment.get('created_at')) or payment.get('created_at') == '':
            continue
        
        dt_ny = convert_timezone(payment['created_at'])
        if dt_ny is None:
            continue
        
        month = dt_ny.month
        weekday = dt_ny.weekday()
        date = dt_ny.date()
        
        # 只分析目標星期
        if weekday not in TARGET_WEEKDAYS:
            continue
        
        # 金額：CSV 中已經是美元
        amount = payment.get('total_amount', 0)
        
        monthly_weekday_stats[month][weekday]['total_revenue'] += amount
        monthly_weekday_stats[month][weekday]['dates'].add(date)
    
    # 計算平均每日金額
    results = []
    for month in sorted(monthly_weekday_stats.keys()):
        for weekday in TARGET_WEEKDAYS:
            if weekday in monthly_weekday_stats[month]:
                stats = monthly_weekday_stats[month][weekday]
                dates_count = len(stats['dates'])
                total_revenue = stats['total_revenue']
                avg_daily_revenue = total_revenue / dates_count if dates_count > 0 else 0
                
                results.append({
                    'month': f"2025-{month:02d}",
                    'month_num': month,
                    'weekday': weekday,
                    'weekday_name': WEEKDAY_NAMES[weekday],
                    'total_revenue': total_revenue,
                    'dates_count': dates_count,
                    'avg_daily_revenue': avg_daily_revenue
                })
    
    return results

def create_visualization(results):
    """創建視覺化圖表"""
    # 設定中文字體
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
    
    # 轉換為 DataFrame
    df = pd.DataFrame(results)
    
    if len(df) == 0:
        print("⚠ 沒有數據可視覺化")
        return
    
    # 準備數據
    months = sorted(df['month'].unique())
    weekdays = TARGET_WEEKDAYS
    weekday_names = [WEEKDAY_NAMES[w] for w in weekdays]
    
    # 創建矩陣數據
    data_matrix = []
    for month in months:
        month_row = []
        for weekday in weekdays:
            month_data = df[(df['month'] == month) & (df['weekday'] == weekday)]
            if len(month_data) > 0:
                month_row.append(month_data['avg_daily_revenue'].values[0])
            else:
                month_row.append(0)
        data_matrix.append(month_row)
    
    # 1. 分組長條圖（按月分組，每個月顯示4個星期）
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x = range(len(months))
    width = 0.2  # 每個長條的寬度
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']  # 藍、綠、紅、紫
    
    for idx, weekday in enumerate(weekdays):
        weekday_data = [data_matrix[i][idx] for i in range(len(months))]
        ax.bar([xi + idx * width for xi in x], weekday_data, width, 
               label=WEEKDAY_NAMES[weekday], color=colors[idx], alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('月份', fontsize=12, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_ylabel('平均每日消費金額 ($)', fontsize=12, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_title('各月份星期別平均每日消費金額', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_xticks([xi + width * 1.5 for xi in x])
    ax.set_xticklabels(months, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.legend(fontsize=10, prop=chinese_font_prop if chinese_font_prop else None)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_WEEKDAY, 'weekday_revenue_by_month.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: weekday_revenue_by_month.png")
    plt.close()
    
    # 2. 折線圖（每個星期一條線，顯示跨月趨勢）
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for idx, weekday in enumerate(weekdays):
        weekday_data = [data_matrix[i][idx] for i in range(len(months))]
        ax.plot(months, weekday_data, marker='o', linewidth=2, markersize=8,
               label=WEEKDAY_NAMES[weekday], color=colors[idx], alpha=0.8)
    
    ax.set_xlabel('月份', fontsize=12, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_ylabel('平均每日消費金額 ($)', fontsize=12, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_title('各星期平均每日消費金額趨勢（跨月）', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.legend(fontsize=10, prop=chinese_font_prop if chinese_font_prop else None)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_WEEKDAY, 'weekday_revenue_trend.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: weekday_revenue_trend.png")
    plt.close()
    
    # 3. 熱力圖（月份 x 星期）
    fig, ax = plt.subplots(figsize=(10, 6))
    
    import numpy as np
    data_array = np.array(data_matrix)
    
    im = ax.imshow(data_array, cmap='YlOrRd', aspect='auto')
    
    # 設置刻度
    ax.set_xticks(range(len(weekday_names)))
    ax.set_xticklabels(weekday_names, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_yticks(range(len(months)))
    ax.set_yticklabels(months, fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    # 添加數值標籤
    for i in range(len(months)):
        for j in range(len(weekday_names)):
            text = ax.text(j, i, f'${data_array[i, j]:,.0f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    ax.set_title('各月份星期別平均每日消費金額熱力圖', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_xlabel('星期', fontsize=12, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_ylabel('月份', fontsize=12, fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    # 添加顏色條
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('平均每日消費金額 ($)', fontsize=10,
                   fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_WEEKDAY, 'weekday_revenue_heatmap.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: weekday_revenue_heatmap.png")
    plt.close()

def print_statistics(results):
    """列印統計資訊"""
    print("\n" + "=" * 60)
    print("各月份星期別平均每日消費金額")
    print("=" * 60)
    
    df = pd.DataFrame(results)
    
    for month in sorted(df['month'].unique()):
        print(f"\n{month}:")
        month_df = df[df['month'] == month]
        for weekday in TARGET_WEEKDAYS:
            weekday_data = month_df[month_df['weekday'] == weekday]
            if len(weekday_data) > 0:
                row = weekday_data.iloc[0]
                print(f"  {row['weekday_name']}: ${row['avg_daily_revenue']:,.2f} ({row['dates_count']} 天)")
    
    # 計算總平均
    print("\n" + "=" * 60)
    print("總平均（所有月份）")
    print("=" * 60)
    
    for weekday in TARGET_WEEKDAYS:
        weekday_df = df[df['weekday'] == weekday]
        if len(weekday_df) > 0:
            avg_all_months = weekday_df['avg_daily_revenue'].mean()
            total_days = weekday_df['dates_count'].sum()
            print(f"  {WEEKDAY_NAMES[weekday]}: ${avg_all_months:,.2f} (總共 {total_days} 天)")
    
    print("=" * 60)

def save_csv_json(results):
    """儲存 CSV 和 JSON"""
    df = pd.DataFrame(results)
    
    # CSV
    csv_file = os.path.join(DATA_DIR_WEEKDAY, 'weekday_revenue_by_month.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"✓ 儲存 CSV: weekday_revenue_by_month.csv")
    
    # JSON
    json_file = os.path.join(DATA_DIR_WEEKDAY, 'weekday_revenue_by_month.json')
    json_data = df.to_dict('records')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"✓ 儲存 JSON: weekday_revenue_by_month.json")

def main():
    """主函數"""
    print("=" * 60)
    print("分析週一、週二、週五、週六各月份平均消費金額")
    print("=" * 60)
    
    ensure_output_dir()
    
    # 載入資料
    payments = load_payments()
    
    # 分析
    print("\n進行分析...")
    results = analyze_weekday_revenue_by_month(payments)
    
    if len(results) == 0:
        print("⚠ 沒有找到符合條件的數據")
        return
    
    # 列印統計
    print_statistics(results)
    
    # 儲存數據
    print("\n儲存數據...")
    save_csv_json(results)
    
    # 繪製圖表
    print("\n繪製視覺化圖表...")
    create_visualization(results)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print(f"結果儲存在: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)

if __name__ == "__main__":
    main()

