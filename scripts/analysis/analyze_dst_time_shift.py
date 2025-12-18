#!/usr/bin/env python3
"""
DST 消費時間偏移分析
分析 10 月和 11 月客戶消費時間是否因冬令時而往前偏移

DST 轉換日：2025 年 11 月 2 日（星期日）
EDT (UTC-4) → EST (UTC-5)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
import seaborn as sns
import json

# 設定中文字體 - 直接設定 rcParams
mpl.rcParams['text.usetex'] = False
mpl.rcParams['axes.unicode_minus'] = False

# 嘗試載入中文字體
FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'
try:
    chinese_font = font_manager.FontProperties(fname=FONT_PATH)
    # 將字體註冊到 matplotlib
    font_manager.fontManager.addfont(FONT_PATH)
    font_name = font_manager.FontProperties(fname=FONT_PATH).get_name()
    mpl.rcParams['font.family'] = [font_name, 'sans-serif']
    print(f"   使用字體：{font_name}")
except Exception as e:
    print(f"   字體載入失敗：{e}")
    chinese_font = font_manager.FontProperties()

# Seaborn 樣式
sns.set_style("whitegrid")
sns.set_palette("husl")

# 路徑設定
BASE_DIR = Path('/Users/lunhsiangyuan/Desktop/square')
DATA_FILE = BASE_DIR / 'data/all_payments/all_payments.csv'
OUTPUT_DIR = BASE_DIR / 'analysis_output/dst_analysis'
CHARTS_DIR = OUTPUT_DIR / 'charts'

# 營業規則
OPERATING_DAYS = [0, 1, 4, 5]  # 週一、二、五、六
OPERATING_HOURS = range(10, 21)  # 10:00-20:00

# NYC 時區
NYC_TZ = ZoneInfo('America/New_York')

def load_and_preprocess_data() -> pd.DataFrame:
    """載入並預處理數據"""
    print("📂 載入數據...")
    df = pd.read_csv(DATA_FILE)

    # 過濾 COMPLETED 交易
    df = df[df['status'] == 'COMPLETED'].copy()
    print(f"   ✓ COMPLETED 交易：{len(df)} 筆")

    # 解析時間並轉換時區
    df['DateTime'] = pd.to_datetime(df['created_at'], utc=True)
    df['DateTime'] = df['DateTime'].dt.tz_convert(NYC_TZ)

    # 提取時間元素
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Month'] = df['DateTime'].dt.month
    df['Date'] = df['DateTime'].dt.date
    df['YearMonth'] = df['DateTime'].dt.to_period('M')

    # 金額處理（amount 欄位已是美元）
    df['Net Sales'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

    # 過濾營業日和營業時間
    df = df[df['DayOfWeek'].isin(OPERATING_DAYS)]
    df = df[df['Hour'].isin(OPERATING_HOURS)]

    print(f"   ✓ 過濾後：{len(df)} 筆")

    return df

def filter_by_month(df: pd.DataFrame, month: int) -> pd.DataFrame:
    """篩選特定月份數據"""
    return df[df['Month'] == month].copy()

def calculate_time_centroid(df: pd.DataFrame) -> float:
    """
    計算消費時間重心（加權平均小時）
    使用營收作為權重
    """
    if df.empty or df['Net Sales'].sum() == 0:
        return np.nan

    weighted_sum = (df['Hour'] * df['Net Sales']).sum()
    total_sales = df['Net Sales'].sum()
    return weighted_sum / total_sales

def calculate_hourly_distribution(df: pd.DataFrame) -> pd.Series:
    """計算每小時營收分布（正規化為百分比）"""
    hourly = df.groupby('Hour')['Net Sales'].sum()
    # 確保所有營業時間都有值
    hourly = hourly.reindex(range(10, 21), fill_value=0)
    return hourly / hourly.sum() * 100

def calculate_transaction_distribution(df: pd.DataFrame) -> pd.Series:
    """計算每小時交易數分布（正規化為百分比）"""
    hourly = df.groupby('Hour').size()
    hourly = hourly.reindex(range(10, 21), fill_value=0)
    return hourly / hourly.sum() * 100

def calculate_cumulative_distribution(distribution: pd.Series) -> pd.Series:
    """計算累積分布（CDF）"""
    return distribution.cumsum()

def perform_ks_test(oct_data: pd.DataFrame, nov_data: pd.DataFrame) -> dict:
    """
    執行 Kolmogorov-Smirnov 檢定
    比較兩個月份的消費時間分布
    """
    # 將每筆交易的小時作為樣本
    oct_hours = oct_data['Hour'].values
    nov_hours = nov_data['Hour'].values

    # K-S 檢定
    statistic, p_value = stats.ks_2samp(oct_hours, nov_hours)

    return {
        'statistic': statistic,
        'p_value': p_value,
        'significant': p_value < 0.05
    }

def calculate_peak_hours(df: pd.DataFrame) -> dict:
    """找出峰值時段"""
    hourly = df.groupby('Hour')['Net Sales'].sum()
    peak_hour = hourly.idxmax()
    peak_revenue = hourly.max()

    # 前三名時段
    top3 = hourly.nlargest(3)

    return {
        'peak_hour': int(peak_hour),
        'peak_revenue': float(peak_revenue),
        'top3_hours': list(top3.index),
        'top3_revenues': list(top3.values)
    }

def calculate_time_band_analysis(df: pd.DataFrame) -> dict:
    """時段分析（上午/午餐/下午/傍晚）"""
    bands = {
        '上午 (10-12)': (10, 12),
        '午餐 (12-14)': (12, 14),
        '下午 (14-16)': (14, 16),
        '傍晚 (16-18)': (16, 18),
        '晚間 (18-20)': (18, 21)
    }

    total_revenue = df['Net Sales'].sum()
    result = {}

    for band_name, (start, end) in bands.items():
        band_df = df[(df['Hour'] >= start) & (df['Hour'] < end)]
        band_revenue = band_df['Net Sales'].sum()
        band_transactions = len(band_df)
        result[band_name] = {
            'revenue': float(band_revenue),
            'percentage': float(band_revenue / total_revenue * 100) if total_revenue > 0 else 0,
            'transactions': int(band_transactions)
        }

    return result

def plot_hourly_comparison(oct_dist: pd.Series, nov_dist: pd.Series,
                           oct_centroid: float, nov_centroid: float):
    """繪製每小時營收分布對比圖"""
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(10, 21)
    width = 0.35

    bars1 = ax.bar(x - width/2, oct_dist.values, width, label='10月 (EDT)',
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width/2, nov_dist.values, width, label='11月 (EST)',
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=0.5)

    # 標記時間重心
    ax.axvline(x=oct_centroid, color='#3498db', linestyle='--', linewidth=2,
               label=f'10月重心: {oct_centroid:.2f}')
    ax.axvline(x=nov_centroid, color='#e74c3c', linestyle='--', linewidth=2,
               label=f'11月重心: {nov_centroid:.2f}')

    ax.set_xlabel('時間 (小時)', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_ylabel('營收佔比 (%)', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_title('10月 vs 11月 每小時營收分布對比\n(DST 轉換：11/2 EDT→EST)',
                 fontsize=14, fontweight='bold', fontproperties=chinese_font)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{h}:00' for h in x], rotation=45)
    ax.legend(loc='upper right', fontsize=10, prop=chinese_font)
    ax.grid(axis='y', alpha=0.3)

    # 添加差異標註
    shift = nov_centroid - oct_centroid
    shift_text = f'時間重心偏移: {shift:+.2f} 小時'
    if shift < 0:
        shift_text += ' (往前偏移)'
    elif shift > 0:
        shift_text += ' (往後偏移)'
    ax.text(0.02, 0.98, shift_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', fontproperties=chinese_font,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'hourly_bar_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ hourly_bar_comparison.png")

def plot_cdf_comparison(oct_dist: pd.Series, nov_dist: pd.Series):
    """繪製累積分布函數（CDF）對比圖"""
    fig, ax = plt.subplots(figsize=(10, 6))

    oct_cdf = calculate_cumulative_distribution(oct_dist)
    nov_cdf = calculate_cumulative_distribution(nov_dist)

    ax.plot(oct_cdf.index, oct_cdf.values, 'o-', color='#3498db', linewidth=2.5,
            markersize=8, label='10月 (EDT)', alpha=0.8)
    ax.plot(nov_cdf.index, nov_cdf.values, 's-', color='#e74c3c', linewidth=2.5,
            markersize=8, label='11月 (EST)', alpha=0.8)

    # 50% 線
    ax.axhline(y=50, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.text(20.2, 50, '50%', fontsize=10, va='center')

    # 填充差異區域
    ax.fill_between(oct_cdf.index, oct_cdf.values, nov_cdf.values,
                    alpha=0.2, color='purple')

    ax.set_xlabel('時間 (小時)', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_ylabel('累積營收佔比 (%)', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    ax.set_title('累積分布函數 (CDF) 對比\n若 11月曲線在左側 → 消費時間往前偏移',
                 fontsize=14, fontweight='bold', fontproperties=chinese_font)
    ax.set_xticks(range(10, 21))
    ax.set_xticklabels([f'{h}:00' for h in range(10, 21)], rotation=45)
    ax.legend(loc='lower right', fontsize=10, prop=chinese_font)
    ax.grid(alpha=0.3)
    ax.set_xlim(9.5, 20.5)
    ax.set_ylim(0, 105)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'cdf_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ cdf_comparison.png")

def plot_difference_heatmap(oct_dist: pd.Series, nov_dist: pd.Series):
    """繪製時間差異熱力圖"""
    fig, ax = plt.subplots(figsize=(14, 3))

    diff = nov_dist - oct_dist
    diff_df = pd.DataFrame([diff.values], columns=[f'{h}:00' for h in range(10, 21)])

    # 使用發散色彩（藍=11月較少，紅=11月較多）
    cmap = sns.diverging_palette(240, 10, as_cmap=True)

    hm = sns.heatmap(diff_df, annot=True, fmt='.1f', cmap=cmap, center=0,
                     ax=ax, linewidths=1, linecolor='white')

    # 設定 colorbar 標籤（使用英文避免字體問題）
    cbar = hm.collections[0].colorbar
    cbar.set_label('Diff %', fontsize=10)

    ax.set_xlabel('Hour', fontsize=12, fontweight='bold')
    ax.set_ylabel('')
    ax.set_title('Nov vs Oct Hourly Revenue Diff (Nov-Oct)\nRed=Nov Higher, Blue=Nov Lower',
                 fontsize=14, fontweight='bold')
    ax.set_yticklabels(['Diff'], rotation=0)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'heatmap_diff.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ heatmap_diff.png")

def plot_time_band_comparison(oct_bands: dict, nov_bands: dict):
    """繪製時段對比圖"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    bands = list(oct_bands.keys())
    oct_pcts = [oct_bands[b]['percentage'] for b in bands]
    nov_pcts = [nov_bands[b]['percentage'] for b in bands]

    # 柱狀圖
    x = np.arange(len(bands))
    width = 0.35

    bars1 = axes[0].bar(x - width/2, oct_pcts, width, label='10月',
                        color='#3498db', alpha=0.8)
    bars2 = axes[0].bar(x + width/2, nov_pcts, width, label='11月',
                        color='#e74c3c', alpha=0.8)

    axes[0].set_ylabel('營收佔比 (%)', fontsize=11, fontweight='bold', fontproperties=chinese_font)
    axes[0].set_title('時段營收佔比對比', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(bands, rotation=30, ha='right', fontsize=9, fontproperties=chinese_font)
    axes[0].legend(prop=chinese_font)
    axes[0].grid(axis='y', alpha=0.3)

    # 添加數值標籤
    for bar, pct in zip(bars1, oct_pcts):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{pct:.1f}%', ha='center', va='bottom', fontsize=8)
    for bar, pct in zip(bars2, nov_pcts):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{pct:.1f}%', ha='center', va='bottom', fontsize=8)

    # 差異圖
    diff_pcts = [nov_pcts[i] - oct_pcts[i] for i in range(len(bands))]
    colors = ['#e74c3c' if d > 0 else '#3498db' for d in diff_pcts]

    bars3 = axes[1].bar(x, diff_pcts, color=colors, alpha=0.8, edgecolor='black')
    axes[1].axhline(y=0, color='black', linewidth=0.5)
    axes[1].set_ylabel('佔比變化 (百分點)', fontsize=11, fontweight='bold', fontproperties=chinese_font)
    axes[1].set_title('11月相對10月的時段佔比變化', fontsize=12, fontweight='bold', fontproperties=chinese_font)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(bands, rotation=30, ha='right', fontsize=9, fontproperties=chinese_font)
    axes[1].grid(axis='y', alpha=0.3)

    # 添加數值標籤
    for bar, diff in zip(bars3, diff_pcts):
        va = 'bottom' if diff >= 0 else 'top'
        offset = 0.2 if diff >= 0 else -0.2
        axes[1].text(bar.get_x() + bar.get_width()/2, diff + offset,
                    f'{diff:+.1f}', ha='center', va=va, fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'time_band_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ time_band_comparison.png")

def generate_report(analysis_results: dict):
    """生成 Markdown 分析報告"""
    report = f"""# DST 消費時間偏移分析報告

**分析目的**：研究冬令時轉換（11月2日）是否影響客戶消費時間

**報告生成時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. 分析背景

### 1.1 冬令時轉換
- **轉換日期**：2025 年 11 月 2 日（星期日）
- **時區變化**：EDT (UTC-4) → EST (UTC-5)
- **影響**：天黑時間提早約 1 小時

### 1.2 分析假說
- **H0（虛無假說）**：10 月和 11 月的消費時間分布無顯著差異
- **H1（對立假說）**：11 月的消費時間往前偏移（重心較早）

---

## 2. 數據摘要

### 2.1 數據範圍

| 指標 | 10 月 | 11 月 |
|------|-------|-------|
| 交易筆數 | {analysis_results['october']['total_transactions']:,} | {analysis_results['november']['total_transactions']:,} |
| 營收總額 | ${analysis_results['october']['total_revenue']:,.2f} | ${analysis_results['november']['total_revenue']:,.2f} |
| 營業天數 | {analysis_results['october']['operating_days']} | {analysis_results['november']['operating_days']} |
| 日均交易 | {analysis_results['october']['avg_daily_transactions']:.1f} | {analysis_results['november']['avg_daily_transactions']:.1f} |

### 2.2 時間範圍
- **10 月**：{analysis_results['october']['date_range']['start']} ~ {analysis_results['october']['date_range']['end']}
- **11 月**：{analysis_results['november']['date_range']['start']} ~ {analysis_results['november']['date_range']['end']}

---

## 3. 時間重心分析

### 3.1 消費時間重心（加權平均小時）

| 月份 | 時間重心 | 說明 |
|------|----------|------|
| 10 月 | **{analysis_results['october']['time_centroid']:.2f}** | {analysis_results['october']['time_centroid_time']} |
| 11 月 | **{analysis_results['november']['time_centroid']:.2f}** | {analysis_results['november']['time_centroid_time']} |
| **偏移量** | **{analysis_results['centroid_shift']:+.2f} 小時** | {analysis_results['shift_direction']} |

### 3.2 解讀
{analysis_results['centroid_interpretation']}

---

## 4. 峰值時段分析

### 4.1 峰值小時

| 月份 | 峰值時段 | 峰值營收 |
|------|----------|----------|
| 10 月 | {analysis_results['october']['peak']['peak_hour']}:00 | ${analysis_results['october']['peak']['peak_revenue']:,.2f} |
| 11 月 | {analysis_results['november']['peak']['peak_hour']}:00 | ${analysis_results['november']['peak']['peak_revenue']:,.2f} |

### 4.2 峰值偏移
- **偏移量**：{analysis_results['peak_shift']:+d} 小時
- **結論**：{analysis_results['peak_interpretation']}

---

## 5. 時段佔比分析

### 5.1 各時段營收佔比

| 時段 | 10 月 | 11 月 | 變化 |
|------|-------|-------|------|
"""

    # 添加時段分析表格
    for band in analysis_results['october']['time_bands'].keys():
        oct_pct = analysis_results['october']['time_bands'][band]['percentage']
        nov_pct = analysis_results['november']['time_bands'][band]['percentage']
        change = nov_pct - oct_pct
        change_str = f"{change:+.1f}" if change != 0 else "0.0"
        report += f"| {band} | {oct_pct:.1f}% | {nov_pct:.1f}% | {change_str}% |\n"

    report += f"""
### 5.2 時段變化解讀
{analysis_results['time_band_interpretation']}

---

## 6. 統計檢定

### 6.1 Kolmogorov-Smirnov 檢定

| 指標 | 數值 |
|------|------|
| K-S 統計量 | {analysis_results['ks_test']['statistic']:.4f} |
| p 值 | {analysis_results['ks_test']['p_value']:.4f} |
| 顯著性 (α=0.05) | {'**顯著**' if analysis_results['ks_test']['significant'] else '不顯著'} |

### 6.2 統計結論
{analysis_results['statistical_conclusion']}

---

## 7. 視覺化圖表

### 7.1 每小時營收分布對比
![每小時營收分布](charts/hourly_bar_comparison.png)

### 7.2 累積分布函數 (CDF)
![CDF 對比](charts/cdf_comparison.png)

### 7.3 時間差異熱力圖
![差異熱力圖](charts/heatmap_diff.png)

### 7.4 時段對比分析
![時段對比](charts/time_band_comparison.png)

---

## 8. 結論與建議

### 8.1 主要發現

{analysis_results['main_findings']}

### 8.2 業務建議

{analysis_results['recommendations']}

### 8.3 分析限制

1. **無法追蹤個別客戶**：`customer_id` 欄位大多為空，無法分析同一客戶的行為變化
2. **樣本量差異**：10 月和 11 月的營業天數可能不同
3. **混淆變數**：季節性因素、天氣變化、節日（感恩節前夕）等可能影響結果
4. **DST 轉換日**：11 月 2 日為週日，非營業日，無法觀察轉換當日影響

---

*報告生成：Claude Code Agent System - DST Analysis Module*
"""

    # 寫入報告
    with open(OUTPUT_DIR / 'dst_time_shift_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("   ✓ 已生成：dst_time_shift_report.md")

def save_hourly_comparison(oct_dist: pd.Series, nov_dist: pd.Series,
                           oct_trans: pd.Series, nov_trans: pd.Series):
    """儲存每小時比較數據為 CSV"""
    comparison_df = pd.DataFrame({
        'Hour': range(10, 21),
        'Oct_Revenue_Pct': oct_dist.values,
        'Nov_Revenue_Pct': nov_dist.values,
        'Revenue_Diff': (nov_dist - oct_dist).values,
        'Oct_Transaction_Pct': oct_trans.values,
        'Nov_Transaction_Pct': nov_trans.values,
        'Transaction_Diff': (nov_trans - oct_trans).values
    })

    comparison_df.to_csv(OUTPUT_DIR / 'hourly_comparison.csv', index=False)
    print("   ✓ 已生成：hourly_comparison.csv")

def generate_interpretation(analysis_results: dict) -> dict:
    """生成分析解讀"""
    shift = analysis_results['centroid_shift']

    # 時間重心解讀
    if shift < -0.3:
        shift_direction = "⬅️ 往前偏移（提早消費）"
        centroid_interpretation = f"""
11 月的消費時間重心比 10 月提早了 **{abs(shift):.2f} 小時**。

這可能與冬令時開始後天黑提早有關：
- 冬令時後，17:00 左右天色已暗，客戶可能傾向更早用餐
- 下班後天黑的心理效應可能促使客戶提前消費
"""
    elif shift > 0.3:
        shift_direction = "➡️ 往後偏移（延後消費）"
        centroid_interpretation = f"""
11 月的消費時間重心比 10 月延後了 **{shift:.2f} 小時**。

這與冬令時的預期影響相反，可能原因：
- 11 月接近感恩節，客戶用餐習慣可能改變
- 天氣變化或其他季節性因素影響
"""
    else:
        shift_direction = "↔️ 無明顯偏移"
        centroid_interpretation = f"""
兩個月份的消費時間重心差異很小（僅 {abs(shift):.2f} 小時）。

冬令時轉換對整體消費時間模式的影響不顯著，客戶的用餐時間習慣相對穩定。
"""

    analysis_results['shift_direction'] = shift_direction
    analysis_results['centroid_interpretation'] = centroid_interpretation

    # 峰值解讀
    peak_shift = analysis_results['peak_shift']
    if peak_shift < 0:
        peak_interpretation = f"峰值時段提前了 {abs(peak_shift)} 小時，支持消費時間往前偏移的假說"
    elif peak_shift > 0:
        peak_interpretation = f"峰值時段延後了 {peak_shift} 小時，與預期相反"
    else:
        peak_interpretation = "峰值時段沒有變化"

    analysis_results['peak_interpretation'] = peak_interpretation

    # 時段變化解讀
    oct_bands = analysis_results['october']['time_bands']
    nov_bands = analysis_results['november']['time_bands']

    morning_change = nov_bands['上午 (10-12)']['percentage'] - oct_bands['上午 (10-12)']['percentage']
    evening_change = nov_bands['晚間 (18-20)']['percentage'] - oct_bands['晚間 (18-20)']['percentage']

    time_band_interpretation = ""
    if morning_change > 1 and evening_change < -1:
        time_band_interpretation = f"""
觀察到明顯的「早移」現象：
- 上午時段 (10-12) 佔比增加 {morning_change:+.1f}%
- 晚間時段 (18-20) 佔比減少 {evening_change:+.1f}%

這符合冬令時後「天黑提早」的假設，客戶傾向在天黑前完成消費。
"""
    elif evening_change > 1:
        time_band_interpretation = f"""
晚間時段佔比反而增加 ({evening_change:+.1f}%)，這與冬令時預期效應相反。

可能原因：
- 11 月的特殊節日效應
- 樣本量差異
- 其他混淆因素
"""
    else:
        time_band_interpretation = f"""
各時段的佔比變化不大，消費時間模式在兩個月份間相對穩定。

- 上午變化：{morning_change:+.1f}%
- 晚間變化：{evening_change:+.1f}%
"""

    analysis_results['time_band_interpretation'] = time_band_interpretation

    # 統計結論
    ks = analysis_results['ks_test']
    if ks['significant']:
        statistical_conclusion = f"""
K-S 檢定結果顯示 **統計顯著** (p = {ks['p_value']:.4f} < 0.05)。

10 月和 11 月的消費時間分布存在顯著差異，虛無假說被拒絕。
"""
    else:
        statistical_conclusion = f"""
K-S 檢定結果 **不顯著** (p = {ks['p_value']:.4f} > 0.05)。

無法在 α=0.05 顯著水準下拒絕虛無假說，兩月份的時間分布差異不具統計顯著性。
"""

    analysis_results['statistical_conclusion'] = statistical_conclusion

    # 主要發現
    findings = []
    if abs(shift) > 0.2:
        findings.append(f"1. 消費時間重心{shift_direction}，偏移 {abs(shift):.2f} 小時")
    else:
        findings.append(f"1. 消費時間重心無明顯偏移（僅 {abs(shift):.2f} 小時）")

    if ks['significant']:
        findings.append("2. K-S 檢定顯示兩月份時間分布存在顯著差異")
    else:
        findings.append("2. K-S 檢定未發現統計顯著差異")

    if peak_shift != 0:
        findings.append(f"3. 峰值時段從 {analysis_results['october']['peak']['peak_hour']}:00 變為 {analysis_results['november']['peak']['peak_hour']}:00")
    else:
        findings.append(f"3. 峰值時段維持在 {analysis_results['october']['peak']['peak_hour']}:00")

    analysis_results['main_findings'] = '\n'.join(findings)

    # 業務建議
    recommendations = []
    if shift < -0.3:
        recommendations.append("1. **人力調配**：考慮在冬季將人力配置往前移動，加強上午和午餐時段")
        recommendations.append("2. **促銷策略**：針對下午時段設計優惠，吸引冬季客戶延長消費時間")
    elif shift > 0.3:
        recommendations.append("1. **人力調配**：維持現有配置或加強晚間時段")
    else:
        recommendations.append("1. **維持現狀**：消費模式穩定，無需大幅調整營運時間")

    recommendations.append("2. **持續監控**：建議觀察整個冬季（11-2月）的變化趨勢")
    recommendations.append("3. **明年對比**：記錄今年數據，與明年同期比較以驗證假說")

    analysis_results['recommendations'] = '\n'.join(recommendations)

    return analysis_results

def main():
    """主執行函數"""
    print("=" * 60)
    print("🕐 DST 消費時間偏移分析")
    print("=" * 60)

    # Phase 1: 數據準備
    print("\n📊 Phase 1: 數據準備")
    df = load_and_preprocess_data()

    # 分離 10 月和 11 月數據
    df_oct = filter_by_month(df, 10)
    df_nov = filter_by_month(df, 11)

    print(f"   ✓ 10 月數據：{len(df_oct)} 筆")
    print(f"   ✓ 11 月數據：{len(df_nov)} 筆")

    # Phase 2: 統計分析
    print("\n📈 Phase 2: 統計分析")

    # 時間重心計算
    oct_centroid = calculate_time_centroid(df_oct)
    nov_centroid = calculate_time_centroid(df_nov)
    centroid_shift = nov_centroid - oct_centroid

    print(f"   ✓ 10 月時間重心：{oct_centroid:.2f}")
    print(f"   ✓ 11 月時間重心：{nov_centroid:.2f}")
    print(f"   ✓ 偏移量：{centroid_shift:+.2f} 小時")

    # 每小時分布計算
    oct_revenue_dist = calculate_hourly_distribution(df_oct)
    nov_revenue_dist = calculate_hourly_distribution(df_nov)
    oct_trans_dist = calculate_transaction_distribution(df_oct)
    nov_trans_dist = calculate_transaction_distribution(df_nov)

    # K-S 檢定
    ks_result = perform_ks_test(df_oct, df_nov)
    print(f"   ✓ K-S 統計量：{ks_result['statistic']:.4f}")
    print(f"   ✓ p 值：{ks_result['p_value']:.4f}")
    print(f"   ✓ 顯著性：{'是' if ks_result['significant'] else '否'}")

    # 峰值分析
    oct_peak = calculate_peak_hours(df_oct)
    nov_peak = calculate_peak_hours(df_nov)
    peak_shift = nov_peak['peak_hour'] - oct_peak['peak_hour']

    print(f"   ✓ 10 月峰值：{oct_peak['peak_hour']}:00")
    print(f"   ✓ 11 月峰值：{nov_peak['peak_hour']}:00")

    # 時段分析
    oct_bands = calculate_time_band_analysis(df_oct)
    nov_bands = calculate_time_band_analysis(df_nov)

    # 組織分析結果
    def to_time_str(centroid):
        hours = int(centroid)
        minutes = int((centroid - hours) * 60)
        return f"{hours}:{minutes:02d}"

    analysis_results = {
        'october': {
            'total_transactions': len(df_oct),
            'total_revenue': float(df_oct['Net Sales'].sum()),
            'operating_days': df_oct['Date'].nunique(),
            'avg_daily_transactions': len(df_oct) / max(df_oct['Date'].nunique(), 1),
            'date_range': {
                'start': str(df_oct['Date'].min()),
                'end': str(df_oct['Date'].max())
            },
            'time_centroid': oct_centroid,
            'time_centroid_time': to_time_str(oct_centroid),
            'peak': oct_peak,
            'time_bands': oct_bands
        },
        'november': {
            'total_transactions': len(df_nov),
            'total_revenue': float(df_nov['Net Sales'].sum()),
            'operating_days': df_nov['Date'].nunique(),
            'avg_daily_transactions': len(df_nov) / max(df_nov['Date'].nunique(), 1),
            'date_range': {
                'start': str(df_nov['Date'].min()),
                'end': str(df_nov['Date'].max())
            },
            'time_centroid': nov_centroid,
            'time_centroid_time': to_time_str(nov_centroid),
            'peak': nov_peak,
            'time_bands': nov_bands
        },
        'centroid_shift': centroid_shift,
        'peak_shift': peak_shift,
        'ks_test': ks_result
    }

    # 生成解讀
    analysis_results = generate_interpretation(analysis_results)

    # Phase 3: 視覺化
    print("\n🎨 Phase 3: 視覺化")
    plot_hourly_comparison(oct_revenue_dist, nov_revenue_dist, oct_centroid, nov_centroid)
    plot_cdf_comparison(oct_revenue_dist, nov_revenue_dist)
    plot_difference_heatmap(oct_revenue_dist, nov_revenue_dist)
    plot_time_band_comparison(oct_bands, nov_bands)

    # 儲存數據
    print("\n💾 儲存結果")
    save_hourly_comparison(oct_revenue_dist, nov_revenue_dist, oct_trans_dist, nov_trans_dist)

    # 儲存 JSON 結果
    with open(OUTPUT_DIR / 'analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=str)
    print("   ✓ 已生成：analysis_results.json")

    # 生成報告
    generate_report(analysis_results)

    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print(f"   報告位置：{OUTPUT_DIR}")
    print("=" * 60)

    # 輸出摘要
    print(f"\n📋 分析摘要：")
    print(f"   • 時間重心偏移：{centroid_shift:+.2f} 小時 ({analysis_results['shift_direction']})")
    print(f"   • K-S 檢定：{'顯著' if ks_result['significant'] else '不顯著'} (p={ks_result['p_value']:.4f})")
    print(f"   • 峰值變化：{oct_peak['peak_hour']}:00 → {nov_peak['peak_hour']}:00")

    return analysis_results

if __name__ == "__main__":
    results = main()
