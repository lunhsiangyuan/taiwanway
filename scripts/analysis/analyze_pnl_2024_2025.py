#!/usr/bin/env python3
"""
Taiwanway 餐廳損益分析（2024/01 - 2025/05）
分析期間：2024 年 1 月至 2025 年 5 月（共 17 個月）
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import pytz

# 設定輸出目錄
output_dir = Path('/Users/lunhsiangyuan/Desktop/square/analysis_output/pnl_analysis')
output_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. 載入數據
# ============================================================================

print("載入數據...")

# 載入 2024 年數據
df_2024 = pd.read_csv('/Users/lunhsiangyuan/Desktop/square/data/all_payments/payments_2024_full.csv')

# 載入 2025 年數據（1-11 月）
df_2025 = pd.read_csv('/Users/lunhsiangyuan/Desktop/square/data/all_payments/payments_2025_01_to_11.csv')

# 合併數據
df = pd.concat([df_2024, df_2025], ignore_index=True)

print(f"總交易筆數：{len(df):,}")

# ============================================================================
# 2. 數據預處理
# ============================================================================

print("數據預處理...")

# 只保留完成的交易
df = df[df['status'] == 'COMPLETED'].copy()
print(f"完成交易筆數：{len(df):,}")

# 轉換時區（UTC → America/New_York）
df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
ny_tz = pytz.timezone('America/New_York')
df['DateTime'] = df['created_at'].dt.tz_convert(ny_tz)

# 提取時間欄位
df['Year'] = df['DateTime'].dt.year
df['Month'] = df['DateTime'].dt.month
df['YearMonth'] = df['DateTime'].dt.to_period('M')
df['DayOfWeek'] = df['DateTime'].dt.dayofweek
df['Date'] = df['DateTime'].dt.date

# 計算淨營收（去除稅金）
# Gross Sales → Net Revenue
# Net = Gross / (1 + 0.08875)
df['Gross_Sales'] = df['amount'].astype(float)
df['Net_Revenue'] = df['Gross_Sales'] / 1.08875

print(f"數據期間：{df['DateTime'].min()} 至 {df['DateTime'].max()}")

# ============================================================================
# 3. 篩選分析期間（2024/01 - 2025/05）
# ============================================================================

# 篩選 2024/01 - 2025/05
df_analysis = df[
    ((df['Year'] == 2024)) |
    ((df['Year'] == 2025) & (df['Month'] <= 5))
].copy()

print(f"分析期間交易筆數：{len(df_analysis):,}")
print(f"分析期間：2024-01 至 2025-05")

# ============================================================================
# 4. 業務規則過濾
# ============================================================================

# 營業日：週一(0)、週二(1)、週五(4)、週六(5)
operating_days = [0, 1, 4, 5]

# 過濾營業日
df_operating = df_analysis[df_analysis['DayOfWeek'].isin(operating_days)].copy()

print(f"營業日交易筆數：{len(df_operating):,}")

# ============================================================================
# 5. 計算每月營收
# ============================================================================

print("\n計算每月營收...")

# 按年月分組計算營收
monthly_revenue = df_operating.groupby('YearMonth').agg({
    'Net_Revenue': 'sum',
    'Gross_Sales': 'sum',
    'Date': 'nunique'  # 營業天數
}).reset_index()

monthly_revenue.columns = ['YearMonth', 'Net_Revenue', 'Gross_Sales', 'Operating_Days']

# 轉換為字串格式
monthly_revenue['YearMonth_Str'] = monthly_revenue['YearMonth'].astype(str)

# ============================================================================
# 6. 計算每月成本
# ============================================================================

print("計算每月成本...")

# 6.1 食材成本（35% of Net Revenue）
monthly_revenue['Food_Cost'] = monthly_revenue['Net_Revenue'] * 0.35

# 6.2 人力成本
# 2024/01-09: $0/天
# 2024/10 起: $70/天
def calculate_labor_cost(row):
    year_month_str = row['YearMonth_Str']
    operating_days = row['Operating_Days']

    year = int(year_month_str[:4])
    month = int(year_month_str[-2:])

    if year == 2024 and month < 10:
        return 0
    else:
        return 70 * operating_days

monthly_revenue['Labor_Cost'] = monthly_revenue.apply(calculate_labor_cost, axis=1)

# 6.3 固定成本（房租 + 水電）
# 每月 $3,800（即使未營業月份也要計算）
monthly_revenue['Fixed_Cost'] = 3800

# 6.4 總成本
monthly_revenue['Total_Cost'] = (
    monthly_revenue['Food_Cost'] +
    monthly_revenue['Labor_Cost'] +
    monthly_revenue['Fixed_Cost']
)

# ============================================================================
# 7. 計算損益
# ============================================================================

print("計算損益...")

# 營業利潤（Net Revenue - Total Cost）
monthly_revenue['Operating_Profit'] = (
    monthly_revenue['Net_Revenue'] - monthly_revenue['Total_Cost']
)

# 毛利（Net Revenue - Food Cost）
monthly_revenue['Gross_Profit'] = (
    monthly_revenue['Net_Revenue'] - monthly_revenue['Food_Cost']
)

# 毛利率
monthly_revenue['Gross_Margin'] = (
    monthly_revenue['Gross_Profit'] / monthly_revenue['Net_Revenue'] * 100
)

# 淨利率
monthly_revenue['Net_Margin'] = (
    monthly_revenue['Operating_Profit'] / monthly_revenue['Net_Revenue'] * 100
)

# ============================================================================
# 8. 處理未營業月份（6月、7月暑假）
# ============================================================================

# 建立完整的月份清單（2024/01 - 2025/05）
all_months = pd.period_range(start='2024-01', end='2025-05', freq='M')

# 建立完整的 DataFrame
full_monthly = pd.DataFrame({'YearMonth': all_months})
full_monthly['YearMonth_Str'] = full_monthly['YearMonth'].astype(str)

# 合併數據（保留所有月份）
monthly_pnl = full_monthly.merge(
    monthly_revenue,
    on='YearMonth',
    how='left',
    suffixes=('', '_drop')
)

# 更新 YearMonth_Str
monthly_pnl['YearMonth_Str'] = monthly_pnl['YearMonth'].astype(str)

# 填充未營業月份的數據
monthly_pnl['Operating_Days'] = monthly_pnl['Operating_Days'].fillna(0)
monthly_pnl['Net_Revenue'] = monthly_pnl['Net_Revenue'].fillna(0)
monthly_pnl['Gross_Sales'] = monthly_pnl['Gross_Sales'].fillna(0)
monthly_pnl['Food_Cost'] = monthly_pnl['Food_Cost'].fillna(0)
monthly_pnl['Labor_Cost'] = monthly_pnl['Labor_Cost'].fillna(0)
monthly_pnl['Fixed_Cost'] = monthly_pnl['Fixed_Cost'].fillna(3800)  # 即使未營業也有房租

# 重新計算未營業月份的損益
monthly_pnl['Total_Cost'] = (
    monthly_pnl['Food_Cost'] +
    monthly_pnl['Labor_Cost'] +
    monthly_pnl['Fixed_Cost']
)

monthly_pnl['Gross_Profit'] = (
    monthly_pnl['Net_Revenue'] - monthly_pnl['Food_Cost']
)

monthly_pnl['Operating_Profit'] = (
    monthly_pnl['Net_Revenue'] - monthly_pnl['Total_Cost']
)

# 避免除以零
monthly_pnl['Gross_Margin'] = np.where(
    monthly_pnl['Net_Revenue'] > 0,
    monthly_pnl['Gross_Profit'] / monthly_pnl['Net_Revenue'] * 100,
    0
)

monthly_pnl['Net_Margin'] = np.where(
    monthly_pnl['Net_Revenue'] > 0,
    monthly_pnl['Operating_Profit'] / monthly_pnl['Net_Revenue'] * 100,
    0
)

# ============================================================================
# 9. 計算總計
# ============================================================================

print("計算總計...")

totals = {
    'YearMonth_Str': '總計',
    'Operating_Days': monthly_pnl['Operating_Days'].sum(),
    'Net_Revenue': monthly_pnl['Net_Revenue'].sum(),
    'Gross_Sales': monthly_pnl['Gross_Sales'].sum(),
    'Food_Cost': monthly_pnl['Food_Cost'].sum(),
    'Labor_Cost': monthly_pnl['Labor_Cost'].sum(),
    'Fixed_Cost': monthly_pnl['Fixed_Cost'].sum(),
    'Total_Cost': monthly_pnl['Total_Cost'].sum(),
    'Gross_Profit': monthly_pnl['Gross_Profit'].sum(),
    'Operating_Profit': monthly_pnl['Operating_Profit'].sum(),
    'Gross_Margin': monthly_pnl['Gross_Profit'].sum() / monthly_pnl['Net_Revenue'].sum() * 100,
    'Net_Margin': monthly_pnl['Operating_Profit'].sum() / monthly_pnl['Net_Revenue'].sum() * 100
}

# 加入總計行
monthly_pnl_with_total = pd.concat([
    monthly_pnl,
    pd.DataFrame([totals])
], ignore_index=True)

# ============================================================================
# 10. 輸出結果
# ============================================================================

print("\n儲存結果...")

# 10.1 輸出完整數據（CSV）
output_csv = output_dir / 'monthly_pnl_2024_2025.csv'
monthly_pnl_with_total.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"已儲存：{output_csv}")

# 10.2 生成 Markdown 報告
report_md = output_dir / 'pnl_report_2024_2025.md'

with open(report_md, 'w', encoding='utf-8') as f:
    f.write("# Taiwanway 餐廳損益分析報告\n\n")
    f.write("**分析期間**：2024 年 1 月 - 2025 年 5 月（共 17 個月）\n\n")
    f.write("---\n\n")

    # 總計摘要
    f.write("## 📊 總計損益摘要\n\n")
    f.write("| 項目 | 金額 (USD) | 備註 |\n")
    f.write("|------|------------|------|\n")
    f.write(f"| **總營業天數** | {totals['Operating_Days']:.0f} 天 | |\n")
    f.write(f"| **總淨營收** | ${totals['Net_Revenue']:,.2f} | 去除稅金後 |\n")
    f.write(f"| **總毛利** | ${totals['Gross_Profit']:,.2f} | 淨營收 - 食材成本 |\n")
    f.write(f"| **總營業利潤** | ${totals['Operating_Profit']:,.2f} | 淨營收 - 總成本 |\n")
    f.write(f"| **平均毛利率** | {totals['Gross_Margin']:.2f}% | |\n")
    f.write(f"| **平均淨利率** | {totals['Net_Margin']:.2f}% | |\n")
    f.write("\n")

    # 成本結構
    f.write("## 💰 成本結構\n\n")
    f.write("| 成本項目 | 金額 (USD) | 佔淨營收比例 |\n")
    f.write("|----------|------------|-------------|\n")
    f.write(f"| **食材成本** | ${totals['Food_Cost']:,.2f} | {totals['Food_Cost']/totals['Net_Revenue']*100:.2f}% |\n")
    f.write(f"| **人力成本** | ${totals['Labor_Cost']:,.2f} | {totals['Labor_Cost']/totals['Net_Revenue']*100:.2f}% |\n")
    f.write(f"| **固定成本** | ${totals['Fixed_Cost']:,.2f} | {totals['Fixed_Cost']/totals['Net_Revenue']*100:.2f}% |\n")
    f.write(f"| **總成本** | ${totals['Total_Cost']:,.2f} | {totals['Total_Cost']/totals['Net_Revenue']*100:.2f}% |\n")
    f.write("\n")

    # 每月明細表
    f.write("## 📅 每月損益明細表\n\n")
    f.write("| 年月 | 營業天數 | 淨營收 | 食材成本 | 人力成本 | 固定成本 | 總成本 | 毛利 | 營業利潤 | 毛利率 | 淨利率 |\n")
    f.write("|------|---------|--------|---------|---------|---------|--------|------|----------|--------|--------|\n")

    for idx, row in monthly_pnl_with_total.iterrows():
        f.write(f"| {row['YearMonth_Str']} | ")
        f.write(f"{row['Operating_Days']:.0f} | ")
        f.write(f"${row['Net_Revenue']:,.2f} | ")
        f.write(f"${row['Food_Cost']:,.2f} | ")
        f.write(f"${row['Labor_Cost']:,.2f} | ")
        f.write(f"${row['Fixed_Cost']:,.2f} | ")
        f.write(f"${row['Total_Cost']:,.2f} | ")
        f.write(f"${row['Gross_Profit']:,.2f} | ")

        # 營業利潤（虧損用括號表示）
        profit = row['Operating_Profit']
        if profit < 0:
            f.write(f"(${abs(profit):,.2f}) | ")
        else:
            f.write(f"${profit:,.2f} | ")

        f.write(f"{row['Gross_Margin']:.2f}% | ")
        f.write(f"{row['Net_Margin']:.2f}% |\n")

    f.write("\n")

    # 關鍵發現
    f.write("## 🔍 關鍵發現\n\n")

    # 計算虧損月份
    loss_months = monthly_pnl[monthly_pnl['Operating_Profit'] < 0]
    profit_months = monthly_pnl[monthly_pnl['Operating_Profit'] > 0]

    f.write(f"1. **盈利月份**：{len(profit_months)} 個月\n")
    f.write(f"2. **虧損月份**：{len(loss_months)} 個月\n")
    f.write(f"3. **平均月營收**：${monthly_pnl['Net_Revenue'].mean():,.2f}\n")
    f.write(f"4. **平均月成本**：${monthly_pnl['Total_Cost'].mean():,.2f}\n")
    f.write(f"5. **平均月利潤**：${monthly_pnl['Operating_Profit'].mean():,.2f}\n")
    f.write("\n")

    # 分年度統計
    f.write("## 📈 分年度統計\n\n")

    # 2024 年統計
    monthly_2024 = monthly_pnl[monthly_pnl['YearMonth_Str'].str.startswith('2024')]
    f.write("### 2024 年（1-12 月）\n\n")
    f.write(f"- **總淨營收**：${monthly_2024['Net_Revenue'].sum():,.2f}\n")
    f.write(f"- **總成本**：${monthly_2024['Total_Cost'].sum():,.2f}\n")
    f.write(f"- **總營業利潤**：${monthly_2024['Operating_Profit'].sum():,.2f}\n")
    f.write(f"- **平均淨利率**：{monthly_2024['Operating_Profit'].sum() / monthly_2024['Net_Revenue'].sum() * 100:.2f}%\n")
    f.write("\n")

    # 2025 年統計
    monthly_2025 = monthly_pnl[monthly_pnl['YearMonth_Str'].str.startswith('2025')]
    f.write("### 2025 年（1-5 月）\n\n")
    f.write(f"- **總淨營收**：${monthly_2025['Net_Revenue'].sum():,.2f}\n")
    f.write(f"- **總成本**：${monthly_2025['Total_Cost'].sum():,.2f}\n")
    f.write(f"- **總營業利潤**：${monthly_2025['Operating_Profit'].sum():,.2f}\n")
    f.write(f"- **平均淨利率**：{monthly_2025['Operating_Profit'].sum() / monthly_2025['Net_Revenue'].sum() * 100:.2f}%\n")
    f.write("\n")

    # 計算規則說明
    f.write("## 📋 計算規則說明\n\n")
    f.write("### 營收計算\n")
    f.write("- **淨營收** = 總銷售額 / (1 + 0.08875)\n")
    f.write("- NYC 稅率：8.875%\n")
    f.write("\n")

    f.write("### 成本計算\n")
    f.write("1. **食材成本**：淨營收 × 35%\n")
    f.write("2. **人力成本**：\n")
    f.write("   - 2024/01-09：$0/天（無人力成本）\n")
    f.write("   - 2024/10 起：$70/天\n")
    f.write("3. **固定成本**：每月 $3,800（房租 $3,100 + 水電 $700）\n")
    f.write("   - **注意**：即使未營業月份（如 6-7 月暑假）也需支付房租\n")
    f.write("\n")

    f.write("### 營業規則\n")
    f.write("- **營業日**：週一、週二、週五、週六\n")
    f.write("- **暑假**：6 月、7 月通常未營業\n")
    f.write("\n")

    # 時間戳
    f.write("---\n\n")
    f.write(f"**報告生成時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print(f"已儲存：{report_md}")

# ============================================================================
# 11. 顯示摘要統計
# ============================================================================

print("\n" + "="*80)
print("Taiwanway 餐廳損益分析摘要（2024/01 - 2025/05）")
print("="*80)

print(f"\n總營業天數：{totals['Operating_Days']:.0f} 天")
print(f"總淨營收：${totals['Net_Revenue']:,.2f}")
print(f"總成本：${totals['Total_Cost']:,.2f}")
print(f"  - 食材成本：${totals['Food_Cost']:,.2f} ({totals['Food_Cost']/totals['Net_Revenue']*100:.2f}%)")
print(f"  - 人力成本：${totals['Labor_Cost']:,.2f} ({totals['Labor_Cost']/totals['Net_Revenue']*100:.2f}%)")
print(f"  - 固定成本：${totals['Fixed_Cost']:,.2f} ({totals['Fixed_Cost']/totals['Net_Revenue']*100:.2f}%)")

print(f"\n總毛利：${totals['Gross_Profit']:,.2f}")
print(f"總營業利潤：${totals['Operating_Profit']:,.2f}")
print(f"平均毛利率：{totals['Gross_Margin']:.2f}%")
print(f"平均淨利率：{totals['Net_Margin']:.2f}%")

print(f"\n盈利月份：{len(profit_months)} 個月")
print(f"虧損月份：{len(loss_months)} 個月")

print("\n" + "="*80)
print(f"完整報告已儲存至：")
print(f"  - CSV：{output_csv}")
print(f"  - Markdown：{report_md}")
print("="*80)

print("\n✅ 分析完成！")
