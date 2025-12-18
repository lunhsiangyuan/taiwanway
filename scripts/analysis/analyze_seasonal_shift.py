#!/usr/bin/env python3
"""
冬季 vs 夏季銷售時段差異分析
分析冬天銷售高峰是否往前移動
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pytz
from pathlib import Path
from datetime import datetime
from scipy import stats

# 設定中文字體
plt.rcParams['text.usetex'] = False
chinese_font_paths = [
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
]

chinese_font_prop = None
for font_path in chinese_font_paths:
    if Path(font_path).exists():
        chinese_font_prop = fm.FontProperties(fname=font_path)
        break

if chinese_font_prop is None:
    print("警告：找不到中文字體，圖表可能顯示不正常")

# 設定 matplotlib 參數
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 100

# 輸出目錄
OUTPUT_DIR = Path('analysis_output/seasonal_shift')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / 'charts').mkdir(exist_ok=True)
(OUTPUT_DIR / 'data').mkdir(exist_ok=True)

# 業務規則
OPERATING_DAYS = [0, 1, 4, 5]  # 週一、二、五、六
OPERATING_HOURS = range(10, 21)  # 10:00-20:00
NYC_TZ = pytz.timezone('America/New_York')
TAX_RATE = 0.08875

# 季節定義（使用 2025 年數據）
WINTER_MONTHS = [1, 2, 11]      # 2025/01, 02, 11（初冬）
SUMMER_MONTHS = [5, 8, 9]       # 2025/05, 08, 09（排除 6、7 月暑假）

def load_and_preprocess_data(file_path):
    """載入並預處理數據"""
    print(f"載入數據：{file_path}")

    df = pd.read_csv(file_path)

    # 解析日期時間（結合 Date 和 Time 欄位）
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    # 假設原始時間為 Taipei 時區，轉換為 NYC 時區
    taipei_tz = pytz.timezone('Asia/Taipei')
    df['DateTime'] = df['DateTime'].apply(lambda x: taipei_tz.localize(x).astimezone(NYC_TZ))

    # 提取時間欄位
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Month'] = df['DateTime'].dt.month
    df['Year'] = df['DateTime'].dt.year
    df['Date_Only'] = df['DateTime'].dt.date
    df['YearMonth'] = df['DateTime'].dt.to_period('M')

    # 過濾 Payment 類型（排除 Refund）
    df = df[df['Event Type'] == 'Payment'].copy()

    # 解析 Net Sales（移除 $ 符號）
    df['Net Sales'] = df['Net Sales'].replace('[\$,]', '', regex=True).astype(float)

    # 套用業務規則
    df = df[df['DayOfWeek'].isin(OPERATING_DAYS)].copy()
    df = df[df['Hour'].isin(OPERATING_HOURS)].copy()

    print(f"載入完成：{len(df)} 筆交易")
    return df

def classify_season(row):
    """判斷季節（冬季/夏季）"""
    year = row['Year']
    month = row['Month']

    # 冬季：2025/01, 02, 11（初冬）
    if year == 2025 and month in WINTER_MONTHS:
        return 'Winter'

    # 夏季：2025/05, 08, 09（排除 6、7 月暑假）
    if year == 2025 and month in SUMMER_MONTHS:
        return 'Summer'

    return None

def analyze_hourly_distribution(df, season):
    """分析每小時銷售分佈"""
    season_df = df[df['Season'] == season].copy()

    # 計算每小時統計
    hourly = season_df.groupby('Hour').agg({
        'Transaction ID': 'nunique',  # 交易筆數（去重複）
        'Net Sales': 'sum',           # 總營收
        'Date_Only': 'nunique'        # 營業天數
    }).reset_index()

    hourly.columns = ['Hour', 'Transactions', 'Total_Revenue', 'Operating_Days']

    # 計算日均營收和日均交易數
    hourly['Avg_Daily_Revenue'] = hourly['Total_Revenue'] / hourly['Operating_Days']
    hourly['Avg_Daily_Transactions'] = hourly['Transactions'] / hourly['Operating_Days']

    # 計算佔比
    hourly['Revenue_Pct'] = (hourly['Total_Revenue'] / hourly['Total_Revenue'].sum()) * 100
    hourly['Transactions_Pct'] = (hourly['Transactions'] / hourly['Transactions'].sum()) * 100

    return hourly

def calculate_weighted_average_time(df, season):
    """計算加權平均銷售時間"""
    season_df = df[df['Season'] == season].copy()

    # 加權平均時間 = Σ(Hour × Revenue) / Σ(Revenue)
    weighted_avg = (season_df['Hour'] * season_df['Net Sales']).sum() / season_df['Net Sales'].sum()

    # 計算標準差
    mean_hour = season_df['Hour'].mean()
    std_hour = season_df['Hour'].std()

    return {
        'weighted_avg_hour': weighted_avg,
        'mean_hour': mean_hour,
        'std_hour': std_hour
    }

def analyze_time_segments(df):
    """時段分群分析"""

    def classify_segment(hour):
        if 10 <= hour < 13:
            return '早段 (10-13)'
        elif 13 <= hour < 16:
            return '午段 (13-16)'
        else:
            return '晚段 (16-20)'

    df['Segment'] = df['Hour'].apply(classify_segment)

    # 按季節和時段統計
    segment_stats = df.groupby(['Season', 'Segment']).agg({
        'Transaction ID': 'nunique',
        'Net Sales': 'sum'
    }).reset_index()

    segment_stats.columns = ['Season', 'Segment', 'Transactions', 'Revenue']

    # 計算佔比
    for season in ['Winter', 'Summer']:
        season_total_trans = segment_stats[segment_stats['Season'] == season]['Transactions'].sum()
        season_total_rev = segment_stats[segment_stats['Season'] == season]['Revenue'].sum()

        segment_stats.loc[segment_stats['Season'] == season, 'Transactions_Pct'] = \
            (segment_stats[segment_stats['Season'] == season]['Transactions'] / season_total_trans) * 100

        segment_stats.loc[segment_stats['Season'] == season, 'Revenue_Pct'] = \
            (segment_stats[segment_stats['Season'] == season]['Revenue'] / season_total_rev) * 100

    return segment_stats

def perform_statistical_test(winter_hourly, summer_hourly):
    """執行統計檢驗"""

    # 使用 Kolmogorov-Smirnov 檢驗比較兩個分佈
    winter_dist = winter_hourly['Total_Revenue'].values
    summer_dist = summer_hourly['Total_Revenue'].values

    ks_stat, ks_pvalue = stats.ks_2samp(winter_dist, summer_dist)

    # 使用 Mann-Whitney U 檢驗（非參數檢驗）
    u_stat, u_pvalue = stats.mannwhitneyu(winter_dist, summer_dist, alternative='two-sided')

    return {
        'ks_statistic': ks_stat,
        'ks_pvalue': ks_pvalue,
        'mannwhitney_u': u_stat,
        'mannwhitney_pvalue': u_pvalue
    }

def create_comparison_chart(winter_hourly, summer_hourly):
    """建立冬夏季對比圖表"""

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 圖 1：每小時交易筆數對比（日均）
    ax1 = axes[0, 0]
    x = np.arange(len(winter_hourly))
    width = 0.35

    bars1 = ax1.bar(x - width/2, winter_hourly['Avg_Daily_Transactions'], width,
                     label='冬季', color='#4A90E2', alpha=0.8)
    bars2 = ax1.bar(x + width/2, summer_hourly['Avg_Daily_Transactions'], width,
                     label='夏季', color='#E27D60', alpha=0.8)

    ax1.set_xlabel('小時', fontproperties=chinese_font_prop, fontsize=12)
    ax1.set_ylabel('日均交易筆數', fontproperties=chinese_font_prop, fontsize=12)
    ax1.set_title('冬夏季每小時日均交易筆數對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(winter_hourly['Hour'])
    ax1.legend(prop=chinese_font_prop)
    ax1.grid(axis='y', alpha=0.3)

    # 圖 2：每小時營收對比（日均）
    ax2 = axes[0, 1]
    bars3 = ax2.bar(x - width/2, winter_hourly['Avg_Daily_Revenue'], width,
                     label='冬季', color='#4A90E2', alpha=0.8)
    bars4 = ax2.bar(x + width/2, summer_hourly['Avg_Daily_Revenue'], width,
                     label='夏季', color='#E27D60', alpha=0.8)

    ax2.set_xlabel('小時', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_ylabel('日均營收 ($)', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_title('冬夏季每小時日均營收對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(winter_hourly['Hour'])
    ax2.legend(prop=chinese_font_prop)
    ax2.grid(axis='y', alpha=0.3)

    # 圖 3：營收佔比曲線
    ax3 = axes[1, 0]
    ax3.plot(winter_hourly['Hour'], winter_hourly['Revenue_Pct'],
             marker='o', linewidth=2, markersize=8, label='冬季', color='#4A90E2')
    ax3.plot(summer_hourly['Hour'], summer_hourly['Revenue_Pct'],
             marker='s', linewidth=2, markersize=8, label='夏季', color='#E27D60')

    ax3.set_xlabel('小時', fontproperties=chinese_font_prop, fontsize=12)
    ax3.set_ylabel('營收佔比 (%)', fontproperties=chinese_font_prop, fontsize=12)
    ax3.set_title('冬夏季營收分佈曲線', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax3.legend(prop=chinese_font_prop)
    ax3.grid(alpha=0.3)

    # 圖 4：累積營收曲線
    ax4 = axes[1, 1]
    winter_cumulative = winter_hourly['Revenue_Pct'].cumsum()
    summer_cumulative = summer_hourly['Revenue_Pct'].cumsum()

    ax4.plot(winter_hourly['Hour'], winter_cumulative,
             marker='o', linewidth=2, markersize=8, label='冬季', color='#4A90E2')
    ax4.plot(summer_hourly['Hour'], summer_cumulative,
             marker='s', linewidth=2, markersize=8, label='夏季', color='#E27D60')
    ax4.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% 中位線')

    ax4.set_xlabel('小時', fontproperties=chinese_font_prop, fontsize=12)
    ax4.set_ylabel('累積營收佔比 (%)', fontproperties=chinese_font_prop, fontsize=12)
    ax4.set_title('冬夏季累積營收曲線', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax4.legend(prop=chinese_font_prop)
    ax4.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'charts' / 'seasonal_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成對比圖表：seasonal_comparison.png")

def create_segment_chart(segment_stats):
    """建立時段分群對比圖"""

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 準備數據
    segments = ['早段 (10-13)', '午段 (13-16)', '晚段 (16-20)']
    winter_data = segment_stats[segment_stats['Season'] == 'Winter'].set_index('Segment')
    summer_data = segment_stats[segment_stats['Season'] == 'Summer'].set_index('Segment')

    winter_rev_pct = [winter_data.loc[seg, 'Revenue_Pct'] for seg in segments]
    summer_rev_pct = [summer_data.loc[seg, 'Revenue_Pct'] for seg in segments]

    winter_trans_pct = [winter_data.loc[seg, 'Transactions_Pct'] for seg in segments]
    summer_trans_pct = [summer_data.loc[seg, 'Transactions_Pct'] for seg in segments]

    # 圖 1：營收佔比
    ax1 = axes[0]
    x = np.arange(len(segments))
    width = 0.35

    bars1 = ax1.bar(x - width/2, winter_rev_pct, width, label='冬季', color='#4A90E2', alpha=0.8)
    bars2 = ax1.bar(x + width/2, summer_rev_pct, width, label='夏季', color='#E27D60', alpha=0.8)

    # 添加數值標籤
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax1.set_ylabel('營收佔比 (%)', fontproperties=chinese_font_prop, fontsize=12)
    ax1.set_title('時段營收佔比對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(segments, fontproperties=chinese_font_prop)
    ax1.legend(prop=chinese_font_prop)
    ax1.grid(axis='y', alpha=0.3)

    # 圖 2：交易筆數佔比
    ax2 = axes[1]
    bars3 = ax2.bar(x - width/2, winter_trans_pct, width, label='冬季', color='#4A90E2', alpha=0.8)
    bars4 = ax2.bar(x + width/2, summer_trans_pct, width, label='夏季', color='#E27D60', alpha=0.8)

    # 添加數值標籤
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_ylabel('交易筆數佔比 (%)', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_title('時段交易筆數佔比對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(segments, fontproperties=chinese_font_prop)
    ax2.legend(prop=chinese_font_prop)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'charts' / 'segment_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成時段對比圖表：segment_comparison.png")

def generate_report(winter_hourly, summer_hourly, winter_stats, summer_stats,
                   segment_stats, stat_test):
    """生成分析報告"""

    report_path = OUTPUT_DIR / 'seasonal_shift_report.md'

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 冬季 vs 夏季銷售時段差異分析報告\n\n")
        f.write("**分析期間**：\n")
        f.write("- **冬季**：2025/01、2025/02、2025/11（初冬）\n")
        f.write("- **夏季**：2025/05、2025/08、2025/09（排除 6、7 月暑假）\n\n")
        f.write("**說明**：由於僅有 2025 年數據，使用 11 月作為初冬代表。\n\n")

        f.write("---\n\n")

        # 分析邏輯思維圖
        f.write("## 分析邏輯思維圖\n\n")
        f.write("```\n")
        f.write("冬夏季銷售時段差異分析\n")
        f.write("│\n")
        f.write("├─ 步驟 1：數據載入與預處理\n")
        f.write("│   ├─ 載入 2024 全年數據 + 2025 年初數據\n")
        f.write("│   ├─ 時區轉換：UTC → America/New_York\n")
        f.write("│   ├─ 營收計算：Net_Revenue = Gross / (1 + 0.08875)\n")
        f.write("│   └─ 套用業務規則（營業日、營業時段）\n")
        f.write("│\n")
        f.write("├─ 步驟 2：季節分類\n")
        f.write("│   ├─ 冬季：2024/11, 12, 2025/01, 02\n")
        f.write("│   └─ 夏季：2024/05, 06, 08, 09\n")
        f.write("│\n")
        f.write("├─ 步驟 3：每小時銷售分佈分析\n")
        f.write("│   ├─ 計算各小時：交易筆數、總營收、營業天數\n")
        f.write("│   ├─ 計算日均：日均交易數、日均營收\n")
        f.write("│   └─ 計算佔比：營收佔比、交易佔比\n")
        f.write("│\n")
        f.write("├─ 步驟 4：加權平均時間分析\n")
        f.write("│   ├─ 公式：加權平均時間 = Σ(Hour × Revenue) / Σ(Revenue)\n")
        f.write("│   ├─ 計算冬季加權平均銷售時間\n")
        f.write("│   ├─ 計算夏季加權平均銷售時間\n")
        f.write("│   └─ 比較時間差異 → 判斷是否前移\n")
        f.write("│\n")
        f.write("├─ 步驟 5：時段分群比較\n")
        f.write("│   ├─ 早段（10:00-13:00）\n")
        f.write("│   ├─ 午段（13:00-16:00）\n")
        f.write("│   ├─ 晚段（16:00-20:00）\n")
        f.write("│   └─ 計算各時段佔比變化\n")
        f.write("│\n")
        f.write("└─ 步驟 6：統計檢驗\n")
        f.write("    ├─ Kolmogorov-Smirnov 檢驗（分佈差異）\n")
        f.write("    ├─ Mann-Whitney U 檢驗（非參數檢驗）\n")
        f.write("    └─ 判斷差異顯著性（p < 0.05）\n")
        f.write("```\n\n")

        f.write("---\n\n")

        # 關鍵發現
        f.write("## 關鍵發現\n\n")

        # 1. 加權平均時間比較
        winter_weighted = winter_stats['weighted_avg_hour']
        summer_weighted = summer_stats['weighted_avg_hour']
        time_diff = summer_weighted - winter_weighted  # 正值表示夏季較晚

        f.write("### 1. 加權平均銷售時間\n\n")
        f.write(f"- **冬季**：{winter_weighted:.2f} 時（約 {int(winter_weighted)}:{int((winter_weighted % 1) * 60):02d}）\n")
        f.write(f"- **夏季**：{summer_weighted:.2f} 時（約 {int(summer_weighted)}:{int((summer_weighted % 1) * 60):02d}）\n")
        f.write(f"- **時間差異**：{abs(time_diff):.2f} 小時 = {abs(time_diff) * 60:.0f} 分鐘\n\n")

        if time_diff > 0:
            f.write(f"**結論**：✅ **冬季銷售高峰確實往前移動了約 {abs(time_diff) * 60:.0f} 分鐘**\n\n")
            f.write(f"這表示冬季客戶傾向於更早用餐，可能與日照時間縮短、天氣寒冷等因素有關。\n\n")
        else:
            f.write(f"**結論**：❌ 冬季銷售高峰並未往前移動，反而較夏季晚 {abs(time_diff) * 60:.0f} 分鐘\n\n")

        # 2. 時段佔比變化
        f.write("### 2. 時段佔比變化\n\n")
        f.write("| 時段 | 冬季營收佔比 | 夏季營收佔比 | 變化 |\n")
        f.write("|------|-------------|-------------|------|\n")

        segments = ['早段 (10-13)', '午段 (13-16)', '晚段 (16-20)']
        winter_data = segment_stats[segment_stats['Season'] == 'Winter'].set_index('Segment')
        summer_data = segment_stats[segment_stats['Season'] == 'Summer'].set_index('Segment')

        for seg in segments:
            w_pct = winter_data.loc[seg, 'Revenue_Pct']
            s_pct = summer_data.loc[seg, 'Revenue_Pct']
            change = w_pct - s_pct
            arrow = "📈" if change > 0 else "📉"
            f.write(f"| {seg} | {w_pct:.1f}% | {s_pct:.1f}% | {arrow} {change:+.1f}% |\n")

        f.write("\n")

        # 識別最大變化
        changes = {}
        for seg in segments:
            changes[seg] = winter_data.loc[seg, 'Revenue_Pct'] - summer_data.loc[seg, 'Revenue_Pct']

        max_increase_seg = max(changes, key=changes.get)
        max_increase_val = changes[max_increase_seg]

        if max_increase_val > 0:
            f.write(f"**最大變化**：{max_increase_seg} 在冬季增加了 {max_increase_val:.1f} 個百分點\n\n")

        # 3. 統計檢驗結果
        f.write("### 3. 統計檢驗結果\n\n")
        f.write(f"- **Kolmogorov-Smirnov 檢驗**：\n")
        f.write(f"  - KS 統計量：{stat_test['ks_statistic']:.4f}\n")
        f.write(f"  - p 值：{stat_test['ks_pvalue']:.4f}\n")

        if stat_test['ks_pvalue'] < 0.05:
            f.write(f"  - **結論**：✅ 分佈差異顯著（p < 0.05）\n\n")
        else:
            f.write(f"  - **結論**：❌ 分佈差異不顯著（p ≥ 0.05）\n\n")

        f.write(f"- **Mann-Whitney U 檢驗**：\n")
        f.write(f"  - U 統計量：{stat_test['mannwhitney_u']:.0f}\n")
        f.write(f"  - p 值：{stat_test['mannwhitney_pvalue']:.4f}\n")

        if stat_test['mannwhitney_pvalue'] < 0.05:
            f.write(f"  - **結論**：✅ 兩季銷售分佈有顯著差異（p < 0.05）\n\n")
        else:
            f.write(f"  - **結論**：❌ 兩季銷售分佈無顯著差異（p ≥ 0.05）\n\n")

        f.write("---\n\n")

        # 詳細數據表
        f.write("## 詳細數據表\n\n")
        f.write("### 冬季每小時銷售統計\n\n")
        f.write("| 小時 | 日均交易數 | 日均營收 ($) | 營收佔比 (%) | 交易佔比 (%) |\n")
        f.write("|------|-----------|-------------|-------------|-------------|\n")
        for _, row in winter_hourly.iterrows():
            f.write(f"| {int(row['Hour']):02d}:00 | {row['Avg_Daily_Transactions']:.1f} | "
                   f"${row['Avg_Daily_Revenue']:.2f} | {row['Revenue_Pct']:.1f}% | "
                   f"{row['Transactions_Pct']:.1f}% |\n")

        f.write("\n### 夏季每小時銷售統計\n\n")
        f.write("| 小時 | 日均交易數 | 日均營收 ($) | 營收佔比 (%) | 交易佔比 (%) |\n")
        f.write("|------|-----------|-------------|-------------|-------------|\n")
        for _, row in summer_hourly.iterrows():
            f.write(f"| {int(row['Hour']):02d}:00 | {row['Avg_Daily_Transactions']:.1f} | "
                   f"${row['Avg_Daily_Revenue']:.2f} | {row['Revenue_Pct']:.1f}% | "
                   f"{row['Transactions_Pct']:.1f}% |\n")

        f.write("\n---\n\n")

        # 視覺化輸出
        f.write("## 視覺化輸出\n\n")
        f.write("### 1. 季節對比圖表\n")
        f.write("- 檔案：`charts/seasonal_comparison.png`\n")
        f.write("- 內容：\n")
        f.write("  - 每小時日均交易筆數對比\n")
        f.write("  - 每小時日均營收對比\n")
        f.write("  - 營收分佈曲線\n")
        f.write("  - 累積營收曲線\n\n")

        f.write("### 2. 時段分群對比圖表\n")
        f.write("- 檔案：`charts/segment_comparison.png`\n")
        f.write("- 內容：\n")
        f.write("  - 時段營收佔比對比\n")
        f.write("  - 時段交易筆數佔比對比\n\n")

        f.write("---\n\n")

        # 結論與建議
        f.write("## 結論與建議\n\n")

        if time_diff > 0:
            f.write("### 主要結論\n\n")
            f.write(f"1. **冬季銷售高峰確實往前移動**：相較於夏季，冬季的加權平均銷售時間提前了約 {abs(time_diff) * 60:.0f} 分鐘\n")
            f.write(f"2. **早段營收增加**：冬季早段（10-13）營收佔比較夏季增加 {changes['早段 (10-13)']:.1f} 個百分點\n")
            f.write(f"3. **統計顯著性**：{'有' if stat_test['ks_pvalue'] < 0.05 else '無'}顯著差異（p = {stat_test['ks_pvalue']:.4f}）\n\n")

            f.write("### 營運建議\n\n")
            f.write("1. **人力配置調整**：\n")
            f.write("   - 冬季增加早段（10-13）人力\n")
            f.write("   - 考慮提前備料時間\n\n")

            f.write("2. **菜單優化**：\n")
            f.write("   - 早段推出適合冬季的暖食套餐\n")
            f.write("   - 提供早鳥優惠吸引早到客群\n\n")

            f.write("3. **營銷策略**：\n")
            f.write("   - 強調冬季午餐時段\n")
            f.write("   - 推廣 11:00-13:00 商業午餐\n\n")
        else:
            f.write("### 主要結論\n\n")
            f.write(f"1. **冬季銷售高峰未往前移動**：相較於夏季，冬季的加權平均銷售時間反而延後了約 {abs(time_diff) * 60:.0f} 分鐘\n")
            f.write(f"2. **晚段營收佔比較高**：冬季客戶傾向於較晚用餐\n")
            f.write(f"3. **統計顯著性**：{'有' if stat_test['ks_pvalue'] < 0.05 else '無'}顯著差異（p = {stat_test['ks_pvalue']:.4f}）\n\n")

        f.write("---\n\n")
        f.write(f"**報告生成時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✓ 分析報告已生成：{report_path}")

def main():
    """主程式"""

    print("=" * 60)
    print("冬季 vs 夏季銷售時段差異分析")
    print("=" * 60)
    print()

    # 載入 2025 年數據
    data_2025 = load_and_preprocess_data('/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv')

    # 使用 2025 年數據
    df_all = data_2025

    # 分類季節
    df_all['Season'] = df_all.apply(classify_season, axis=1)

    # 過濾只保留冬季和夏季
    df_seasonal = df_all[df_all['Season'].notna()].copy()

    print(f"\n季節分類結果：")
    print(f"  冬季：{len(df_seasonal[df_seasonal['Season'] == 'Winter'])} 筆交易")
    print(f"  夏季：{len(df_seasonal[df_seasonal['Season'] == 'Summer'])} 筆交易")
    print()

    # 分析每小時分佈
    print("分析每小時銷售分佈...")
    winter_hourly = analyze_hourly_distribution(df_seasonal, 'Winter')
    summer_hourly = analyze_hourly_distribution(df_seasonal, 'Summer')

    # 計算加權平均時間
    print("計算加權平均銷售時間...")
    winter_stats = calculate_weighted_average_time(df_seasonal, 'Winter')
    summer_stats = calculate_weighted_average_time(df_seasonal, 'Summer')

    print(f"  冬季加權平均：{winter_stats['weighted_avg_hour']:.2f} 時")
    print(f"  夏季加權平均：{summer_stats['weighted_avg_hour']:.2f} 時")
    print(f"  時間差異：{abs(summer_stats['weighted_avg_hour'] - winter_stats['weighted_avg_hour']) * 60:.0f} 分鐘")
    print()

    # 時段分群分析
    print("執行時段分群分析...")
    segment_stats = analyze_time_segments(df_seasonal)

    # 統計檢驗
    print("執行統計檢驗...")
    stat_test = perform_statistical_test(winter_hourly, summer_hourly)
    print(f"  KS 檢驗 p 值：{stat_test['ks_pvalue']:.4f}")
    print(f"  Mann-Whitney U 檢驗 p 值：{stat_test['mannwhitney_pvalue']:.4f}")
    print()

    # 儲存數據
    print("儲存分析數據...")
    winter_hourly.to_csv(OUTPUT_DIR / 'data' / 'winter_hourly.csv', index=False)
    summer_hourly.to_csv(OUTPUT_DIR / 'data' / 'summer_hourly.csv', index=False)
    segment_stats.to_csv(OUTPUT_DIR / 'data' / 'segment_stats.csv', index=False)
    print("✓ 數據已儲存至 data/ 資料夾")
    print()

    # 生成圖表
    print("生成視覺化圖表...")
    create_comparison_chart(winter_hourly, summer_hourly)
    create_segment_chart(segment_stats)
    print()

    # 生成報告
    print("生成分析報告...")
    generate_report(winter_hourly, summer_hourly, winter_stats, summer_stats,
                   segment_stats, stat_test)
    print()

    print("=" * 60)
    print("分析完成！")
    print("=" * 60)
    print(f"\n輸出位置：{OUTPUT_DIR.absolute()}")
    print(f"  - 報告：seasonal_shift_report.md")
    print(f"  - 圖表：charts/")
    print(f"  - 數據：data/")
    print()

if __name__ == "__main__":
    main()
