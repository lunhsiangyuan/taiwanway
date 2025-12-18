#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客戶集群分析 - 方案 A：優化特徵組合
移除共線性和低區分度特徵，使用 5 個核心特徵和 K=3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, silhouette_samples
import warnings
import os
import json
from datetime import datetime
import pytz
import matplotlib.font_manager as fm

warnings.filterwarnings('ignore')

# 設置中文字體
plt.rcParams['text.usetex'] = False
plt.rcParams['axes.unicode_minus'] = False

# 載入中文字體
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
    print("⚠️  未找到中文字體")
    chinese_font_prop = fm.FontProperties()

# 配置
DATA_FILE = 'data/all_payments/all_payments.json'
OUTPUT_DIR = 'analysis_output/clustering/optimized'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/charts', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/data', exist_ok=True)


def load_payments_json(file_path, start_date='2025-01-01', end_date='2025-11-16'):
    """從 JSON 文件載入支付數據"""
    print("📊 載入 JSON 數據...")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    payments = data.get('payments', [])
    print(f"✓ 載入 {len(payments)} 筆支付記錄")

    df = pd.json_normalize(payments)
    return df


def preprocess_payments_data(df, start_date='2025-01-01', end_date='2025-11-16'):
    """預處理支付數據"""
    print("\n🔧 預處理數據...")

    # 轉換金額
    if 'amount_money.amount' in df.columns:
        df['amount_usd'] = df['amount_money.amount'] / 100

    if 'tip_money.amount' in df.columns:
        df['tip_usd'] = df['tip_money.amount'].fillna(0) / 100
    else:
        df['tip_usd'] = 0

    # 處理時間戳
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
    ny_tz = pytz.timezone('America/New_York')
    df['datetime_ny'] = df['created_at'].dt.tz_convert(ny_tz)

    # 提取時間特徵
    df['date'] = df['datetime_ny'].dt.date
    df['hour'] = df['datetime_ny'].dt.hour
    df['dayofweek'] = df['datetime_ny'].dt.dayofweek
    df['month'] = df['datetime_ny'].dt.month

    # 過濾日期範圍
    start = pd.to_datetime(start_date).date()
    end = pd.to_datetime(end_date).date()
    df = df[(df['date'] >= start) & (df['date'] <= end)].copy()

    df_with_customers = df[df['customer_id'].notna()].copy()
    print(f"✓ 日期範圍: {df['date'].min()} 至 {df['date'].max()}")
    print(f"✓ 有客戶ID的記錄: {len(df_with_customers)} 筆")
    print(f"✓ 唯一客戶數: {df_with_customers['customer_id'].nunique()}")

    return df_with_customers


def engineer_customer_features(df):
    """計算客戶特徵"""
    print("\n🔧 進行特徵工程...")

    customer_agg = df.groupby('customer_id').agg({
        'id': 'count',
        'amount_usd': ['sum', 'mean', 'std'],
        'tip_usd': ['sum', 'mean'],
        'datetime_ny': ['min', 'max'],
        'source_type': lambda x: x.mode()[0] if len(x) > 0 else None,
    }).reset_index()

    customer_agg.columns = [
        'customer_id', 'transaction_count', 'total_spending', 'avg_spending', 'std_spending',
        'total_tip', 'avg_tip', 'first_purchase', 'last_purchase', 'preferred_payment_method'
    ]

    # 信用卡使用率
    card_usage = df.groupby('customer_id').apply(
        lambda x: (x['source_type'] == 'CARD').sum() / len(x) if len(x) > 0 else 0
    ).reset_index(name='card_usage_ratio')
    customer_agg = customer_agg.merge(card_usage, on='customer_id')

    # 小費給予率
    tip_frequency = df.groupby('customer_id').apply(
        lambda x: (x['tip_usd'] > 0).sum() / len(x) if len(x) > 0 else 0
    ).reset_index(name='tip_frequency')
    customer_agg = customer_agg.merge(tip_frequency, on='customer_id')

    # 購買頻率
    customer_agg['days_since_first'] = (
        customer_agg['last_purchase'] - customer_agg['first_purchase']
    ).dt.days

    customer_agg['purchase_frequency'] = (
        customer_agg['transaction_count'] / (customer_agg['days_since_first'] + 1)
    )

    customer_agg['std_spending'].fillna(0, inplace=True)

    print(f"✓ 生成 {len(customer_agg)} 個客戶的特徵")

    return customer_agg


def select_optimized_features(customer_features):
    """選擇優化後的特徵組合"""
    print("\n✨ 使用優化特徵組合（方案 A）...")

    # 方案 A：5 個核心特徵
    feature_cols = [
        'transaction_count',       # F - Frequency
        'total_spending',          # M - Monetary
        'purchase_frequency',      # F 變體
        'tip_frequency',           # 行為模式
        'card_usage_ratio'         # 支付偏好
    ]

    print("✓ 選擇的特徵:")
    for i, feat in enumerate(feature_cols, 1):
        print(f"  {i}. {feat}")

    X = customer_features[feature_cols].copy()
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(0, inplace=True)

    return X, feature_cols


def evaluate_optimal_k(X, max_k=8):
    """評估最佳集群數"""
    print("\n📈 評估最佳集群數...")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertias = []
    silhouette_scores = []
    db_scores = []
    K_range = range(2, min(max_k + 1, len(X)))

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, clusters))
        db_scores.append(davies_bouldin_score(X_scaled, clusters))

    # 繪製評估圖
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 肘部法則
    axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
    axes[0].axvline(x=3, color='red', linestyle='--', alpha=0.5, label='K=3')
    axes[0].set_xlabel('集群數 (k)', fontproperties=chinese_font_prop, fontsize=12)
    axes[0].set_ylabel('慣性 (Inertia)', fontproperties=chinese_font_prop, fontsize=12)
    axes[0].set_title('肘部法則', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[0].legend(prop=chinese_font_prop)
    axes[0].grid(True, alpha=0.3)

    # Silhouette Score
    axes[1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
    axes[1].axvline(x=3, color='red', linestyle='--', alpha=0.5, label='K=3')
    axes[1].axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='良好閾值 (0.5)')
    axes[1].set_xlabel('集群數 (k)', fontproperties=chinese_font_prop, fontsize=12)
    axes[1].set_ylabel('Silhouette Score', fontproperties=chinese_font_prop, fontsize=12)
    axes[1].set_title('Silhouette 分數', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[1].legend(prop=chinese_font_prop)
    axes[1].grid(True, alpha=0.3)

    # Davies-Bouldin Index
    axes[2].plot(K_range, db_scores, 'ro-', linewidth=2, markersize=8)
    axes[2].axvline(x=3, color='red', linestyle='--', alpha=0.5, label='K=3')
    axes[2].set_xlabel('集群數 (k)', fontproperties=chinese_font_prop, fontsize=12)
    axes[2].set_ylabel('Davies-Bouldin Index', fontproperties=chinese_font_prop, fontsize=12)
    axes[2].set_title('Davies-Bouldin 指數（越低越好）', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
    axes[2].legend(prop=chinese_font_prop)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/optimized_elbow_curve.png', dpi=300, bbox_inches='tight')
    print(f"✓ 評估圖已保存")
    plt.close()

    # 顯示 K=3 的指標
    k3_idx = 1  # K=3 對應索引 1 (range 從 2 開始)
    print(f"\nK=3 的評估指標:")
    print(f"  Silhouette Score: {silhouette_scores[k3_idx]:.4f}")
    print(f"  Davies-Bouldin Index: {db_scores[k3_idx]:.4f}")

    return silhouette_scores, db_scores


def perform_clustering(X, n_clusters=3):
    """執行 K-means 集群"""
    print(f"\n🎯 執行 K-means 集群 (K={n_clusters})...")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    sil_score = silhouette_score(X_scaled, clusters)
    db_score = davies_bouldin_score(X_scaled, clusters)

    print(f"✓ 集群完成")
    print(f"✓ 各集群樣本數: {np.bincount(clusters)}")
    print(f"✓ Silhouette Score: {sil_score:.4f}")
    print(f"✓ Davies-Bouldin Index: {db_score:.4f}")

    return clusters, kmeans, scaler, X_scaled, sil_score, db_score


def visualize_clusters(X, X_scaled, clusters, feature_cols, customer_features):
    """視覺化集群"""
    print("\n📊 生成視覺化...")

    # PCA 降維
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Silhouette 樣本分數
    silhouette_vals = silhouette_samples(X_scaled, clusters)

    fig = plt.figure(figsize=(20, 10))

    # 1. PCA 視覺化
    ax1 = plt.subplot(2, 3, 1)
    scatter = ax1.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters,
                         cmap='viridis', s=100, alpha=0.6, edgecolors='black')
    plt.colorbar(scatter, label='集群', ax=ax1)
    ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',
                  fontproperties=chinese_font_prop, fontsize=12)
    ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})',
                  fontproperties=chinese_font_prop, fontsize=12)
    ax1.set_title('PCA 降維視覺化', fontproperties=chinese_font_prop,
                 fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # 2. Silhouette 圖
    ax2 = plt.subplot(2, 3, 2)
    y_lower = 10
    n_clusters = len(np.unique(clusters))

    for i in range(n_clusters):
        cluster_silhouette_vals = silhouette_vals[clusters == i]
        cluster_silhouette_vals.sort()

        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i

        color = plt.cm.viridis(float(i) / n_clusters)
        ax2.fill_betweenx(np.arange(y_lower, y_upper),
                         0, cluster_silhouette_vals,
                         facecolor=color, edgecolor=color, alpha=0.7)

        ax2.text(-0.05, y_lower + 0.5 * size_cluster_i, f'集群 {i}',
                fontproperties=chinese_font_prop)

        y_lower = y_upper + 10

    avg_score = silhouette_score(X_scaled, clusters)
    ax2.axvline(x=avg_score, color="red", linestyle="--", linewidth=2,
               label=f'平均分數: {avg_score:.3f}')
    ax2.set_xlabel('Silhouette Coefficient', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_ylabel('集群', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_title('Silhouette 分析圖', fontproperties=chinese_font_prop,
                 fontsize=14, fontweight='bold')
    ax2.legend(prop=chinese_font_prop)

    # 3. 集群分佈餅圖
    ax3 = plt.subplot(2, 3, 3)
    cluster_counts = pd.Series(clusters).value_counts().sort_index()
    colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_counts)))
    labels = [f'集群 {i}\n({count} 人)' for i, count in enumerate(cluster_counts)]

    wedges, texts, autotexts = ax3.pie(cluster_counts, labels=labels,
                                        autopct='%1.1f%%', colors=colors,
                                        startangle=90)
    for text in texts:
        text.set_fontproperties(chinese_font_prop)
    for autotext in autotexts:
        autotext.set_fontproperties(chinese_font_prop)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax3.set_title('集群分佈', fontproperties=chinese_font_prop,
                 fontsize=14, fontweight='bold')

    # 4-5. 特徵分佈箱型圖
    for idx, col in enumerate(feature_cols[:2]):  # 前兩個特徵
        ax = plt.subplot(2, 3, 4 + idx)
        data_to_plot = [X[clusters == i][col].values for i in range(n_clusters)]
        labels_box = [f'集群 {i}' for i in range(n_clusters)]

        bp = ax.boxplot(data_to_plot, labels=labels_box, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_title(col, fontproperties=chinese_font_prop, fontsize=12)
        ax.set_ylabel('數值', fontproperties=chinese_font_prop)
        ax.grid(True, alpha=0.3)

        for label in ax.get_xticklabels():
            label.set_fontproperties(chinese_font_prop)

    # 6. 特徵重要性（基於集群中心距離）
    ax6 = plt.subplot(2, 3, 6)

    # 計算各特徵的標準差（代表重要性）
    feature_importance = X_scaled.std(axis=0)
    feature_names_short = [f.replace('_', '\n') for f in feature_cols]

    bars = ax6.barh(feature_names_short, feature_importance, color='steelblue')
    ax6.set_xlabel('標準差（重要性）', fontproperties=chinese_font_prop, fontsize=12)
    ax6.set_title('特徵重要性分析', fontproperties=chinese_font_prop,
                 fontsize=14, fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='x')

    for label in ax6.get_yticklabels():
        label.set_fontproperties(chinese_font_prop)

    plt.suptitle('方案 A：優化特徵組合集群分析', fontproperties=chinese_font_prop,
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/optimized_cluster_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✓ 綜合分析圖已保存")
    plt.close()


def analyze_cluster_characteristics(customer_features, clusters, feature_cols):
    """分析集群特徵"""
    print("\n📋 分析集群特徵...")

    customer_features_copy = customer_features.copy()
    customer_features_copy['Cluster'] = clusters

    cluster_summary = customer_features_copy.groupby('Cluster')[feature_cols].agg(['mean', 'median', 'std'])

    cluster_profiles = {}

    for cluster_id in range(clusters.max() + 1):
        cluster_data = customer_features_copy[customer_features_copy['Cluster'] == cluster_id]

        profile = {
            'cluster_id': int(cluster_id),
            'customer_count': int(len(cluster_data)),
            'avg_transaction_count': float(cluster_data['transaction_count'].mean()),
            'avg_total_spending': float(cluster_data['total_spending'].mean()),
            'avg_purchase_frequency': float(cluster_data['purchase_frequency'].mean()),
            'avg_tip_frequency': float(cluster_data['tip_frequency'].mean()),
            'avg_card_usage_ratio': float(cluster_data['card_usage_ratio'].mean()),
        }

        # 命名邏輯
        if profile['avg_total_spending'] > customer_features_copy['total_spending'].quantile(0.75):
            if profile['avg_transaction_count'] > customer_features_copy['transaction_count'].quantile(0.75):
                profile['cluster_name'] = 'VIP 忠誠客戶'
                profile['description'] = '高消費、高頻率的核心客戶群'
            else:
                profile['cluster_name'] = '高價值客戶'
                profile['description'] = '消費金額高但頻率較低'
        elif profile['avg_transaction_count'] > customer_features_copy['transaction_count'].quantile(0.5):
            profile['cluster_name'] = '活躍客戶'
            profile['description'] = '購買頻率較高的穩定客戶'
        else:
            profile['cluster_name'] = '偶爾消費客戶'
            profile['description'] = '購買頻率低、消費金額一般'

        cluster_profiles[cluster_id] = profile

        print(f"\n集群 {cluster_id}: {profile['cluster_name']}")
        print(f"  客戶數: {profile['customer_count']}")
        print(f"  平均交易次數: {profile['avg_transaction_count']:.2f}")
        print(f"  平均總消費: ${profile['avg_total_spending']:.2f}")
        print(f"  購買頻率: {profile['avg_purchase_frequency']:.4f}")
        print(f"  小費給予率: {profile['avg_tip_frequency']:.1%}")
        print(f"  信用卡使用率: {profile['avg_card_usage_ratio']:.1%}")

    return cluster_profiles, cluster_summary, customer_features_copy


def save_results(cluster_profiles, cluster_summary, customer_features_with_clusters,
                sil_score, db_score):
    """保存結果"""
    print("\n💾 保存結果...")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # JSON
    results = {
        'method': 'Optimized Features (方案 A)',
        'timestamp': timestamp,
        'n_features': 5,
        'features': ['transaction_count', 'total_spending', 'purchase_frequency',
                    'tip_frequency', 'card_usage_ratio'],
        'n_clusters': 3,
        'total_customers': int(len(customer_features_with_clusters)),
        'silhouette_score': float(sil_score),
        'davies_bouldin_score': float(db_score),
        'cluster_profiles': cluster_profiles
    }

    with open(f'{OUTPUT_DIR}/data/cluster_profiles_optimized.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 已保存")

    # CSV
    cluster_summary.to_csv(f'{OUTPUT_DIR}/data/cluster_summary_optimized.csv', encoding='utf-8-sig')
    print(f"✓ 摘要 CSV 已保存")

    customer_clusters = customer_features_with_clusters[['customer_id', 'Cluster']].copy()
    customer_clusters['Cluster_Name'] = customer_clusters['Cluster'].map(
        {k: v['cluster_name'] for k, v in cluster_profiles.items()}
    )
    customer_clusters.to_csv(f'{OUTPUT_DIR}/data/customer_clusters_optimized.csv',
                            index=False, encoding='utf-8-sig')
    print(f"✓ 客戶分配 CSV 已保存")

    # Markdown 報告
    generate_report(results, timestamp)

    return timestamp


def generate_report(results, timestamp):
    """生成 Markdown 報告"""
    report = f"""# 客戶集群分析報告 - 方案 A：優化特徵組合

**生成時間**: {timestamp}
**方法**: 優化特徵組合（移除共線性和低區分度特徵）
**特徵數量**: 5 個
**集群數量**: K=3

---

## 方法說明

### 特徵選擇策略

**保留的 5 個核心特徵：**
1. transaction_count (交易次數 - Frequency)
2. total_spending (總消費 - Monetary)
3. purchase_frequency (購買頻率 - Frequency 變體)
4. tip_frequency (小費給予率 - 行為模式)
5. card_usage_ratio (信用卡使用率 - 支付偏好)

**移除的特徵及原因：**
- avg_spending：變異係數僅 0.164，與 total_spending 高度共線
- weekend_ratio：變異係數僅 0.390，區分度低
- avg_tip：與 tip_frequency 概念重複

---

## 評估指標

**集群品質：**
- **Silhouette Score**: {results['silhouette_score']:.4f} {'✓ 良好' if results['silhouette_score'] > 0.5 else '⚠️ 中等' if results['silhouette_score'] > 0.3 else '✗ 較差'}
- **Davies-Bouldin Index**: {results['davies_bouldin_score']:.4f} (越低越好)
- **總客戶數**: {results['total_customers']} 位

---

## 集群概覽

"""

    for cluster_id, profile in results['cluster_profiles'].items():
        pct = profile['customer_count'] / results['total_customers'] * 100
        report += f"""
### 集群 {cluster_id}: {profile['cluster_name']}

**描述**: {profile['description']}

**規模**: {profile['customer_count']} 人 ({pct:.1f}%)

**關鍵指標**:
- 平均交易次數: {profile['avg_transaction_count']:.2f} 次
- 平均總消費: ${profile['avg_total_spending']:.2f}
- 購買頻率: {profile['avg_purchase_frequency']:.4f} 次/天
- 小費給予率: {profile['avg_tip_frequency']:.1%}
- 信用卡使用率: {profile['avg_card_usage_ratio']:.1%}

---
"""

    report += f"""
## 輸出文件

- **圖表**: `{OUTPUT_DIR}/charts/`
  - optimized_elbow_curve.png - 評估指標圖
  - optimized_cluster_analysis.png - 綜合分析圖

- **數據**: `{OUTPUT_DIR}/data/`
  - cluster_profiles_optimized.json - 集群配置
  - cluster_summary_optimized.csv - 統計摘要
  - customer_clusters_optimized.csv - 客戶分配表

---

**分析方法**: K-means Clustering + StandardScaler
**隨機種子**: 42
"""

    with open(f'{OUTPUT_DIR}/comparison_report_optimized.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Markdown 報告已保存")


def main():
    """主函數"""
    print("=" * 70)
    print("客戶集群分析 - 方案 A：優化特徵組合 (5 特徵, K=3)")
    print("=" * 70)

    # 1. 載入數據
    df_payments = load_payments_json(DATA_FILE)
    df_processed = preprocess_payments_data(df_payments)

    # 2. 特徵工程
    customer_features = engineer_customer_features(df_processed)

    # 3. 選擇優化特徵
    X, feature_cols = select_optimized_features(customer_features)

    # 4. 評估最佳 K
    sil_scores, db_scores = evaluate_optimal_k(X, max_k=8)

    # 5. 執行集群 (K=3)
    clusters, kmeans, scaler, X_scaled, sil_score, db_score = perform_clustering(X, n_clusters=3)

    # 6. 視覺化
    visualize_clusters(X, X_scaled, clusters, feature_cols, customer_features)

    # 7. 分析特徵
    cluster_profiles, cluster_summary, customer_features_with_clusters = \
        analyze_cluster_characteristics(customer_features, clusters, feature_cols)

    # 8. 保存結果
    timestamp = save_results(cluster_profiles, cluster_summary,
                            customer_features_with_clusters, sil_score, db_score)

    print("\n" + "=" * 70)
    print("✅ 方案 A 分析完成!")
    print(f"✅ Silhouette Score: {sil_score:.4f}")
    print("=" * 70)

    return timestamp


if __name__ == '__main__':
    main()
