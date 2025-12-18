#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客戶集群分析腳本
使用 K-means 演算法對客戶進行分群,基於購買行為特徵
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
import os
import json
from datetime import datetime

warnings.filterwarnings('ignore')

# 設置中文字體
plt.rcParams['text.usetex'] = False
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 配置
DATA_FILE = 'data/items-2025-01-01-2025-11-16.csv'
OUTPUT_DIR = 'analysis_output/clustering'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/charts', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/data', exist_ok=True)


def load_and_preprocess_data(file_path):
    """載入並預處理數據"""
    print("📊 載入數據...")
    df = pd.read_csv(file_path)

    # 解析貨幣欄位
    for col in ['Gross Sales', 'Discounts', 'Net Sales', 'Tax']:
        df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

    # 解析日期時間
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Month'] = df['DateTime'].dt.month

    print(f"✓ 載入 {len(df)} 筆交易記錄")
    print(f"✓ 日期範圍: {df['Date'].min()} 至 {df['Date'].max()}")
    print(f"✓ 唯一客戶數: {df['Customer ID'].nunique()}")

    return df


def engineer_customer_features(df):
    """為每個客戶計算特徵"""
    print("\n🔧 進行特徵工程...")

    # 只分析有客戶ID的交易
    df_customers = df[df['Customer ID'].notna()].copy()

    # 按客戶聚合特徵
    customer_features = df_customers.groupby('Customer ID').agg({
        'Transaction ID': 'nunique',  # 交易次數
        'Net Sales': ['sum', 'mean', 'std'],  # 總消費、平均消費、消費變異
        'Qty': 'sum',  # 總購買數量
        'DateTime': ['min', 'max'],  # 第一次和最後一次購買
        'Category': lambda x: x.nunique(),  # 購買的類別數
        'Item': lambda x: x.nunique(),  # 購買的商品種類數
        'Dining Option': lambda x: (x == 'For Here').sum() / len(x) if len(x) > 0 else 0,  # 內用比例
    }).reset_index()

    # 扁平化列名
    customer_features.columns = [
        'Customer ID',
        'transaction_count',  # 交易次數
        'total_spending',  # 總消費金額
        'avg_spending',  # 平均消費
        'std_spending',  # 消費標準差
        'total_qty',  # 總購買數量
        'first_purchase',  # 第一次購買
        'last_purchase',  # 最後一次購買
        'category_diversity',  # 類別多樣性
        'item_diversity',  # 商品多樣性
        'dine_in_ratio'  # 內用比例
    ]

    # 計算衍生特徵
    customer_features['days_since_first'] = (
        customer_features['last_purchase'] - customer_features['first_purchase']
    ).dt.days

    customer_features['purchase_frequency'] = (
        customer_features['transaction_count'] /
        (customer_features['days_since_first'] + 1)  # +1 避免除以零
    )

    customer_features['avg_items_per_transaction'] = (
        customer_features['total_qty'] / customer_features['transaction_count']
    )

    # 填補缺失值
    customer_features['std_spending'].fillna(0, inplace=True)

    print(f"✓ 生成 {len(customer_features)} 個客戶的特徵")
    print(f"✓ 特徵數量: {len(customer_features.columns) - 1}")

    return customer_features


def select_features_for_clustering(customer_features):
    """選擇用於集群分析的特徵"""
    # 選擇數值特徵進行集群
    feature_cols = [
        'transaction_count',  # 交易次數
        'total_spending',  # 總消費
        'avg_spending',  # 平均消費
        'category_diversity',  # 類別多樣性
        'item_diversity',  # 商品多樣性
        'purchase_frequency',  # 購買頻率
        'avg_items_per_transaction',  # 平均每次交易購買數量
        'dine_in_ratio'  # 內用比例
    ]

    X = customer_features[feature_cols].copy()

    # 處理無限值和缺失值
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(0, inplace=True)

    return X, feature_cols


def find_optimal_k(X, max_k=10):
    """使用肘部法則和輪廓係數確定最佳集群數"""
    print("\n📈 尋找最佳集群數...")

    inertias = []
    K_range = range(2, min(max_k + 1, len(X)))

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    # 繪製肘部圖
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('集群數 (k)', fontsize=12, fontproperties='Arial Unicode MS')
    plt.ylabel('慣性 (Inertia)', fontsize=12, fontproperties='Arial Unicode MS')
    plt.title('肘部法則 - 確定最佳集群數', fontsize=14, fontproperties='Arial Unicode MS', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/elbow_curve.png', dpi=300, bbox_inches='tight')
    print(f"✓ 肘部圖已保存至: {OUTPUT_DIR}/charts/elbow_curve.png")
    plt.close()

    return inertias


def perform_clustering(X, n_clusters=4):
    """執行 K-means 集群分析"""
    print(f"\n🎯 執行 K-means 集群分析 (k={n_clusters})...")

    # 標準化特徵
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means 集群
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    print(f"✓ 集群分析完成")
    print(f"✓ 各集群樣本數: {np.bincount(clusters)}")

    return clusters, kmeans, scaler, X_scaled


def visualize_clusters(X, clusters, feature_cols, customer_features):
    """視覺化集群結果"""
    print("\n📊 生成視覺化圖表...")

    # 1. PCA 降維視覺化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters,
                         cmap='viridis', s=100, alpha=0.6, edgecolors='black')
    plt.colorbar(scatter, label='集群')
    plt.xlabel(f'第一主成分 (解釋變異: {pca.explained_variance_ratio_[0]:.2%})',
              fontproperties='Arial Unicode MS', fontsize=12)
    plt.ylabel(f'第二主成分 (解釋變異: {pca.explained_variance_ratio_[1]:.2%})',
              fontproperties='Arial Unicode MS', fontsize=12)
    plt.title('客戶集群分析 - PCA 視覺化', fontproperties='Arial Unicode MS',
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/cluster_pca.png', dpi=300, bbox_inches='tight')
    print(f"✓ PCA 視覺化已保存")
    plt.close()

    # 2. 特徵分佈箱型圖
    n_features = len(feature_cols)
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.flatten()

    for idx, col in enumerate(feature_cols):
        if idx < len(axes):
            data_to_plot = [X[clusters == i][col].values for i in range(clusters.max() + 1)]
            axes[idx].boxplot(data_to_plot, labels=[f'集群 {i}' for i in range(clusters.max() + 1)])
            axes[idx].set_title(col, fontproperties='Arial Unicode MS', fontsize=10)
            axes[idx].grid(True, alpha=0.3)

    # 隱藏多餘的子圖
    for idx in range(len(feature_cols), len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle('各集群特徵分佈比較', fontproperties='Arial Unicode MS',
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/cluster_features_boxplot.png', dpi=300, bbox_inches='tight')
    print(f"✓ 特徵分佈箱型圖已保存")
    plt.close()

    # 3. 集群大小餅圖
    cluster_counts = pd.Series(clusters).value_counts().sort_index()
    plt.figure(figsize=(10, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_counts)))
    plt.pie(cluster_counts, labels=[f'集群 {i}\n({count} 人)' for i, count in enumerate(cluster_counts)],
           autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontproperties': 'Arial Unicode MS'})
    plt.title('客戶集群分佈', fontproperties='Arial Unicode MS', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/cluster_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✓ 集群分佈餅圖已保存")
    plt.close()


def analyze_cluster_characteristics(customer_features, clusters, feature_cols):
    """分析各集群的特徵"""
    print("\n📋 分析各集群特徵...")

    customer_features_copy = customer_features.copy()
    customer_features_copy['Cluster'] = clusters

    # 計算各集群的統計摘要
    cluster_summary = customer_features_copy.groupby('Cluster')[feature_cols].agg(['mean', 'median', 'std'])

    # 為每個集群命名
    cluster_profiles = {}

    for cluster_id in range(clusters.max() + 1):
        cluster_data = customer_features_copy[customer_features_copy['Cluster'] == cluster_id]

        profile = {
            'cluster_id': int(cluster_id),
            'customer_count': int(len(cluster_data)),
            'avg_transaction_count': float(cluster_data['transaction_count'].mean()),
            'avg_total_spending': float(cluster_data['total_spending'].mean()),
            'avg_spending_per_transaction': float(cluster_data['avg_spending'].mean()),
            'avg_category_diversity': float(cluster_data['category_diversity'].mean()),
            'avg_purchase_frequency': float(cluster_data['purchase_frequency'].mean()),
            'avg_dine_in_ratio': float(cluster_data['dine_in_ratio'].mean()),
        }

        # 根據特徵為集群命名
        if profile['avg_total_spending'] > customer_features_copy['total_spending'].quantile(0.75):
            if profile['avg_transaction_count'] > customer_features_copy['transaction_count'].quantile(0.75):
                profile['cluster_name'] = 'VIP 忠誠客戶'
                profile['description'] = '高消費、高頻率的忠誠客戶'
            else:
                profile['cluster_name'] = '高價值客戶'
                profile['description'] = '消費金額高但頻率較低的客戶'
        elif profile['avg_transaction_count'] > customer_features_copy['transaction_count'].quantile(0.75):
            profile['cluster_name'] = '常客'
            profile['description'] = '購買頻率高但單次消費較低的客戶'
        elif profile['avg_transaction_count'] <= customer_features_copy['transaction_count'].quantile(0.25):
            profile['cluster_name'] = '新客戶 / 偶爾消費'
            profile['description'] = '購買次數少、可能是新客戶或偶爾消費的客戶'
        else:
            profile['cluster_name'] = '一般客戶'
            profile['description'] = '中等消費頻率和金額的一般客戶'

        cluster_profiles[cluster_id] = profile

        print(f"\n集群 {cluster_id}: {profile['cluster_name']}")
        print(f"  - 客戶數: {profile['customer_count']}")
        print(f"  - 平均交易次數: {profile['avg_transaction_count']:.2f}")
        print(f"  - 平均總消費: ${profile['avg_total_spending']:.2f}")
        print(f"  - 平均單次消費: ${profile['avg_spending_per_transaction']:.2f}")
        print(f"  - 平均類別多樣性: {profile['avg_category_diversity']:.2f}")
        print(f"  - 平均購買頻率: {profile['avg_purchase_frequency']:.4f} 次/天")
        print(f"  - 內用比例: {profile['avg_dine_in_ratio']:.2%}")

    return cluster_profiles, cluster_summary, customer_features_copy


def save_results(cluster_profiles, cluster_summary, customer_features_with_clusters):
    """保存分析結果"""
    print("\n💾 保存分析結果...")

    # 保存集群配置文件 JSON
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    results = {
        'timestamp': timestamp,
        'total_customers': int(len(customer_features_with_clusters)),
        'n_clusters': int(customer_features_with_clusters['Cluster'].nunique()),
        'cluster_profiles': cluster_profiles
    }

    with open(f'{OUTPUT_DIR}/data/cluster_profiles_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ 集群配置已保存至: {OUTPUT_DIR}/data/cluster_profiles_{timestamp}.json")

    # 保存詳細統計摘要 CSV
    cluster_summary.to_csv(f'{OUTPUT_DIR}/data/cluster_summary_{timestamp}.csv')
    print(f"✓ 集群摘要已保存至: {OUTPUT_DIR}/data/cluster_summary_{timestamp}.csv")

    # 保存客戶集群分配
    customer_clusters = customer_features_with_clusters[['Customer ID', 'Cluster']].copy()
    customer_clusters['Cluster_Name'] = customer_clusters['Cluster'].map(
        {k: v['cluster_name'] for k, v in cluster_profiles.items()}
    )
    customer_clusters.to_csv(f'{OUTPUT_DIR}/data/customer_clusters_{timestamp}.csv', index=False)
    print(f"✓ 客戶集群分配已保存至: {OUTPUT_DIR}/data/customer_clusters_{timestamp}.csv")

    # 生成 Markdown 報告
    generate_markdown_report(results, cluster_summary, timestamp)


def generate_markdown_report(results, cluster_summary, timestamp):
    """生成 Markdown 分析報告"""
    report = f"""# 客戶集群分析報告

**生成時間**: {timestamp}
**分析客戶總數**: {results['total_customers']}
**集群數量**: {results['n_clusters']}

---

## 集群概覽

"""

    for cluster_id, profile in results['cluster_profiles'].items():
        report += f"""
### 集群 {cluster_id}: {profile['cluster_name']}

**描述**: {profile['description']}

**關鍵指標**:
- 客戶數量: {profile['customer_count']} 人 ({profile['customer_count']/results['total_customers']*100:.1f}%)
- 平均交易次數: {profile['avg_transaction_count']:.2f} 次
- 平均總消費金額: ${profile['avg_total_spending']:.2f}
- 平均單次消費: ${profile['avg_spending_per_transaction']:.2f}
- 平均類別多樣性: {profile['avg_category_diversity']:.2f} 種類別
- 購買頻率: {profile['avg_purchase_frequency']:.4f} 次/天
- 內用比例: {profile['avg_dine_in_ratio']:.1%}

**營銷建議**:
"""

        # 根據集群特徵提供建議
        if 'VIP' in profile['cluster_name'] or '高價值' in profile['cluster_name']:
            report += """- 提供 VIP 會員專屬優惠和服務
- 定期發送個性化推薦和新品資訊
- 邀請參加專屬活動或品酒會
- 建立積分回饋計劃
"""
        elif '常客' in profile['cluster_name']:
            report += """- 推出累積消費優惠活動
- 提供集點卡或會員卡
- 鼓勵嘗試新產品類別
- 定期發送促銷資訊
"""
        elif '新客戶' in profile['cluster_name'] or '偶爾' in profile['cluster_name']:
            report += """- 提供新客優惠吸引回購
- 發送歡迎優惠券
- 透過 Email/SMS 保持聯繫
- 推薦熱門商品和套餐
"""
        else:
            report += """- 提供中等價位的套餐優惠
- 定期促銷活動提升購買頻率
- 推薦多樣化產品選擇
- 建立忠誠度計劃
"""

        report += "\n---\n"

    report += f"""
## 分析方法

本分析使用 **K-means 集群演算法**,基於以下客戶特徵進行分群:

1. **交易次數** (transaction_count): 客戶累計交易次數
2. **總消費金額** (total_spending): 客戶累計消費總額
3. **平均消費** (avg_spending): 每次交易的平均消費金額
4. **類別多樣性** (category_diversity): 購買的商品類別數量
5. **商品多樣性** (item_diversity): 購買的不同商品種類數
6. **購買頻率** (purchase_frequency): 每天的平均交易次數
7. **平均每次購買數量** (avg_items_per_transaction): 每次交易的平均商品數量
8. **內用比例** (dine_in_ratio): 選擇內用的交易比例

## 輸出文件

- **視覺化圖表**: `{OUTPUT_DIR}/charts/`
  - `elbow_curve.png`: 肘部法則圖
  - `cluster_pca.png`: PCA 降維視覺化
  - `cluster_features_boxplot.png`: 特徵分佈箱型圖
  - `cluster_distribution.png`: 集群分佈餅圖

- **數據文件**: `{OUTPUT_DIR}/data/`
  - `cluster_profiles_{timestamp}.json`: 集群配置 JSON
  - `cluster_summary_{timestamp}.csv`: 集群統計摘要
  - `customer_clusters_{timestamp}.csv`: 客戶集群分配表

---

**分析工具**: Python (pandas, scikit-learn, matplotlib, seaborn)
**演算法**: K-means Clustering + PCA 降維
"""

    with open(f'{OUTPUT_DIR}/cluster_analysis_report_{timestamp}.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ 分析報告已保存至: {OUTPUT_DIR}/cluster_analysis_report_{timestamp}.md")


def main():
    """主函數"""
    print("=" * 60)
    print("客戶集群分析系統")
    print("=" * 60)

    # 1. 載入數據
    df = load_and_preprocess_data(DATA_FILE)

    # 2. 特徵工程
    customer_features = engineer_customer_features(df)

    # 3. 選擇特徵
    X, feature_cols = select_features_for_clustering(customer_features)

    # 4. 尋找最佳集群數
    inertias = find_optimal_k(X, max_k=8)

    # 5. 執行集群分析 (這裡使用 k=4,可根據肘部圖調整)
    optimal_k = 4  # 可根據肘部圖手動調整
    clusters, kmeans, scaler, X_scaled = perform_clustering(X, n_clusters=optimal_k)

    # 6. 視覺化
    visualize_clusters(X, clusters, feature_cols, customer_features)

    # 7. 分析集群特徵
    cluster_profiles, cluster_summary, customer_features_with_clusters = analyze_cluster_characteristics(
        customer_features, clusters, feature_cols
    )

    # 8. 保存結果
    save_results(cluster_profiles, cluster_summary, customer_features_with_clusters)

    print("\n" + "=" * 60)
    print("✅ 集群分析完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
