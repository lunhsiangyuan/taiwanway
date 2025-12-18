#!/usr/bin/env python3
"""
分析 Taiwanway 餐廳的 Pot 沖泡茶銷售數據

數據來源：items-2025-01-01-2025-11-16.csv
分析內容：
1. Pot 沖泡茶總銷售數量和淨營收
2. 按品項排名
3. 按月份趨勢
4. 按類別分析
5. 佔店鋪總營收比例
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# NYC 稅率
NYC_TAX_RATE = 0.08875

def load_and_clean_data(file_path):
    """載入並清理數據"""
    print(f"載入數據：{file_path}")
    df = pd.read_csv(file_path)

    print(f"原始記錄數：{len(df):,}")

    # 解析貨幣欄位
    for col in ['Gross Sales', 'Discounts', 'Net Sales', 'Tax']:
        df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

    # 解析日期時間
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Year'] = df['DateTime'].dt.year
    df['Month'] = df['DateTime'].dt.month
    df['YearMonth'] = df['DateTime'].dt.to_period('M')

    # 計算淨營收（扣除稅金）
    df['Net_Revenue'] = df['Net Sales'] / (1 + NYC_TAX_RATE)

    # 處理 Qty 欄位
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0)

    # 處理 Price Point Name 的空值
    df['Price Point Name'] = df['Price Point Name'].fillna('')

    return df

def analyze_pot_tea(df):
    """分析 Pot 沖泡茶銷售數據"""

    # 1. 篩選包含 "Pot" 的記錄（在 Modifiers Applied 欄位）
    df['Modifiers Applied'] = df['Modifiers Applied'].fillna('')
    pot_df = df[df['Modifiers Applied'].str.contains('Pot', case=False, na=False)].copy()

    print(f"\n{'='*60}")
    print(f"Pot 沖泡茶記錄數：{len(pot_df):,}")
    print(f"{'='*60}\n")

    if len(pot_df) == 0:
        print("⚠️  未找到包含 'Pot' 的記錄")
        return None, None

    # 2. 總銷售統計
    total_qty = pot_df['Qty'].sum()
    total_net_revenue = pot_df['Net_Revenue'].sum()
    total_net_sales = pot_df['Net Sales'].sum()

    print(f"【總銷售統計】")
    print(f"總銷售數量：{total_qty:,.0f} 壺")
    print(f"總 Net Sales：${total_net_sales:,.2f}")
    print(f"總淨營收（扣稅）：${total_net_revenue:,.2f}")
    print(f"平均單價（淨）：${total_net_revenue/total_qty:,.2f} / 壺")

    # 3. 按品項排名
    print(f"\n{'='*60}")
    print(f"【按品項排名】")
    print(f"{'='*60}")

    item_stats = pot_df.groupby('Item').agg({
        'Qty': 'sum',
        'Net_Revenue': 'sum',
        'Transaction ID': 'nunique'
    }).reset_index()

    item_stats.columns = ['品項', '總數量', '總淨營收', '交易筆數']
    item_stats['平均單價'] = item_stats['總淨營收'] / item_stats['總數量']
    item_stats['佔比'] = (item_stats['總淨營收'] / total_net_revenue * 100)
    item_stats = item_stats.sort_values('總淨營收', ascending=False)

    print(f"\n{item_stats.to_string(index=False)}")

    # 4. 按月份趨勢
    print(f"\n{'='*60}")
    print(f"【按月份趨勢】")
    print(f"{'='*60}")

    monthly_stats = pot_df.groupby('YearMonth').agg({
        'Qty': 'sum',
        'Net_Revenue': 'sum',
        'Transaction ID': 'nunique'
    }).reset_index()

    monthly_stats.columns = ['年月', '總數量', '總淨營收', '交易筆數']
    monthly_stats['平均單價'] = monthly_stats['總淨營收'] / monthly_stats['總數量']

    print(f"\n{monthly_stats.to_string(index=False)}")

    # 5. 按類別分析
    print(f"\n{'='*60}")
    print(f"【按類別分析】")
    print(f"{'='*60}")

    category_stats = pot_df.groupby('Category').agg({
        'Qty': 'sum',
        'Net_Revenue': 'sum',
        'Transaction ID': 'nunique',
        'Item': lambda x: x.nunique()
    }).reset_index()

    category_stats.columns = ['類別', '總數量', '總淨營收', '交易筆數', '品項數']
    category_stats['平均單價'] = category_stats['總淨營收'] / category_stats['總數量']
    category_stats['佔比'] = (category_stats['總淨營收'] / total_net_revenue * 100)
    category_stats = category_stats.sort_values('總淨營收', ascending=False)

    print(f"\n{category_stats.to_string(index=False)}")

    # 6. 計算佔店鋪總營收比例
    print(f"\n{'='*60}")
    print(f"【佔店鋪總營收比例】")
    print(f"{'='*60}")

    total_store_revenue = df['Net_Revenue'].sum()
    pot_percentage = (total_net_revenue / total_store_revenue) * 100

    print(f"\n店鋪總淨營收：${total_store_revenue:,.2f}")
    print(f"Pot 沖泡茶淨營收：${total_net_revenue:,.2f}")
    print(f"佔比：{pot_percentage:.2f}%")

    # 7. 詳細記錄列表（全部記錄）
    print(f"\n{'='*60}")
    print(f"【詳細記錄列表（全部 {len(pot_df)} 筆）】")
    print(f"{'='*60}")

    detail_cols = ['Date', 'Time', 'Item', 'Category', 'Modifiers Applied', 'Qty', 'Net Sales', 'Net_Revenue']
    pot_df_sorted = pot_df.sort_values('Date')
    print(f"\n{pot_df_sorted[detail_cols].to_string(index=False)}")

    # 8. 保存結果
    results = {
        'summary': {
            'total_qty': float(total_qty),
            'total_net_sales': float(total_net_sales),
            'total_net_revenue': float(total_net_revenue),
            'avg_price': float(total_net_revenue / total_qty),
            'total_transactions': int(pot_df['Transaction ID'].nunique()),
            'percentage_of_store': float(pot_percentage)
        },
        'by_item': item_stats.to_dict('records'),
        'by_month': monthly_stats.astype(str).to_dict('records'),
        'by_category': category_stats.to_dict('records')
    }

    return results, pot_df

def main():
    """主函數"""
    # 數據文件路徑
    data_file = Path('/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv')

    if not data_file.exists():
        print(f"❌ 數據文件不存在：{data_file}")
        return

    # 載入數據
    df = load_and_clean_data(data_file)

    # 分析 Pot 沖泡茶
    results, pot_df = analyze_pot_tea(df)

    if results is None:
        return

    # 保存結果
    output_dir = Path('/Users/lunhsiangyuan/Desktop/square/analysis_output/pot_tea')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 保存 JSON
    json_file = output_dir / 'pot_tea_analysis.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 結果已保存至：{json_file}")

    # 保存詳細數據 CSV
    csv_file = output_dir / 'pot_tea_details.csv'
    pot_df.to_csv(csv_file, index=False)
    print(f"✅ 詳細數據已保存至：{csv_file}")

    # 生成 Markdown 報告
    generate_markdown_report(results, output_dir)

    print(f"\n{'='*60}")
    print(f"分析完成！")
    print(f"{'='*60}")

def generate_markdown_report(results, output_dir):
    """生成 Markdown 報告"""

    md_file = output_dir / 'pot_tea_report.md'

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Taiwanway Pot 沖泡茶銷售分析報告\n\n")
        f.write(f"**分析期間**：2025-01-01 至 2025-11-16\n\n")
        f.write(f"**生成時間**：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # 總覽
        f.write("## 📊 總銷售統計\n\n")
        summary = results['summary']
        f.write(f"- **總銷售數量**：{summary['total_qty']:,.0f} 壺\n")
        f.write(f"- **總 Net Sales**：${summary['total_net_sales']:,.2f}\n")
        f.write(f"- **總淨營收（扣稅）**：${summary['total_net_revenue']:,.2f}\n")
        f.write(f"- **平均單價（淨）**：${summary['avg_price']:,.2f} / 壺\n")
        f.write(f"- **交易筆數**：{summary['total_transactions']:,} 筆\n")
        f.write(f"- **佔店鋪總營收**：{summary['percentage_of_store']:.2f}%\n\n")

        # 按品項排名
        f.write("## 🏆 按品項排名\n\n")
        f.write("| 品項 | 總數量 | 總淨營收 | 交易筆數 | 平均單價 | 佔比 |\n")
        f.write("|------|--------|----------|----------|----------|------|\n")
        for item in results['by_item']:
            f.write(f"| {item['品項']} | {item['總數量']:.0f} | ${item['總淨營收']:,.2f} | {item['交易筆數']} | ${item['平均單價']:,.2f} | {item['佔比']:.1f}% |\n")
        f.write("\n")

        # 按月份趨勢
        f.write("## 📈 按月份趨勢\n\n")
        f.write("| 年月 | 總數量 | 總淨營收 | 交易筆數 | 平均單價 |\n")
        f.write("|------|--------|----------|----------|----------|\n")
        for month in results['by_month']:
            f.write(f"| {month['年月']} | {float(month['總數量']):.0f} | ${float(month['總淨營收']):,.2f} | {month['交易筆數']} | ${float(month['平均單價']):,.2f} |\n")
        f.write("\n")

        # 按類別分析
        f.write("## 📂 按類別分析\n\n")
        f.write("| 類別 | 總數量 | 總淨營收 | 交易筆數 | 品項數 | 平均單價 | 佔比 |\n")
        f.write("|------|--------|----------|----------|--------|----------|------|\n")
        for cat in results['by_category']:
            f.write(f"| {cat['類別']} | {cat['總數量']:.0f} | ${cat['總淨營收']:,.2f} | {cat['交易筆數']} | {cat['品項數']} | ${cat['平均單價']:,.2f} | {cat['佔比']:.1f}% |\n")
        f.write("\n")

        # 結論
        f.write("## 💡 關鍵發現\n\n")
        top_item = results['by_item'][0]
        f.write(f"1. **最暢銷品項**：{top_item['品項']}，佔 Pot 沖泡茶營收的 {top_item['佔比']:.1f}%\n")
        f.write(f"2. **Pot 沖泡茶佔店鋪營收**：{summary['percentage_of_store']:.2f}%\n")
        f.write(f"3. **平均單價**：${summary['avg_price']:.2f} / 壺\n\n")

        f.write("---\n\n")
        f.write("*本報告由自動化腳本生成*\n")

    print(f"✅ Markdown 報告已保存至：{md_file}")

if __name__ == "__main__":
    main()
