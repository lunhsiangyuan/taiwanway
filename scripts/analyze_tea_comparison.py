#!/usr/bin/env python3
"""
烏龍茶 vs 紅茶 每週銷售對比分析
使用 Claude Agent SDK 架構的分析工具
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體
plt.rcParams['text.usetex'] = False
chinese_font_paths = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
]
chinese_font = None
for path in chinese_font_paths:
    if Path(path).exists():
        chinese_font = fm.FontProperties(fname=path, size=12)
        break

# 定義茶飲分類
OOLONG_KEYWORDS = ['oolong', '烏龍', '奶烏']
BLACK_TEA_KEYWORDS = ['taiwanese bubble tea', 'taiwanese milk tea', '蜜香奶茶', 
                       '珍珠奶茶', '珍奶', 'classic milk tea', '古早味奶茶',
                       'black tea', 'lychee jelly black tea']

def classify_tea(item_name):
    """分類茶飲品項"""
    item_lower = item_name.lower()
    
    # 先檢查烏龍（優先級較高）
    for keyword in OOLONG_KEYWORDS:
        if keyword.lower() in item_lower:
            return '烏龍茶類'
    
    # 再檢查紅茶
    for keyword in BLACK_TEA_KEYWORDS:
        if keyword.lower() in item_lower:
            return '紅茶類'
    
    return None

def main():
    # 載入數據
    data_path = Path('/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv')
    print(f"載入數據：{data_path}")
    
    df = pd.read_csv(data_path)
    print(f"總筆數：{len(df):,}")
    
    # 處理金額欄位
    df['Net Sales'] = df['Net Sales'].replace('[\$,]', '', regex=True).astype(float)
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0)
    
    # 處理日期
    df['Date'] = pd.to_datetime(df['Date'])
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Year'] = df['Date'].dt.year
    df['YearWeek'] = df['Year'].astype(str) + '-W' + df['Week'].astype(str).str.zfill(2)
    
    # 分類茶飲
    df['Tea_Category'] = df['Item'].apply(classify_tea)
    
    # 過濾茶飲品項
    tea_df = df[df['Tea_Category'].notna()].copy()
    print(f"\n茶飲品項筆數：{len(tea_df):,}")
    
    # 顯示分類結果
    print("\n=== 烏龍茶類品項 ===")
    oolong_items = tea_df[tea_df['Tea_Category'] == '烏龍茶類']['Item'].value_counts()
    for item, count in oolong_items.head(10).items():
        print(f"  {item}: {count} 筆")
    
    print("\n=== 紅茶類品項 ===")
    black_tea_items = tea_df[tea_df['Tea_Category'] == '紅茶類']['Item'].value_counts()
    for item, count in black_tea_items.head(10).items():
        print(f"  {item}: {count} 筆")
    
    # 按週和茶類統計
    weekly_sales = tea_df.groupby(['YearWeek', 'Tea_Category']).agg({
        'Net Sales': 'sum',
        'Qty': 'sum'
    }).reset_index()
    
    # 樞紐表
    pivot_sales = weekly_sales.pivot(index='YearWeek', columns='Tea_Category', values='Net Sales').fillna(0)
    pivot_qty = weekly_sales.pivot(index='YearWeek', columns='Tea_Category', values='Qty').fillna(0)
    
    # 確保兩個類別都存在
    for cat in ['烏龍茶類', '紅茶類']:
        if cat not in pivot_sales.columns:
            pivot_sales[cat] = 0
        if cat not in pivot_qty.columns:
            pivot_qty[cat] = 0
    
    # 排序
    pivot_sales = pivot_sales.sort_index()
    pivot_qty = pivot_qty.sort_index()
    
    print("\n=== 每週銷售額統計 ===")
    print(pivot_sales.tail(10).to_string())
    
    # 計算總計
    print("\n=== 總計 ===")
    print(f"烏龍茶類 總銷售額：${pivot_sales['烏龍茶類'].sum():,.2f}")
    print(f"紅茶類 總銷售額：${pivot_sales['紅茶類'].sum():,.2f}")
    print(f"烏龍茶類 總銷售量：{pivot_qty['烏龍茶類'].sum():,.0f} 杯")
    print(f"紅茶類 總銷售量：{pivot_qty['紅茶類'].sum():,.0f} 杯")
    
    # 繪製圖表
    output_dir = Path('/Users/lunhsiangyuan/Desktop/square/agents/output/tea_analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 只取最近 20 週的數據
    recent_weeks = pivot_sales.tail(20)
    recent_qty = pivot_qty.tail(20)
    
    # 圖表 1：每週銷售額對比
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 每週銷售額柱狀圖
    ax1 = axes[0, 0]
    x = range(len(recent_weeks))
    width = 0.35
    bars1 = ax1.bar([i - width/2 for i in x], recent_weeks['烏龍茶類'], width, 
                     label='烏龍茶類', color='#2E86AB', alpha=0.8)
    bars2 = ax1.bar([i + width/2 for i in x], recent_weeks['紅茶類'], width, 
                     label='紅茶類', color='#A23B72', alpha=0.8)
    ax1.set_xlabel('週次', fontproperties=chinese_font)
    ax1.set_ylabel('銷售額 ($)', fontproperties=chinese_font)
    ax1.set_title('烏龍茶 vs 紅茶 每週銷售額對比', fontproperties=chinese_font, fontsize=14, fontweight='bold')
    ax1.set_xticks(x[::2])
    ax1.set_xticklabels([recent_weeks.index[i] for i in range(0, len(recent_weeks), 2)], rotation=45, ha='right')
    ax1.legend(prop=chinese_font)
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. 每週銷售量柱狀圖
    ax2 = axes[0, 1]
    bars3 = ax2.bar([i - width/2 for i in x], recent_qty['烏龍茶類'], width, 
                     label='烏龍茶類', color='#2E86AB', alpha=0.8)
    bars4 = ax2.bar([i + width/2 for i in x], recent_qty['紅茶類'], width, 
                     label='紅茶類', color='#A23B72', alpha=0.8)
    ax2.set_xlabel('週次', fontproperties=chinese_font)
    ax2.set_ylabel('銷售量 (杯)', fontproperties=chinese_font)
    ax2.set_title('烏龍茶 vs 紅茶 每週銷售量對比', fontproperties=chinese_font, fontsize=14, fontweight='bold')
    ax2.set_xticks(x[::2])
    ax2.set_xticklabels([recent_qty.index[i] for i in range(0, len(recent_qty), 2)], rotation=45, ha='right')
    ax2.legend(prop=chinese_font)
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. 銷售額趨勢折線圖
    ax3 = axes[1, 0]
    ax3.plot(recent_weeks.index, recent_weeks['烏龍茶類'], marker='o', 
             linewidth=2, label='烏龍茶類', color='#2E86AB')
    ax3.plot(recent_weeks.index, recent_weeks['紅茶類'], marker='s', 
             linewidth=2, label='紅茶類', color='#A23B72')
    ax3.set_xlabel('週次', fontproperties=chinese_font)
    ax3.set_ylabel('銷售額 ($)', fontproperties=chinese_font)
    ax3.set_title('每週銷售額趨勢', fontproperties=chinese_font, fontsize=14, fontweight='bold')
    ax3.set_xticks(range(0, len(recent_weeks), 2))
    ax3.set_xticklabels([recent_weeks.index[i] for i in range(0, len(recent_weeks), 2)], rotation=45, ha='right')
    ax3.legend(prop=chinese_font)
    ax3.grid(alpha=0.3)
    
    # 4. 總銷售額圓餅圖
    ax4 = axes[1, 1]
    total_sales = [pivot_sales['烏龍茶類'].sum(), pivot_sales['紅茶類'].sum()]
    labels = ['烏龍茶類', '紅茶類']
    colors = ['#2E86AB', '#A23B72']
    explode = (0.05, 0)
    wedges, texts, autotexts = ax4.pie(total_sales, labels=labels, colors=colors, explode=explode,
                                         autopct='%1.1f%%', startangle=90,
                                         textprops={'fontproperties': chinese_font})
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    ax4.set_title(f'總銷售額佔比\n(烏龍 ${total_sales[0]:,.0f} vs 紅茶 ${total_sales[1]:,.0f})', 
                  fontproperties=chinese_font, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # 儲存圖表
    chart_path = output_dir / 'oolong_vs_black_tea_comparison.png'
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\n✅ 圖表已儲存：{chart_path}")
    
    # 生成詳細報告
    report_path = output_dir / 'tea_comparison_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 烏龍茶 vs 紅茶 每週銷售對比分析報告\n\n")
        f.write(f"**分析日期**：{datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"**數據範圍**：{df['Date'].min().strftime('%Y-%m-%d')} ~ {df['Date'].max().strftime('%Y-%m-%d')}\n\n")
        
        f.write("---\n\n")
        f.write("## 總體銷售統計\n\n")
        f.write("| 類別 | 總銷售額 | 總銷售量 | 平均單價 |\n")
        f.write("|------|----------|----------|----------|\n")
        oolong_avg = pivot_sales['烏龍茶類'].sum() / pivot_qty['烏龍茶類'].sum() if pivot_qty['烏龍茶類'].sum() > 0 else 0
        black_avg = pivot_sales['紅茶類'].sum() / pivot_qty['紅茶類'].sum() if pivot_qty['紅茶類'].sum() > 0 else 0
        f.write(f"| 烏龍茶類 | ${pivot_sales['烏龍茶類'].sum():,.2f} | {pivot_qty['烏龍茶類'].sum():,.0f} 杯 | ${oolong_avg:.2f} |\n")
        f.write(f"| 紅茶類 | ${pivot_sales['紅茶類'].sum():,.2f} | {pivot_qty['紅茶類'].sum():,.0f} 杯 | ${black_avg:.2f} |\n\n")
        
        f.write("## 烏龍茶類品項明細\n\n")
        f.write("| 品項 | 銷售筆數 |\n")
        f.write("|------|----------|\n")
        for item, count in oolong_items.items():
            f.write(f"| {item} | {count} |\n")
        
        f.write("\n## 紅茶類品項明細\n\n")
        f.write("| 品項 | 銷售筆數 |\n")
        f.write("|------|----------|\n")
        for item, count in black_tea_items.items():
            f.write(f"| {item} | {count} |\n")
        
        f.write("\n## 近 10 週銷售數據\n\n")
        f.write("| 週次 | 烏龍茶銷售額 | 紅茶銷售額 | 差異 |\n")
        f.write("|------|-------------|-----------|------|\n")
        for week in recent_weeks.tail(10).index:
            oolong_val = recent_weeks.loc[week, '烏龍茶類']
            black_val = recent_weeks.loc[week, '紅茶類']
            diff = oolong_val - black_val
            diff_sign = "+" if diff > 0 else ""
            f.write(f"| {week} | ${oolong_val:,.2f} | ${black_val:,.2f} | {diff_sign}${diff:,.2f} |\n")
        
        f.write("\n## 洞察與建議\n\n")
        
        # 計算比較
        oolong_total = pivot_sales['烏龍茶類'].sum()
        black_total = pivot_sales['紅茶類'].sum()
        ratio = black_total / oolong_total if oolong_total > 0 else 0
        
        f.write(f"1. **銷售比較**：紅茶類總銷售額是烏龍茶類的 {ratio:.1f} 倍\n")
        f.write(f"2. **平均單價**：烏龍茶類 ${oolong_avg:.2f}，紅茶類 ${black_avg:.2f}\n")
        
        # 趨勢分析
        recent_oolong = recent_weeks['烏龍茶類'].tail(4).mean()
        earlier_oolong = recent_weeks['烏龍茶類'].head(4).mean()
        oolong_trend = ((recent_oolong - earlier_oolong) / earlier_oolong * 100) if earlier_oolong > 0 else 0
        
        recent_black = recent_weeks['紅茶類'].tail(4).mean()
        earlier_black = recent_weeks['紅茶類'].head(4).mean()
        black_trend = ((recent_black - earlier_black) / earlier_black * 100) if earlier_black > 0 else 0
        
        f.write(f"3. **近期趨勢**：\n")
        f.write(f"   - 烏龍茶類：{'↑' if oolong_trend > 0 else '↓'} {abs(oolong_trend):.1f}%\n")
        f.write(f"   - 紅茶類：{'↑' if black_trend > 0 else '↓'} {abs(black_trend):.1f}%\n")
        
        f.write("\n---\n")
        f.write(f"*報告生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print(f"✅ 報告已儲存：{report_path}")
    
    plt.close()
    return str(chart_path)

if __name__ == "__main__":
    chart_path = main()
    print(f"\n🎉 分析完成！")
