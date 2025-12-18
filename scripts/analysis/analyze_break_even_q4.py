#!/usr/bin/env python3
"""
Taiwanway Q4 2025 損益平衡分析
分析 9、10、11 月營收，計算不同營業天數的損益平衡點
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os
from pathlib import Path
from datetime import datetime

# ============================================================
# 成本參數設定
# ============================================================
FIXED_COSTS = {
    'rent': 3100,      # 房租/月
    'utilities': 700,  # 水電/月
}
FIXED_COST_TOTAL = sum(FIXED_COSTS.values())  # $3,800/月

# 人力成本（四種情境）
DAILY_LABOR_COSTS = [100, 160, 200, 250]
DAILY_LABOR_COST = 160  # 預設值（向後相容）

# 食材成本率（三種情境）
FOOD_COST_RATES = [0.30, 0.35, 0.40]

# NYC 銷售稅率 (NY State 4% + NYC 4.5% + MTA 0.375%)
NYC_TAX_RATE = 0.08875

# ============================================================
# 路徑設定
# ============================================================
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
# 使用更完整的月度數據
DATA_DIR = PROJECT_ROOT / 'data' / 'all_payments'
OUTPUT_DIR = PROJECT_ROOT / 'analysis_output' / 'break_even_q4'

# ============================================================
# 中文字體設定
# ============================================================
def setup_chinese_font():
    """設定中文字體"""
    plt.rcParams['text.usetex'] = False

    font_paths = [
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    ]

    chinese_font_prop = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            chinese_font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.sans-serif'] = [chinese_font_prop.get_name(), 'DejaVu Sans', 'Arial']
            break

    plt.rcParams['axes.unicode_minus'] = False
    sns.set_style("whitegrid")

    return chinese_font_prop

# ============================================================
# 數據處理
# ============================================================
def load_and_process_data():
    """載入並處理月度 CSV 數據（使用 payments_2025_XX.csv 格式）"""
    all_data = []

    for month in [9, 10, 11]:
        file_path = DATA_DIR / f'payments_2025_{month:02d}.csv'
        if file_path.exists():
            print(f"載入數據: {file_path.name}")
            df = pd.read_csv(file_path)

            # 解析日期時間（UTC 格式）
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['Date'] = df['created_at'].dt.date
            df['Month'] = df['created_at'].dt.month

            # 篩選 COMPLETED 交易（排除 FAILED、CANCELED）
            total_count = len(df)
            df = df[df['status'] == 'COMPLETED']
            completed_count = len(df)

            # 計算 Net Sales（扣除 NYC 銷售稅 8.875%）
            # payments CSV 的 amount 是含稅金額，需除以 (1 + 稅率) 得到稅前淨銷售額
            df['Revenue'] = df['amount'].astype(float) / (1 + NYC_TAX_RATE)

            all_data.append(df)
            print(f"  {month}月: {completed_count}/{total_count} 筆 COMPLETED 交易")

    if all_data:
        df_combined = pd.concat(all_data, ignore_index=True)
        print(f"\nQ4 總數據筆數: {len(df_combined)}")
        return df_combined

    return pd.DataFrame()

def calculate_monthly_stats(df):
    """計算月度統計"""
    monthly_stats = df.groupby('Month').agg({
        'Revenue': 'sum',
        'Date': 'nunique'
    }).reset_index()

    monthly_stats.columns = ['Month', 'Total Revenue', 'Business Days']
    monthly_stats['Daily Avg Revenue'] = monthly_stats['Total Revenue'] / monthly_stats['Business Days']

    # 月份名稱
    month_names = {9: '9月', 10: '10月', 11: '11月'}
    monthly_stats['Month Name'] = monthly_stats['Month'].map(month_names)

    return monthly_stats

# ============================================================
# 損益平衡計算
# ============================================================
def calculate_break_even(days_per_week, food_cost_rate, daily_labor_cost=None):
    """
    計算損益平衡點

    公式：
    損益平衡營收 = (固定成本 + 人力成本) / (1 - 食材成本率)

    參數：
    - days_per_week: 每週營業天數
    - food_cost_rate: 食材成本率（0.30, 0.35, 0.40）
    - daily_labor_cost: 每日人力成本（預設 $160）
    """
    if daily_labor_cost is None:
        daily_labor_cost = DAILY_LABOR_COST

    monthly_days = days_per_week * 4.33  # 每月約 4.33 週
    labor_cost = daily_labor_cost * monthly_days

    contribution_margin = 1 - food_cost_rate
    break_even_revenue = (FIXED_COST_TOTAL + labor_cost) / contribution_margin
    break_even_daily = break_even_revenue / monthly_days

    return {
        'days_per_week': days_per_week,
        'monthly_days': round(monthly_days, 1),
        'daily_labor_cost': daily_labor_cost,
        'labor_cost': round(labor_cost, 2),
        'food_cost_rate': food_cost_rate,
        'break_even_monthly': round(break_even_revenue, 2),
        'break_even_daily': round(break_even_daily, 2),
    }

def calculate_profit_loss(revenue, business_days, food_cost_rate):
    """計算特定月份的損益"""
    food_cost = revenue * food_cost_rate
    labor_cost = business_days * DAILY_LABOR_COST
    total_cost = FIXED_COST_TOTAL + food_cost + labor_cost
    net_profit = revenue - total_cost
    profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0

    return {
        'revenue': revenue,
        'food_cost': round(food_cost, 2),
        'labor_cost': round(labor_cost, 2),
        'fixed_cost': FIXED_COST_TOTAL,
        'total_cost': round(total_cost, 2),
        'net_profit': round(net_profit, 2),
        'profit_margin': round(profit_margin, 1),
    }

# ============================================================
# 視覺化
# ============================================================
def create_break_even_chart(chinese_font_prop, actual_daily_avg=None):
    """創建損益平衡分析圖（改善版，避免重疊）"""
    fig, ax = plt.subplots(figsize=(14, 9))

    days_range = list(range(2, 8))  # 2-7 天
    colors = ['#27ae60', '#3498db', '#e74c3c']  # 30%, 35%, 40%
    labels = ['食材 30%', '食材 35%', '食材 40%']
    markers = ['o', 's', '^']

    # 計算並繪製每條線
    for i, rate in enumerate(FOOD_COST_RATES):
        daily_values = []
        for days in days_range:
            result = calculate_break_even(days, rate)
            daily_values.append(result['break_even_daily'])

        ax.plot(days_range, daily_values, marker=markers[i], linewidth=3,
                markersize=12, color=colors[i], label=labels[i], alpha=0.9)

    # 只在最右邊標註數值（避免重疊）
    for i, rate in enumerate(FOOD_COST_RATES):
        result = calculate_break_even(7, rate)
        y_offset = [-15, 0, 15][i]  # 錯開標籤
        ax.annotate(f'${result["break_even_daily"]:.0f}',
                   xy=(7, result['break_even_daily']),
                   xytext=(15, y_offset), textcoords='offset points',
                   fontsize=11, fontweight='bold', color=colors[i],
                   fontproperties=chinese_font_prop)

    # 標記當前營運天數（4天）
    ax.axvline(x=4, color='#7f8c8d', linestyle='--', linewidth=2, alpha=0.8)
    ax.text(4.15, ax.get_ylim()[0] + 50, '目前\n4天/週',
            fontsize=11, fontproperties=chinese_font_prop, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f1c40f', alpha=0.9))

    # 如果有實際日均，畫一條水平線
    if actual_daily_avg:
        ax.axhline(y=actual_daily_avg, color='#9b59b6', linestyle='-.',
                   linewidth=2, alpha=0.8, label=f'實際日均 ${actual_daily_avg:.0f}')

    ax.set_xlabel('每週營業天數', fontsize=13, fontproperties=chinese_font_prop, fontweight='bold')
    ax.set_ylabel('損益平衡日均營收 ($)', fontsize=13, fontproperties=chinese_font_prop, fontweight='bold')
    ax.set_title('損益平衡分析：不同營業天數 × 食材成本率',
                fontsize=16, fontweight='bold', fontproperties=chinese_font_prop, pad=20)
    ax.set_xticks(days_range)
    ax.set_xticklabels([f'{d}天' for d in days_range], fontproperties=chinese_font_prop, fontsize=11)
    ax.legend(loc='upper right', prop=chinese_font_prop, fontsize=11,
              frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 設定 Y 軸範圍
    ax.set_ylim(300, 1000)

    plt.tight_layout()
    return fig

def create_cost_breakdown_chart(monthly_stats, chinese_font_prop):
    """創建成本結構分解圖（包含人力成本）"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    months = monthly_stats['Month Name'].tolist()
    x = np.arange(len(months))
    width = 0.7

    # 使用 35% 食材成本率計算各項成本
    food_rate = 0.35

    revenues = monthly_stats['Total Revenue'].tolist()
    business_days = monthly_stats['Business Days'].tolist()

    food_costs = [r * food_rate for r in revenues]
    labor_costs = [d * DAILY_LABOR_COST for d in business_days]
    fixed_costs = [FIXED_COST_TOTAL] * len(months)
    profits = [r - f - l - FIXED_COST_TOTAL for r, f, l in zip(revenues, food_costs, labor_costs)]

    # 左圖：堆疊柱狀圖（成本結構）
    ax1 = axes[0]

    # 堆疊各項成本
    bars1 = ax1.bar(x, food_costs, width, label='食材成本 (35%)', color='#e74c3c', alpha=0.85)
    bars2 = ax1.bar(x, labor_costs, width, bottom=food_costs, label='人力成本', color='#3498db', alpha=0.85)
    bars3 = ax1.bar(x, fixed_costs, width, bottom=[f+l for f, l in zip(food_costs, labor_costs)],
                    label='固定成本', color='#9b59b6', alpha=0.85)

    # 營收線
    ax1.plot(x, revenues, marker='D', linewidth=3, markersize=10,
             color='#2ecc71', label='總營收', linestyle='-')

    # 標註營收和利潤
    for i, (rev, profit) in enumerate(zip(revenues, profits)):
        ax1.text(i, rev + 200, f'${rev:,.0f}', ha='center', va='bottom',
                fontsize=11, fontweight='bold', fontproperties=chinese_font_prop)
        color = '#27ae60' if profit > 0 else '#c0392b'
        sign = '+' if profit > 0 else ''
        ax1.text(i, -800, f'{sign}${profit:,.0f}', ha='center', va='top',
                fontsize=12, fontweight='bold', color=color,
                fontproperties=chinese_font_prop,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.9))

    ax1.axhline(y=0, color='black', linewidth=1)
    ax1.set_xlabel('月份', fontsize=12, fontproperties=chinese_font_prop)
    ax1.set_ylabel('金額 ($)', fontsize=12, fontproperties=chinese_font_prop)
    ax1.set_title('成本結構分析（食材 35%）', fontsize=14, fontweight='bold',
                  fontproperties=chinese_font_prop, pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(months, fontproperties=chinese_font_prop, fontsize=12)
    ax1.legend(loc='upper left', prop=chinese_font_prop, fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')

    # 右圖：人力成本佔比分析
    ax2 = axes[1]

    # 計算各成本佔營收比例
    total_costs = [f + l + FIXED_COST_TOTAL for f, l in zip(food_costs, labor_costs)]
    labor_pct = [l / r * 100 for l, r in zip(labor_costs, revenues)]
    food_pct = [f / r * 100 for f, r in zip(food_costs, revenues)]
    fixed_pct = [FIXED_COST_TOTAL / r * 100 for r in revenues]

    bar_width = 0.25
    x2 = np.arange(len(months))

    ax2.bar(x2 - bar_width, food_pct, bar_width, label='食材成本', color='#e74c3c', alpha=0.85)
    ax2.bar(x2, labor_pct, bar_width, label='人力成本', color='#3498db', alpha=0.85)
    ax2.bar(x2 + bar_width, fixed_pct, bar_width, label='固定成本', color='#9b59b6', alpha=0.85)

    # 標註百分比
    for i, (fp, lp, xp) in enumerate(zip(food_pct, labor_pct, fixed_pct)):
        ax2.text(i - bar_width, fp + 1, f'{fp:.0f}%', ha='center', fontsize=10, fontweight='bold')
        ax2.text(i, lp + 1, f'{lp:.0f}%', ha='center', fontsize=10, fontweight='bold')
        ax2.text(i + bar_width, xp + 1, f'{xp:.0f}%', ha='center', fontsize=10, fontweight='bold')

    ax2.set_xlabel('月份', fontsize=12, fontproperties=chinese_font_prop)
    ax2.set_ylabel('佔營收比例 (%)', fontsize=12, fontproperties=chinese_font_prop)
    ax2.set_title('各項成本佔營收比例', fontsize=14, fontweight='bold',
                  fontproperties=chinese_font_prop, pad=15)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(months, fontproperties=chinese_font_prop, fontsize=12)
    ax2.legend(loc='upper right', prop=chinese_font_prop, fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax2.set_ylim(0, 50)

    plt.tight_layout()
    return fig

def create_sensitivity_heatmap(chinese_font_prop):
    """創建敏感度熱力圖"""
    fig, ax = plt.subplots(figsize=(10, 8))

    days_range = list(range(2, 8))
    food_rates = [0.25, 0.30, 0.35, 0.40, 0.45]

    # 建立矩陣
    matrix = []
    for rate in food_rates:
        row = []
        for days in days_range:
            result = calculate_break_even(days, rate)
            row.append(result['break_even_daily'])
        matrix.append(row)

    matrix = np.array(matrix)

    # 繪製熱力圖
    im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto')

    # 設定標籤
    ax.set_xticks(range(len(days_range)))
    ax.set_xticklabels([f'{d}天/週' for d in days_range], fontproperties=chinese_font_prop)
    ax.set_yticks(range(len(food_rates)))
    ax.set_yticklabels([f'{int(r*100)}%' for r in food_rates], fontproperties=chinese_font_prop)

    # 添加數值標註
    for i in range(len(food_rates)):
        for j in range(len(days_range)):
            text = ax.text(j, i, f'${matrix[i, j]:.0f}',
                          ha='center', va='center', color='black', fontsize=10,
                          fontweight='bold')

    ax.set_xlabel('每週營業天數', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_ylabel('食材成本率', fontsize=12, fontproperties=chinese_font_prop)
    ax.set_title('損益平衡日均營收敏感度分析',
                fontsize=14, fontweight='bold', fontproperties=chinese_font_prop, pad=20)

    # 顏色條
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('損益平衡日均 ($)', fontproperties=chinese_font_prop)

    plt.tight_layout()
    return fig

def calculate_break_even_days(food_cost_rate, daily_labor_cost, actual_daily_avg):
    """
    計算達到損益平衡需要的月營業天數

    公式：
    損益平衡月營收 = (固定成本 + 人力成本) / (1 - 食材成本率)
    所需天數 = 損益平衡月營收 / 日均營收
    """
    # 先假設每週 4 天（約 17.3 天/月）來計算人力成本
    # 但我們需要迭代求解，因為天數會影響人力成本
    # 使用二分法求解

    contribution_margin = 1 - food_cost_rate

    # 迭代求解
    for days in range(1, 32):  # 1-31 天
        labor_cost = daily_labor_cost * days
        break_even_monthly = (FIXED_COST_TOTAL + labor_cost) / contribution_margin
        required_days = break_even_monthly / actual_daily_avg

        if days >= required_days:
            return round(required_days, 1)

    return 31  # 如果超過 31 天，返回 31


def calculate_days_for_target_profit(target_profit, food_cost_rate, daily_labor_cost, daily_avg_revenue):
    """
    計算達到目標利潤所需的月營業天數

    公式：Days = (Target Profit + Fixed Costs) / (Daily Revenue × (1 - Food Rate) - Daily Labor)

    推導：
    利潤 = 營收 - 固定成本 - 人力成本 - 食材成本
         = R × D - F - L × D - R × D × C
         = D × [R × (1 - C) - L] - F
    ∴ D = (利潤 + F) / [R × (1 - C) - L]

    參數：
    - target_profit: 目標月利潤（如 $5,000）
    - food_cost_rate: 食材成本率（0.30, 0.35, 0.40）
    - daily_labor_cost: 每日人力成本（$100, $160, $200, $250）
    - daily_avg_revenue: 日均營收（$640, $753, $820）

    返回：
    - 所需天數（float），如果無法達成返回 float('inf')
    """
    # 計算日淨貢獻 = 日均營收 × (1 - 食材成本率) - 日人力成本
    daily_contribution = daily_avg_revenue * (1 - food_cost_rate) - daily_labor_cost

    if daily_contribution <= 0:
        return float('inf')  # 無法達成（日淨貢獻為負或零）

    # 所需天數 = (目標利潤 + 固定成本) / 日淨貢獻
    required_days = (target_profit + FIXED_COST_TOTAL) / daily_contribution
    return round(required_days, 1)

def create_3d_sensitivity_heatmap(chinese_font_prop, actual_daily_avg=None):
    """
    創建三維敏感度熱力圖（2×2 子圖）

    三個維度：
    - X 軸：食材成本率 (30%, 35%, 40%)
    - Y 軸：每週營業天數 (2-7 天)
    - 子圖：人力成本 ($100, $160, $200, $250)
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    axes = axes.flatten()  # 展平為 1D 陣列

    days_range = list(range(2, 8))  # 2-7 天/週
    food_rates = FOOD_COST_RATES    # 30%, 35%, 40%

    # 找出整體的最小/最大值用於統一色階
    all_values = []
    for labor_cost in DAILY_LABOR_COSTS:
        for days in days_range:
            for rate in food_rates:
                result = calculate_break_even(days, rate, labor_cost)
                all_values.append(result['break_even_daily'])

    vmin = min(all_values)
    vmax = max(all_values)

    for idx, labor_cost in enumerate(DAILY_LABOR_COSTS):
        ax = axes[idx]

        # 建立矩陣（Y=營業天數, X=食材成本率）
        matrix = []
        for days in days_range:
            row = []
            for rate in food_rates:
                result = calculate_break_even(days, rate, labor_cost)
                row.append(result['break_even_daily'])
            matrix.append(row)

        matrix = np.array(matrix)

        # 繪製熱力圖
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', vmin=vmin, vmax=vmax)

        # 設定標籤
        ax.set_xticks(range(len(food_rates)))
        ax.set_xticklabels([f'{int(r*100)}%' for r in food_rates],
                          fontproperties=chinese_font_prop, fontsize=11)
        ax.set_yticks(range(len(days_range)))
        ax.set_yticklabels([f'{d}天' for d in days_range],
                          fontproperties=chinese_font_prop, fontsize=11)

        # 添加數值標註（含盈虧標記）
        for i in range(len(days_range)):
            for j in range(len(food_rates)):
                value = matrix[i, j]
                # 判斷是否達到損益平衡（使用文字符號避免字體問題）
                if actual_daily_avg:
                    if actual_daily_avg >= value:
                        marker = "[OK]"
                        text_color = 'darkgreen'
                    else:
                        marker = "[X]"
                        text_color = 'darkred'
                    text = f'${value:.0f}\n{marker}'
                else:
                    text = f'${value:.0f}'
                    text_color = 'black'

                # 根據背景色調整文字顏色
                bg_intensity = (value - vmin) / (vmax - vmin) if vmax != vmin else 0.5
                if 0.3 < bg_intensity < 0.7:
                    text_color = 'black'

                ax.text(j, i, text, ha='center', va='center',
                       fontsize=10, fontweight='bold',
                       fontproperties=chinese_font_prop)

        ax.set_xlabel('食材成本率', fontsize=12, fontproperties=chinese_font_prop, fontweight='bold')
        if idx == 0 or idx == 2:
            ax.set_ylabel('每週營業天數', fontsize=12, fontproperties=chinese_font_prop, fontweight='bold')

        ax.set_title(f'人力 ${labor_cost}/天', fontsize=14, fontweight='bold',
                    fontproperties=chinese_font_prop, pad=10)

    # 整體標題
    fig.suptitle('損益平衡日均營收 - 三維敏感度分析矩陣（含 $100/天）',
                fontsize=16, fontweight='bold', fontproperties=chinese_font_prop, y=0.98)

    # 添加共用顏色條（調整位置適應 2×2 佈局）
    cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('損益平衡日均 ($)', fontproperties=chinese_font_prop, fontsize=11)

    # 添加實際日均參考線說明
    if actual_daily_avg:
        fig.text(0.5, 0.02,
                f'[OK] = 日均 ${actual_daily_avg:.0f} 可達損益平衡 | [X] = 需提高營收',
                ha='center', fontsize=12, fontproperties=chinese_font_prop,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', alpha=0.9))

    plt.tight_layout(rect=[0, 0.05, 0.92, 0.96])
    return fig

def create_break_even_days_heatmap(chinese_font_prop, monthly_stats):
    """
    創建「每月需營業幾天才打平」熱力圖（4×3 子圖）

    三種日營收情境 × 四種人力成本：
    - 淡季：11月日均 $640
    - 平均：Q4 平均 $753
    - 旺季：9月日均 $820
    """
    # 從 monthly_stats 提取三種日營收情境
    daily_revenues = {
        '淡季 $640': monthly_stats[monthly_stats['Month'] == 11]['Daily Avg Revenue'].values[0],
        '平均 $753': monthly_stats['Daily Avg Revenue'].mean(),
        '旺季 $820': monthly_stats[monthly_stats['Month'] == 9]['Daily Avg Revenue'].values[0],
    }

    fig, axes = plt.subplots(4, 3, figsize=(18, 20))

    food_rates = FOOD_COST_RATES  # 30%, 35%, 40%

    # 計算所有天數用於統一色階
    all_days = []
    for labor_cost in DAILY_LABOR_COSTS:
        for scenario, daily_avg in daily_revenues.items():
            for rate in food_rates:
                days = calculate_break_even_days(rate, labor_cost, daily_avg)
                all_days.append(days)

    vmax = min(max(all_days), 31)  # 限制最大為 31 天

    for row, labor_cost in enumerate(DAILY_LABOR_COSTS):
        for col, (scenario, daily_avg) in enumerate(daily_revenues.items()):
            ax = axes[row, col]

            # 計算各食材成本率下的損益平衡天數
            days_values = []
            for rate in food_rates:
                days = calculate_break_even_days(rate, labor_cost, daily_avg)
                days_values.append(days)

            # 根據天數設定顏色
            colors = []
            for d in days_values:
                if d <= 15:
                    colors.append('#27ae60')  # 綠色（容易達成）
                elif d <= 20:
                    colors.append('#f39c12')  # 橙色（中等）
                else:
                    colors.append('#e74c3c')  # 紅色（困難）

            x = np.arange(len(food_rates))
            bars = ax.bar(x, days_values, color=colors, edgecolor='black', linewidth=1.5)

            # 標註天數
            for bar, d in zip(bars, days_values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{d:.1f}',
                       ha='center', va='bottom', fontsize=11, fontweight='bold',
                       fontproperties=chinese_font_prop)

            ax.set_xticks(x)
            ax.set_xticklabels([f'{int(r*100)}%' for r in food_rates],
                              fontproperties=chinese_font_prop, fontsize=10)

            # 只在最下面一行顯示 X 軸標籤
            if row == 3:
                ax.set_xlabel('食材成本率', fontsize=10, fontproperties=chinese_font_prop, fontweight='bold')

            # 只在最左邊一列顯示 Y 軸標籤
            if col == 0:
                ax.set_ylabel(f'人力 ${labor_cost}/天', fontsize=11,
                             fontproperties=chinese_font_prop, fontweight='bold')

            # 只在第一行顯示情境標題
            if row == 0:
                ax.set_title(scenario, fontsize=13, fontweight='bold',
                            fontproperties=chinese_font_prop, pad=8)

            ax.set_ylim(0, vmax * 1.15)
            ax.axhline(y=17, color='#3498db', linestyle='--', linewidth=1.5, alpha=0.7)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    # 整體標題
    fig.suptitle('損益平衡所需月營業天數 - 三種日營收情境比較',
                fontsize=18, fontweight='bold', fontproperties=chinese_font_prop, y=0.98)

    # 圖例說明
    fig.text(0.5, 0.01,
            '綠色 ≤15天（容易）| 橙色 16-20天（中等）| 紅色 >20天（困難） | 藍線 = 目前~17天/月',
            ha='center', fontsize=11, fontproperties=chinese_font_prop,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', alpha=0.9))

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    return fig


def create_profit_target_days_chart(chinese_font_prop, monthly_stats, target_profit=5000):
    """
    創建「達到目標利潤所需營業天數」圖表（4×3 子圖）

    橫軸（3 列）：淡季 $640、平均 $753、旺季 $820
    縱軸（4 行）：人力 $100、$160、$200、$250/天
    每格內：30%、35%、40% 三種食材成本率
    """
    # 從 monthly_stats 提取三種日營收情境
    daily_revenues = {
        '淡季 $640': monthly_stats[monthly_stats['Month'] == 11]['Daily Avg Revenue'].values[0],
        '平均 $753': monthly_stats['Daily Avg Revenue'].mean(),
        '旺季 $820': monthly_stats[monthly_stats['Month'] == 9]['Daily Avg Revenue'].values[0],
    }

    fig, axes = plt.subplots(4, 3, figsize=(18, 20))

    for row, labor_cost in enumerate(DAILY_LABOR_COSTS):
        for col, (scenario, daily_avg) in enumerate(daily_revenues.items()):
            ax = axes[row, col]

            days_values = []
            colors = []

            for rate in FOOD_COST_RATES:
                days = calculate_days_for_target_profit(target_profit, rate, labor_cost, daily_avg)

                # 限制顯示最大 35 天
                display_days = min(days, 35) if days != float('inf') else 35
                days_values.append(display_days)

                # 顏色判斷
                if days <= 20:
                    colors.append('#27ae60')  # 綠色（輕鬆達成）
                elif days <= 25:
                    colors.append('#f39c12')  # 橙色（可行但緊繃）
                elif days <= 31:
                    colors.append('#e74c3c')  # 紅色（勉強可行）
                else:
                    colors.append('#95a5a6')  # 灰色（不可能）

            x = np.arange(len(FOOD_COST_RATES))
            bars = ax.bar(x, days_values, color=colors, edgecolor='black', linewidth=1.5)

            # 標註天數
            for bar, d, rate in zip(bars, days_values, FOOD_COST_RATES):
                original_days = calculate_days_for_target_profit(target_profit, rate, labor_cost, daily_avg)
                if original_days <= 31:
                    label = f'{original_days:.1f}'
                else:
                    label = '∞'
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                       label, ha='center', va='bottom', fontsize=11, fontweight='bold',
                       fontproperties=chinese_font_prop)

            ax.set_xticks(x)
            ax.set_xticklabels([f'{int(r*100)}%' for r in FOOD_COST_RATES],
                              fontproperties=chinese_font_prop, fontsize=10)

            # 只在最下面一行顯示 X 軸標籤
            if row == 3:
                ax.set_xlabel('食材成本率', fontsize=10, fontproperties=chinese_font_prop, fontweight='bold')

            # 只在最左邊一列顯示 Y 軸標籤
            if col == 0:
                ax.set_ylabel(f'人力 ${labor_cost}/天', fontsize=11,
                             fontproperties=chinese_font_prop, fontweight='bold')

            # 只在第一行顯示情境標題
            if row == 0:
                ax.set_title(scenario, fontsize=13, fontweight='bold',
                            fontproperties=chinese_font_prop, pad=8)

            ax.set_ylim(0, 38)
            # 參考線：31 天（一個月最大）
            ax.axhline(y=31, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    # 整體標題
    fig.suptitle(f'每月賺 ${target_profit:,} 所需營業天數（36 種情境分析）',
                fontsize=18, fontweight='bold', fontproperties=chinese_font_prop, y=0.98)

    # 圖例說明（使用文字符號避免 emoji 字體問題）
    fig.text(0.5, 0.01,
            '[綠] ≤20天（輕鬆）| [橙] 21-25天（緊繃）| [紅] 26-31天（勉強）| [灰] >31天（不可能） | 紅線 = 31天上限',
            ha='center', fontsize=11, fontproperties=chinese_font_prop,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', alpha=0.9))

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    return fig


def create_labor_sensitivity_table(actual_daily_avg, chinese_font_prop):
    """
    創建人力成本敏感度比較表（橫向比較）
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')

    # 建立表格數據
    headers = ['營業天數', '食材成本']
    for labor in DAILY_LABOR_COSTS:
        headers.append(f'人力${labor}/天')

    table_data = []

    for days in range(2, 8):
        for rate in FOOD_COST_RATES:
            row = [f'{days}天/週', f'{int(rate*100)}%']
            for labor in DAILY_LABOR_COSTS:
                result = calculate_break_even(days, rate, labor)
                be = result['break_even_daily']
                if actual_daily_avg >= be:
                    cell = f'${be:.0f} [OK]'
                else:
                    cell = f'${be:.0f} [X]'
                row.append(cell)
            table_data.append(row)

    # 創建表格
    table = ax.table(cellText=table_data, colLabels=headers,
                     loc='center', cellLoc='center')

    # 設定表格樣式
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    # 表頭樣式
    for i, key in enumerate(headers):
        cell = table[(0, i)]
        cell.set_facecolor('#3498db')
        cell.set_text_props(color='white', fontweight='bold')

    # 設定單元格顏色
    for i, row in enumerate(table_data):
        for j in range(len(row)):
            cell = table[(i + 1, j)]
            if '[OK]' in str(row[j]):
                cell.set_facecolor('#d5f5e3')  # 淺綠
            elif '[X]' in str(row[j]):
                cell.set_facecolor('#fadbd8')  # 淺紅

    ax.set_title(f'損益平衡日均營收比較表（目前日均: ${actual_daily_avg:.0f}）',
                fontsize=14, fontweight='bold', fontproperties=chinese_font_prop, pad=20)

    plt.tight_layout()
    return fig

def create_monthly_pnl_chart(monthly_stats, chinese_font_prop):
    """創建月度損益圖（三種食材成本率）"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))

    months = monthly_stats['Month Name'].tolist()
    x = np.arange(len(months))
    width = 0.6

    for idx, rate in enumerate(FOOD_COST_RATES):
        ax = axes[idx]

        profits = []
        for _, row in monthly_stats.iterrows():
            pnl = calculate_profit_loss(row['Total Revenue'], row['Business Days'], rate)
            profits.append(pnl['net_profit'])

        colors = ['#2ecc71' if p > 0 else '#e74c3c' for p in profits]
        bars = ax.bar(x, profits, width, color=colors, edgecolor='white', linewidth=1.5)

        # 標註數值
        for i, (bar, profit) in enumerate(zip(bars, profits)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${profit:,.0f}',
                   ha='center', va='bottom' if profit > 0 else 'top',
                   fontsize=11, fontweight='bold',
                   fontproperties=chinese_font_prop)

        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.set_xticks(x)
        ax.set_xticklabels(months, fontproperties=chinese_font_prop)
        ax.set_ylabel('淨利潤 ($)', fontsize=11, fontproperties=chinese_font_prop)
        ax.set_title(f'食材成本 {int(rate*100)}%', fontsize=12, fontweight='bold',
                    fontproperties=chinese_font_prop)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    fig.suptitle('各月淨利潤分析（三種食材成本率情境）',
                fontsize=14, fontweight='bold', fontproperties=chinese_font_prop, y=1.02)

    plt.tight_layout()
    return fig

# ============================================================
# 報告生成
# ============================================================
def generate_report(monthly_stats, target_profit=5000):
    """生成 Markdown 報告（含目標利潤分析）"""
    report = []
    report.append("# Taiwanway Q4 2025 損益平衡分析報告\n")
    report.append(f"**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 成本參數
    report.append("\n## 一、成本參數\n")
    report.append("| 項目 | 金額 |")
    report.append("|------|------|")
    report.append(f"| 房租 | ${FIXED_COSTS['rent']:,}/月 |")
    report.append(f"| 水電 | ${FIXED_COSTS['utilities']:,}/月 |")
    report.append(f"| **固定成本合計** | **${FIXED_COST_TOTAL:,}/月** |")
    report.append(f"| 員工費用 | ${DAILY_LABOR_COST}/天 |")
    report.append(f"| 食材成本率 | 30% / 35% / 40% |")

    # 實際營收數據
    report.append("\n## 二、實際營收數據（2025 Q4）\n")
    report.append("| 月份 | 營業天數 | 總營收 | 日均營收 |")
    report.append("|------|---------|--------|---------|")

    for _, row in monthly_stats.iterrows():
        report.append(f"| {row['Month Name']} | {row['Business Days']} 天 | ${row['Total Revenue']:,.2f} | ${row['Daily Avg Revenue']:,.2f} |")

    # 計算總計
    total_revenue = monthly_stats['Total Revenue'].sum()
    total_days = monthly_stats['Business Days'].sum()
    avg_daily = total_revenue / total_days
    report.append(f"| **合計** | **{total_days} 天** | **${total_revenue:,.2f}** | **${avg_daily:,.2f}** |")

    # 損益分析
    report.append("\n## 三、損益分析\n")

    for rate in FOOD_COST_RATES:
        report.append(f"\n### 食材成本 {int(rate*100)}% 情境\n")
        report.append("| 月份 | 營收 | 食材成本 | 人力成本 | 固定成本 | 總成本 | 淨利潤 | 利潤率 |")
        report.append("|------|------|---------|---------|---------|--------|--------|-------|")

        total_profit = 0
        for _, row in monthly_stats.iterrows():
            pnl = calculate_profit_loss(row['Total Revenue'], row['Business Days'], rate)
            total_profit += pnl['net_profit']
            profit_indicator = "✅" if pnl['net_profit'] > 0 else "❌"
            report.append(f"| {row['Month Name']} | ${pnl['revenue']:,.0f} | ${pnl['food_cost']:,.0f} | ${pnl['labor_cost']:,.0f} | ${pnl['fixed_cost']:,} | ${pnl['total_cost']:,.0f} | ${pnl['net_profit']:,.0f} {profit_indicator} | {pnl['profit_margin']:.1f}% |")

        report.append(f"\n**三個月累計淨利潤**: ${total_profit:,.0f}")

    # 損益平衡分析
    report.append("\n## 四、損益平衡分析\n")
    report.append(f"\n**目前日均營收**: ${avg_daily:,.2f}\n")
    report.append("\n### 每週 4 天營業的損益平衡日均\n")
    report.append("| 食材成本率 | 損益平衡日均 | 目前狀態 |")
    report.append("|-----------|-------------|---------|")

    for rate in FOOD_COST_RATES:
        result = calculate_break_even(4, rate)
        status = "✅ 達標" if avg_daily >= result['break_even_daily'] else f"❌ 差距 ${result['break_even_daily'] - avg_daily:.0f}"
        report.append(f"| {int(rate*100)}% | ${result['break_even_daily']:.0f} | {status} |")

    # 不同營業天數的損益平衡
    report.append("\n### 不同營業天數的損益平衡日均（35% 食材成本）\n")
    report.append("| 每週天數 | 月營業天 | 損益平衡日均 | 以目前日均的盈虧 |")
    report.append("|---------|---------|-------------|-----------------|")

    for days in range(2, 8):
        result = calculate_break_even(days, 0.35)
        monthly_days = result['monthly_days']
        monthly_revenue = avg_daily * monthly_days
        pnl = calculate_profit_loss(monthly_revenue, monthly_days, 0.35)
        status = f"✅ +${pnl['net_profit']:,.0f}" if pnl['net_profit'] > 0 else f"❌ ${pnl['net_profit']:,.0f}"
        report.append(f"| {days} 天 | {monthly_days:.1f} 天 | ${result['break_even_daily']:.0f} | {status} |")

    # 結論與建議
    report.append("\n## 五、結論與建議\n")

    # 根據數據生成結論
    be_35 = calculate_break_even(4, 0.35)['break_even_daily']

    if avg_daily >= be_35:
        report.append(f"1. **目前營運狀況良好**：日均營收 ${avg_daily:.0f} 高於 35% 食材成本的損益平衡點 ${be_35:.0f}")
    else:
        gap = be_35 - avg_daily
        report.append(f"1. **目前接近損益平衡**：日均營收 ${avg_daily:.0f} 略低於 35% 食材成本的損益平衡點 ${be_35:.0f}（差距 ${gap:.0f}）")

    # 計算最低可行營業天數
    for days in range(2, 8):
        result = calculate_break_even(days, 0.35)
        if avg_daily >= result['break_even_daily']:
            report.append(f"\n2. **最低可行營業天數**：以目前日均營收 ${avg_daily:.0f}，每週營業 **{days} 天** 即可打平（損益平衡日均 ${result['break_even_daily']:.0f}）")
            break

    report.append("\n3. **食材成本敏感度**：")
    report.append(f"   - 若控制在 30%：每週 4 天營業的損益平衡日均降至 ${calculate_break_even(4, 0.30)['break_even_daily']:.0f}")
    report.append(f"   - 若升高至 40%：每週 4 天營業的損益平衡日均升至 ${calculate_break_even(4, 0.40)['break_even_daily']:.0f}")

    # 人力成本敏感度分析（新增）
    report.append("\n## 六、人力成本敏感度分析\n")
    report.append(f"**分析情境**: 人力成本 ${DAILY_LABOR_COSTS[0]}, ${DAILY_LABOR_COSTS[1]}, ${DAILY_LABOR_COSTS[2]}/天\n")

    report.append("\n### 不同人力成本的損益平衡點比較（4天/週, 35%食材成本）\n")
    report.append("| 人力成本 | 月人力成本 | 損益平衡日均 | 目前狀態 |")
    report.append("|---------|-----------|-------------|---------|")

    for labor in DAILY_LABOR_COSTS:
        result = calculate_break_even(4, 0.35, labor)
        monthly_labor = labor * result['monthly_days']
        status = "✅ 達標" if avg_daily >= result['break_even_daily'] else f"❌ 差距 ${result['break_even_daily'] - avg_daily:.0f}"
        report.append(f"| ${labor}/天 | ${monthly_labor:,.0f} | ${result['break_even_daily']:.0f} | {status} |")

    report.append("\n### 三維敏感度矩陣（營業天數 × 食材成本率 × 人力成本）\n")
    report.append("詳見圖表：`sensitivity_3d_heatmap.png`\n")

    # 完整敏感度表格（四種人力成本）
    report.append("\n#### 人力 $100/天\n")
    report.append("| 營業天數 | 30% | 35% | 40% |")
    report.append("|---------|-----|-----|-----|")
    for days in range(2, 8):
        row = f"| {days}天/週 |"
        for rate in FOOD_COST_RATES:
            result = calculate_break_even(days, rate, 100)
            be = result['break_even_daily']
            marker = "✅" if avg_daily >= be else "❌"
            row += f" ${be:.0f} {marker} |"
        report.append(row)

    report.append("\n#### 人力 $160/天\n")
    report.append("| 營業天數 | 30% | 35% | 40% |")
    report.append("|---------|-----|-----|-----|")
    for days in range(2, 8):
        row = f"| {days}天/週 |"
        for rate in FOOD_COST_RATES:
            result = calculate_break_even(days, rate, 160)
            be = result['break_even_daily']
            marker = "✅" if avg_daily >= be else "❌"
            row += f" ${be:.0f} {marker} |"
        report.append(row)

    report.append("\n#### 人力 $200/天\n")
    report.append("| 營業天數 | 30% | 35% | 40% |")
    report.append("|---------|-----|-----|-----|")
    for days in range(2, 8):
        row = f"| {days}天/週 |"
        for rate in FOOD_COST_RATES:
            result = calculate_break_even(days, rate, 200)
            be = result['break_even_daily']
            marker = "✅" if avg_daily >= be else "❌"
            row += f" ${be:.0f} {marker} |"
        report.append(row)

    report.append("\n#### 人力 $250/天\n")
    report.append("| 營業天數 | 30% | 35% | 40% |")
    report.append("|---------|-----|-----|-----|")
    for days in range(2, 8):
        row = f"| {days}天/週 |"
        for rate in FOOD_COST_RATES:
            result = calculate_break_even(days, rate, 250)
            be = result['break_even_daily']
            marker = "✅" if avg_daily >= be else "❌"
            row += f" ${be:.0f} {marker} |"
        report.append(row)

    report.append("\n### 人力成本建議\n")
    report.append(f"1. 以目前日均營收 ${avg_daily:.0f}：")

    # 分析每種人力成本的可行性
    for labor in DAILY_LABOR_COSTS:
        viable_days = []
        for days in range(2, 8):
            result = calculate_break_even(days, 0.35, labor)
            if avg_daily >= result['break_even_daily']:
                viable_days.append(days)
        if viable_days:
            report.append(f"   - 人力 ${labor}/天：每週營業 **{viable_days[0]}-7 天** 皆可獲利")
        else:
            report.append(f"   - 人力 ${labor}/天：**無法達到損益平衡**（需提高日均營收）")

    # ============================================================
    # 七、目標利潤分析
    # ============================================================
    report.append(f"\n## 七、目標利潤分析（每月 ${target_profit:,}）\n")
    report.append(f"**目標月利潤**: ${target_profit:,}\n")
    report.append("### 計算公式\n")
    report.append("```")
    report.append("所需天數 = (目標利潤 + 固定成本) / [日均營收 × (1 - 食材成本率) - 人力成本/天]")
    report.append(f"        = (${target_profit:,} + $3,800) / 日淨貢獻")
    report.append("```\n")

    report.append("### 各情境所需營業天數\n")

    # 三種日營收情境
    daily_revenues = [
        ('淡季', monthly_stats[monthly_stats['Month'] == 11]['Daily Avg Revenue'].values[0]),
        ('平均', avg_daily),
        ('旺季', monthly_stats[monthly_stats['Month'] == 9]['Daily Avg Revenue'].values[0]),
    ]

    for scenario, daily_avg in daily_revenues:
        report.append(f"\n#### {scenario}情境（日均 ${daily_avg:.0f}）\n")
        report.append("| 人力成本 | 30% | 35% | 40% |")
        report.append("|---------|-----|-----|-----|")

        for labor in DAILY_LABOR_COSTS:
            row = f"| ${labor}/天 |"
            for rate in FOOD_COST_RATES:
                days = calculate_days_for_target_profit(target_profit, rate, labor, daily_avg)
                if days <= 20:
                    marker = "🟢"
                elif days <= 25:
                    marker = "🟠"
                elif days <= 31:
                    marker = "🔴"
                else:
                    marker = "❌"

                if days <= 31:
                    row += f" {days:.1f} 天 {marker} |"
                else:
                    row += f" 不可能 {marker} |"
            report.append(row)

    report.append("\n### 圖例說明\n")
    report.append("- 🟢 ≤20 天：輕鬆達成，有安全邊際")
    report.append("- 🟠 21-25 天：可行但緊繃，需嚴格控制成本")
    report.append("- 🔴 26-31 天：勉強可行，幾乎每天都要營業")
    report.append("- ❌ >31 天：不可能，需提高營收或降低成本")

    report.append("\n### 關鍵發現\n")

    # 找出最佳和最差情境
    best_days = float('inf')
    best_scenario = ""
    worst_possible_days = 0
    worst_scenario = ""

    for scenario, daily_avg in daily_revenues:
        for labor in DAILY_LABOR_COSTS:
            for rate in FOOD_COST_RATES:
                days = calculate_days_for_target_profit(target_profit, rate, labor, daily_avg)
                if days < best_days:
                    best_days = days
                    best_scenario = f"{scenario} ${daily_avg:.0f} + 人力 ${labor} + 食材 {int(rate*100)}%"
                if days <= 31 and days > worst_possible_days:
                    worst_possible_days = days
                    worst_scenario = f"{scenario} ${daily_avg:.0f} + 人力 ${labor} + 食材 {int(rate*100)}%"

    report.append(f"1. **最佳情境**：{best_scenario} → **{best_days:.1f} 天**")
    if worst_possible_days > 0:
        report.append(f"2. **最困難可行情境**：{worst_scenario} → **{worst_possible_days:.1f} 天**")

    # 計算以 Q4 平均表現的建議
    report.append(f"\n3. **以 Q4 平均日均 ${avg_daily:.0f} 的建議**：")
    for labor in DAILY_LABOR_COSTS:
        days_35 = calculate_days_for_target_profit(target_profit, 0.35, labor, avg_daily)
        if days_35 <= 31:
            report.append(f"   - 人力 ${labor}/天 + 食材 35%：需 **{days_35:.1f} 天**")
        else:
            report.append(f"   - 人力 ${labor}/天 + 食材 35%：**不可行**")

    report.append("\n### 詳細圖表\n")
    report.append("詳見：`profit_target_days.png`")

    return "\n".join(report)

# ============================================================
# 主程序
# ============================================================
def main():
    print("=" * 60)
    print("Taiwanway Q4 2025 損益平衡分析")
    print("=" * 60)

    # 建立輸出目錄
    (OUTPUT_DIR / 'data').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'charts').mkdir(parents=True, exist_ok=True)

    # 設定字體
    chinese_font_prop = setup_chinese_font()

    # 載入數據
    df = load_and_process_data()

    # 計算月度統計
    monthly_stats = calculate_monthly_stats(df)
    print("\n月度統計:")
    print(monthly_stats.to_string(index=False))

    # 計算總計
    total_revenue = monthly_stats['Total Revenue'].sum()
    total_days = monthly_stats['Business Days'].sum()
    avg_daily = total_revenue / total_days
    print(f"\n三個月合計: ${total_revenue:,.2f} / {total_days} 天 = 日均 ${avg_daily:,.2f}")

    # 損益平衡分析
    print("\n" + "=" * 60)
    print("損益平衡分析（每週 4 天營業）")
    print("=" * 60)

    for rate in FOOD_COST_RATES:
        result = calculate_break_even(4, rate)
        status = "✅" if avg_daily >= result['break_even_daily'] else "❌"
        print(f"食材成本 {int(rate*100)}%: 損益平衡日均 ${result['break_even_daily']:.0f} {status}")

    # 各月損益分析
    print("\n" + "=" * 60)
    print("各月損益分析（35% 食材成本）")
    print("=" * 60)

    for _, row in monthly_stats.iterrows():
        pnl = calculate_profit_loss(row['Total Revenue'], row['Business Days'], 0.35)
        status = "✅ 獲利" if pnl['net_profit'] > 0 else "❌ 虧損"
        print(f"{row['Month Name']}: 營收 ${pnl['revenue']:,.0f} - 成本 ${pnl['total_cost']:,.0f} = 淨利 ${pnl['net_profit']:,.0f} {status}")

    # 儲存數據
    monthly_stats.to_csv(OUTPUT_DIR / 'data' / 'monthly_stats.csv', index=False, encoding='utf-8-sig')
    print(f"\n✓ 儲存: monthly_stats.csv")

    # 生成圖表
    print("\n生成視覺化圖表...")

    fig1 = create_break_even_chart(chinese_font_prop, actual_daily_avg=avg_daily)
    fig1.savefig(OUTPUT_DIR / 'charts' / 'break_even_analysis.png', dpi=300, bbox_inches='tight')
    plt.close(fig1)
    print("✓ 儲存: break_even_analysis.png")

    fig2 = create_cost_breakdown_chart(monthly_stats, chinese_font_prop)
    fig2.savefig(OUTPUT_DIR / 'charts' / 'cost_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close(fig2)
    print("✓ 儲存: cost_breakdown.png")

    fig3 = create_sensitivity_heatmap(chinese_font_prop)
    fig3.savefig(OUTPUT_DIR / 'charts' / 'sensitivity_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close(fig3)
    print("✓ 儲存: sensitivity_heatmap.png")

    fig4 = create_monthly_pnl_chart(monthly_stats, chinese_font_prop)
    fig4.savefig(OUTPUT_DIR / 'charts' / 'monthly_pnl_comparison.png', dpi=300, bbox_inches='tight')
    plt.close(fig4)
    print("✓ 儲存: monthly_pnl_comparison.png")

    # 新增：三維敏感度熱力圖（人力成本 $160, $200, $250）
    fig5 = create_3d_sensitivity_heatmap(chinese_font_prop, actual_daily_avg=avg_daily)
    fig5.savefig(OUTPUT_DIR / 'charts' / 'sensitivity_3d_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close(fig5)
    print("✓ 儲存: sensitivity_3d_heatmap.png")

    # 新增：人力成本敏感度比較表
    fig6 = create_labor_sensitivity_table(avg_daily, chinese_font_prop)
    fig6.savefig(OUTPUT_DIR / 'charts' / 'labor_sensitivity_table.png', dpi=300, bbox_inches='tight')
    plt.close(fig6)
    print("✓ 儲存: labor_sensitivity_table.png")

    # 新增：損益平衡所需營業天數圖（三種日營收情境）
    fig7 = create_break_even_days_heatmap(chinese_font_prop, monthly_stats)
    fig7.savefig(OUTPUT_DIR / 'charts' / 'break_even_days.png', dpi=300, bbox_inches='tight')
    plt.close(fig7)
    print("✓ 儲存: break_even_days.png")

    # 新增：目標利潤所需營業天數圖（每月 $5,000）
    TARGET_PROFIT = 5000
    fig8 = create_profit_target_days_chart(chinese_font_prop, monthly_stats, TARGET_PROFIT)
    fig8.savefig(OUTPUT_DIR / 'charts' / 'profit_target_days.png', dpi=300, bbox_inches='tight')
    plt.close(fig8)
    print("✓ 儲存: profit_target_days.png")

    # 目標利潤分析輸出
    print("\n" + "=" * 60)
    print(f"目標利潤分析（每月賺 ${TARGET_PROFIT:,}）")
    print("=" * 60)
    print(f"公式：天數 = (${TARGET_PROFIT:,} + $3,800) / 日淨貢獻")
    print(f"      日淨貢獻 = 日均營收 × (1 - 食材率) - 人力/天\n")

    # 以 Q4 平均日均計算
    for labor in DAILY_LABOR_COSTS:
        days = calculate_days_for_target_profit(TARGET_PROFIT, 0.35, labor, avg_daily)
        if days <= 31:
            status = "🟢" if days <= 20 else ("🟠" if days <= 25 else "🔴")
            print(f"人力 ${labor}/天 + 食材 35%: {days:.1f} 天 {status}")
        else:
            print(f"人力 ${labor}/天 + 食材 35%: 不可能 ❌")

    # 生成報告（含目標利潤分析）
    report = generate_report(monthly_stats, TARGET_PROFIT)
    report_path = OUTPUT_DIR / 'break_even_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ 儲存: break_even_report.md")

    print("\n" + "=" * 60)
    print("分析完成！")
    print(f"輸出目錄: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
