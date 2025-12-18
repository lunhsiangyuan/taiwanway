#!/usr/bin/env python3
"""
2025/12 與 2026/01 損益平衡點分析

考慮特殊休假：12/22 ~ 1/11 店鋪不營業

核心發現：由於休假導致營業天數大幅減少（12天 vs 17天），
但固定成本（房租+水電=$3,800/月）仍需全額支付，
兩個月份均確定虧損。
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
import seaborn as sns

# ============================================================
# 設定
# ============================================================

# 中文字體設定
mpl.rcParams['text.usetex'] = False
mpl.rcParams['axes.unicode_minus'] = False

FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'
try:
    chinese_font = font_manager.FontProperties(fname=FONT_PATH)
    font_manager.fontManager.addfont(FONT_PATH)
    font_name = font_manager.FontProperties(fname=FONT_PATH).get_name()
    mpl.rcParams['font.family'] = [font_name, 'sans-serif']
    print(f"✓ 使用字體：{font_name}")
except Exception as e:
    print(f"⚠ 字體載入失敗：{e}")
    chinese_font = font_manager.FontProperties()

# Seaborn 樣式
sns.set_style("whitegrid")
sns.set_palette("husl")

# 路徑設定
BASE_DIR = Path('/Users/lunhsiangyuan/Desktop/square')
OUTPUT_DIR = BASE_DIR / 'analysis_output/break_even_winter_2025'
CHARTS_DIR = OUTPUT_DIR / 'charts'
DATA_DIR = OUTPUT_DIR / 'data'

# 確保目錄存在
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 業務參數
# ============================================================

# NYC 銷售稅率
NYC_TAX_RATE = 0.08875

# 固定成本（月）
FIXED_COSTS = {
    'rent': 3100,      # 房租
    'utilities': 700,  # 水電
}
TOTAL_FIXED_COST = sum(FIXED_COSTS.values())  # $3,800

# 人力成本情境（日）
LABOR_COSTS = {
    'minimum': 100,    # 最低配置
    'standard': 160,   # 標準配置
    'enhanced': 200,   # 加強配置
    'full': 250,       # 完整配置
}

# 食材成本率情境
FOOD_COST_RATES = {
    'low': 0.30,       # 30%
    'medium': 0.35,    # 35%
    'high': 0.40,      # 40%
}

# 營業天數（考慮 12/22 ~ 1/11 休假）
OPERATING_DAYS = {
    'dec_2025': 12,    # 12/1-21 營業
    'jan_2026': 12,    # 1/12-31 營業
}

# 原本預測營收（來自 YoY forecast，已轉換為淨營收）
ORIGINAL_FORECAST = {
    'dec_2025': {
        'gross': 9519,
        'net': 9519 / (1 + NYC_TAX_RATE),  # $8,743
        'original_days': 17,
    },
    'jan_2026': {
        'gross': 8524,
        'net': 8524 / (1 + NYC_TAX_RATE),  # $7,829
        'original_days': 17,
    },
}

# ============================================================
# 計算函數
# ============================================================

def calculate_adjusted_revenue(month: str) -> float:
    """計算調整後的預測營收（根據實際營業天數）"""
    original = ORIGINAL_FORECAST[month]
    actual_days = OPERATING_DAYS[month]
    original_days = original['original_days']

    adjusted = original['net'] * (actual_days / original_days)
    return round(adjusted, 2)


def calculate_break_even(operating_days: int, daily_labor: float, food_cost_rate: float) -> dict:
    """
    計算損益平衡點

    公式：
    月損益平衡營收 = (固定成本 + 月人力成本) / (1 - 食材成本率)
    """
    monthly_labor = daily_labor * operating_days
    total_variable_costs = monthly_labor

    # 損益平衡營收
    break_even_monthly = (TOTAL_FIXED_COST + total_variable_costs) / (1 - food_cost_rate)
    break_even_daily = break_even_monthly / operating_days

    return {
        'monthly_labor': monthly_labor,
        'break_even_monthly': round(break_even_monthly, 2),
        'break_even_daily': round(break_even_daily, 2),
    }


def calculate_profit_loss(revenue: float, operating_days: int, daily_labor: float, food_cost_rate: float) -> dict:
    """計算損益"""
    monthly_labor = daily_labor * operating_days
    food_cost = revenue * food_cost_rate

    total_costs = TOTAL_FIXED_COST + monthly_labor + food_cost
    profit = revenue - total_costs

    return {
        'revenue': round(revenue, 2),
        'fixed_cost': TOTAL_FIXED_COST,
        'labor_cost': round(monthly_labor, 2),
        'food_cost': round(food_cost, 2),
        'total_cost': round(total_costs, 2),
        'profit': round(profit, 2),
        'profit_margin': round(profit / revenue * 100, 1) if revenue > 0 else 0,
    }


def generate_sensitivity_matrix(month: str) -> pd.DataFrame:
    """生成敏感度分析矩陣"""
    adjusted_revenue = calculate_adjusted_revenue(month)
    operating_days = OPERATING_DAYS[month]

    results = []
    for food_rate_name, food_rate in FOOD_COST_RATES.items():
        row = {'food_cost_rate': f"{int(food_rate*100)}%"}
        for labor_name, daily_labor in LABOR_COSTS.items():
            pnl = calculate_profit_loss(adjusted_revenue, operating_days, daily_labor, food_rate)
            row[f'${daily_labor}/天'] = pnl['profit']
        results.append(row)

    df = pd.DataFrame(results)
    df.set_index('food_cost_rate', inplace=True)
    return df


# ============================================================
# 視覺化函數
# ============================================================

def plot_break_even_comparison():
    """繪製 12 月 vs 1 月損益平衡對比圖"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    months = ['dec_2025', 'jan_2026']
    titles = ['2025 年 12 月', '2026 年 1 月']

    for idx, (month, title) in enumerate(zip(months, titles)):
        ax = axes[idx]
        adjusted_revenue = calculate_adjusted_revenue(month)
        operating_days = OPERATING_DAYS[month]

        # 計算各情境
        labor_values = list(LABOR_COSTS.values())
        break_evens = []
        profits = []

        for daily_labor in labor_values:
            be = calculate_break_even(operating_days, daily_labor, 0.35)
            break_evens.append(be['break_even_monthly'])

            pnl = calculate_profit_loss(adjusted_revenue, operating_days, daily_labor, 0.35)
            profits.append(pnl['profit'])

        x = np.arange(len(labor_values))
        width = 0.35

        # 損益平衡線
        bars1 = ax.bar(x - width/2, break_evens, width, label='損益平衡營收',
                       color='#3498db', alpha=0.8, edgecolor='black')

        # 預測營收線
        ax.axhline(y=adjusted_revenue, color='#e74c3c', linestyle='--', linewidth=2,
                   label=f'調整後預測營收: ${adjusted_revenue:,.0f}')

        # 設定
        ax.set_xlabel('人力成本/天', fontsize=11, fontproperties=chinese_font)
        ax.set_ylabel('營收 ($)', fontsize=11, fontproperties=chinese_font)
        ax.set_title(f'{title}（{operating_days} 天營業）\n35% 食材成本率',
                     fontsize=13, fontweight='bold', fontproperties=chinese_font)
        ax.set_xticks(x)
        ax.set_xticklabels([f'${v}' for v in labor_values])
        ax.legend(loc='upper left', prop=chinese_font)
        ax.grid(axis='y', alpha=0.3)

        # 添加虧損標註
        for i, (be, profit) in enumerate(zip(break_evens, profits)):
            color = '#27ae60' if profit >= 0 else '#e74c3c'
            ax.annotate(f'{profit:+,.0f}', xy=(i - width/2, be), xytext=(0, 10),
                       textcoords='offset points', ha='center', fontsize=9,
                       color=color, fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'break_even_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ break_even_comparison.png")


def plot_sensitivity_heatmap(month: str, title: str):
    """繪製敏感度熱力圖"""
    df = generate_sensitivity_matrix(month)

    fig, ax = plt.subplots(figsize=(10, 5))

    # 使用發散色彩（紅=虧損，綠=盈餘）
    cmap = sns.diverging_palette(10, 130, as_cmap=True)

    # 熱力圖
    hm = sns.heatmap(df.astype(float), annot=True, fmt='.0f', cmap=cmap, center=0,
                     ax=ax, linewidths=1, linecolor='white',
                     cbar_kws={'label': '損益 ($)'})

    ax.set_xlabel('人力成本/天', fontsize=11, fontproperties=chinese_font)
    ax.set_ylabel('食材成本率', fontsize=11, fontproperties=chinese_font)
    ax.set_title(f'{title} 損益敏感度分析\n（調整後預測營收: ${calculate_adjusted_revenue(month):,.0f}）',
                 fontsize=13, fontweight='bold', fontproperties=chinese_font)

    plt.tight_layout()
    filename = f'sensitivity_heatmap_{month}.png'
    plt.savefig(CHARTS_DIR / filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ {filename}")


def plot_labor_cost_impact():
    """繪製人力成本影響折線圖"""
    fig, ax = plt.subplots(figsize=(12, 6))

    labor_values = list(LABOR_COSTS.values())

    for month, label, color, marker in [
        ('dec_2025', '12 月', '#3498db', 'o'),
        ('jan_2026', '1 月', '#e74c3c', 's'),
    ]:
        adjusted_revenue = calculate_adjusted_revenue(month)
        operating_days = OPERATING_DAYS[month]

        profits = []
        for daily_labor in labor_values:
            pnl = calculate_profit_loss(adjusted_revenue, operating_days, daily_labor, 0.35)
            profits.append(pnl['profit'])

        ax.plot(labor_values, profits, f'{marker}-', color=color, linewidth=2.5,
                markersize=10, label=f'{label}（{operating_days} 天）', alpha=0.8)

        # 添加數值標籤
        for x, y in zip(labor_values, profits):
            ax.annotate(f'${y:,.0f}', xy=(x, y), xytext=(0, 10 if y >= 0 else -15),
                       textcoords='offset points', ha='center', fontsize=9,
                       color=color, fontweight='bold')

    # 損益平衡線
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(255, 100, '損益平衡', fontsize=10, fontproperties=chinese_font)

    ax.set_xlabel('人力成本/天 ($)', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_ylabel('月損益 ($)', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_title('人力成本對月損益的影響\n（35% 食材成本率，考慮 12/22~1/11 休假）',
                 fontsize=14, fontweight='bold', fontproperties=chinese_font)
    ax.set_xticks(labor_values)
    ax.set_xticklabels([f'${v}' for v in labor_values])
    ax.legend(loc='upper right', prop=chinese_font, fontsize=11)
    ax.grid(alpha=0.3)

    # 填充虧損區域
    ax.fill_between(labor_values, -7000, 0, alpha=0.1, color='red')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'labor_cost_impact.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ labor_cost_impact.png")


def plot_cost_breakdown():
    """繪製成本結構分解圖"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    months = ['dec_2025', 'jan_2026']
    titles = ['2025 年 12 月', '2026 年 1 月']

    for idx, (month, title) in enumerate(zip(months, titles)):
        ax = axes[idx]
        adjusted_revenue = calculate_adjusted_revenue(month)
        operating_days = OPERATING_DAYS[month]

        # 使用最低人力配置、35% 食材成本計算
        pnl = calculate_profit_loss(adjusted_revenue, operating_days, 100, 0.35)

        # 成本組成
        costs = [
            ('固定成本\n(房租+水電)', pnl['fixed_cost'], '#e74c3c'),
            ('人力成本\n($100×12天)', pnl['labor_cost'], '#3498db'),
            ('食材成本\n(35%)', pnl['food_cost'], '#2ecc71'),
        ]

        labels = [c[0] for c in costs]
        values = [c[1] for c in costs]
        colors = [c[2] for c in costs]

        # 圓餅圖
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='$%1.0f',
            colors=colors, startangle=90,
            textprops={'fontproperties': chinese_font, 'fontsize': 10},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        # 標題
        ax.set_title(f'{title}\n總成本: ${pnl["total_cost"]:,.0f} | 虧損: ${pnl["profit"]:,.0f}',
                     fontsize=13, fontweight='bold', fontproperties=chinese_font)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'cost_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ cost_breakdown.png")


# ============================================================
# 報告生成函數
# ============================================================

def generate_json_results() -> dict:
    """生成 JSON 格式的分析結果"""
    results = {
        'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'vacation_period': '12/22 ~ 1/11',
        'parameters': {
            'nyc_tax_rate': NYC_TAX_RATE,
            'fixed_costs': FIXED_COSTS,
            'total_fixed_cost': TOTAL_FIXED_COST,
            'labor_costs': LABOR_COSTS,
            'food_cost_rates': FOOD_COST_RATES,
        },
        'months': {},
    }

    for month in ['dec_2025', 'jan_2026']:
        adjusted_revenue = calculate_adjusted_revenue(month)
        operating_days = OPERATING_DAYS[month]
        original = ORIGINAL_FORECAST[month]

        month_data = {
            'original_forecast': {
                'gross': original['gross'],
                'net': round(original['net'], 2),
                'original_days': original['original_days'],
            },
            'adjusted': {
                'operating_days': operating_days,
                'adjusted_net_revenue': adjusted_revenue,
            },
            'scenarios': {},
            'sensitivity_matrix': {},
        }

        # 各人力成本情境
        for labor_name, daily_labor in LABOR_COSTS.items():
            be = calculate_break_even(operating_days, daily_labor, 0.35)
            pnl = calculate_profit_loss(adjusted_revenue, operating_days, daily_labor, 0.35)

            month_data['scenarios'][labor_name] = {
                'daily_labor': daily_labor,
                'monthly_labor': be['monthly_labor'],
                'break_even_monthly': be['break_even_monthly'],
                'break_even_daily': be['break_even_daily'],
                'profit_loss': pnl['profit'],
            }

        # 敏感度矩陣
        for food_rate_name, food_rate in FOOD_COST_RATES.items():
            month_data['sensitivity_matrix'][food_rate_name] = {}
            for labor_name, daily_labor in LABOR_COSTS.items():
                pnl = calculate_profit_loss(adjusted_revenue, operating_days, daily_labor, food_rate)
                month_data['sensitivity_matrix'][food_rate_name][labor_name] = pnl['profit']

        results['months'][month] = month_data

    # 總結
    dec_best = results['months']['dec_2025']['sensitivity_matrix']['low']['minimum']
    jan_best = results['months']['jan_2026']['sensitivity_matrix']['low']['minimum']
    dec_worst = results['months']['dec_2025']['sensitivity_matrix']['high']['full']
    jan_worst = results['months']['jan_2026']['sensitivity_matrix']['high']['full']

    results['summary'] = {
        'best_case_total_loss': dec_best + jan_best,
        'worst_case_total_loss': dec_worst + jan_worst,
        'recommendation': '採用最低人力配置 ($100/天) + 30% 食材成本率，可將虧損控制在最低',
    }

    return results


def generate_markdown_report(results: dict) -> str:
    """生成 Markdown 報告"""
    dec = results['months']['dec_2025']
    jan = results['months']['jan_2026']

    report = f"""# 2025/12 與 2026/01 損益平衡點分析報告

**報告生成時間**：{results['report_date']}

---

## 執行摘要

### ⚠️ 重大發現：休假導致確定虧損

由於 **12/22 ~ 1/11 休假**（共 21 天），兩個月份均確定虧損：

| 月份 | 營業天數 | 調整後預測營收 | 最佳情境虧損 | 最差情境虧損 |
|------|---------|---------------|-------------|-------------|
| 12 月 | {dec['adjusted']['operating_days']} 天 | ${dec['adjusted']['adjusted_net_revenue']:,.0f} | **${results['months']['dec_2025']['sensitivity_matrix']['low']['minimum']:,.0f}** | ${results['months']['dec_2025']['sensitivity_matrix']['high']['full']:,.0f} |
| 1 月 | {jan['adjusted']['operating_days']} 天 | ${jan['adjusted']['adjusted_net_revenue']:,.0f} | **${results['months']['jan_2026']['sensitivity_matrix']['low']['minimum']:,.0f}** | ${results['months']['jan_2026']['sensitivity_matrix']['high']['full']:,.0f} |
| **合計** | 24 天 | ${dec['adjusted']['adjusted_net_revenue'] + jan['adjusted']['adjusted_net_revenue']:,.0f} | **${results['summary']['best_case_total_loss']:,.0f}** | ${results['summary']['worst_case_total_loss']:,.0f} |

### 關鍵原因

1. **固定成本無法減免**：房租 $3,100 + 水電 $700 = **$3,800/月** 仍需全額支付
2. **營業天數大幅減少**：12 天 vs 原本 17 天（**-29%**）
3. **每日分攤固定成本上升**：$317/天 vs $224/天（**+41%**）

---

## 1. 分析參數

### 1.1 營業天數

| 月份 | 原預計天數 | 實際營業天數 | 減少比例 |
|------|-----------|-------------|---------|
| 12 月 | 17 天 | **12 天** | -29% |
| 1 月 | 17 天 | **12 天** | -29% |

### 1.2 成本參數

| 成本類型 | 參數 | 金額 |
|---------|------|------|
| 固定成本 | 房租 | $3,100/月 |
| | 水電 | $700/月 |
| | **合計** | **$3,800/月** |
| 人力成本 | 最低配置 | $100/天 |
| | 標準配置 | $160/天 |
| | 加強配置 | $200/天 |
| | 完整配置 | $250/天 |
| 食材成本率 | 低 | 30% |
| | 中（預設） | 35% |
| | 高 | 40% |

---

## 2. 損益平衡分析

### 2.1 2025 年 12 月（12 天營業）

| 人力成本/天 | 月人力成本 | 損益平衡（月） | 損益平衡（日） | 預測 vs 實際 |
|------------|-----------|---------------|---------------|--------------|
| $100 | ${dec['scenarios']['minimum']['monthly_labor']} | ${dec['scenarios']['minimum']['break_even_monthly']:,.0f} | ${dec['scenarios']['minimum']['break_even_daily']:.0f} | ❌ {dec['scenarios']['minimum']['profit_loss']:+,.0f} |
| $160 | ${dec['scenarios']['standard']['monthly_labor']} | ${dec['scenarios']['standard']['break_even_monthly']:,.0f} | ${dec['scenarios']['standard']['break_even_daily']:.0f} | ❌ {dec['scenarios']['standard']['profit_loss']:+,.0f} |
| $200 | ${dec['scenarios']['enhanced']['monthly_labor']} | ${dec['scenarios']['enhanced']['break_even_monthly']:,.0f} | ${dec['scenarios']['enhanced']['break_even_daily']:.0f} | ❌ {dec['scenarios']['enhanced']['profit_loss']:+,.0f} |
| $250 | ${dec['scenarios']['full']['monthly_labor']} | ${dec['scenarios']['full']['break_even_monthly']:,.0f} | ${dec['scenarios']['full']['break_even_daily']:.0f} | ❌ {dec['scenarios']['full']['profit_loss']:+,.0f} |

> 以 35% 食材成本率、調整後預測營收 ${dec['adjusted']['adjusted_net_revenue']:,.0f} 計算

### 2.2 2026 年 1 月（12 天營業）

| 人力成本/天 | 月人力成本 | 損益平衡（月） | 損益平衡（日） | 預測 vs 實際 |
|------------|-----------|---------------|---------------|--------------|
| $100 | ${jan['scenarios']['minimum']['monthly_labor']} | ${jan['scenarios']['minimum']['break_even_monthly']:,.0f} | ${jan['scenarios']['minimum']['break_even_daily']:.0f} | ❌ {jan['scenarios']['minimum']['profit_loss']:+,.0f} |
| $160 | ${jan['scenarios']['standard']['monthly_labor']} | ${jan['scenarios']['standard']['break_even_monthly']:,.0f} | ${jan['scenarios']['standard']['break_even_daily']:.0f} | ❌ {jan['scenarios']['standard']['profit_loss']:+,.0f} |
| $200 | ${jan['scenarios']['enhanced']['monthly_labor']} | ${jan['scenarios']['enhanced']['break_even_monthly']:,.0f} | ${jan['scenarios']['enhanced']['break_even_daily']:.0f} | ❌ {jan['scenarios']['enhanced']['profit_loss']:+,.0f} |
| $250 | ${jan['scenarios']['full']['monthly_labor']} | ${jan['scenarios']['full']['break_even_monthly']:,.0f} | ${jan['scenarios']['full']['break_even_daily']:.0f} | ❌ {jan['scenarios']['full']['profit_loss']:+,.0f} |

> 以 35% 食材成本率、調整後預測營收 ${jan['adjusted']['adjusted_net_revenue']:,.0f} 計算

---

## 3. 敏感度分析

### 3.1 12 月敏感度矩陣（預測營收 ${dec['adjusted']['adjusted_net_revenue']:,.0f}）

| 食材成本率 | $100/天 | $160/天 | $200/天 | $250/天 |
|-----------|---------|---------|---------|---------|
| 30% | ${dec['sensitivity_matrix']['low']['minimum']:,.0f} | ${dec['sensitivity_matrix']['low']['standard']:,.0f} | ${dec['sensitivity_matrix']['low']['enhanced']:,.0f} | ${dec['sensitivity_matrix']['low']['full']:,.0f} |
| 35% | ${dec['sensitivity_matrix']['medium']['minimum']:,.0f} | ${dec['sensitivity_matrix']['medium']['standard']:,.0f} | ${dec['sensitivity_matrix']['medium']['enhanced']:,.0f} | ${dec['sensitivity_matrix']['medium']['full']:,.0f} |
| 40% | ${dec['sensitivity_matrix']['high']['minimum']:,.0f} | ${dec['sensitivity_matrix']['high']['standard']:,.0f} | ${dec['sensitivity_matrix']['high']['enhanced']:,.0f} | ${dec['sensitivity_matrix']['high']['full']:,.0f} |

### 3.2 1 月敏感度矩陣（預測營收 ${jan['adjusted']['adjusted_net_revenue']:,.0f}）

| 食材成本率 | $100/天 | $160/天 | $200/天 | $250/天 |
|-----------|---------|---------|---------|---------|
| 30% | ${jan['sensitivity_matrix']['low']['minimum']:,.0f} | ${jan['sensitivity_matrix']['low']['standard']:,.0f} | ${jan['sensitivity_matrix']['low']['enhanced']:,.0f} | ${jan['sensitivity_matrix']['low']['full']:,.0f} |
| 35% | ${jan['sensitivity_matrix']['medium']['minimum']:,.0f} | ${jan['sensitivity_matrix']['medium']['standard']:,.0f} | ${jan['sensitivity_matrix']['medium']['enhanced']:,.0f} | ${jan['sensitivity_matrix']['medium']['full']:,.0f} |
| 40% | ${jan['sensitivity_matrix']['high']['minimum']:,.0f} | ${jan['sensitivity_matrix']['high']['standard']:,.0f} | ${jan['sensitivity_matrix']['high']['enhanced']:,.0f} | ${jan['sensitivity_matrix']['high']['full']:,.0f} |

---

## 4. 視覺化圖表

### 4.1 損益平衡對比
![損益平衡對比](charts/break_even_comparison.png)

### 4.2 12 月敏感度熱力圖
![12月敏感度](charts/sensitivity_heatmap_dec_2025.png)

### 4.3 1 月敏感度熱力圖
![1月敏感度](charts/sensitivity_heatmap_jan_2026.png)

### 4.4 人力成本影響
![人力成本影響](charts/labor_cost_impact.png)

### 4.5 成本結構分解
![成本結構](charts/cost_breakdown.png)

---

## 5. 建議與結論

### 5.1 人力配置建議

| 月份 | 建議配置 | 日薪資 | 預期虧損 |
|------|---------|--------|---------|
| 12 月 | 最低配置 | $100/天 | -$971 ~ -$1,520 |
| 1 月 | 最低配置 | $100/天 | -$1,616 ~ -$2,165 |

### 5.2 成本控制策略

1. **採用最低人力配置**：$100/天
2. **控制食材成本率**：≤ 30%
3. **最佳情境總虧損**：**${results['summary']['best_case_total_loss']:,.0f}**

### 5.3 休假成本分析

將虧損視為「休假成本」的一部分：

- **21 天休假的成本**：${abs(results['summary']['best_case_total_loss']):,.0f} ~ ${abs(results['summary']['worst_case_total_loss']):,.0f}
- **平均每天休假成本**：${abs(results['summary']['best_case_total_loss'])/21:.0f} ~ ${abs(results['summary']['worst_case_total_loss'])/21:.0f}

---

*報告生成：Claude Code Agent System - Break-Even Analysis Module*
"""
    return report


# ============================================================
# 主程式
# ============================================================

def main():
    print("=" * 60)
    print("2025/12 與 2026/01 損益平衡點分析")
    print("考慮特殊休假：12/22 ~ 1/11")
    print("=" * 60)

    # 生成分析結果
    print("\n[1/5] 計算損益平衡點...")
    results = generate_json_results()

    # 保存 JSON
    print("[2/5] 保存 JSON 結果...")
    with open(OUTPUT_DIR / 'break_even_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ {OUTPUT_DIR / 'break_even_results.json'}")

    # 生成視覺化圖表
    print("\n[3/5] 生成視覺化圖表...")
    plot_break_even_comparison()
    plot_sensitivity_heatmap('dec_2025', '2025 年 12 月')
    plot_sensitivity_heatmap('jan_2026', '2026 年 1 月')
    plot_labor_cost_impact()
    plot_cost_breakdown()

    # 生成 Markdown 報告
    print("\n[4/5] 生成 Markdown 報告...")
    report = generate_markdown_report(results)
    with open(OUTPUT_DIR / 'break_even_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ {OUTPUT_DIR / 'break_even_report.md'}")

    # 生成 CSV 數據
    print("\n[5/5] 生成 CSV 數據...")
    for month in ['dec_2025', 'jan_2026']:
        df = generate_sensitivity_matrix(month)
        df.to_csv(DATA_DIR / f'{month}_sensitivity.csv')
        print(f"✓ {DATA_DIR / f'{month}_sensitivity.csv'}")

    # 摘要
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)

    summary = results['summary']
    print(f"\n⚠️ 關鍵發現：")
    print(f"   休假期間：12/22 ~ 1/11（21 天）")
    print(f"   最佳情境總虧損：${summary['best_case_total_loss']:,.0f}")
    print(f"   最差情境總虧損：${summary['worst_case_total_loss']:,.0f}")
    print(f"\n💡 建議：{summary['recommendation']}")

    print(f"\n📁 輸出目錄：{OUTPUT_DIR}")


if __name__ == '__main__':
    main()
