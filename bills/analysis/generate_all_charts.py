#!/usr/bin/env python3
"""
TaiwanWay 餐廳能源帳單視覺化圖表生成腳本（完整版）
包含省錢分析圖表
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體
font_paths = [p for p in fm.findSystemFonts() if 'PingFang' in p]
for p in font_paths:
    if 'PingFang.ttc' in p:
        fm.fontManager.addfont(p)
        break

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['PingFang TC', 'PingFang SC', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 數據
months = ['Jun-Jul', 'Jul-Aug', 'Aug-Sep', 'Sep-Oct', 'Oct-Nov', 'Nov-Dec']
electricity = [156.79, 553.81, 481.05, 438.92, 372.98, 448.59]
gas = [30.75, 32.49, 32.02, 44.41, 182.39, 375.11]
total = [187.54, 586.30, 513.07, 483.33, 555.37, 823.70]

output_dir = '/Users/lunhsiangyuan/Desktop/TaiwanWay/bills/analysis/charts'

# ===== 圖表 1：月度費用趨勢 =====
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(months))
width = 0.35

bars1 = ax.bar(x - width/2, electricity, width, label='電費', color='#3498db', edgecolor='black')
bars2 = ax.bar(x + width/2, gas, width, label='瓦斯費', color='#e74c3c', edgecolor='black')

ax.plot(x, total, 'ko-', linewidth=2, markersize=8, label='總計')

ax.set_xlabel('帳單期間', fontsize=12, fontweight='bold')
ax.set_ylabel('費用 (USD)', fontsize=12, fontweight='bold')
ax.set_title('TaiwanWay 餐廳 2025 年能源費用趨勢', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(months)
ax.legend(loc='upper left')
ax.grid(axis='y', alpha=0.3)

for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'${height:.0f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'${height:.0f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(f'{output_dir}/monthly_cost_trend.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: monthly_cost_trend.png")

# ===== 圖表 2：瓦斯費季節變化 =====
fig, ax = plt.subplots(figsize=(10, 6))

colors = ['#27ae60', '#27ae60', '#27ae60', '#f39c12', '#e74c3c', '#c0392b']
bars = ax.bar(months, gas, color=colors, edgecolor='black', linewidth=1.5)

ax.set_xlabel('帳單期間', fontsize=12, fontweight='bold')
ax.set_ylabel('瓦斯費 (USD)', fontsize=12, fontweight='bold')
ax.set_title('瓦斯費季節性變化：夏季 vs 冬季', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, gas)):
    ax.annotate(f'${val:.0f}', xy=(bar.get_x() + bar.get_width()/2, val),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=11, fontweight='bold')

ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
ax.text(0.5, 40, '夏季（無暖氣）~$30/月', fontsize=10, color='#27ae60')
ax.text(4.2, 280, '冬季（暖氣）', fontsize=10, color='#c0392b')
ax.text(4.2, 250, '$182-$375/月', fontsize=10, color='#c0392b')

ax.annotate('', xy=(5, 375), xytext=(2, 32),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(3.5, 180, '12倍增長！', fontsize=12, color='red', fontweight='bold', rotation=45)

plt.tight_layout()
plt.savefig(f'{output_dir}/gas_seasonal.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: gas_seasonal.png")

# ===== 圖表 3：溫控排程視覺化 =====
fig, ax = plt.subplots(figsize=(14, 6))

hours = np.arange(0, 24.5, 0.5)
temps = []

for h in hours:
    if h < 6.5:
        temps.append(55)
    elif h < 8:
        temps.append(65)
    elif h < 19:
        temps.append(68)
    elif h < 19.5:
        temps.append(65)
    else:
        temps.append(55)

ax.fill_between(hours, temps, 50, alpha=0.3, color='#e74c3c')
ax.plot(hours, temps, 'r-', linewidth=3, label='溫度設定')

ax.axvspan(0, 6.5, alpha=0.1, color='blue', label='休息時段')
ax.axvspan(6.5, 8, alpha=0.1, color='yellow', label='預熱時段')
ax.axvspan(8, 19, alpha=0.1, color='green', label='營業時段')
ax.axvspan(19, 19.5, alpha=0.1, color='yellow')
ax.axvspan(19.5, 24, alpha=0.1, color='blue')

ax.annotate('55°F\n(13°C)', xy=(3, 55), xytext=(3, 58), fontsize=11, ha='center', fontweight='bold')
ax.annotate('65°F\n(18°C)', xy=(7.25, 65), xytext=(7.25, 68), fontsize=11, ha='center', fontweight='bold')
ax.annotate('68°F\n(20°C)', xy=(13.5, 68), xytext=(13.5, 71), fontsize=11, ha='center', fontweight='bold')

ax.axvline(x=6.5, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=8, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=19, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=19.5, color='gray', linestyle='--', alpha=0.5)

ax.text(6.5, 52, '06:30\n預熱', ha='center', fontsize=9)
ax.text(8, 52, '08:00\n營業', ha='center', fontsize=9)
ax.text(19, 52, '19:00\n清潔', ha='center', fontsize=9)
ax.text(19.5, 52, '19:30\n打烊', ha='center', fontsize=9)

ax.set_xlabel('時間（小時）', fontsize=12, fontweight='bold')
ax.set_ylabel('溫度 (°F)', fontsize=12, fontweight='bold')
ax.set_title('建議溫控排程：每年可省 $788', fontsize=14, fontweight='bold')
ax.set_xlim(0, 24)
ax.set_ylim(50, 75)
ax.set_xticks(range(0, 25, 2))
ax.legend(loc='upper right')
ax.grid(axis='both', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/temperature_schedule.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: temperature_schedule.png")

# ===== 圖表 4：冬季能源成本分解 =====
fig, ax = plt.subplots(figsize=(10, 8))

categories = ['瓦斯暖氣\n$342 (41.5%)', '電爐/烹飪\n$300 (36.4%)', '冷藏設備\n$80 (9.7%)',
              '照明\n$40 (4.9%)', '熱水器\n$33 (4.0%)', '其他\n$28 (3.4%)']
values = [342, 300, 80, 40, 33, 28]
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6', '#95a5a6']

wedges, texts, autotexts = ax.pie(values, labels=categories, autopct='%1.1f%%',
                                   colors=colors, startangle=90,
                                   explode=(0.05, 0.02, 0, 0, 0, 0),
                                   textprops={'fontsize': 10})

for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

ax.set_title('冬季月度能源成本分解（總計 $823.70）', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/cost_breakdown.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: cost_breakdown.png")

# ===== 圖表 5：商業 vs 住宅比較 =====
fig, ax = plt.subplots(figsize=(10, 6))

categories = ['電費', '瓦斯費', '總計']
commercial = [448.59, 375.11, 823.70]
residential = [267.52, 212.61, 480.13]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, commercial, width, label='商業 (FONGGOOD)', color='#3498db', edgecolor='black')
bars2 = ax.bar(x + width/2, residential, width, label='住宅 (HUEIJU)', color='#2ecc71', edgecolor='black')

ax.set_xlabel('費用類別', fontsize=12, fontweight='bold')
ax.set_ylabel('費用 (USD)', fontsize=12, fontweight='bold')
ax.set_title('商業 vs 住宅能源費用比較（Nov-Dec 2025）', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
ax.grid(axis='y', alpha=0.3)

diffs = [(c-r)/r*100 for c, r in zip(commercial, residential)]
for i, (c, r, d) in enumerate(zip(commercial, residential, diffs)):
    ax.annotate(f'+{d:.0f}%', xy=(i, max(c, r) + 20), ha='center',
                fontsize=11, fontweight='bold', color='red')

for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'${height:.0f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'${height:.0f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/commercial_vs_residential.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: commercial_vs_residential.png")

# ===== 圖表 6：省錢方案比較 =====
fig, ax = plt.subplots(figsize=(10, 6))

methods = ['溫控排程\n(免費)', '+ 可程式溫控器\n($75)', '+ 密封漏風\n($100)', '+ 降低 1°F\n($0)']
savings = [788, 788, 1028, 1148]
investments = [0, 75, 175, 175]

colors = ['#27ae60', '#2ecc71', '#3498db', '#9b59b6']
bars = ax.bar(methods, savings, color=colors, edgecolor='black', linewidth=1.5)

ax.set_xlabel('省錢方案（累積）', fontsize=12, fontweight='bold')
ax.set_ylabel('年節省金額 (USD)', fontsize=12, fontweight='bold')
ax.set_title('各種省錢方案年度效益比較', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for bar, s, inv in zip(bars, savings, investments):
    height = bar.get_height()
    ax.annotate(f'${s}/年', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=12, fontweight='bold')
    if inv > 0:
        ax.annotate(f'投資: ${inv}', xy=(bar.get_x() + bar.get_width()/2, 50),
                    ha='center', fontsize=9, color='gray')

ax.annotate('最佳方案！', xy=(3, 1148), xytext=(2.5, 1200),
            fontsize=12, fontweight='bold', color='purple',
            arrowprops=dict(arrowstyle='->', color='purple'))

plt.tight_layout()
plt.savefig(f'{output_dir}/savings_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: savings_comparison.png")

# ===== 圖表 7：溫度與省錢對照圖（新增）=====
fig, ax = plt.subplots(figsize=(12, 7))

temps_f = [68, 67, 66, 65, 64, 63, 60, 55, 50]
temps_c = [20, 19, 18, 18, 18, 17, 16, 13, 10]
monthly_savings = [0, 10, 20, 31, 41, 51, 82, 133, 184]
yearly_savings = [0, 60, 120, 186, 246, 306, 492, 798, 1104]

# 主軸：月省錢
color1 = '#e74c3c'
ax.bar(range(len(temps_f)), monthly_savings, color=color1, alpha=0.7, edgecolor='black', label='每月節省')

# 標註月省錢金額
for i, (t, m) in enumerate(zip(temps_f, monthly_savings)):
    if m > 0:
        ax.annotate(f'${m}', xy=(i, m), xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=color1)

# 次軸：年省錢
ax2 = ax.twinx()
color2 = '#3498db'
ax2.plot(range(len(temps_f)), yearly_savings, 'o-', color=color2, linewidth=2, markersize=8, label='每年節省')

# 標註年省錢金額
for i, y in enumerate(yearly_savings):
    if y > 0:
        ax2.annotate(f'${y}', xy=(i, y), xytext=(5, 0), textcoords="offset points",
                     ha='left', va='center', fontsize=9, color=color2)

# 設定 X 軸標籤
x_labels = [f'{f}°F\n({c}°C)' for f, c in zip(temps_f, temps_c)]
ax.set_xticks(range(len(temps_f)))
ax.set_xticklabels(x_labels)

ax.set_xlabel('溫度設定', fontsize=12, fontweight='bold')
ax.set_ylabel('每月節省 (USD)', fontsize=12, fontweight='bold', color=color1)
ax2.set_ylabel('每年節省 (USD)', fontsize=12, fontweight='bold', color=color2)

ax.tick_params(axis='y', labelcolor=color1)
ax2.tick_params(axis='y', labelcolor=color2)

ax.set_title('溫度設定與省錢對照：每降 1°F 省 $10/月', fontsize=14, fontweight='bold')

# 合併圖例
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax.grid(axis='y', alpha=0.3)

# 標示建議區間
ax.axvspan(6.5, 8.5, alpha=0.2, color='green')
ax.text(7.5, max(monthly_savings) * 0.9, '建議範圍\n55-50°F', ha='center', fontsize=10, color='green', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/temperature_savings.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: temperature_savings.png")

# ===== 圖表 8：聖誕節休假省錢分析（新增）=====
fig, ax = plt.subplots(figsize=(10, 6))

scenarios = ['維持 68°F\n（不調整）', '降到 60°F', '降到 55°F\n（建議）', '降到 50°F\n（最省）']
daily_cost = [11.00, 7.10, 5.50, 4.00]
total_14_days = [154, 99, 77, 56]
savings_vs_68 = [0, 55, 77, 98]

x = np.arange(len(scenarios))
width = 0.4

colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db']
bars = ax.bar(x, total_14_days, width, color=colors, edgecolor='black', linewidth=1.5)

# 標註 14 天總費用
for bar, cost in zip(bars, total_14_days):
    height = bar.get_height()
    ax.annotate(f'${cost}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=14, fontweight='bold')

# 標註節省金額
for i, (bar, save) in enumerate(zip(bars, savings_vs_68)):
    if save > 0:
        ax.annotate(f'省 ${save}', xy=(bar.get_x() + bar.get_width()/2, 20),
                    ha='center', fontsize=11, color='white', fontweight='bold')

# 標註每日費用
for i, (bar, d) in enumerate(zip(bars, daily_cost)):
    ax.annotate(f'${d}/日', xy=(bar.get_x() + bar.get_width()/2, bar.get_height() + 15),
                ha='center', fontsize=9, color='gray')

ax.set_xlabel('溫度設定', fontsize=12, fontweight='bold')
ax.set_ylabel('14 天總費用 (USD)', fontsize=12, fontweight='bold')
ax.set_title('聖誕節休假 14 天（12/23 - 1/5）省錢分析', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.grid(axis='y', alpha=0.3)

# 標示建議選項
ax.annotate('推薦！', xy=(2, 77), xytext=(2.5, 100),
            fontsize=12, fontweight='bold', color='green',
            arrowprops=dict(arrowstyle='->', color='green'))

plt.tight_layout()
plt.savefig(f'{output_dir}/christmas_vacation_savings.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: christmas_vacation_savings.png")

# ===== 圖表 9：年度省錢總結（新增）=====
fig, ax = plt.subplots(figsize=(12, 7))

categories = ['營業日\n溫控排程', '每週休息日\n(2天×52週)', '聖誕節假期\n(14天)', '密封漏風', '降低 1°F']
annual_savings = [788, 264, 77, 240, 60]
investments = [0, 0, 0, 100, 0]
cumulative = np.cumsum(annual_savings)

colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6']
bars = ax.bar(categories, annual_savings, color=colors, edgecolor='black', linewidth=1.5)

# 標註年省錢
for bar, s in zip(bars, annual_savings):
    height = bar.get_height()
    ax.annotate(f'${s}/年', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=12, fontweight='bold')

# 累積線
ax2 = ax.twinx()
ax2.plot(range(len(categories)), cumulative, 'ko-', linewidth=2, markersize=10)
for i, c in enumerate(cumulative):
    ax2.annotate(f'累積: ${c}', xy=(i, c), xytext=(5, 5), textcoords="offset points",
                 ha='left', va='bottom', fontsize=10, fontweight='bold')

ax.set_xlabel('省錢項目', fontsize=12, fontweight='bold')
ax.set_ylabel('年節省金額 (USD)', fontsize=12, fontweight='bold')
ax2.set_ylabel('累積節省 (USD)', fontsize=12, fontweight='bold')
ax.set_title('年度省錢總結：總計可省 $1,429/年', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# 標註總投資
ax.text(0.98, 0.02, '總投資: $175\n回本期: 1.5 個月', transform=ax.transAxes,
        fontsize=11, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(f'{output_dir}/annual_savings_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: annual_savings_summary.png")

# ===== 圖表 10：溫度安全等級（新增）=====
fig, ax = plt.subplots(figsize=(10, 6))

temps = [68, 65, 60, 55, 50, 45, 40, 32]
labels = ['68°F\n營業', '65°F\n預熱', '60°F\n短休', '55°F\n建議最低', '50°F\n注意', '45°F\n風險', '40°F\n危險', '32°F\n禁止']
risk_colors = ['#27ae60', '#27ae60', '#2ecc71', '#27ae60', '#f39c12', '#e67e22', '#e74c3c', '#c0392b']

bars = ax.barh(range(len(temps)), temps, color=risk_colors, edgecolor='black', linewidth=1.5)

ax.set_yticks(range(len(temps)))
ax.set_yticklabels(labels)
ax.set_xlabel('溫度 (°F)', fontsize=12, fontweight='bold')
ax.set_title('溫度安全等級指南', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# 添加安全區域標示
ax.axvline(x=55, color='green', linestyle='--', linewidth=2, alpha=0.7)
ax.axvline(x=45, color='red', linestyle='--', linewidth=2, alpha=0.7)

ax.text(56, 7.5, '建議最低線', fontsize=10, color='green', fontweight='bold')
ax.text(46, 7.5, '危險警戒線', fontsize=10, color='red', fontweight='bold')

# 標註說明
ax.text(35, 3, '✅ 安全區', fontsize=12, color='green', fontweight='bold')
ax.text(35, 5, '⚠️ 注意區', fontsize=12, color='orange', fontweight='bold')
ax.text(35, 6.5, '🔴 危險區', fontsize=12, color='red', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/temperature_safety.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: temperature_safety.png")

print("\n" + "="*50)
print("所有圖表已生成完成！共 10 張")
print(f"輸出目錄: {output_dir}")
print("="*50)
