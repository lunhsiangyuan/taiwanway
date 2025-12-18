#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客戶分群比較分析 - 春季 vs 秋季
比較 2025-01-05 和 2025-08-12/01 兩個時間段的客戶分群差異

特徵維度：擴展 RFM（6 維）
- Recency: 最近購買距今天數
- Frequency: 交易次數
- Monetary: 總消費金額
- Avg Order Value: 平均單次消費
- Hour Preference: 最常消費時段
- Category Diversity: 品項多樣性
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import warnings
import os
import json
from datetime import datetime, date
from collections import Counter

warnings.filterwarnings('ignore')

# ============================================================
# 中文字體設置
# ============================================================
plt.rcParams['text.usetex'] = False
plt.rcParams['axes.unicode_minus'] = False

chinese_font_paths = [
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
]

chinese_font_prop = None
for font_path in chinese_font_paths:
    if os.path.exists(font_path):
        try:
            chinese_font_prop = fm.FontProperties(fname=font_path)
            print(f"✓ 載入中文字體: {font_path}")
            break
        except:
            continue

if chinese_font_prop is None:
    print("⚠️  未找到中文字體，使用系統預設")
    chinese_font_prop = fm.FontProperties()

# ============================================================
# 配置
# ============================================================
DATA_FILE = 'data/items-2025-01-01-2025-11-16.csv'
OUTPUT_DIR = 'analysis_output/customer_segmentation'

# 時間段定義
SPRING_START = '2025-01-01'
SPRING_END = '2025-05-31'
FALL_START = '2025-08-01'
FALL_END = '2025-12-01'

# 基準日期（用於計算 Recency）
SPRING_REFERENCE = date(2025, 5, 31)
FALL_REFERENCE = date(2025, 12, 1)

# 分群數量
N_CLUSTERS = 3

# 建立輸出目錄
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/data', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/charts', exist_ok=True)


# ============================================================
# 數據載入與預處理
# ============================================================
def load_and_preprocess(file_path):
    """載入並預處理 Items CSV 數據"""
    print("=" * 70)
    print("📊 載入數據...")
    print("=" * 70)

    df = pd.read_csv(file_path)
    print(f"✓ 載入 {len(df)} 筆交易記錄")
    print(f"✓ 欄位: {list(df.columns)}")

    # 建立 DateTime（處理時區轉換：Taipei → NY）
    import pytz
    taipei_tz = pytz.timezone('Asia/Taipei')
    ny_tz = pytz.timezone('America/New_York')

    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    # 標記為 Taipei 時區，然後轉換為 NY 時區
    df['DateTime'] = df['DateTime'].dt.tz_localize(taipei_tz).dt.tz_convert(ny_tz)
    df['Hour'] = df['DateTime'].dt.hour
    df['Date_parsed'] = df['DateTime'].dt.date

    # 清理金額欄位
    df['Net Sales'] = df['Net Sales'].replace(r'[\$,]', '', regex=True).astype(float)
    df['Gross Sales'] = df['Gross Sales'].replace(r'[\$,]', '', regex=True).astype(float)

    # 建立代理客戶 ID（Card Brand + PAN Suffix）
    df['Card Brand'] = df['Card Brand'].fillna('')
    df['PAN Suffix'] = df['PAN Suffix'].fillna('')

    # 過濾有卡片資訊的記錄
    df_valid = df[(df['Card Brand'] != '') & (df['PAN Suffix'] != '')].copy()
    df_valid['proxy_customer_id'] = df_valid['Card Brand'] + '_' + df_valid['PAN Suffix'].astype(str)

    coverage = len(df_valid) / len(df) * 100
    print(f"\n✓ 有效記錄（有卡片資訊）: {len(df_valid)} 筆 ({coverage:.1f}%)")
    print(f"✓ 唯一代理客戶數: {df_valid['proxy_customer_id'].nunique()}")

    return df_valid


def filter_by_period(df, start_date, end_date):
    """按時間段篩選數據"""
    start = pd.to_datetime(start_date).date()
    end = pd.to_datetime(end_date).date()

    mask = (df['Date_parsed'] >= start) & (df['Date_parsed'] <= end)
    df_filtered = df[mask].copy()

    print(f"  日期範圍: {start} 至 {end}")
    print(f"  記錄數: {len(df_filtered)}")
    print(f"  唯一客戶: {df_filtered['proxy_customer_id'].nunique()}")

    return df_filtered


# ============================================================
# 特徵計算（擴展 RFM）
# ============================================================
def calculate_extended_rfm(df, reference_date, period_name):
    """計算擴展 RFM 特徵（6 維）"""
    print(f"\n🔧 計算 {period_name} RFM 特徵（基準日: {reference_date}）...")

    # 按客戶聚合
    customer_data = df.groupby('proxy_customer_id').agg({
        'Date_parsed': ['max', 'nunique'],           # 最近購買日、購買天數
        'Transaction ID': 'nunique',                  # 交易次數
        'Net Sales': 'sum',                           # 總消費
        'Hour': lambda x: Counter(x).most_common(1)[0][0],  # 最常消費時段
        'Category': 'nunique',                        # 品項多樣性
    }).reset_index()

    # 扁平化欄位名稱
    customer_data.columns = [
        'proxy_customer_id',
        'last_purchase', 'purchase_days',
        'frequency',
        'monetary',
        'hour_preference',
        'category_diversity'
    ]

    # 計算 Recency
    customer_data['recency'] = customer_data['last_purchase'].apply(
        lambda x: (reference_date - x).days
    )

    # 計算平均單次消費
    customer_data['avg_order_value'] = customer_data['monetary'] / customer_data['frequency']

    # 選擇最終特徵
    rfm_features = customer_data[[
        'proxy_customer_id',
        'recency',
        'frequency',
        'monetary',
        'avg_order_value',
        'hour_preference',
        'category_diversity'
    ]].copy()

    # 統計摘要
    print(f"\n  ✓ 客戶數: {len(rfm_features)}")
    print(f"  ✓ Recency: 平均 {rfm_features['recency'].mean():.1f} 天, 範圍 {rfm_features['recency'].min()}-{rfm_features['recency'].max()} 天")
    print(f"  ✓ Frequency: 平均 {rfm_features['frequency'].mean():.2f} 次, 範圍 {rfm_features['frequency'].min()}-{rfm_features['frequency'].max()} 次")
    print(f"  ✓ Monetary: 平均 ${rfm_features['monetary'].mean():.2f}, 範圍 ${rfm_features['monetary'].min():.2f}-${rfm_features['monetary'].max():.2f}")
    print(f"  ✓ AOV: 平均 ${rfm_features['avg_order_value'].mean():.2f}")
    print(f"  ✓ Category Diversity: 平均 {rfm_features['category_diversity'].mean():.2f} 類")

    return rfm_features, customer_data


# ============================================================
# K-means 分群
# ============================================================
def perform_clustering(rfm_features, n_clusters=N_CLUSTERS, period_name=''):
    """執行 K-means 分群"""
    print(f"\n🎯 執行 {period_name} K-means 分群 (K={n_clusters})...")

    # 選擇分群特徵
    feature_cols = ['recency', 'frequency', 'monetary', 'avg_order_value', 'hour_preference', 'category_diversity']
    X = rfm_features[feature_cols].values

    # 標準化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # 評估指標
    sil_score = silhouette_score(X_scaled, clusters)
    db_score = davies_bouldin_score(X_scaled, clusters)

    print(f"  ✓ 分群完成")
    print(f"  ✓ 各群人數: {dict(zip(*np.unique(clusters, return_counts=True)))}")
    print(f"  ✓ Silhouette Score: {sil_score:.4f}")
    print(f"  ✓ Davies-Bouldin Index: {db_score:.4f}")

    # 添加分群結果
    rfm_features = rfm_features.copy()
    rfm_features['cluster'] = clusters

    return rfm_features, kmeans, scaler, sil_score, db_score


def name_clusters(rfm_features):
    """為分群命名（基於分群間相對排名）"""
    rfm_copy = rfm_features.copy()

    # 計算各群的平均指標
    cluster_stats = rfm_copy.groupby('cluster').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    }).reset_index()

    # 計算綜合分數（Frequency 和 Monetary 越高越好，Recency 越低越好）
    # 標準化後加權
    cluster_stats['r_rank'] = cluster_stats['recency'].rank(ascending=True)   # Recency 低 = 好
    cluster_stats['f_rank'] = cluster_stats['frequency'].rank(ascending=False) # Frequency 高 = 好
    cluster_stats['m_rank'] = cluster_stats['monetary'].rank(ascending=False)  # Monetary 高 = 好
    cluster_stats['total_rank'] = cluster_stats['r_rank'] + cluster_stats['f_rank'] + cluster_stats['m_rank']

    # 根據總排名分配名稱
    cluster_stats = cluster_stats.sort_values('total_rank')
    n_clusters = len(cluster_stats)

    cluster_names = {}
    cluster_descriptions = {}

    name_list = ['VIP 忠誠客戶', '活躍客戶', '潛在流失客戶']
    desc_list = [
        '高頻率、高消費的核心客戶',
        '中等活躍度的穩定客戶',
        '低頻率或低消費，需關注'
    ]

    for i, row in enumerate(cluster_stats.itertuples()):
        cluster_id = row.cluster
        name_idx = min(i, len(name_list) - 1)
        cluster_names[cluster_id] = name_list[name_idx]
        cluster_descriptions[cluster_id] = desc_list[name_idx]

    rfm_copy['cluster_name'] = rfm_copy['cluster'].map(cluster_names)

    # 打印分群統計
    print(f"\n  分群統計:")
    for cluster_id in sorted(cluster_names.keys()):
        cluster_data = rfm_copy[rfm_copy['cluster'] == cluster_id]
        name = cluster_names[cluster_id]
        print(f"    {name}: {len(cluster_data)} 人, "
              f"R={cluster_data['recency'].mean():.1f}, "
              f"F={cluster_data['frequency'].mean():.2f}, "
              f"M=${cluster_data['monetary'].mean():.2f}")

    return rfm_copy, cluster_names, cluster_descriptions


# ============================================================
# 跨時段比較分析
# ============================================================
def compare_periods(spring_rfm, fall_rfm, spring_names, fall_names):
    """比較兩個時段的分群差異"""
    print("\n" + "=" * 70)
    print("📊 跨時段比較分析")
    print("=" * 70)

    comparison = {}

    # 1. 分群人數分布
    print("\n【1. 分群人數分布】")
    spring_dist = spring_rfm['cluster_name'].value_counts()
    fall_dist = fall_rfm['cluster_name'].value_counts()

    distribution = {}
    all_names = set(spring_dist.index) | set(fall_dist.index)
    for name in all_names:
        spring_count = spring_dist.get(name, 0)
        fall_count = fall_dist.get(name, 0)
        spring_pct = spring_count / len(spring_rfm) * 100
        fall_pct = fall_count / len(fall_rfm) * 100
        change = fall_count - spring_count
        pct_change = fall_pct - spring_pct

        distribution[name] = {
            'spring_count': int(spring_count),
            'spring_pct': round(spring_pct, 1),
            'fall_count': int(fall_count),
            'fall_pct': round(fall_pct, 1),
            'change': int(change),
            'pct_change': round(pct_change, 1)
        }

        print(f"  {name}:")
        print(f"    春季: {spring_count} 人 ({spring_pct:.1f}%)")
        print(f"    秋季: {fall_count} 人 ({fall_pct:.1f}%)")
        print(f"    變化: {change:+d} 人 ({pct_change:+.1f}%)")

    comparison['distribution'] = distribution

    # 2. RFM 指標變化
    print("\n【2. RFM 指標變化】")
    metrics = ['recency', 'frequency', 'monetary', 'avg_order_value', 'category_diversity']
    metric_names = {
        'recency': 'Recency (天)',
        'frequency': 'Frequency (次)',
        'monetary': 'Monetary ($)',
        'avg_order_value': 'AOV ($)',
        'category_diversity': 'Category Diversity'
    }

    rfm_changes = {}
    for metric in metrics:
        spring_avg = spring_rfm[metric].mean()
        fall_avg = fall_rfm[metric].mean()
        change = fall_avg - spring_avg
        pct_change = (change / spring_avg * 100) if spring_avg != 0 else 0

        rfm_changes[metric] = {
            'spring_avg': round(spring_avg, 2),
            'fall_avg': round(fall_avg, 2),
            'change': round(change, 2),
            'pct_change': round(pct_change, 1)
        }

        print(f"  {metric_names[metric]}:")
        print(f"    春季: {spring_avg:.2f}")
        print(f"    秋季: {fall_avg:.2f}")
        print(f"    變化: {change:+.2f} ({pct_change:+.1f}%)")

    comparison['rfm_changes'] = rfm_changes

    # 3. 客戶留存分析
    print("\n【3. 客戶留存分析】")
    spring_ids = set(spring_rfm['proxy_customer_id'].unique())
    fall_ids = set(fall_rfm['proxy_customer_id'].unique())

    returning = spring_ids & fall_ids
    new_fall = fall_ids - spring_ids
    lost = spring_ids - fall_ids

    retention_rate = len(returning) / len(spring_ids) * 100 if spring_ids else 0

    retention = {
        'spring_total': len(spring_ids),
        'fall_total': len(fall_ids),
        'returning_customers': len(returning),
        'new_customers_fall': len(new_fall),
        'lost_customers': len(lost),
        'retention_rate': round(retention_rate, 1)
    }

    print(f"  春季總客戶: {len(spring_ids)} 人")
    print(f"  秋季總客戶: {len(fall_ids)} 人")
    print(f"  回頭客: {len(returning)} 人 ({retention_rate:.1f}%)")
    print(f"  新客戶（秋季）: {len(new_fall)} 人")
    print(f"  流失客戶: {len(lost)} 人")

    comparison['retention'] = retention

    # 4. 分群轉移矩陣（僅回頭客）
    print("\n【4. 分群轉移矩陣】")
    if returning:
        spring_returning = spring_rfm[spring_rfm['proxy_customer_id'].isin(returning)]
        fall_returning = fall_rfm[fall_rfm['proxy_customer_id'].isin(returning)]

        # 合併
        merged = spring_returning[['proxy_customer_id', 'cluster_name']].merge(
            fall_returning[['proxy_customer_id', 'cluster_name']],
            on='proxy_customer_id',
            suffixes=('_spring', '_fall')
        )

        transition = pd.crosstab(
            merged['cluster_name_spring'],
            merged['cluster_name_fall'],
            margins=True
        )

        print(transition.to_string())
        comparison['transition_matrix'] = transition.to_dict()

    # 5. 時段偏好變化
    print("\n【5. 消費時段偏好變化】")
    time_periods = {
        '上午 (10-14)': (10, 14),
        '下午 (14-18)': (14, 18),
        '晚間 (18-21)': (18, 21)
    }

    hour_changes = {}
    for period_name, (start_h, end_h) in time_periods.items():
        spring_mask = (spring_rfm['hour_preference'] >= start_h) & (spring_rfm['hour_preference'] < end_h)
        fall_mask = (fall_rfm['hour_preference'] >= start_h) & (fall_rfm['hour_preference'] < end_h)

        spring_pct = (spring_mask.sum() / len(spring_rfm)) * 100
        fall_pct = (fall_mask.sum() / len(fall_rfm)) * 100

        hour_changes[period_name] = {
            'spring_pct': round(spring_pct, 1),
            'fall_pct': round(fall_pct, 1),
            'change': round(fall_pct - spring_pct, 1)
        }

        print(f"  {period_name}:")
        print(f"    春季: {spring_pct:.1f}%")
        print(f"    秋季: {fall_pct:.1f}%")

    comparison['hour_changes'] = hour_changes

    return comparison, returning


# ============================================================
# 視覺化圖表
# ============================================================
def generate_visualizations(spring_rfm, fall_rfm, comparison, returning_customers):
    """生成視覺化圖表"""
    print("\n" + "=" * 70)
    print("📊 生成視覺化圖表...")
    print("=" * 70)

    # 顏色方案
    colors_spring = '#3498db'  # 藍色
    colors_fall = '#e74c3c'    # 紅色
    cluster_colors = ['#2ecc71', '#f39c12', '#9b59b6']  # 綠、橙、紫

    # ========================================
    # 圖 1: 分群人數對比
    # ========================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 春季圓餅圖
    spring_dist = spring_rfm['cluster_name'].value_counts()
    wedges1, texts1, autotexts1 = axes[0].pie(
        spring_dist.values,
        labels=None,
        autopct='%1.1f%%',
        colors=cluster_colors[:len(spring_dist)],
        startangle=90
    )
    axes[0].set_title('春季分群分布 (2025/01-05)', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[0].legend(spring_dist.index, prop=chinese_font_prop, loc='lower left')
    for autotext in autotexts1:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    # 秋季圓餅圖
    fall_dist = fall_rfm['cluster_name'].value_counts()
    wedges2, texts2, autotexts2 = axes[1].pie(
        fall_dist.values,
        labels=None,
        autopct='%1.1f%%',
        colors=cluster_colors[:len(fall_dist)],
        startangle=90
    )
    axes[1].set_title('秋季分群分布 (2025/08-12)', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[1].legend(fall_dist.index, prop=chinese_font_prop, loc='lower left')
    for autotext in autotexts2:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig01_cluster_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig01_cluster_distribution.png")

    # ========================================
    # 圖 2: 分群人數變化橫條圖
    # ========================================
    fig, ax = plt.subplots(figsize=(12, 6))

    cluster_names = list(comparison['distribution'].keys())
    spring_counts = [comparison['distribution'][n]['spring_count'] for n in cluster_names]
    fall_counts = [comparison['distribution'][n]['fall_count'] for n in cluster_names]

    y = np.arange(len(cluster_names))
    height = 0.35

    bars1 = ax.barh(y - height/2, spring_counts, height, label='春季 (01-05)', color=colors_spring)
    bars2 = ax.barh(y + height/2, fall_counts, height, label='秋季 (08-12)', color=colors_fall)

    ax.set_xlabel('客戶數', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title('分群人數變化對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(cluster_names, fontproperties=chinese_font_prop)
    ax.legend(prop=chinese_font_prop)
    ax.grid(axis='x', alpha=0.3)

    # 添加數值標籤
    for bar, count in zip(bars1, spring_counts):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, str(count),
                va='center', fontsize=10)
    for bar, count in zip(bars2, fall_counts):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, str(count),
                va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig02_cluster_size_change.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig02_cluster_size_change.png")

    # ========================================
    # 圖 3: RFM 指標雷達圖
    # ========================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw=dict(projection='polar'))

    metrics = ['recency', 'frequency', 'monetary', 'avg_order_value', 'category_diversity']
    metric_labels = ['Recency', 'Frequency', 'Monetary', 'AOV', 'Category\nDiversity']

    # 標準化數值以便比較
    spring_values = [spring_rfm[m].mean() for m in metrics]
    fall_values = [fall_rfm[m].mean() for m in metrics]

    # 對 recency 取反（越小越好）
    max_vals = [max(spring_values[i], fall_values[i]) for i in range(len(metrics))]
    spring_norm = [(max_vals[0] - spring_values[0]) / max_vals[0] if i == 0 else spring_values[i] / max_vals[i]
                   for i, v in enumerate(spring_values)]
    fall_norm = [(max_vals[0] - fall_values[0]) / max_vals[0] if i == 0 else fall_values[i] / max_vals[i]
                 for i, v in enumerate(fall_values)]

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    spring_norm += spring_norm[:1]
    fall_norm += fall_norm[:1]
    angles += angles[:1]

    # 春季
    axes[0].fill(angles, spring_norm, color=colors_spring, alpha=0.25)
    axes[0].plot(angles, spring_norm, color=colors_spring, linewidth=2)
    axes[0].set_xticks(angles[:-1])
    axes[0].set_xticklabels(metric_labels, fontproperties=chinese_font_prop)
    axes[0].set_title('春季 RFM 輪廓', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold', pad=20)

    # 秋季
    axes[1].fill(angles, fall_norm, color=colors_fall, alpha=0.25)
    axes[1].plot(angles, fall_norm, color=colors_fall, linewidth=2)
    axes[1].set_xticks(angles[:-1])
    axes[1].set_xticklabels(metric_labels, fontproperties=chinese_font_prop)
    axes[1].set_title('秋季 RFM 輪廓', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig03_rfm_radar.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig03_rfm_radar.png")

    # ========================================
    # 圖 4: 客戶留存分析
    # ========================================
    fig, ax = plt.subplots(figsize=(10, 6))

    retention = comparison['retention']
    categories = ['春季總客戶', '回頭客', '新客戶\n（秋季）', '流失客戶', '秋季總客戶']
    values = [
        retention['spring_total'],
        retention['returning_customers'],
        retention['new_customers_fall'],
        retention['lost_customers'],
        retention['fall_total']
    ]
    colors_bar = [colors_spring, '#2ecc71', '#f39c12', '#e74c3c', colors_fall]

    bars = ax.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.2)

    ax.set_ylabel('客戶數', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title(f'客戶留存分析（留存率: {retention["retention_rate"]:.1f}%）',
                 fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, str(val),
                ha='center', fontsize=12, fontweight='bold')

    for label in ax.get_xticklabels():
        label.set_fontproperties(chinese_font_prop)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig04_retention_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig04_retention_analysis.png")

    # ========================================
    # 圖 5: 時段偏好變化
    # ========================================
    fig, ax = plt.subplots(figsize=(10, 6))

    periods = list(comparison['hour_changes'].keys())
    spring_pcts = [comparison['hour_changes'][p]['spring_pct'] for p in periods]
    fall_pcts = [comparison['hour_changes'][p]['fall_pct'] for p in periods]

    x = np.arange(len(periods))
    width = 0.35

    bars1 = ax.bar(x - width/2, spring_pcts, width, label='春季', color=colors_spring)
    bars2 = ax.bar(x + width/2, fall_pcts, width, label='秋季', color=colors_fall)

    ax.set_ylabel('客戶比例 (%)', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title('消費時段偏好變化', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontproperties=chinese_font_prop)
    ax.legend(prop=chinese_font_prop)
    ax.grid(axis='y', alpha=0.3)

    for bar, pct in zip(bars1, spring_pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{pct:.1f}%',
                ha='center', fontsize=10)
    for bar, pct in zip(bars2, fall_pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{pct:.1f}%',
                ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig05_hour_preference.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig05_hour_preference.png")

    # ========================================
    # 圖 6: Frequency 分布對比
    # ========================================
    fig, ax = plt.subplots(figsize=(12, 6))

    bins = range(0, max(spring_rfm['frequency'].max(), fall_rfm['frequency'].max()) + 2)

    ax.hist(spring_rfm['frequency'], bins=bins, alpha=0.5, label='春季', color=colors_spring, edgecolor='black')
    ax.hist(fall_rfm['frequency'], bins=bins, alpha=0.5, label='秋季', color=colors_fall, edgecolor='black')

    ax.set_xlabel('交易次數', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_ylabel('客戶數', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title('交易頻率分布對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.legend(prop=chinese_font_prop)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig06_frequency_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig06_frequency_distribution.png")

    # ========================================
    # 圖 7: Monetary 分布對比
    # ========================================
    fig, ax = plt.subplots(figsize=(12, 6))

    # 定義金額區間
    bins = [0, 20, 50, 100, 200, 500, float('inf')]
    labels = ['$0-20', '$20-50', '$50-100', '$100-200', '$200-500', '$500+']

    spring_binned = pd.cut(spring_rfm['monetary'], bins=bins, labels=labels).value_counts().sort_index()
    fall_binned = pd.cut(fall_rfm['monetary'], bins=bins, labels=labels).value_counts().sort_index()

    x = np.arange(len(labels))
    width = 0.35

    bars1 = ax.bar(x - width/2, spring_binned.values, width, label='春季', color=colors_spring)
    bars2 = ax.bar(x + width/2, fall_binned.values, width, label='秋季', color=colors_fall)

    ax.set_xlabel('消費金額區間', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_ylabel('客戶數', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title('消費金額分布對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(prop=chinese_font_prop)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig07_monetary_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig07_monetary_distribution.png")

    # ========================================
    # 圖 8: AOV 箱型圖對比
    # ========================================
    fig, ax = plt.subplots(figsize=(10, 6))

    data_to_plot = [spring_rfm['avg_order_value'], fall_rfm['avg_order_value']]
    bp = ax.boxplot(data_to_plot, labels=['春季', '秋季'], patch_artist=True)

    bp['boxes'][0].set_facecolor(colors_spring)
    bp['boxes'][1].set_facecolor(colors_fall)

    ax.set_ylabel('平均單次消費 ($)', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title('平均單次消費 (AOV) 對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    for label in ax.get_xticklabels():
        label.set_fontproperties(chinese_font_prop)

    # 添加統計值
    spring_aov = spring_rfm['avg_order_value'].mean()
    fall_aov = fall_rfm['avg_order_value'].mean()
    ax.axhline(y=spring_aov, color=colors_spring, linestyle='--', alpha=0.7, label=f'春季平均: ${spring_aov:.2f}')
    ax.axhline(y=fall_aov, color=colors_fall, linestyle='--', alpha=0.7, label=f'秋季平均: ${fall_aov:.2f}')
    ax.legend(prop=chinese_font_prop)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig08_aov_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig08_aov_comparison.png")

    # ========================================
    # 圖 9: Category Diversity 小提琴圖
    # ========================================
    fig, ax = plt.subplots(figsize=(10, 6))

    combined_df = pd.DataFrame({
        'Category Diversity': pd.concat([spring_rfm['category_diversity'], fall_rfm['category_diversity']]),
        'Period': ['春季'] * len(spring_rfm) + ['秋季'] * len(fall_rfm)
    })

    parts = ax.violinplot([spring_rfm['category_diversity'], fall_rfm['category_diversity']],
                          positions=[1, 2], showmeans=True, showmedians=True)

    parts['bodies'][0].set_facecolor(colors_spring)
    parts['bodies'][1].set_facecolor(colors_fall)
    parts['bodies'][0].set_alpha(0.7)
    parts['bodies'][1].set_alpha(0.7)

    ax.set_xticks([1, 2])
    ax.set_xticklabels(['春季', '秋季'], fontproperties=chinese_font_prop)
    ax.set_ylabel('品項多樣性（類別數）', fontproperties=chinese_font_prop, fontsize=12)
    ax.set_title('品項多樣性分布對比', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig09_category_diversity.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig09_category_diversity.png")

    # ========================================
    # 圖 10: 分群 RFM 熱力圖
    # ========================================
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 春季
    spring_cluster_stats = spring_rfm.groupby('cluster_name')[['recency', 'frequency', 'monetary', 'avg_order_value']].mean()
    sns.heatmap(spring_cluster_stats.T, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[0])
    axes[0].set_title('春季各分群 RFM 指標', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), fontproperties=chinese_font_prop, rotation=45, ha='right')

    # 秋季
    fall_cluster_stats = fall_rfm.groupby('cluster_name')[['recency', 'frequency', 'monetary', 'avg_order_value']].mean()
    sns.heatmap(fall_cluster_stats.T, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1])
    axes[1].set_title('秋季各分群 RFM 指標', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), fontproperties=chinese_font_prop, rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/fig10_cluster_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig10_cluster_heatmap.png")

    # ========================================
    # 圖 11: 轉移矩陣熱力圖
    # ========================================
    if 'transition_matrix' in comparison and returning_customers:
        fig, ax = plt.subplots(figsize=(10, 8))

        spring_returning = spring_rfm[spring_rfm['proxy_customer_id'].isin(returning_customers)]
        fall_returning = fall_rfm[fall_rfm['proxy_customer_id'].isin(returning_customers)]

        merged = spring_returning[['proxy_customer_id', 'cluster_name']].merge(
            fall_returning[['proxy_customer_id', 'cluster_name']],
            on='proxy_customer_id',
            suffixes=('_spring', '_fall')
        )

        transition = pd.crosstab(merged['cluster_name_spring'], merged['cluster_name_fall'])

        sns.heatmap(transition, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('秋季分群', fontproperties=chinese_font_prop, fontsize=12)
        ax.set_ylabel('春季分群', fontproperties=chinese_font_prop, fontsize=12)
        ax.set_title('客戶分群轉移矩陣（回頭客）', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')

        ax.set_xticklabels(ax.get_xticklabels(), fontproperties=chinese_font_prop, rotation=45, ha='right')
        ax.set_yticklabels(ax.get_yticklabels(), fontproperties=chinese_font_prop, rotation=0)

        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/charts/fig11_transition_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ fig11_transition_matrix.png")

    # ========================================
    # 圖 12: 綜合儀表板
    # ========================================
    fig = plt.figure(figsize=(20, 16))

    # 子圖 1: 分群分布對比
    ax1 = fig.add_subplot(3, 4, 1)
    spring_dist = spring_rfm['cluster_name'].value_counts()
    ax1.pie(spring_dist.values, labels=None, autopct='%1.0f%%', colors=cluster_colors[:len(spring_dist)])
    ax1.set_title('春季分群', fontproperties=chinese_font_prop, fontsize=11, fontweight='bold')

    ax2 = fig.add_subplot(3, 4, 2)
    fall_dist = fall_rfm['cluster_name'].value_counts()
    ax2.pie(fall_dist.values, labels=None, autopct='%1.0f%%', colors=cluster_colors[:len(fall_dist)])
    ax2.set_title('秋季分群', fontproperties=chinese_font_prop, fontsize=11, fontweight='bold')

    # 子圖 3: 留存率
    ax3 = fig.add_subplot(3, 4, 3)
    retention = comparison['retention']
    ax3.bar(['留存率'], [retention['retention_rate']], color='#2ecc71', edgecolor='black')
    ax3.set_ylim(0, 100)
    ax3.set_ylabel('%', fontproperties=chinese_font_prop)
    ax3.set_title(f'客戶留存率\n{retention["retention_rate"]:.1f}%', fontproperties=chinese_font_prop, fontsize=11, fontweight='bold')
    ax3.axhline(y=50, color='red', linestyle='--', alpha=0.5)
    for label in ax3.get_xticklabels():
        label.set_fontproperties(chinese_font_prop)

    # 子圖 4: 客戶數變化
    ax4 = fig.add_subplot(3, 4, 4)
    change = retention['fall_total'] - retention['spring_total']
    pct_change = change / retention['spring_total'] * 100
    color = '#2ecc71' if change >= 0 else '#e74c3c'
    ax4.bar(['客戶數變化'], [change], color=color, edgecolor='black')
    ax4.axhline(y=0, color='black', linewidth=0.5)
    ax4.set_title(f'客戶數變化\n{change:+d} ({pct_change:+.1f}%)', fontproperties=chinese_font_prop, fontsize=11, fontweight='bold')
    for label in ax4.get_xticklabels():
        label.set_fontproperties(chinese_font_prop)

    # 子圖 5-8: RFM 指標變化
    metrics_display = [
        ('frequency', 'Frequency', '次'),
        ('monetary', 'Monetary', '$'),
        ('avg_order_value', 'AOV', '$'),
        ('category_diversity', 'Category', '')
    ]

    for i, (metric, label, unit) in enumerate(metrics_display):
        ax = fig.add_subplot(3, 4, 5 + i)
        spring_val = spring_rfm[metric].mean()
        fall_val = fall_rfm[metric].mean()

        ax.bar(['春季', '秋季'], [spring_val, fall_val], color=[colors_spring, colors_fall], edgecolor='black')
        change = fall_val - spring_val
        pct = (change / spring_val * 100) if spring_val != 0 else 0
        ax.set_title(f'{label}\n{change:+.1f} ({pct:+.1f}%)', fontproperties=chinese_font_prop, fontsize=10, fontweight='bold')
        for lbl in ax.get_xticklabels():
            lbl.set_fontproperties(chinese_font_prop)

    # 子圖 9-12: 分群人數變化
    for i, name in enumerate(comparison['distribution'].keys()):
        if i >= 4:
            break
        ax = fig.add_subplot(3, 4, 9 + i)
        dist = comparison['distribution'][name]
        ax.bar(['春季', '秋季'], [dist['spring_count'], dist['fall_count']],
               color=[colors_spring, colors_fall], edgecolor='black')
        ax.set_title(f'{name}\n{dist["change"]:+d}', fontproperties=chinese_font_prop, fontsize=10, fontweight='bold')
        for lbl in ax.get_xticklabels():
            lbl.set_fontproperties(chinese_font_prop)

    plt.suptitle('客戶分群比較分析儀表板', fontproperties=chinese_font_prop, fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{OUTPUT_DIR}/charts/fig12_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ fig12_dashboard.png")

    print(f"\n✓ 所有 12 張圖表已保存至 {OUTPUT_DIR}/charts/")


# ============================================================
# 報告生成
# ============================================================
def generate_reports(spring_rfm, fall_rfm, comparison, spring_sil, spring_db, fall_sil, fall_db):
    """生成分析報告"""
    print("\n" + "=" * 70)
    print("📝 生成分析報告...")
    print("=" * 70)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ========================================
    # JSON 報告
    # ========================================
    results = {
        'metadata': {
            'timestamp': timestamp,
            'spring_period': f'{SPRING_START} to {SPRING_END}',
            'fall_period': f'{FALL_START} to {FALL_END}',
            'n_clusters': N_CLUSTERS,
            'features': ['recency', 'frequency', 'monetary', 'avg_order_value', 'hour_preference', 'category_diversity']
        },
        'spring_analysis': {
            'total_customers': len(spring_rfm),
            'silhouette_score': round(spring_sil, 4),
            'davies_bouldin_score': round(spring_db, 4),
            'cluster_distribution': spring_rfm['cluster_name'].value_counts().to_dict(),
            'rfm_stats': {
                'recency_mean': round(spring_rfm['recency'].mean(), 2),
                'frequency_mean': round(spring_rfm['frequency'].mean(), 2),
                'monetary_mean': round(spring_rfm['monetary'].mean(), 2),
                'aov_mean': round(spring_rfm['avg_order_value'].mean(), 2)
            }
        },
        'fall_analysis': {
            'total_customers': len(fall_rfm),
            'silhouette_score': round(fall_sil, 4),
            'davies_bouldin_score': round(fall_db, 4),
            'cluster_distribution': fall_rfm['cluster_name'].value_counts().to_dict(),
            'rfm_stats': {
                'recency_mean': round(fall_rfm['recency'].mean(), 2),
                'frequency_mean': round(fall_rfm['frequency'].mean(), 2),
                'monetary_mean': round(fall_rfm['monetary'].mean(), 2),
                'aov_mean': round(fall_rfm['avg_order_value'].mean(), 2)
            }
        },
        'comparison': comparison
    }

    # 處理 transition_matrix（如果存在）
    if 'transition_matrix' in results['comparison']:
        # 將 DataFrame dict 轉換為可序列化格式
        tm = results['comparison']['transition_matrix']
        if isinstance(tm, dict):
            results['comparison']['transition_matrix'] = {
                str(k): {str(k2): int(v2) if isinstance(v2, (np.integer, np.int64)) else v2
                         for k2, v2 in v.items()}
                for k, v in tm.items()
            }

    with open(f'{OUTPUT_DIR}/data/comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ comparison_results.json")

    # ========================================
    # CSV 檔案
    # ========================================
    spring_rfm.to_csv(f'{OUTPUT_DIR}/data/spring_rfm_features.csv', index=False, encoding='utf-8-sig')
    fall_rfm.to_csv(f'{OUTPUT_DIR}/data/fall_rfm_features.csv', index=False, encoding='utf-8-sig')
    print(f"  ✓ spring_rfm_features.csv")
    print(f"  ✓ fall_rfm_features.csv")

    # 轉移矩陣 CSV
    if 'transition_matrix' in comparison:
        pd.DataFrame(comparison['transition_matrix']).to_csv(
            f'{OUTPUT_DIR}/data/customer_transition.csv', encoding='utf-8-sig'
        )
        print(f"  ✓ customer_transition.csv")

    # ========================================
    # Markdown 報告
    # ========================================
    retention = comparison['retention']

    report = f"""# 客戶分群比較分析報告

**生成時間**: {timestamp}

---

## 執行摘要

本報告比較 Taiwanway 餐廳兩個時間段的客戶分群差異：
- **春季**: {SPRING_START} 至 {SPRING_END}
- **秋季**: {FALL_START} 至 {FALL_END}

### 核心發現

1. **客戶留存率**: {retention['retention_rate']:.1f}%（{retention['returning_customers']} 位回頭客）
2. **新客戶**: 秋季新增 {retention['new_customers_fall']} 位新客戶
3. **流失客戶**: {retention['lost_customers']} 位客戶未在秋季消費
4. **總客戶變化**: {retention['fall_total'] - retention['spring_total']:+d} 人

---

## 分群概覽

### 春季分群（{SPRING_START} - {SPRING_END}）

| 分群 | 人數 | 占比 |
|------|------|------|
"""

    for name, count in spring_rfm['cluster_name'].value_counts().items():
        pct = count / len(spring_rfm) * 100
        report += f"| {name} | {count} | {pct:.1f}% |\n"

    report += f"""
**評估指標**:
- Silhouette Score: {spring_sil:.4f}
- Davies-Bouldin Index: {spring_db:.4f}

### 秋季分群（{FALL_START} - {FALL_END}）

| 分群 | 人數 | 占比 |
|------|------|------|
"""

    for name, count in fall_rfm['cluster_name'].value_counts().items():
        pct = count / len(fall_rfm) * 100
        report += f"| {name} | {count} | {pct:.1f}% |\n"

    report += f"""
**評估指標**:
- Silhouette Score: {fall_sil:.4f}
- Davies-Bouldin Index: {fall_db:.4f}

---

## RFM 指標變化

| 指標 | 春季平均 | 秋季平均 | 變化 | 變化率 |
|------|----------|----------|------|--------|
"""

    for metric, data in comparison['rfm_changes'].items():
        metric_names = {
            'recency': 'Recency (天)',
            'frequency': 'Frequency (次)',
            'monetary': 'Monetary ($)',
            'avg_order_value': 'AOV ($)',
            'category_diversity': 'Category Diversity'
        }
        name = metric_names.get(metric, metric)
        report += f"| {name} | {data['spring_avg']:.2f} | {data['fall_avg']:.2f} | {data['change']:+.2f} | {data['pct_change']:+.1f}% |\n"

    report += f"""

---

## 客戶留存分析

| 指標 | 數值 |
|------|------|
| 春季總客戶 | {retention['spring_total']} |
| 秋季總客戶 | {retention['fall_total']} |
| 回頭客 | {retention['returning_customers']} |
| 新客戶（秋季） | {retention['new_customers_fall']} |
| 流失客戶 | {retention['lost_customers']} |
| **留存率** | **{retention['retention_rate']:.1f}%** |

---

## 消費時段偏好變化

| 時段 | 春季 | 秋季 | 變化 |
|------|------|------|------|
"""

    for period, data in comparison['hour_changes'].items():
        report += f"| {period} | {data['spring_pct']:.1f}% | {data['fall_pct']:.1f}% | {data['change']:+.1f}% |\n"

    report += f"""

---

## 分群人數變化

| 分群 | 春季 | 秋季 | 變化 |
|------|------|------|------|
"""

    for name, data in comparison['distribution'].items():
        report += f"| {name} | {data['spring_count']} ({data['spring_pct']:.1f}%) | {data['fall_count']} ({data['fall_pct']:.1f}%) | {data['change']:+d} ({data['pct_change']:+.1f}%) |\n"

    report += f"""

---

## 分析方法

- **客戶識別**: Card Brand + PAN Suffix 代理 ID
- **特徵維度**: 擴展 RFM（6 維）
  - Recency: 最近購買距今天數
  - Frequency: 交易次數
  - Monetary: 總消費金額
  - Avg Order Value: 平均單次消費
  - Hour Preference: 最常消費時段
  - Category Diversity: 品項多樣性
- **分群算法**: K-means (K={N_CLUSTERS})
- **標準化**: StandardScaler

---

## 輸出檔案

### 數據檔案 (`{OUTPUT_DIR}/data/`)
- `comparison_results.json` - 完整比較結果
- `spring_rfm_features.csv` - 春季客戶特徵
- `fall_rfm_features.csv` - 秋季客戶特徵
- `customer_transition.csv` - 分群轉移矩陣

### 視覺化圖表 (`{OUTPUT_DIR}/charts/`)
1. `fig01_cluster_distribution.png` - 分群分布對比
2. `fig02_cluster_size_change.png` - 分群人數變化
3. `fig03_rfm_radar.png` - RFM 雷達圖
4. `fig04_retention_analysis.png` - 客戶留存分析
5. `fig05_hour_preference.png` - 時段偏好變化
6. `fig06_frequency_distribution.png` - 頻率分布
7. `fig07_monetary_distribution.png` - 消費金額分布
8. `fig08_aov_comparison.png` - AOV 對比
9. `fig09_category_diversity.png` - 品項多樣性
10. `fig10_cluster_heatmap.png` - 分群熱力圖
11. `fig11_transition_matrix.png` - 轉移矩陣
12. `fig12_dashboard.png` - 綜合儀表板

---

**分析完成時間**: {timestamp}
"""

    with open(f'{OUTPUT_DIR}/README.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  ✓ README.md")

    print(f"\n✓ 所有報告已保存至 {OUTPUT_DIR}/")


# ============================================================
# 主函數
# ============================================================
def main():
    """主函數"""
    print("\n" + "=" * 70)
    print("🎯 客戶分群比較分析")
    print("   春季 (2025/01-05) vs 秋季 (2025/08-12)")
    print("=" * 70)

    # 1. 載入數據
    df = load_and_preprocess(DATA_FILE)

    # 2. 分割時間段
    print("\n📅 分割時間段...")
    print("\n【春季數據】")
    df_spring = filter_by_period(df, SPRING_START, SPRING_END)
    print("\n【秋季數據】")
    df_fall = filter_by_period(df, FALL_START, FALL_END)

    # 3. 計算 RFM 特徵
    spring_rfm, spring_details = calculate_extended_rfm(df_spring, SPRING_REFERENCE, '春季')
    fall_rfm, fall_details = calculate_extended_rfm(df_fall, FALL_REFERENCE, '秋季')

    # 4. 執行分群
    spring_rfm, spring_kmeans, spring_scaler, spring_sil, spring_db = perform_clustering(
        spring_rfm, N_CLUSTERS, '春季'
    )
    fall_rfm, fall_kmeans, fall_scaler, fall_sil, fall_db = perform_clustering(
        fall_rfm, N_CLUSTERS, '秋季'
    )

    # 5. 命名分群
    spring_rfm, spring_names, spring_desc = name_clusters(spring_rfm)
    fall_rfm, fall_names, fall_desc = name_clusters(fall_rfm)

    # 6. 跨時段比較
    comparison, returning_customers = compare_periods(spring_rfm, fall_rfm, spring_names, fall_names)

    # 7. 生成視覺化
    generate_visualizations(spring_rfm, fall_rfm, comparison, returning_customers)

    # 8. 生成報告
    generate_reports(spring_rfm, fall_rfm, comparison, spring_sil, spring_db, fall_sil, fall_db)

    print("\n" + "=" * 70)
    print("✅ 分析完成！")
    print(f"✅ 輸出目錄: {OUTPUT_DIR}")
    print("=" * 70)


if __name__ == '__main__':
    main()
