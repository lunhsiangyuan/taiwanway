#!/usr/bin/env python3
"""
VIP 和高消費客戶分析腳本
分析 VIP 客戶和單筆高消費客戶的消費型態、時間、場景和商品組合。
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pytz
from pathlib import Path
from datetime import datetime
from collections import Counter
import json

# 禁用 LaTeX 渲染以支持中文
plt.rcParams['text.usetex'] = False

# 設置中文字體
chinese_font_paths = [
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
]

for font_path in chinese_font_paths:
    if Path(font_path).exists():
        from matplotlib import font_manager
        chinese_font_prop = font_manager.FontProperties(fname=font_path)
        break


class VIPHighSpenderAnalyzer:
    """VIP 和高消費客戶分析器"""

    def __init__(self, items_csv_path, vip_visit_threshold=10, vip_spending_threshold=200,
                 high_transaction_threshold=50):
        """
        初始化分析器

        Args:
            items_csv_path: 商品明細 CSV 檔案路徑
            vip_visit_threshold: VIP 客戶最低造訪次數閾值
            vip_spending_threshold: VIP 客戶最低總消費閾值($)
            high_transaction_threshold: 高消費交易閾值($)
        """
        self.items_csv_path = items_csv_path
        self.vip_visit_threshold = vip_visit_threshold
        self.vip_spending_threshold = vip_spending_threshold
        self.high_transaction_threshold = high_transaction_threshold

        self.ny_tz = pytz.timezone('America/New_York')
        self.operating_days = [0, 1, 4, 5]  # Mon, Tue, Fri, Sat
        self.closed_months = [6, 7]  # June, July

        # 數據儲存
        self.df = None
        self.vip_customers = None
        self.high_transactions = None

        # 輸出目錄
        self.output_base = Path('analysis_output/vip_analysis')
        self.output_base.mkdir(parents=True, exist_ok=True)
        (self.output_base / 'charts').mkdir(exist_ok=True)
        (self.output_base / 'data').mkdir(exist_ok=True)

    def load_and_preprocess_data(self):
        """載入並預處理數據"""
        print("📊 載入商品明細數據...")

        # 讀取 CSV
        df = pd.read_csv(self.items_csv_path)
        print(f"   總記錄數: {len(df):,}")

        # 解析時間並轉換時區
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        # 假設原始時間是 Taipei 時區,轉換到 NY
        taipei_tz = pytz.timezone('Asia/Taipei')
        df['DateTime'] = df['DateTime'].dt.tz_localize(taipei_tz).dt.tz_convert(self.ny_tz)

        # 提取時間特徵
        df['Hour'] = df['DateTime'].dt.hour
        df['DayOfWeek'] = df['DateTime'].dt.dayofweek
        df['DayName'] = df['DateTime'].dt.day_name()
        df['Month'] = df['DateTime'].dt.month
        df['YearMonth'] = df['DateTime'].dt.to_period('M')
        df['Date'] = df['DateTime'].dt.date

        # 解析金額欄位
        for col in ['Gross Sales', 'Discounts', 'Net Sales', 'Tax']:
            if col in df.columns:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

        # 過濾營業時間(可選,根據需求)
        # 這裡保留所有數據以獲得完整視角

        self.df = df
        print(f"✓ 數據載入完成,共 {len(df):,} 筆記錄")

        return df

    def identify_vip_customers(self):
        """識別 VIP 客戶"""
        print("\n🌟 識別 VIP 客戶...")

        # 只分析有 Customer ID 的記錄
        df_with_customer = self.df[self.df['Customer ID'].notna()].copy()

        # 按客戶聚合
        customer_stats = df_with_customer.groupby('Customer ID').agg({
            'Transaction ID': 'nunique',  # 造訪次數(唯一交易數)
            'Net Sales': 'sum',  # 總消費
            'Customer Name': 'first'  # 客戶名稱
        }).reset_index()

        customer_stats.columns = ['CustomerID', 'VisitCount', 'TotalSpent', 'CustomerName']
        customer_stats['AvgSpent'] = customer_stats['TotalSpent'] / customer_stats['VisitCount']

        # 應用 VIP 規則: visits > 10 OR total_spent > $200
        vip_mask = (
            (customer_stats['VisitCount'] > self.vip_visit_threshold) |
            (customer_stats['TotalSpent'] > self.vip_spending_threshold)
        )

        vip_customers = customer_stats[vip_mask].copy()
        vip_customers = vip_customers.sort_values('TotalSpent', ascending=False)

        print(f"✓ 識別出 {len(vip_customers)} 位 VIP 客戶")
        print(f"  - 總消費: ${vip_customers['TotalSpent'].sum():,.2f}")
        print(f"  - 平均造訪次數: {vip_customers['VisitCount'].mean():.1f}")
        print(f"  - 平均總消費: ${vip_customers['TotalSpent'].mean():.2f}")

        self.vip_customers = vip_customers
        return vip_customers

    def identify_high_transactions(self):
        """識別高單筆消費交易"""
        print(f"\n💰 識別高消費交易(>${self.high_transaction_threshold})...")

        # 按交易聚合
        transaction_stats = self.df.groupby('Transaction ID').agg({
            'Net Sales': 'sum',  # 交易總金額
            'Item': 'count',  # 商品數量
            'Customer ID': 'first',
            'Customer Name': 'first',
            'DateTime': 'first',
            'Dining Option': 'first'
        }).reset_index()

        transaction_stats.columns = [
            'TransactionID', 'TotalAmount', 'ItemCount',
            'CustomerID', 'CustomerName', 'DateTime', 'DiningOption'
        ]

        # 篩選高消費交易
        high_transactions = transaction_stats[
            transaction_stats['TotalAmount'] >= self.high_transaction_threshold
        ].copy()

        high_transactions = high_transactions.sort_values('TotalAmount', ascending=False)

        print(f"✓ 識別出 {len(high_transactions)} 筆高消費交易")
        print(f"  - 總金額: ${high_transactions['TotalAmount'].sum():,.2f}")
        print(f"  - 平均交易額: ${high_transactions['TotalAmount'].mean():.2f}")
        print(f"  - 平均商品數: {high_transactions['ItemCount'].mean():.1f}")

        self.high_transactions = high_transactions
        return high_transactions

    def analyze_vip_product_preferences(self):
        """分析 VIP 客戶的商品偏好"""
        print("\n📦 分析 VIP 客戶商品偏好...")

        # 獲取 VIP 客戶的所有交易
        vip_ids = self.vip_customers['CustomerID'].tolist()
        vip_transactions = self.df[self.df['Customer ID'].isin(vip_ids)].copy()

        results = {}

        # 1. Top 商品
        top_items = vip_transactions.groupby('Item').agg({
            'Qty': 'sum',
            'Net Sales': 'sum',
            'Transaction ID': 'nunique'
        }).reset_index()
        top_items.columns = ['Item', 'TotalQty', 'TotalRevenue', 'TransactionCount']
        top_items = top_items.sort_values('TotalQty', ascending=False).head(20)
        results['top_items'] = top_items.to_dict('records')

        # 2. Top 類別
        top_categories = vip_transactions.groupby('Category').agg({
            'Qty': 'sum',
            'Net Sales': 'sum',
            'Transaction ID': 'nunique'
        }).reset_index()
        top_categories.columns = ['Category', 'TotalQty', 'TotalRevenue', 'TransactionCount']
        top_categories = top_categories.sort_values('TotalRevenue', ascending=False)
        results['top_categories'] = top_categories.to_dict('records')

        # 3. 商品組合分析(同一交易中的商品)
        combos = self._analyze_product_combinations(vip_transactions, top_n=15)
        results['common_combinations'] = combos

        # 4. 客製化偏好
        customization_rate = len(
            vip_transactions[vip_transactions['Modifiers Applied'].notna() &
                           (vip_transactions['Modifiers Applied'] != '')]
        ) / len(vip_transactions) * 100
        results['customization_rate'] = f"{customization_rate:.1f}%"

        print(f"✓ VIP 客戶最愛商品: {top_items.iloc[0]['Item']} (購買 {top_items.iloc[0]['TotalQty']:.0f} 次)")
        print(f"✓ VIP 客戶最愛類別: {top_categories.iloc[0]['Category']} (營收 ${top_categories.iloc[0]['TotalRevenue']:,.2f})")
        print(f"✓ 客製化比例: {customization_rate:.1f}%")

        return results

    def analyze_vip_temporal_patterns(self):
        """分析 VIP 客戶的時間型態"""
        print("\n🕐 分析 VIP 客戶時間型態...")

        vip_ids = self.vip_customers['CustomerID'].tolist()
        vip_transactions = self.df[self.df['Customer ID'].isin(vip_ids)].copy()

        results = {}

        # 1. 小時分布
        hourly = vip_transactions.groupby('Hour').agg({
            'Transaction ID': 'nunique',
            'Net Sales': 'sum'
        }).reset_index()
        hourly.columns = ['Hour', 'TransactionCount', 'Revenue']
        results['hourly_distribution'] = hourly.to_dict('records')

        # 2. 星期幾分布
        weekday = vip_transactions.groupby('DayName').agg({
            'Transaction ID': 'nunique',
            'Net Sales': 'sum'
        }).reset_index()
        weekday.columns = ['DayName', 'TransactionCount', 'Revenue']
        results['weekday_distribution'] = weekday.to_dict('records')

        # 3. 月份分布
        monthly = vip_transactions.groupby('Month').agg({
            'Transaction ID': 'nunique',
            'Net Sales': 'sum'
        }).reset_index()
        monthly.columns = ['Month', 'TransactionCount', 'Revenue']
        results['monthly_distribution'] = monthly.to_dict('records')

        peak_hour = hourly.loc[hourly['TransactionCount'].idxmax(), 'Hour']
        peak_day = weekday.loc[weekday['TransactionCount'].idxmax(), 'DayName']

        print(f"✓ VIP 客戶尖峰時段: {int(peak_hour)}:00")
        print(f"✓ VIP 客戶偏好日: {peak_day}")

        return results

    def analyze_vip_dining_preferences(self):
        """分析 VIP 客戶的用餐場景偏好"""
        print("\n🍽️  分析 VIP 客戶用餐場景...")

        vip_ids = self.vip_customers['CustomerID'].tolist()
        vip_transactions = self.df[self.df['Customer ID'].isin(vip_ids)].copy()

        # Dining Option 分布
        dining_stats = vip_transactions.groupby('Dining Option').agg({
            'Transaction ID': 'nunique',
            'Net Sales': 'sum'
        }).reset_index()
        dining_stats.columns = ['DiningOption', 'TransactionCount', 'Revenue']
        dining_stats['Percentage'] = (
            dining_stats['TransactionCount'] / dining_stats['TransactionCount'].sum() * 100
        )

        results = dining_stats.to_dict('records')

        if len(dining_stats) > 0:
            top_option = dining_stats.loc[dining_stats['TransactionCount'].idxmax(), 'DiningOption']
            top_pct = dining_stats.loc[dining_stats['TransactionCount'].idxmax(), 'Percentage']
            print(f"✓ VIP 客戶偏好: {top_option} ({top_pct:.1f}%)")

        return results

    def analyze_high_transaction_patterns(self):
        """分析高單筆消費交易的型態"""
        print("\n💎 分析高消費交易型態...")

        high_tx_ids = self.high_transactions['TransactionID'].tolist()
        high_tx_items = self.df[self.df['Transaction ID'].isin(high_tx_ids)].copy()

        results = {}

        # 1. 商品組合
        combos = self._analyze_product_combinations(high_tx_items, top_n=15)
        results['common_combinations'] = combos

        # 2. 類別分布
        category_dist = high_tx_items.groupby('Category').agg({
            'Qty': 'sum',
            'Net Sales': 'sum'
        }).reset_index()
        category_dist.columns = ['Category', 'TotalQty', 'TotalRevenue']
        category_dist = category_dist.sort_values('TotalRevenue', ascending=False)
        results['category_distribution'] = category_dist.to_dict('records')

        # 3. 平均商品數
        avg_items = self.high_transactions['ItemCount'].mean()
        results['avg_items_per_transaction'] = avg_items

        # 4. 時間分布
        high_tx_items['Hour'] = high_tx_items['DateTime'].dt.hour
        hourly = high_tx_items.groupby('Hour')['Transaction ID'].nunique()
        peak_hour = hourly.idxmax()
        results['peak_hour'] = int(peak_hour)

        # 5. Dining Option
        dining = high_tx_items.groupby('Dining Option')['Transaction ID'].nunique()
        results['dining_distribution'] = dining.to_dict()

        print(f"✓ 高消費交易平均含 {avg_items:.1f} 個商品")
        print(f"✓ 高消費交易尖峰時段: {int(peak_hour)}:00")

        return results

    def _analyze_product_combinations(self, df, top_n=10):
        """分析同一交易中的商品組合"""
        # 按交易分組,獲取商品列表
        transaction_items = df.groupby('Transaction ID')['Item'].apply(list).reset_index()

        # 只看多商品交易
        multi_item_tx = transaction_items[transaction_items['Item'].apply(len) > 1]

        # 計算商品對組合
        combinations = []
        for items in multi_item_tx['Item']:
            items_sorted = sorted(set(items))
            if len(items_sorted) >= 2:
                # 生成所有兩兩組合
                from itertools import combinations as iter_combinations
                for combo in iter_combinations(items_sorted, 2):
                    combinations.append(' + '.join(combo))

        # 統計最常見組合
        combo_counts = Counter(combinations)
        top_combos = [
            {"combination": combo, "count": count}
            for combo, count in combo_counts.most_common(top_n)
        ]

        return top_combos

    def generate_visualizations(self):
        """生成視覺化圖表"""
        print("\n📊 生成視覺化圖表...")

        # 1. VIP 客戶 Top 商品
        self._plot_vip_top_items()

        # 2. VIP 客戶時間分布
        self._plot_vip_temporal_patterns()

        # 3. VIP vs 非VIP 比較
        self._plot_vip_comparison()

        # 4. 高消費交易分析
        self._plot_high_transaction_analysis()

        print("✓ 圖表已保存到 analysis_output/vip_analysis/charts/")

    def _plot_vip_top_items(self):
        """繪製 VIP 客戶 Top 商品圖表"""
        vip_ids = self.vip_customers['CustomerID'].tolist()
        vip_transactions = self.df[self.df['Customer ID'].isin(vip_ids)].copy()

        top_items = vip_transactions.groupby('Item')['Qty'].sum().sort_values(ascending=False).head(15)

        fig, ax = plt.subplots(figsize=(12, 8))
        top_items.plot(kind='barh', ax=ax, color='steelblue')
        ax.set_title('VIP 客戶最常購買的商品 Top 15', fontproperties=chinese_font_prop, fontsize=16, pad=20)
        ax.set_xlabel('購買次數', fontproperties=chinese_font_prop, fontsize=12)
        ax.set_ylabel('商品名稱', fontproperties=chinese_font_prop, fontsize=12)
        ax.invert_yaxis()

        # 設置 y 軸標籤字體
        ax.set_yticklabels(ax.get_yticklabels(), fontproperties=chinese_font_prop)

        plt.tight_layout()
        plt.savefig(self.output_base / 'charts' / 'vip_top_items.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _plot_vip_temporal_patterns(self):
        """繪製 VIP 客戶時間型態圖表"""
        vip_ids = self.vip_customers['CustomerID'].tolist()
        vip_transactions = self.df[self.df['Customer ID'].isin(vip_ids)].copy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # 小時分布
        hourly = vip_transactions.groupby('Hour')['Transaction ID'].nunique()
        ax1.bar(hourly.index, hourly.values, color='coral')
        ax1.set_title('VIP 客戶消費時段分布', fontproperties=chinese_font_prop, fontsize=14, pad=15)
        ax1.set_xlabel('小時', fontproperties=chinese_font_prop, fontsize=12)
        ax1.set_ylabel('交易次數', fontproperties=chinese_font_prop, fontsize=12)
        ax1.grid(axis='y', alpha=0.3)

        # 星期分布
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = vip_transactions.groupby('DayName')['Transaction ID'].nunique()
        weekday = weekday.reindex(day_order, fill_value=0)

        ax2.bar(range(len(weekday)), weekday.values, color='teal')
        ax2.set_title('VIP 客戶星期分布', fontproperties=chinese_font_prop, fontsize=14, pad=15)
        ax2.set_xlabel('星期', fontproperties=chinese_font_prop, fontsize=12)
        ax2.set_ylabel('交易次數', fontproperties=chinese_font_prop, fontsize=12)
        ax2.set_xticks(range(len(day_order)))
        ax2.set_xticklabels(['一', '二', '三', '四', '五', '六', '日'], fontproperties=chinese_font_prop)
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_base / 'charts' / 'vip_temporal_patterns.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _plot_vip_comparison(self):
        """繪製 VIP vs 非VIP 比較圖"""
        vip_ids = self.vip_customers['CustomerID'].tolist()

        # 有客戶ID的交易
        df_with_customer = self.df[self.df['Customer ID'].notna()].copy()
        df_with_customer['IsVIP'] = df_with_customer['Customer ID'].isin(vip_ids)

        comparison = df_with_customer.groupby('IsVIP').agg({
            'Transaction ID': 'nunique',
            'Net Sales': 'sum'
        }).reset_index()

        comparison['AvgTransactionValue'] = comparison['Net Sales'] / comparison['Transaction ID']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # 交易次數比較
        labels = ['非VIP', 'VIP']
        values = comparison['Transaction ID'].values
        colors = ['lightblue', 'gold']

        ax1.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('VIP vs 非VIP 交易次數比例', fontproperties=chinese_font_prop, fontsize=14, pad=15)

        # 平均交易額比較
        ax2.bar(labels, comparison['AvgTransactionValue'].values, color=colors)
        ax2.set_title('VIP vs 非VIP 平均交易額', fontproperties=chinese_font_prop, fontsize=14, pad=15)
        ax2.set_ylabel('平均交易額 ($)', fontproperties=chinese_font_prop, fontsize=12)
        ax2.set_xticklabels(labels, fontproperties=chinese_font_prop)
        for i, v in enumerate(comparison['AvgTransactionValue'].values):
            ax2.text(i, v + 0.5, f'${v:.2f}', ha='center', fontsize=10)

        plt.tight_layout()
        plt.savefig(self.output_base / 'charts' / 'vip_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _plot_high_transaction_analysis(self):
        """繪製高消費交易分析圖"""
        high_tx_ids = self.high_transactions['TransactionID'].tolist()
        high_tx_items = self.df[self.df['Transaction ID'].isin(high_tx_ids)].copy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Top 類別
        top_categories = high_tx_items.groupby('Category')['Net Sales'].sum().sort_values(ascending=False).head(10)
        ax1.barh(range(len(top_categories)), top_categories.values, color='darkgreen')
        ax1.set_yticks(range(len(top_categories)))
        ax1.set_yticklabels(top_categories.index, fontproperties=chinese_font_prop)
        ax1.set_title('高消費交易 Top 類別(按營收)', fontproperties=chinese_font_prop, fontsize=14, pad=15)
        ax1.set_xlabel('營收 ($)', fontproperties=chinese_font_prop, fontsize=12)
        ax1.invert_yaxis()

        # 時段分布
        high_tx_items['Hour'] = high_tx_items['DateTime'].dt.hour
        hourly = high_tx_items.groupby('Hour')['Transaction ID'].nunique()
        ax2.bar(hourly.index, hourly.values, color='purple', alpha=0.7)
        ax2.set_title('高消費交易時段分布', fontproperties=chinese_font_prop, fontsize=14, pad=15)
        ax2.set_xlabel('小時', fontproperties=chinese_font_prop, fontsize=12)
        ax2.set_ylabel('交易次數', fontproperties=chinese_font_prop, fontsize=12)
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_base / 'charts' / 'high_transaction_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()

    def generate_report(self):
        """生成完整分析報告"""
        print("\n📄 生成分析報告...")

        # 收集所有分析結果
        report = {
            "generated_at": datetime.now().isoformat(),
            "parameters": {
                "vip_visit_threshold": self.vip_visit_threshold,
                "vip_spending_threshold": self.vip_spending_threshold,
                "high_transaction_threshold": self.high_transaction_threshold
            },
            "vip_analysis": {
                "customer_count": len(self.vip_customers),
                "total_revenue": float(self.vip_customers['TotalSpent'].sum()),
                "avg_visits": float(self.vip_customers['VisitCount'].mean()),
                "avg_spending": float(self.vip_customers['TotalSpent'].mean()),
                "product_preferences": self.analyze_vip_product_preferences(),
                "temporal_patterns": self.analyze_vip_temporal_patterns(),
                "dining_preferences": self.analyze_vip_dining_preferences()
            },
            "high_transaction_analysis": {
                "transaction_count": len(self.high_transactions),
                "total_amount": float(self.high_transactions['TotalAmount'].sum()),
                "avg_amount": float(self.high_transactions['TotalAmount'].mean()),
                "patterns": self.analyze_high_transaction_patterns()
            }
        }

        # 保存 JSON 報告
        report_path = self.output_base / 'data' / f'vip_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"✓ JSON 報告已保存: {report_path}")

        # 保存 CSV 數據
        self.vip_customers.to_csv(
            self.output_base / 'data' / 'vip_customers.csv',
            index=False,
            encoding='utf-8-sig'
        )

        self.high_transactions.to_csv(
            self.output_base / 'data' / 'high_transactions.csv',
            index=False,
            encoding='utf-8-sig'
        )

        print("✓ CSV 數據已保存")

        # 生成 Markdown 摘要
        self._generate_markdown_summary(report)

        return report

    def _generate_markdown_summary(self, report):
        """生成 Markdown 摘要報告"""
        vip = report['vip_analysis']
        high_tx = report['high_transaction_analysis']

        md_content = f"""# VIP 和高消費客戶分析報告

生成時間: {report['generated_at']}

## 📋 分析參數

- VIP 客戶定義: 造訪次數 > {self.vip_visit_threshold} 或 總消費 > ${self.vip_spending_threshold}
- 高消費交易定義: 單筆交易 ≥ ${self.high_transaction_threshold}

---

## 🌟 VIP 客戶分析

### 基本統計

- **VIP 客戶數量**: {vip['customer_count']} 位
- **VIP 總營收**: ${vip['total_revenue']:,.2f}
- **平均造訪次數**: {vip['avg_visits']:.1f} 次
- **平均總消費**: ${vip['avg_spending']:.2f}

### 商品偏好

**最受歡迎的商品 Top 5:**

"""

        for i, item in enumerate(vip['product_preferences']['top_items'][:5], 1):
            md_content += f"{i}. **{item['Item']}** - 購買 {item['TotalQty']:.0f} 次,營收 ${item['TotalRevenue']:,.2f}\n"

        md_content += "\n**最受歡迎的類別:**\n\n"

        for i, cat in enumerate(vip['product_preferences']['top_categories'][:5], 1):
            md_content += f"{i}. **{cat['Category']}** - 營收 ${cat['TotalRevenue']:,.2f}\n"

        md_content += f"""
### 時間型態

**尖峰時段:** {vip['temporal_patterns']['hourly_distribution'][0]['Hour']}:00

**偏好星期:** 分布如下圖表

### 用餐場景偏好

"""

        for pref in vip['dining_preferences']:
            md_content += f"- **{pref['DiningOption']}**: {pref['Percentage']:.1f}% ({pref['TransactionCount']} 筆交易)\n"

        md_content += f"""
---

## 💰 高消費交易分析

### 基本統計

- **高消費交易數量**: {high_tx['transaction_count']} 筆
- **總金額**: ${high_tx['total_amount']:,.2f}
- **平均交易額**: ${high_tx['avg_amount']:.2f}
- **平均商品數**: {high_tx['patterns']['avg_items_per_transaction']:.1f} 個

### 商品組合特徵

**常見組合 Top 10:**

"""

        for i, combo in enumerate(high_tx['patterns']['common_combinations'][:10], 1):
            md_content += f"{i}. {combo['combination']} (出現 {combo['count']} 次)\n"

        md_content += f"""
### 時間特徵

**尖峰時段:** {high_tx['patterns']['peak_hour']}:00

### 場景分布

"""

        for option, count in high_tx['patterns']['dining_distribution'].items():
            md_content += f"- **{option}**: {count} 筆交易\n"

        md_content += """
---

## 📊 圖表

請查看 `analysis_output/vip_analysis/charts/` 目錄中的視覺化圖表:

- `vip_top_items.png` - VIP 客戶最常購買的商品
- `vip_temporal_patterns.png` - VIP 客戶時間型態分布
- `vip_comparison.png` - VIP vs 非VIP 比較
- `high_transaction_analysis.png` - 高消費交易分析

## 📁 數據檔案

- `vip_customers.csv` - VIP 客戶明細
- `high_transactions.csv` - 高消費交易明細
- `vip_analysis_report_*.json` - 完整 JSON 報告
"""

        # 保存 Markdown
        md_path = self.output_base / f'VIP_Analysis_Summary_{datetime.now().strftime("%Y%m%d")}.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✓ Markdown 摘要已保存: {md_path}")

    def run_full_analysis(self):
        """執行完整分析流程"""
        print("=" * 80)
        print("VIP 和高消費客戶分析系統")
        print("=" * 80)

        # 1. 載入數據
        self.load_and_preprocess_data()

        # 2. 識別 VIP 和高消費交易
        self.identify_vip_customers()
        self.identify_high_transactions()

        # 3. 生成報告和視覺化
        self.generate_visualizations()
        report = self.generate_report()

        print("\n" + "=" * 80)
        print("✅ 分析完成!")
        print(f"📂 輸出目錄: {self.output_base}")
        print("=" * 80)

        return report


def main():
    """主函數"""
    import sys

    # 設定檔案路徑
    items_csv = 'data/items-2025-01-01-2025-11-16.csv'

    if not Path(items_csv).exists():
        print(f"❌ 錯誤: 找不到檔案 {items_csv}")
        sys.exit(1)

    # 初始化分析器
    analyzer = VIPHighSpenderAnalyzer(
        items_csv_path=items_csv,
        vip_visit_threshold=10,
        vip_spending_threshold=200,
        high_transaction_threshold=50
    )

    # 執行分析
    report = analyzer.run_full_analysis()

    return report


if __name__ == '__main__':
    main()
