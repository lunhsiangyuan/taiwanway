#!/usr/bin/env python3
"""
TaiwanWay 餐廳能源帳單視覺化圖表生成腳本
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

# 標註數值
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

# 標註
for i, (bar, val) in enumerate(zip(bars, gas)):
    ax.annotate(f'${val:.0f}', xy=(bar.get_x() + bar.get_width()/2, val),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=11, fontweight='bold')

# 添加分區說明
ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
ax.text(0.5, 40, '夏季（無暖氣）~$30/月', fontsize=10, color='#27ae60')
ax.text(4.2, 280, '冬季（暖氣）', fontsize=10, color='#c0392b')
ax.text(4.2, 250, '$182-$375/月', fontsize=10, color='#c0392b')

# 添加箭頭標示增幅
ax.annotate('', xy=(5, 375), xytext=(2, 32),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(3.5, 180, '12倍增長！', fontsize=12, color='red', fontweight='bold', rotation=45)

plt.tight_layout()
plt.savefig(f'{output_dir}/gas_seasonal.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: gas_seasonal.png")

# ===== 圖表 3：溫控排程視覺化 =====
fig, ax = plt.subplots(figsize=(14, 6))

# 時間軸（24小時）
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

# 標示區域
ax.axvspan(0, 6.5, alpha=0.1, color='blue', label='休息時段')
ax.axvspan(6.5, 8, alpha=0.1, color='yellow', label='預熱時段')
ax.axvspan(8, 19, alpha=0.1, color='green', label='營業時段')
ax.axvspan(19, 19.5, alpha=0.1, color='yellow')
ax.axvspan(19.5, 24, alpha=0.1, color='blue')

# 標註溫度
ax.annotate('55°F\n(13°C)', xy=(3, 55), xytext=(3, 58), fontsize=11, ha='center', fontweight='bold')
ax.annotate('65°F\n(18°C)', xy=(7.25, 65), xytext=(7.25, 68), fontsize=11, ha='center', fontweight='bold')
ax.annotate('68°F\n(20°C)', xy=(13.5, 68), xytext=(13.5, 71), fontsize=11, ha='center', fontweight='bold')

# 標註時間點
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

# 標註差異百分比
diffs = [(c-r)/r*100 for c, r in zip(commercial, residential)]
for i, (c, r, d) in enumerate(zip(commercial, residential, diffs)):
    ax.annotate(f'+{d:.0f}%', xy=(i, max(c, r) + 20), ha='center',
                fontsize=11, fontweight='bold', color='red')

# 標註金額
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

# 標註金額
for bar, s, inv in zip(bars, savings, investments):
    height = bar.get_height()
    ax.annotate(f'${s}/年', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=12, fontweight='bold')
    if inv > 0:
        ax.annotate(f'投資: ${inv}', xy=(bar.get_x() + bar.get_width()/2, 50),
                    ha='center', fontsize=9, color='gray')

# 標示最佳方案
ax.annotate('最佳方案！', xy=(3, 1148), xytext=(2.5, 1200),
            fontsize=12, fontweight='bold', color='purple',
            arrowprops=dict(arrowstyle='->', color='purple'))

plt.tight_layout()
plt.savefig(f'{output_dir}/savings_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 已生成: savings_comparison.png")

print("\n" + "="*50)
print("所有圖表已生成完成！")
print(f"輸出目錄: {output_dir}")
print("="*50)
