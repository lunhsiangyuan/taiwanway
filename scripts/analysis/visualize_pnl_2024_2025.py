#!/usr/bin/env python3
"""
Taiwanway 餐廳損益分析視覺化（2024/01 - 2025/05）
生成多種圖表展示財務表現
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from pathlib import Path

# 設定繁體中文字體
mpl.rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'Heiti TC']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['text.usetex'] = False

# 設定 Seaborn 樣式
sns.set_style("whitegrid")
sns.set_palette("husl")

# 載入數據
data_path = Path('/Users/lunhsiangyuan/Desktop/square/analysis_output/pnl_analysis/monthly_pnl_2024_2025.csv')
output_dir = Path('/Users/lunhsiangyuan/Desktop/square/analysis_output/pnl_analysis/charts')
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_path)

# 移除總計行
df = df[df['YearMonth_Str'] != '總計'].copy()

print(f"載入 {len(df)} 個月的數據")

# ============================================================================
# 圖表 1：每月營收與成本趨勢（折線圖）
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 6))

x = range(len(df))
labels = df['YearMonth_Str'].tolist()

# 繪製營收和成本線
ax.plot(x, df['Net_Revenue'], marker='o', linewidth=2.5, markersize=8,
        label='淨營收', color='#2E7D32', zorder=3)
ax.plot(x, df['Total_Cost'], marker='s', linewidth=2.5, markersize=8,
        label='總成本', color='#C62828', zorder=3)

# 填充盈虧區域
ax.fill_between(x, df['Net_Revenue'], df['Total_Cost'],
                where=(df['Net_Revenue'] >= df['Total_Cost']),
                alpha=0.3, color='green', label='盈利區')
ax.fill_between(x, df['Net_Revenue'], df['Total_Cost'],
                where=(df['Net_Revenue'] < df['Total_Cost']),
                alpha=0.3, color='red', label='虧損區')

ax.set_xlabel('年月', fontsize=12, fontweight='bold')
ax.set_ylabel('金額 (USD)', fontsize=12, fontweight='bold')
ax.set_title('Taiwanway 每月營收與成本趨勢 (2024/01 - 2025/05)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linewidth=0.8, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / 'fig1_monthly_revenue_cost_trend.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 1：每月營收與成本趨勢")

# ============================================================================
# 圖表 2：每月營業利潤（瀑布圖風格的長條圖）
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 6))

colors = ['green' if profit >= 0 else 'red' for profit in df['Operating_Profit']]

bars = ax.bar(x, df['Operating_Profit'], color=colors, alpha=0.7,
              edgecolor='black', linewidth=1.2)

# 添加數值標籤
for i, (bar, profit) in enumerate(zip(bars, df['Operating_Profit'])):
    height = bar.get_height()
    if profit >= 0:
        va = 'bottom'
        y_offset = 100
    else:
        va = 'top'
        y_offset = -100

    ax.text(bar.get_x() + bar.get_width()/2, height + y_offset,
            f'${profit:,.0f}',
            ha='center', va=va, fontsize=9, fontweight='bold')

ax.set_xlabel('年月', fontsize=12, fontweight='bold')
ax.set_ylabel('營業利潤 (USD)', fontsize=12, fontweight='bold')
ax.set_title('Taiwanway 每月營業利潤 (2024/01 - 2025/05)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.axhline(y=0, color='black', linewidth=1.5, linestyle='-')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / 'fig2_monthly_operating_profit.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 2：每月營業利潤")

# ============================================================================
# 圖表 3：成本結構堆疊長條圖
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 6))

# 堆疊長條圖
p1 = ax.bar(x, df['Food_Cost'], label='食材成本', color='#FFA726', edgecolor='black', linewidth=0.8)
p2 = ax.bar(x, df['Labor_Cost'], bottom=df['Food_Cost'],
            label='人力成本', color='#42A5F5', edgecolor='black', linewidth=0.8)
p3 = ax.bar(x, df['Fixed_Cost'], bottom=df['Food_Cost'] + df['Labor_Cost'],
            label='固定成本', color='#66BB6A', edgecolor='black', linewidth=0.8)

# 添加淨營收線（參考線）
ax.plot(x, df['Net_Revenue'], marker='o', linewidth=2.5, markersize=8,
        label='淨營收', color='#D32F2F', zorder=5)

ax.set_xlabel('年月', fontsize=12, fontweight='bold')
ax.set_ylabel('金額 (USD)', fontsize=12, fontweight='bold')
ax.set_title('Taiwanway 每月成本結構與營收比較 (2024/01 - 2025/05)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / 'fig3_monthly_cost_structure.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 3：成本結構堆疊長條圖")

# ============================================================================
# 圖表 4：毛利率與淨利率趨勢
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 6))

# 只顯示有營收的月份
df_revenue = df[df['Net_Revenue'] > 0].copy()
x_revenue = range(len(df_revenue))
labels_revenue = df_revenue['YearMonth_Str'].tolist()

ax.plot(x_revenue, df_revenue['Gross_Margin'], marker='o', linewidth=2.5, markersize=8,
        label='毛利率', color='#2E7D32')
ax.plot(x_revenue, df_revenue['Net_Margin'], marker='s', linewidth=2.5, markersize=8,
        label='淨利率', color='#1976D2')

ax.set_xlabel('年月', fontsize=12, fontweight='bold')
ax.set_ylabel('利潤率 (%)', fontsize=12, fontweight='bold')
ax.set_title('Taiwanway 毛利率與淨利率趨勢 (2024/01 - 2025/05)', fontsize=14, fontweight='bold')
ax.set_xticks(x_revenue)
ax.set_xticklabels(labels_revenue, rotation=45, ha='right')
ax.axhline(y=0, color='black', linewidth=1.5, linestyle='--')
ax.axhline(y=65, color='green', linewidth=1, linestyle=':', alpha=0.5, label='毛利率目標 (65%)')
ax.legend(fontsize=11, loc='lower right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'fig4_profit_margin_trend.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 4：毛利率與淨利率趨勢")

# ============================================================================
# 圖表 5：2024 vs 2025 對比（分組長條圖）
# ============================================================================

# 計算年度統計
df['Year'] = df['YearMonth_Str'].str[:4]
yearly_stats = df.groupby('Year').agg({
    'Net_Revenue': 'sum',
    'Food_Cost': 'sum',
    'Labor_Cost': 'sum',
    'Fixed_Cost': 'sum',
    'Total_Cost': 'sum',
    'Operating_Profit': 'sum'
}).reset_index()

# 2025 年只有 5 個月，計算月平均後乘以 12 個月進行年化
yearly_stats_normalized = yearly_stats.copy()
for idx, row in yearly_stats_normalized.iterrows():
    if row['Year'] == '2025':
        # 年化調整（5 個月 → 12 個月）
        for col in ['Net_Revenue', 'Food_Cost', 'Labor_Cost', 'Fixed_Cost', 'Total_Cost', 'Operating_Profit']:
            yearly_stats_normalized.loc[idx, col] = row[col] / 5 * 12

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 左圖：實際值
categories = ['淨營收', '總成本', '營業利潤']
x_pos = np.arange(len(categories))
width = 0.35

data_2024_actual = [
    yearly_stats[yearly_stats['Year'] == '2024']['Net_Revenue'].values[0],
    yearly_stats[yearly_stats['Year'] == '2024']['Total_Cost'].values[0],
    yearly_stats[yearly_stats['Year'] == '2024']['Operating_Profit'].values[0]
]

data_2025_actual = [
    yearly_stats[yearly_stats['Year'] == '2025']['Net_Revenue'].values[0],
    yearly_stats[yearly_stats['Year'] == '2025']['Total_Cost'].values[0],
    yearly_stats[yearly_stats['Year'] == '2025']['Operating_Profit'].values[0]
]

bars1 = axes[0].bar(x_pos - width/2, data_2024_actual, width, label='2024 (12 個月)',
                     color='#1976D2', edgecolor='black', linewidth=1.2)
bars2 = axes[0].bar(x_pos + width/2, data_2025_actual, width, label='2025 (5 個月)',
                     color='#388E3C', edgecolor='black', linewidth=1.2)

# 添加數值標籤
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height >= 0:
            va = 'bottom'
            y_offset = 500
        else:
            va = 'top'
            y_offset = -500
        axes[0].text(bar.get_x() + bar.get_width()/2, height + y_offset,
                     f'${height:,.0f}',
                     ha='center', va=va, fontsize=10, fontweight='bold')

axes[0].set_ylabel('金額 (USD)', fontsize=12, fontweight='bold')
axes[0].set_title('2024 vs 2025 財務表現對比（實際值）', fontsize=13, fontweight='bold')
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(categories)
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3, axis='y')
axes[0].axhline(y=0, color='black', linewidth=1.5, linestyle='-')

# 右圖：年化值
data_2024_norm = data_2024_actual
data_2025_norm = [
    yearly_stats_normalized[yearly_stats_normalized['Year'] == '2025']['Net_Revenue'].values[0],
    yearly_stats_normalized[yearly_stats_normalized['Year'] == '2025']['Total_Cost'].values[0],
    yearly_stats_normalized[yearly_stats_normalized['Year'] == '2025']['Operating_Profit'].values[0]
]

bars3 = axes[1].bar(x_pos - width/2, data_2024_norm, width, label='2024 (12 個月)',
                     color='#1976D2', edgecolor='black', linewidth=1.2)
bars4 = axes[1].bar(x_pos + width/2, data_2025_norm, width, label='2025 (年化)',
                     color='#388E3C', edgecolor='black', linewidth=1.2)

# 添加數值標籤
for bars in [bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        if height >= 0:
            va = 'bottom'
            y_offset = 1000
        else:
            va = 'top'
            y_offset = -1000
        axes[1].text(bar.get_x() + bar.get_width()/2, height + y_offset,
                     f'${height:,.0f}',
                     ha='center', va=va, fontsize=10, fontweight='bold')

axes[1].set_ylabel('金額 (USD)', fontsize=12, fontweight='bold')
axes[1].set_title('2024 vs 2025 財務表現對比（2025 年化）', fontsize=13, fontweight='bold')
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(categories)
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].axhline(y=0, color='black', linewidth=1.5, linestyle='-')

plt.tight_layout()
plt.savefig(output_dir / 'fig5_yearly_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 5：2024 vs 2025 年度對比")

# ============================================================================
# 圖表 6：成本佔營收比例（圓餅圖）
# ============================================================================

# 計算總計
total_net_revenue = df['Net_Revenue'].sum()
total_food_cost = df['Food_Cost'].sum()
total_labor_cost = df['Labor_Cost'].sum()
total_fixed_cost = df['Fixed_Cost'].sum()
total_operating_profit = df['Operating_Profit'].sum()

# 準備數據
sizes = [total_food_cost, total_labor_cost, total_fixed_cost]
labels_pie = ['食材成本', '人力成本', '固定成本']
colors_pie = ['#FFA726', '#42A5F5', '#66BB6A']

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 左圖：成本結構
wedges, texts, autotexts = axes[0].pie(sizes, labels=labels_pie, autopct='%1.1f%%',
                                         colors=colors_pie, startangle=90,
                                         textprops={'fontsize': 12, 'fontweight': 'bold'})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)

axes[0].set_title('成本結構組成 (2024/01 - 2025/05)', fontsize=14, fontweight='bold')

# 右圖：營收分配
if total_operating_profit >= 0:
    sizes_revenue = [total_food_cost, total_labor_cost, total_fixed_cost, total_operating_profit]
    labels_revenue = ['食材成本', '人力成本', '固定成本', '營業利潤']
    colors_revenue = ['#FFA726', '#42A5F5', '#66BB6A', '#4CAF50']
else:
    # 虧損情況：顯示虧損額
    sizes_revenue = [total_food_cost, total_labor_cost, total_fixed_cost, abs(total_operating_profit)]
    labels_revenue = ['食材成本', '人力成本', '固定成本', '虧損']
    colors_revenue = ['#FFA726', '#42A5F5', '#66BB6A', '#F44336']

wedges2, texts2, autotexts2 = axes[1].pie(sizes_revenue, labels=labels_revenue, autopct='%1.1f%%',
                                            colors=colors_revenue, startangle=90,
                                            textprops={'fontsize': 12, 'fontweight': 'bold'})

for autotext in autotexts2:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)

axes[1].set_title('淨營收分配 (2024/01 - 2025/05)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'fig6_cost_revenue_breakdown.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 6：成本與營收分配（圓餅圖）")

# ============================================================================
# 圖表 7：綜合儀表板（2x2）
# ============================================================================

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# 子圖 1：營收趨勢
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(x, df['Net_Revenue'], marker='o', linewidth=2.5, markersize=8,
         color='#2E7D32', label='淨營收')
ax1.fill_between(x, df['Net_Revenue'], alpha=0.3, color='#2E7D32')
ax1.set_xlabel('年月', fontweight='bold')
ax1.set_ylabel('金額 (USD)', fontweight='bold')
ax1.set_title('淨營收趨勢', fontweight='bold', fontsize=13)
ax1.set_xticks(x[::2])
ax1.set_xticklabels(labels[::2], rotation=45, ha='right')
ax1.grid(True, alpha=0.3)

# 子圖 2：營業利潤
ax2 = fig.add_subplot(gs[0, 1])
colors_profit = ['green' if profit >= 0 else 'red' for profit in df['Operating_Profit']]
ax2.bar(x, df['Operating_Profit'], color=colors_profit, alpha=0.7,
        edgecolor='black', linewidth=1)
ax2.axhline(y=0, color='black', linewidth=1.5, linestyle='-')
ax2.set_xlabel('年月', fontweight='bold')
ax2.set_ylabel('營業利潤 (USD)', fontweight='bold')
ax2.set_title('每月營業利潤', fontweight='bold', fontsize=13)
ax2.set_xticks(x[::2])
ax2.set_xticklabels(labels[::2], rotation=45, ha='right')
ax2.grid(True, alpha=0.3, axis='y')

# 子圖 3：成本結構
ax3 = fig.add_subplot(gs[1, 0])
ax3.bar(x, df['Food_Cost'], label='食材', color='#FFA726', edgecolor='black', linewidth=0.8)
ax3.bar(x, df['Labor_Cost'], bottom=df['Food_Cost'],
        label='人力', color='#42A5F5', edgecolor='black', linewidth=0.8)
ax3.bar(x, df['Fixed_Cost'], bottom=df['Food_Cost'] + df['Labor_Cost'],
        label='固定', color='#66BB6A', edgecolor='black', linewidth=0.8)
ax3.set_xlabel('年月', fontweight='bold')
ax3.set_ylabel('金額 (USD)', fontweight='bold')
ax3.set_title('成本結構', fontweight='bold', fontsize=13)
ax3.set_xticks(x[::2])
ax3.set_xticklabels(labels[::2], rotation=45, ha='right')
ax3.legend(fontsize=10, loc='upper left')
ax3.grid(True, alpha=0.3, axis='y')

# 子圖 4：關鍵指標摘要（文字）
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

summary_text = f"""
Taiwanway 餐廳財務摘要
2024/01 - 2025/05（17 個月）

━━━━━━━━━━━━━━━━━━━━━━━━

📊 總計指標

總營業天數：{df['Operating_Days'].sum():.0f} 天
總淨營收：${df['Net_Revenue'].sum():,.2f}
總成本：${df['Total_Cost'].sum():,.2f}
總營業利潤：${df['Operating_Profit'].sum():,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━

💰 成本結構

食材成本：${df['Food_Cost'].sum():,.2f} (35.0%)
人力成本：${df['Labor_Cost'].sum():,.2f} (7.6%)
固定成本：${df['Fixed_Cost'].sum():,.2f} (63.7%)

━━━━━━━━━━━━━━━━━━━━━━━━

📈 盈利表現

平均毛利率：65.0%
平均淨利率：{df['Operating_Profit'].sum() / df['Net_Revenue'].sum() * 100:.2f}%

盈利月份：{len(df[df['Operating_Profit'] > 0])} 個月
虧損月份：{len(df[df['Operating_Profit'] < 0])} 個月

━━━━━━━━━━━━━━━━━━━━━━━━

🔄 年度對比

2024 年淨利率：{yearly_stats[yearly_stats['Year'] == '2024']['Operating_Profit'].values[0] / yearly_stats[yearly_stats['Year'] == '2024']['Net_Revenue'].values[0] * 100:.2f}%
2025 年淨利率：{yearly_stats[yearly_stats['Year'] == '2025']['Operating_Profit'].values[0] / yearly_stats[yearly_stats['Year'] == '2025']['Net_Revenue'].values[0] * 100:.2f}%
"""

ax4.text(0.5, 0.5, summary_text, transform=ax4.transAxes,
         fontsize=11, verticalalignment='center', horizontalalignment='center',
         family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

fig.suptitle('Taiwanway 餐廳財務綜合儀表板 (2024/01 - 2025/05)',
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig(output_dir / 'fig7_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ 圖表 7：綜合儀表板")

print("\n" + "="*80)
print(f"所有圖表已儲存至：{output_dir}")
print("="*80)
print("\n✅ 視覺化完成！")
