#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客戶集群分析 - 方案 B：純 RFM 分析
使用經典 RFM 三要素（Recency, Frequency, Monetary）和 K=3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, silhouette_samples
from mpl_toolkits.mplot3d import Axes3D
import warnings
import os
import json
from datetime import datetime, date
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
OUTPUT_DIR = 'analysis_output/clustering/rfm'
REFERENCE_DATE = date(2025, 11, 16)  # 分析基準日期

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

    # 處理時間戳
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
    ny_tz = pytz.timezone('America/New_York')
    df['datetime_ny'] = df['created_at'].dt.tz_convert(ny_tz)
    df['date'] = df['datetime_ny'].dt.date

    # 過濾日期範圍
    start = pd.to_datetime(start_date).date()
    end = pd.to_datetime(end_date).date()
    df = df[(df['date'] >= start) & (df['date'] <= end)].copy()

    df_with_customers = df[df['customer_id'].notna()].copy()
    print(f"✓ 日期範圍: {df['date'].min()} 至 {df['date'].max()}")
    print(f"✓ 有客戶ID的記錄: {len(df_with_customers)} 筆")
    print(f"✓ 唯一客戶數: {df_with_customers['customer_id'].nunique()}")

    return df_with_customers


def calculate_rfm_features(df, reference_date=REFERENCE_DATE):
    """計算 RFM 三要素"""
    print("\n🔧 計算 RFM 特徵...")
    print(f"   基準日期: {reference_date}")

    # 按客戶聚合
    rfm_data = df.groupby('customer_id').agg({
        'date': lambda x: (reference_date - x.max()).days,  # Recency
        'id': 'count',                                       # Frequency
        'amount_usd': 'sum'                                  # Monetary
    }).reset_index()

    rfm_data.columns = ['customer_id', 'recency', 'frequency', 'monetary']

    # 基本統計
    print(f"\n✓ RFM 特徵統計:")
    print(f"   Recency (距今天數):")
    print(f"     - 平均: {rfm_data['recency'].mean():.1f} 天")
    print(f"     - 範圍: {rfm_data['recency'].min()}-{rfm_data['recency'].max()} 天")
    print(f"   Frequency (交易次數):")
    print(f"     - 平均: {rfm_data['frequency'].mean():.2f} 次")
    print(f"     - 範圍: {rfm_data['frequency'].min()}-{rfm_data['frequency'].max()} 次")
    print(f"   Monetary (總消費):")
    print(f"     - 平均: ${rfm_data['monetary'].mean():.2f}")
    print(f"     - 範圍: ${rfm_data['monetary'].min():.2f}-${rfm_data['monetary'].max():.2f}")

    print(f"\n✓ 生成 {len(rfm_data)} 個客戶的 RFM 特徵")

    return rfm_data


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
    plt.savefig(f'{OUTPUT_DIR}/charts/rfm_elbow_curve.png', dpi=300, bbox_inches='tight')
    print(f"✓ 評估圖已保存")
    plt.close()

    # 顯示 K=3 的指標
    k3_idx = 1  # K=3 對應索引 1
    print(f"\nK=3 的評估指標:")
    print(f"  Silhouette Score: {silhouette_scores[k3_idx]:.4f}")
    print(f"  Davies-Bouldin Index: {db_scores[k3_idx]:.4f}")

    return silhouette_scores, db_scores


def perform_clustering(X, n_clusters=3):
    """執行 K-means 集群"""
    print(f"\n🎯 執行 RFM K-means 集群 (K={n_clusters})...")

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


def visualize_rfm_clusters(rfm_data, X_scaled, clusters):
    """視覺化 RFM 集群"""
    print("\n📊 生成 RFM 視覺化...")

    # Silhouette 樣本分數
    silhouette_vals = silhouette_samples(X_scaled, clusters)

    fig = plt.figure(figsize=(24, 12))

    # 1. 3D RFM 散點圖
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    n_clusters = len(np.unique(clusters))
    colors = plt.cm.viridis(np.linspace(0, 1, n_clusters))

    for i in range(n_clusters):
        mask = clusters == i
        ax1.scatter(rfm_data.loc[mask, 'recency'],
                   rfm_data.loc[mask, 'frequency'],
                   rfm_data.loc[mask, 'monetary'],
                   c=[colors[i]], label=f'集群 {i}',
                   s=50, alpha=0.6, edgecolors='black')

    ax1.set_xlabel('Recency (天)', fontproperties=chinese_font_prop, fontsize=10)
    ax1.set_ylabel('Frequency (次)', fontproperties=chinese_font_prop, fontsize=10)
    ax1.set_zlabel('Monetary ($)', fontproperties=chinese_font_prop, fontsize=10)
    ax1.set_title('RFM 3D 散點圖', fontproperties=chinese_font_prop,
                 fontsize=14, fontweight='bold')
    ax1.legend(prop=chinese_font_prop)

    # 2. Silhouette 圖
    ax2 = fig.add_subplot(2, 3, 2)
    y_lower = 10

    for i in range(n_clusters):
        cluster_silhouette_vals = silhouette_vals[clusters == i]
        cluster_silhouette_vals.sort()

        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i

        ax2.fill_betweenx(np.arange(y_lower, y_upper),
                         0, cluster_silhouette_vals,
                         facecolor=colors[i], edgecolor=colors[i], alpha=0.7)

        ax2.text(-0.05, y_lower + 0.5 * size_cluster_i, f'集群 {i}',
                fontproperties=chinese_font_prop)

        y_lower = y_upper + 10

    avg_score = silhouette_score(X_scaled, clusters)
    ax2.axvline(x=avg_score, color="red", linestyle="--", linewidth=2,
               label=f'平均: {avg_score:.3f}')
    ax2.set_xlabel('Silhouette Coefficient', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_ylabel('集群', fontproperties=chinese_font_prop, fontsize=12)
    ax2.set_title('Silhouette 分析', fontproperties=chinese_font_prop,
                 fontsize=14, fontweight='bold')
    ax2.legend(prop=chinese_font_prop)

    # 3. 集群分佈餅圖
    ax3 = fig.add_subplot(2, 3, 3)
    cluster_counts = pd.Series(clusters).value_counts().sort_index()
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

    # 4-6. RFM 各維度箱型圖
    rfm_cols = ['recency', 'frequency', 'monetary']
    rfm_labels = ['Recency (天)', 'Frequency (次)', 'Monetary ($)']

    for idx, (col, label) in enumerate(zip(rfm_cols, rfm_labels)):
        ax = fig.add_subplot(2, 3, 4 + idx)
        data_to_plot = [rfm_data.loc[clusters == i, col].values for i in range(n_clusters)]
        labels_box = [f'集群 {i}' for i in range(n_clusters)]

        bp = ax.boxplot(data_to_plot, labels=labels_box, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_title(label, fontproperties=chinese_font_prop, fontsize=12, fontweight='bold')
        ax.set_ylabel('數值', fontproperties=chinese_font_prop)
        ax.grid(True, alpha=0.3)

        for label_tick in ax.get_xticklabels():
            label_tick.set_fontproperties(chinese_font_prop)

    plt.suptitle('方案 B：RFM 集群分析', fontproperties=chinese_font_prop,
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/rfm_cluster_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✓ RFM 分析圖已保存")
    plt.close()


def analyze_rfm_clusters(rfm_data, clusters):
    """分析 RFM 集群特徵"""
    print("\n📋 分析 RFM 集群特徵...")

    rfm_data_copy = rfm_data.copy()
    rfm_data_copy['Cluster'] = clusters

    cluster_summary = rfm_data_copy.groupby('Cluster')[['recency', 'frequency', 'monetary']].agg(
        ['mean', 'median', 'std']
    )

    cluster_profiles = {}

    for cluster_id in range(clusters.max() + 1):
        cluster_data = rfm_data_copy[rfm_data_copy['Cluster'] == cluster_id]

        profile = {
            'cluster_id': int(cluster_id),
            'customer_count': int(len(cluster_data)),
            'avg_recency': float(cluster_data['recency'].mean()),
            'avg_frequency': float(cluster_data['frequency'].mean()),
            'avg_monetary': float(cluster_data['monetary'].mean()),
        }

        # RFM 集群命名邏輯
        r_score = 1 if profile['avg_recency'] < rfm_data['recency'].median() else 0
        f_score = 1 if profile['avg_frequency'] > rfm_data['frequency'].median() else 0
        m_score = 1 if profile['avg_monetary'] > rfm_data['monetary'].median() else 0

        total_score = r_score + f_score + m_score

        if total_score >= 2:
            if f_score == 1 and m_score == 1:
                profile['cluster_name'] = 'VIP 忠誠客戶'
                profile['description'] = '近期活躍、高頻率、高消費的核心客戶'
            else:
                profile['cluster_name'] = '高潛力客戶'
                profile['description'] = '部分指標優秀，有升級潛力'
        elif total_score == 1:
            profile['cluster_name'] = '活躍客戶'
            profile['description'] = '中等活躍度的穩定客戶'
        else:
            profile['cluster_name'] = '休眠/新客戶'
            profile['description'] = '低活躍度，需激活或剛加入'

        cluster_profiles[cluster_id] = profile

        print(f"\n集群 {cluster_id}: {profile['cluster_name']}")
        print(f"  客戶數: {profile['customer_count']}")
        print(f"  平均 Recency: {profile['avg_recency']:.1f} 天")
        print(f"  平均 Frequency: {profile['avg_frequency']:.2f} 次")
        print(f"  平均 Monetary: ${profile['avg_monetary']:.2f}")
        print(f"  RFM 評分: R={r_score} F={f_score} M={m_score}")

    return cluster_profiles, cluster_summary, rfm_data_copy


def save_results(cluster_profiles, cluster_summary, rfm_data_with_clusters,
                sil_score, db_score):
    """保存結果"""
    print("\n💾 保存結果...")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # JSON
    results = {
        'method': 'RFM Analysis (方案 B)',
        'timestamp': timestamp,
        'n_features': 3,
        'features': ['recency', 'frequency', 'monetary'],
        'n_clusters': 3,
        'total_customers': int(len(rfm_data_with_clusters)),
        'silhouette_score': float(sil_score),
        'davies_bouldin_score': float(db_score),
        'cluster_profiles': cluster_profiles
    }

    with open(f'{OUTPUT_DIR}/data/cluster_profiles_rfm.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON 已保存")

    # CSV
    cluster_summary.to_csv(f'{OUTPUT_DIR}/data/cluster_summary_rfm.csv', encoding='utf-8-sig')
    print(f"✓ 摘要 CSV 已保存")

    customer_clusters = rfm_data_with_clusters[['customer_id', 'Cluster']].copy()
    customer_clusters['Cluster_Name'] = customer_clusters['Cluster'].map(
        {k: v['cluster_name'] for k, v in cluster_profiles.items()}
    )
    customer_clusters.to_csv(f'{OUTPUT_DIR}/data/customer_clusters_rfm.csv',
                            index=False, encoding='utf-8-sig')
    print(f"✓ 客戶分配 CSV 已保存")

    # Markdown 報告
    generate_report(results, timestamp)

    return timestamp


def generate_report(results, timestamp):
    """生成 Markdown 報告"""
    report = f"""# 客戶集群分析報告 - 方案 B：RFM 分析

**生成時間**: {timestamp}
**方法**: 純 RFM 分析（經典零售客戶分層）
**特徵數量**: 3 個
**集群數量**: K=3
**基準日期**: {REFERENCE_DATE}

---

## RFM 模型說明

### 三大核心指標

**RFM 是零售業最經典的客戶分層模型：**

1. **Recency (R - 最近購買)**: 距今天數
   - 數值越小 = 越近期購買 = 越活躍
   - 用於識別流失風險客戶

2. **Frequency (F - 購買頻率)**: 交易次數
   - 數值越大 = 購買越頻繁 = 忠誠度越高
   - 用於識別核心客戶

3. **Monetary (M - 消費金額)**: 總消費
   - 數值越大 = 貢獻營收越多 = 價值越高
   - 用於識別高價值客戶

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

**RFM 指標**:
- 平均 Recency: {profile['avg_recency']:.1f} 天（距上次購買）
- 平均 Frequency: {profile['avg_frequency']:.2f} 次（交易次數）
- 平均 Monetary: ${profile['avg_monetary']:.2f}（總消費）

---
"""

    report += f"""
## 輸出文件

- **圖表**: `{OUTPUT_DIR}/charts/`
  - rfm_elbow_curve.png - 評估指標圖
  - rfm_cluster_analysis.png - RFM 3D 視覺化及分析

- **數據**: `{OUTPUT_DIR}/data/`
  - cluster_profiles_rfm.json - 集群配置
  - cluster_summary_rfm.csv - RFM 統計摘要
  - customer_clusters_rfm.csv - 客戶分配表

---

## RFM 集群命名規則

集群命名基於 RFM 評分（各維度與中位數比較）：

- **R分**: Recency < 中位數 = 1 分（近期活躍）
- **F分**: Frequency > 中位數 = 1 分（高頻率）
- **M分**: Monetary > 中位數 = 1 分（高消費）

**總分 3 分**: VIP 忠誠客戶（R=1, F=1, M=1）
**總分 2 分**: 高潛力客戶或活躍客戶
**總分 0-1 分**: 休眠客戶或新客戶

---

**分析方法**: K-means Clustering + StandardScaler
**隨機種子**: 42
**業界基準**: RFM 模型（零售業標準）
"""

    with open(f'{OUTPUT_DIR}/comparison_report_rfm.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Markdown 報告已保存")


def main():
    """主函數"""
    print("=" * 70)
    print("客戶集群分析 - 方案 B：純 RFM 分析 (3 特徵, K=3)")
    print("=" * 70)

    # 1. 載入數據
    df_payments = load_payments_json(DATA_FILE)
    df_processed = preprocess_payments_data(df_payments)

    # 2. 計算 RFM 特徵
    rfm_data = calculate_rfm_features(df_processed, REFERENCE_DATE)

    # 3. 選擇 RFM 特徵
    X = rfm_data[['recency', 'frequency', 'monetary']].copy()

    # 4. 評估最佳 K
    sil_scores, db_scores = evaluate_optimal_k(X, max_k=8)

    # 5. 執行集群 (K=3)
    clusters, kmeans, scaler, X_scaled, sil_score, db_score = perform_clustering(X, n_clusters=3)

    # 6. 視覺化
    visualize_rfm_clusters(rfm_data, X_scaled, clusters)

    # 7. 分析特徵
    cluster_profiles, cluster_summary, rfm_data_with_clusters = \
        analyze_rfm_clusters(rfm_data, clusters)

    # 8. 保存結果
    timestamp = save_results(cluster_profiles, cluster_summary,
                            rfm_data_with_clusters, sil_score, db_score)

    print("\n" + "=" * 70)
    print("✅ 方案 B (RFM) 分析完成!")
    print(f"✅ Silhouette Score: {sil_score:.4f}")
    print("=" * 70)

    return timestamp


if __name__ == '__main__':
    main()
