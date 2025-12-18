#!/usr/bin/env python3
"""
Taiwanway 成本結構與人力配置分析
包含：人力配置時段圖、成本結構圖、利潤分析圖等
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 設定
DATA_DIR = "../data/2025_08_11"
PAYMENTS_FILE = os.path.join(DATA_DIR, "taiwanway_payments.csv")
OUTPUT_DIR = "../analysis_output"
COST_ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "cost_analysis")  # 統一目錄
CHARTS_DIR_COST = os.path.join(COST_ANALYSIS_DIR, "charts")  # 圖表目錄
DATA_DIR_COST = os.path.join(COST_ANALYSIS_DIR, "data")  # 數據目錄
REPORTS_DIR_COST = os.path.join(COST_ANALYSIS_DIR, "reports")  # 報告目錄

# 成本參數
HOURLY_LABOR_COST = 15  # 每小時人力成本
MONTHLY_RENT_UTILITIES = 4000  # 房租保險水電/月
FOOD_PACKAGING_RATE = 0.35  # 食材包材成本率 35%

# 人力配置方案（$3,300/月預算）
LABOR_SCHEDULE = {
    '11:00-12:00': {'fulltime': 1, 'parttime': 0, 'total': 1},
    '12:00-13:00': {'fulltime': 1, 'parttime': 2, 'total': 3},  # 午餐高峰
    '13:00-14:00': {'fulltime': 1, 'parttime': 1, 'total': 2},
    '14:00-15:30': {'fulltime': 1, 'parttime': 0, 'total': 1},  # 低峰
    '15:30-16:00': {'fulltime': 0, 'parttime': 0, 'total': 0},  # 休息
    '16:00-17:00': {'fulltime': 1, 'parttime': 0, 'total': 1},
    '17:00-18:00': {'fulltime': 1, 'parttime': 2, 'total': 3},  # 晚餐高峰
    '18:00-19:00': {'fulltime': 1, 'parttime': 0, 'total': 1},
}

# 每日人力成本計算
DAILY_LABOR_HOURS = 13.5  # 總人時/天
DAILY_LABOR_COST = DAILY_LABOR_HOURS * HOURLY_LABOR_COST  # $202.5/天
MONTHLY_LABOR_COST = DAILY_LABOR_COST * 16  # 以16營業日計算 = $3,240/月

def ensure_output_dir():
    """確保輸出目錄存在"""
    os.makedirs(COST_ANALYSIS_DIR, exist_ok=True)
    os.makedirs(CHARTS_DIR_COST, exist_ok=True)
    os.makedirs(DATA_DIR_COST, exist_ok=True)
    os.makedirs(REPORTS_DIR_COST, exist_ok=True)

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
    
    # 設定現代風格
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = '#f8f9fa'
    
    return chinese_font_prop

def load_monthly_data():
    """載入月度營收數據"""
    # 嘗試多個可能的路徑
    possible_paths = [
        os.path.join(OUTPUT_DIR, "..", "data", "all_payments", "all_payments_monthly_report.csv"),
        os.path.join("data", "all_payments", "all_payments_monthly_report.csv"),
        os.path.join("..", "data", "all_payments", "all_payments_monthly_report.csv"),
    ]
    
    for monthly_file in possible_paths:
        if os.path.exists(monthly_file):
            df = pd.read_csv(monthly_file, encoding='utf-8-sig')
            print(f"✓ 載入數據: {monthly_file}")
            return df
    
    print(f"⚠ 無法找到月度數據文件，嘗試的路徑：")
    for path in possible_paths:
        print(f"  - {os.path.abspath(path)}")
    return None

def calculate_cost_structure(df):
    """計算各月份成本結構"""
    results = []
    
    for _, row in df.iterrows():
        month = row['月份']
        business_days = row['營業日數']
        revenue = row['總營收 (USD)']
        daily_revenue = row['日均營收 (USD)']
        
        # 計算成本
        food_cost = revenue * FOOD_PACKAGING_RATE
        labor_cost = DAILY_LABOR_COST * business_days
        rent_utilities = MONTHLY_RENT_UTILITIES
        total_cost = food_cost + labor_cost + rent_utilities
        net_profit = revenue - total_cost
        profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
        
        results.append({
            'month': month,
            'business_days': business_days,
            'revenue': revenue,
            'daily_revenue': daily_revenue,
            'food_cost': food_cost,
            'labor_cost': labor_cost,
            'rent_utilities': rent_utilities,
            'total_cost': total_cost,
            'net_profit': net_profit,
            'profit_margin': profit_margin,
        })
    
    return pd.DataFrame(results)

def create_labor_schedule_chart(chinese_font_prop):
    """創建人力配置時段圖（Gantt 風格）"""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # 準備數據
    time_slots = list(LABOR_SCHEDULE.keys())
    y_positions = np.arange(len(time_slots))
    
    # 顏色配置
    colors = {
        'fulltime': '#3498db',  # 藍色（全職）
        'parttime': '#e74c3c',  # 紅色（兼職）
    }
    
    # 繪製橫條圖
    fulltime_bars = [LABOR_SCHEDULE[slot]['fulltime'] for slot in time_slots]
    parttime_bars = [LABOR_SCHEDULE[slot]['parttime'] for slot in time_slots]
    total_bars = [LABOR_SCHEDULE[slot]['total'] for slot in time_slots]
    
    # 堆疊柱狀圖
    ax.barh(y_positions, fulltime_bars, height=0.6, label='全職', 
            color=colors['fulltime'], alpha=0.8, edgecolor='white', linewidth=1)
    ax.barh(y_positions, parttime_bars, height=0.6, left=fulltime_bars, 
            label='兼職', color=colors['parttime'], alpha=0.8, 
            edgecolor='white', linewidth=1)
    
    # 標註總人數
    for i, (slot, total) in enumerate(zip(time_slots, total_bars)):
        if total > 0:
            ax.text(total + 0.1, i, f'{total}人', 
                   va='center', fontsize=10, fontweight='bold',
                   fontproperties=chinese_font_prop)
    
    # 設定標籤
    ax.set_yticks(y_positions)
    ax.set_yticklabels(time_slots, fontproperties=chinese_font_prop)
    ax.set_xlabel('人力配置（人）', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('人力配置時段圖（每日配置）', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop, pad=20)
    
    # 添加網格
    ax.grid(True, alpha=0.3, axis='x', linestyle='--')
    ax.set_axisbelow(True)
    
    # 圖例
    ax.legend(loc='lower right', frameon=True, fancybox=True, 
             shadow=True, prop=chinese_font_prop, fontsize=10)
    
    # 添加成本標註
    cost_text = f'每日人力成本: ${DAILY_LABOR_COST:.2f} | 月預算: ${MONTHLY_LABOR_COST:.0f}'
    ax.text(0.02, 0.98, cost_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
           fontproperties=chinese_font_prop)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_COST, 'labor_schedule_chart.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: labor_schedule_chart.png")
    plt.close()

def create_cost_structure_chart(df_cost, chinese_font_prop):
    """創建成本結構堆疊柱狀圖"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    months = df_cost['month'].tolist()
    x = np.arange(len(months))
    width = 0.6
    
    # 成本數據
    food_costs = df_cost['food_cost'].tolist()
    labor_costs = df_cost['labor_cost'].tolist()
    rent_costs = df_cost['rent_utilities'].tolist()
    revenues = df_cost['revenue'].tolist()
    profits = df_cost['net_profit'].tolist()
    
    # 顏色配置
    colors = {
        'food': '#e74c3c',      # 紅色（食材包材）
        'labor': '#3498db',     # 藍色（人力）
        'rent': '#9b59b6',      # 紫色（房租水電）
        'profit': '#2ecc71',    # 綠色（利潤）
        'revenue': '#34495e',   # 深灰（營收線）
    }
    
    # 繪製堆疊柱狀圖（成本）
    p1 = ax.bar(x, food_costs, width, label='食材包材 (35%)', 
               color=colors['food'], alpha=0.8, edgecolor='white', linewidth=1)
    p2 = ax.bar(x, labor_costs, width, bottom=food_costs, label='人力成本', 
               color=colors['labor'], alpha=0.8, edgecolor='white', linewidth=1)
    p3 = ax.bar(x, rent_costs, width, 
               bottom=[f + l for f, l in zip(food_costs, labor_costs)], 
               label='房租保險水電', color=colors['rent'], alpha=0.8, 
               edgecolor='white', linewidth=1)
    
    # 繪製利潤柱狀圖（在成本上方）
    p4 = ax.bar(x, profits, width, 
               bottom=[f + l + r for f, l, r in zip(food_costs, labor_costs, rent_costs)], 
               label='淨利潤', color=colors['profit'], alpha=0.8, 
               edgecolor='white', linewidth=1)
    
    # 繪製營收線（參考線）
    ax2 = ax.twinx()
    line = ax2.plot(x, revenues, marker='o', linewidth=2.5, markersize=8, 
                   color=colors['revenue'], label='總營收', alpha=0.7)
    ax2.set_ylabel('總營收 ($)', fontsize=12, fontproperties=chinese_font_prop)
    ax2.tick_params(axis='y', labelsize=10)
    
    # 標註數值
    for i, (month, revenue, profit) in enumerate(zip(months, revenues, profits)):
        # 營收標註
        ax2.text(i, revenue, f'${revenue:,.0f}', ha='center', va='bottom',
                fontsize=9, fontweight='bold', fontproperties=chinese_font_prop)
        # 利潤標註
        if profit > 0:
            total_cost = food_costs[i] + labor_costs[i] + rent_costs[i]
            ax.text(i, total_cost + profit, f'${profit:,.0f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold',
                   color=colors['profit'], fontproperties=chinese_font_prop)
        else:
            ax.text(i, revenues[i], f'${profit:,.0f}',
                   ha='center', va='top', fontsize=9, fontweight='bold',
                   color='red', fontproperties=chinese_font_prop)
    
    # 設定標籤
    ax.set_xlabel('月份', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('金額 ($)', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('成本結構分析（各月份對比）', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontproperties=chinese_font_prop)
    
    # 添加網格
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)
    
    # 添加損益平衡線（0線）
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
    
    # 合併圖例
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
             frameon=True, fancybox=True, shadow=True, 
             prop=chinese_font_prop, fontsize=10)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_COST, 'cost_structure_chart.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: cost_structure_chart.png")
    plt.close()

def create_cost_pie_chart(df_cost, chinese_font_prop):
    """創建成本佔比餅圖（以16營業日為基準）"""
    # 選擇16營業日的月份（2025-10）
    target_month = df_cost[df_cost['business_days'] == 16].iloc[0] if len(df_cost[df_cost['business_days'] == 16]) > 0 else df_cost.iloc[-1]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左圖：成本結構餅圖
    cost_labels = ['食材包材', '人力成本', '房租保險水電']
    cost_values = [
        target_month['food_cost'],
        target_month['labor_cost'],
        target_month['rent_utilities']
    ]
    cost_colors = ['#e74c3c', '#3498db', '#9b59b6']
    
    # 添加百分比標籤
    def autopct_format(pct):
        total = sum(cost_values)
        val = pct / 100. * total
        return f'${val:,.0f}\n({pct:.1f}%)'
    
    wedges, texts, autotexts = ax1.pie(cost_values, labels=cost_labels, 
                                      colors=cost_colors, autopct=autopct_format,
                                      startangle=90, textprops={'fontproperties': chinese_font_prop})
    
    # 美化文字
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax1.set_title(f'{target_month["month"]} 成本結構\n（總成本: ${target_month["total_cost"]:,.2f}）', 
                 fontsize=14, fontweight='bold', fontproperties=chinese_font_prop, pad=20)
    
    # 右圖：營收分配餅圖
    # 如果淨利潤為負，則不顯示在餅圖中，改為顯示虧損標註
    if target_month['net_profit'] >= 0:
        revenue_labels = ['食材包材', '人力成本', '房租保險水電', '淨利潤']
        revenue_values = [
            target_month['food_cost'],
            target_month['labor_cost'],
            target_month['rent_utilities'],
            target_month['net_profit']
        ]
        revenue_colors = ['#e74c3c', '#3498db', '#9b59b6', '#2ecc71']
    else:
        # 虧損時只顯示成本項目
        revenue_labels = ['食材包材', '人力成本', '房租保險水電']
        revenue_values = [
            target_month['food_cost'],
            target_month['labor_cost'],
            target_month['rent_utilities']
        ]
        revenue_colors = ['#e74c3c', '#3498db', '#9b59b6']
    
    def autopct_revenue(pct):
        total = target_month['revenue']
        val = pct / 100. * total
        return f'${val:,.0f}\n({pct:.1f}%)'
    
    wedges2, texts2, autotexts2 = ax2.pie(revenue_values, labels=revenue_labels,
                                         colors=revenue_colors, autopct=autopct_revenue,
                                         startangle=90, textprops={'fontproperties': chinese_font_prop})
    
    # 如果虧損，在圖上標註
    if target_month['net_profit'] < 0:
        ax2.text(0, 0, f'虧損\n${abs(target_month["net_profit"]):,.0f}',
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='red', fontproperties=chinese_font_prop,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    ax2.set_title(f'{target_month["month"]} 營收分配\n（總營收: ${target_month["revenue"]:,.2f}）', 
                 fontsize=14, fontweight='bold', fontproperties=chinese_font_prop, pad=20)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_COST, 'cost_pie_chart.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: cost_pie_chart.png")
    plt.close()

def create_profit_trend_chart(df_cost, chinese_font_prop):
    """創建利潤趨勢圖（折線圖 + 區域圖）"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    months = df_cost['month'].tolist()
    x = np.arange(len(months))
    
    revenues = df_cost['revenue'].tolist()
    profits = df_cost['net_profit'].tolist()
    profit_margins = df_cost['profit_margin'].tolist()
    
    # 計算損益平衡點
    break_even_revenue = MONTHLY_RENT_UTILITIES / (1 - FOOD_PACKAGING_RATE - DAILY_LABOR_COST / 1000)  # 簡化計算
    break_even_daily = break_even_revenue / 16  # 假設16營業日
    
    # 繪製區域圖（利潤區間）
    ax.fill_between(x, 0, profits, where=np.array(profits) > 0, 
                   alpha=0.3, color='#2ecc71', label='獲利區間')
    ax.fill_between(x, 0, profits, where=np.array(profits) < 0, 
                   alpha=0.3, color='#e74c3c', label='虧損區間')
    
    # 繪製營收柱狀圖
    ax2 = ax.twinx()
    bars = ax2.bar(x, revenues, width=0.5, alpha=0.6, color='#3498db', 
                   label='總營收', edgecolor='white', linewidth=1)
    
    # 繪製利潤折線圖
    line1 = ax.plot(x, profits, marker='o', linewidth=3, markersize=10, 
                   color='#2ecc71', label='淨利潤', alpha=0.9)
    
    # 繪製利潤率折線圖（使用右軸）
    ax3 = ax.twinx()
    ax3.spines['right'].set_position(('outward', 60))
    line2 = ax3.plot(x, profit_margins, marker='s', linewidth=2, markersize=8,
                    color='#f39c12', label='利潤率 (%)', linestyle='--', alpha=0.8)
    
    # 添加損益平衡線
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.5, 
              label='損益平衡線')
    
    # 標註數值
    for i, (month, revenue, profit, margin) in enumerate(zip(months, revenues, profits, profit_margins)):
        # 營收標註
        ax2.text(i, revenue, f'${revenue:,.0f}', ha='center', va='bottom',
                fontsize=9, fontweight='bold', fontproperties=chinese_font_prop)
        # 利潤標註
        ax.text(i, profit, f'${profit:,.0f}\n({margin:.1f}%)', 
               ha='center', va='bottom' if profit > 0 else 'top',
               fontsize=9, fontweight='bold',
               color='#2ecc71' if profit > 0 else 'red',
               fontproperties=chinese_font_prop,
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # 設定標籤
    ax.set_xlabel('月份', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('淨利潤 ($)', fontsize=12, fontproperties=chinese_font_prop, color='#2ecc71')
    ax2.set_ylabel('總營收 ($)', fontsize=12, fontproperties=chinese_font_prop, color='#3498db')
    ax3.set_ylabel('利潤率 (%)', fontsize=12, fontproperties=chinese_font_prop, color='#f39c12')
    ax.set_title('利潤趨勢分析', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontproperties=chinese_font_prop)
    
    # 顏色設定
    ax.tick_params(axis='y', labelcolor='#2ecc71')
    ax2.tick_params(axis='y', labelcolor='#3498db')
    ax3.tick_params(axis='y', labelcolor='#f39c12')
    
    # 添加網格
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)
    
    # 合併圖例
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, 
             loc='upper left', frameon=True, fancybox=True, shadow=True,
             prop=chinese_font_prop, fontsize=10)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_COST, 'profit_trend_chart.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: profit_trend_chart.png")
    plt.close()

def create_break_even_analysis(df_cost, chinese_font_prop):
    """創建損益平衡分析圖"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 計算損益平衡點
    fixed_cost = MONTHLY_RENT_UTILITIES + MONTHLY_LABOR_COST
    contribution_margin_rate = 1 - FOOD_PACKAGING_RATE  # 65%
    break_even_revenue = fixed_cost / contribution_margin_rate
    
    # 不同營業日數的損益平衡分析
    business_days_range = range(7, 19)
    break_even_data = []
    
    for days in business_days_range:
        labor_cost = DAILY_LABOR_COST * days
        total_fixed = MONTHLY_RENT_UTILITIES + labor_cost
        break_even = total_fixed / contribution_margin_rate
        break_even_daily = break_even / days
        break_even_data.append({
            'days': days,
            'break_even_revenue': break_even,
            'break_even_daily': break_even_daily,
            'labor_cost': labor_cost,
        })
    
    df_break_even = pd.DataFrame(break_even_data)
    
    # 繪製損益平衡線
    ax.plot(df_break_even['days'], df_break_even['break_even_daily'], 
           marker='o', linewidth=3, markersize=8, color='#e74c3c', 
           label='損益平衡日均營收', linestyle='--', alpha=0.8)
    
    # 添加實際數據點
    for _, row in df_cost.iterrows():
        days = row['business_days']
        daily_rev = row['daily_revenue']
        profit = row['net_profit']
        color = '#2ecc71' if profit > 0 else '#e74c3c'
        marker = '^' if profit > 0 else 'v'
        ax.scatter(days, daily_rev, s=200, color=color, marker=marker, 
                  edgecolors='black', linewidth=2, alpha=0.7,
                  label='實際日均營收' if days == df_cost.iloc[0]['business_days'] else '')
    
    # 添加安全區域
    ax.fill_between(df_break_even['days'], 0, df_break_even['break_even_daily'],
                    alpha=0.2, color='#e74c3c', label='虧損區域')
    ax.fill_between(df_break_even['days'], df_break_even['break_even_daily'], 
                    df_break_even['break_even_daily'].max() * 1.5,
                    alpha=0.2, color='#2ecc71', label='獲利區域')
    
    # 標註關鍵點
    for _, row in df_break_even[df_break_even['days'].isin([12, 14, 16, 18])].iterrows():
        ax.annotate(f'{row["break_even_daily"]:.0f}',
                   xy=(row['days'], row['break_even_daily']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   fontproperties=chinese_font_prop)
    
    ax.set_xlabel('營業日數', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('日均營收 ($)', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('損益平衡分析（不同營業日數）', fontsize=14, fontweight='bold',
                fontproperties=chinese_font_prop, pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # 圖例
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left',
             frameon=True, fancybox=True, shadow=True,
             prop=chinese_font_prop, fontsize=10)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_COST, 'break_even_analysis.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存圖表: break_even_analysis.png")
    plt.close()

def save_cost_data(df_cost):
    """儲存成本數據為 CSV 和 JSON"""
    # CSV
    csv_file = os.path.join(DATA_DIR_COST, 'cost_structure_analysis.csv')
    df_cost.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"✓ 儲存數據: cost_structure_analysis.csv")
    
    # JSON
    json_file = os.path.join(DATA_DIR_COST, 'cost_structure_analysis.json')
    json_data = df_cost.to_dict('records')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"✓ 儲存數據: cost_structure_analysis.json")

def save_labor_schedule_data():
    """儲存人力配置數據"""
    schedule_data = {
        'daily_labor_hours': DAILY_LABOR_HOURS,
        'daily_labor_cost': DAILY_LABOR_COST,
        'monthly_labor_budget': MONTHLY_LABOR_COST,
        'hourly_labor_cost': HOURLY_LABOR_COST,
        'schedule': LABOR_SCHEDULE
    }
    
    json_file = os.path.join(DATA_DIR_COST, 'labor_schedule.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(schedule_data, f, indent=2, ensure_ascii=False)
    print(f"✓ 儲存數據: labor_schedule.json")

def create_summary_report(df_cost):
    """創建文字摘要報告"""
    report_file = os.path.join(REPORTS_DIR_COST, 'cost_analysis_summary.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("Taiwanway 成本結構與人力配置分析報告\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("成本參數設定\n")
        f.write("-" * 60 + "\n")
        f.write(f"每小時人力成本: ${HOURLY_LABOR_COST}\n")
        f.write(f"房租保險水電: ${MONTHLY_RENT_UTILITIES:,}/月\n")
        f.write(f"食材包材成本率: {FOOD_PACKAGING_RATE*100:.0f}%\n\n")
        
        f.write("人力配置摘要\n")
        f.write("-" * 60 + "\n")
        f.write(f"每日人力配置: {DAILY_LABOR_HOURS} 人時\n")
        f.write(f"每日人力成本: ${DAILY_LABOR_COST:.2f}\n")
        f.write(f"月人力預算: ${MONTHLY_LABOR_COST:.0f} (16營業日)\n\n")
        
        f.write("各月份成本結構分析\n")
        f.write("-" * 60 + "\n")
        
        for _, row in df_cost.iterrows():
            f.write(f"\n{row['month']}:\n")
            f.write(f"  營業日數: {row['business_days']} 天\n")
            f.write(f"  總營收: ${row['revenue']:,.2f}\n")
            f.write(f"  食材包材: ${row['food_cost']:,.2f} ({row['food_cost']/row['revenue']*100:.1f}%)\n")
            f.write(f"  人力成本: ${row['labor_cost']:,.2f} ({row['labor_cost']/row['revenue']*100:.1f}%)\n")
            f.write(f"  房租水電: ${row['rent_utilities']:,.2f} ({row['rent_utilities']/row['revenue']*100:.1f}%)\n")
            f.write(f"  總成本: ${row['total_cost']:,.2f} ({row['total_cost']/row['revenue']*100:.1f}%)\n")
            f.write(f"  淨利潤: ${row['net_profit']:,.2f} ({row['profit_margin']:.1f}%)\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("報告生成時間: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 60 + "\n")
    
    print(f"✓ 儲存報告: cost_analysis_summary.txt")

def print_summary(df_cost):
    """列印分析摘要"""
    print("\n" + "=" * 60)
    print("成本結構分析摘要")
    print("=" * 60)
    
    for _, row in df_cost.iterrows():
        print(f"\n{row['month']}:")
        print(f"  營業日數: {row['business_days']} 天")
        print(f"  總營收: ${row['revenue']:,.2f}")
        print(f"  食材包材: ${row['food_cost']:,.2f} ({row['food_cost']/row['revenue']*100:.1f}%)")
        print(f"  人力成本: ${row['labor_cost']:,.2f} ({row['labor_cost']/row['revenue']*100:.1f}%)")
        print(f"  房租水電: ${row['rent_utilities']:,.2f} ({row['rent_utilities']/row['revenue']*100:.1f}%)")
        print(f"  總成本: ${row['total_cost']:,.2f} ({row['total_cost']/row['revenue']*100:.1f}%)")
        print(f"  淨利潤: ${row['net_profit']:,.2f} ({row['profit_margin']:.1f}%)")
    
    print("\n" + "=" * 60)
    print("人力配置摘要")
    print("=" * 60)
    print(f"每日人力配置: {DAILY_LABOR_HOURS} 人時")
    print(f"每日人力成本: ${DAILY_LABOR_COST:.2f}")
    print(f"月人力預算: ${MONTHLY_LABOR_COST:.0f} (16營業日)")
    print("=" * 60)

def main():
    """主函數"""
    print("=" * 60)
    print("Taiwanway 成本結構與人力配置分析")
    print("=" * 60)
    
    ensure_output_dir()
    
    # 設定中文字體
    chinese_font_prop = setup_chinese_font()
    
    # 載入數據
    print("\n載入月度數據...")
    df_monthly = load_monthly_data()
    
    if df_monthly is None or len(df_monthly) == 0:
        print("⚠ 無法載入月度數據，請先執行其他分析腳本")
        return
    
    # 計算成本結構
    print("\n計算成本結構...")
    df_cost = calculate_cost_structure(df_monthly)
    
    # 列印摘要
    print_summary(df_cost)
    
    # 儲存數據
    print("\n儲存分析數據...")
    save_cost_data(df_cost)
    save_labor_schedule_data()
    
    # 創建圖表
    print("\n繪製視覺化圖表...")
    create_labor_schedule_chart(chinese_font_prop)
    create_cost_structure_chart(df_cost, chinese_font_prop)
    create_cost_pie_chart(df_cost, chinese_font_prop)
    create_profit_trend_chart(df_cost, chinese_font_prop)
    create_break_even_analysis(df_cost, chinese_font_prop)
    
    # 創建摘要報告
    print("\n生成文字報告...")
    create_summary_report(df_cost)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print(f"所有內容儲存在: {os.path.abspath(COST_ANALYSIS_DIR)}")
    print(f"  - 圖表: charts/")
    print(f"  - 數據: data/")
    print(f"  - 報告: reports/")
    print("=" * 60)

if __name__ == "__main__":
    main()

