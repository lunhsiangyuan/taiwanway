#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客戶集群分析腳本 - JSON 版本
使用 K-means 演算法對客戶進行分群，基於購買行為特徵
數據來源：all_payments.json
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
import pytz
import matplotlib.font_manager as fm

warnings.filterwarnings('ignore')

# 設置中文字體 - 使用系統中文字體
plt.rcParams['text.usetex'] = False
plt.rcParams['axes.unicode_minus'] = False

# 嘗試載入中文字體
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
    print("⚠️  未找到中文字體，圖表可能顯示不正確")
    chinese_font_prop = fm.FontProperties()

# 配置
DATA_FILE = 'data/all_payments/all_payments.json'
OUTPUT_DIR = 'analysis_output/clustering'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/charts', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/data', exist_ok=True)


def load_payments_json(file_path, start_date='2025-01-01', end_date='2025-11-16'):
    """從 JSON 文件載入支付數據"""
    print("📊 載入 JSON 數據...")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取支付記錄
    payments = data.get('payments', [])
    print(f"✓ 載入 {len(payments)} 筆支付記錄")

    # 轉換為 DataFrame
    df = pd.json_normalize(payments)

    return df


def preprocess_payments_data(df, start_date='2025-01-01', end_date='2025-11-16'):
    """預處理支付數據"""
    print("\n🔧 預處理數據...")

    # 轉換金額（從 cents 轉為 dollars）
    if 'amount_money.amount' in df.columns:
        df['amount_usd'] = df['amount_money.amount'] / 100

    if 'tip_money.amount' in df.columns:
        df['tip_usd'] = df['tip_money.amount'].fillna(0) / 100
    else:
        df['tip_usd'] = 0

    if 'total_money.amount' in df.columns:
        df['total_usd'] = df['total_money.amount'] / 100

    # 處理時間戳
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

    # 轉換到紐約時區
    ny_tz = pytz.timezone('America/New_York')
    df['datetime_ny'] = df['created_at'].dt.tz_convert(ny_tz)

    # 提取時間特徵
    df['date'] = df['datetime_ny'].dt.date
    df['hour'] = df['datetime_ny'].dt.hour
    df['dayofweek'] = df['datetime_ny'].dt.dayofweek
    df['month'] = df['datetime_ny'].dt.month
    df['year'] = df['datetime_ny'].dt.year

    # 過濾日期範圍
    start = pd.to_datetime(start_date).date()
    end = pd.to_datetime(end_date).date()
    df = df[(df['date'] >= start) & (df['date'] <= end)].copy()

    print(f"✓ 日期範圍過濾後: {len(df)} 筆記錄")
    print(f"✓ 日期範圍: {df['date'].min()} 至 {df['date'].max()}")

    # 只保留有 customer_id 的記錄
    df_with_customers = df[df['customer_id'].notna()].copy()
    print(f"✓ 有客戶ID的記錄: {len(df_with_customers)} 筆 ({len(df_with_customers)/len(df)*100:.1f}%)")
    print(f"✓ 唯一客戶數: {df_with_customers['customer_id'].nunique()}")

    return df_with_customers


def engineer_customer_features_from_payments(df):
    """從支付數據中為每個客戶計算特徵"""
    print("\n🔧 進行特徵工程...")

    # 按客戶聚合特徵
    customer_agg = df.groupby('customer_id').agg({
        'id': 'count',  # 交易次數
        'amount_usd': ['sum', 'mean', 'std'],  # 總消費、平均消費、消費變異
        'tip_usd': ['sum', 'mean'],  # 總小費、平均小費
        'datetime_ny': ['min', 'max'],  # 第一次和最後一次購買
        'source_type': lambda x: x.mode()[0] if len(x) > 0 else None,  # 最常用支付方式
    }).reset_index()

    # 扁平化列名
    customer_agg.columns = [
        'customer_id',
        'transaction_count',
        'total_spending',
        'avg_spending',
        'std_spending',
        'total_tip',
        'avg_tip',
        'first_purchase',
        'last_purchase',
        'preferred_payment_method'
    ]

    # 計算信用卡使用率
    card_usage = df.groupby('customer_id').apply(
        lambda x: (x['source_type'] == 'CARD').sum() / len(x) if len(x) > 0 else 0
    ).reset_index(name='card_usage_ratio')
    customer_agg = customer_agg.merge(card_usage, on='customer_id')

    # 計算小費給予率
    tip_frequency = df.groupby('customer_id').apply(
        lambda x: (x['tip_usd'] > 0).sum() / len(x) if len(x) > 0 else 0
    ).reset_index(name='tip_frequency')
    customer_agg = customer_agg.merge(tip_frequency, on='customer_id')

    # 計算時段偏好（營業時間內的平均小時）
    hour_preference = df.groupby('customer_id')['hour'].mean().reset_index(name='avg_hour')
    customer_agg = customer_agg.merge(hour_preference, on='customer_id')

    # 計算週末消費比例
    weekend_ratio = df.groupby('customer_id').apply(
        lambda x: (x['dayofweek'].isin([5, 6])).sum() / len(x) if len(x) > 0 else 0
    ).reset_index(name='weekend_ratio')
    customer_agg = customer_agg.merge(weekend_ratio, on='customer_id')

    # 計算衍生特徵
    customer_agg['days_since_first'] = (
        customer_agg['last_purchase'] - customer_agg['first_purchase']
    ).dt.days

    customer_agg['purchase_frequency'] = (
        customer_agg['transaction_count'] /
        (customer_agg['days_since_first'] + 1)  # +1 避免除以零
    )

    # 計算客戶價值指數 (LTV 估算)
    customer_agg['customer_value_index'] = (
        customer_agg['total_spending'] * customer_agg['purchase_frequency']
    )

    # 填補缺失值
    customer_agg['std_spending'].fillna(0, inplace=True)
    customer_agg['total_tip'].fillna(0, inplace=True)
    customer_agg['avg_tip'].fillna(0, inplace=True)

    print(f"✓ 生成 {len(customer_agg)} 個客戶的特徵")
    print(f"✓ 特徵數量: {len(customer_agg.columns) - 1}")

    # 顯示特徵摘要
    print("\n特徵統計摘要:")
    print(f"  - 平均交易次數: {customer_agg['transaction_count'].mean():.2f}")
    print(f"  - 平均總消費: ${customer_agg['total_spending'].mean():.2f}")
    print(f"  - 平均單次消費: ${customer_agg['avg_spending'].mean():.2f}")
    print(f"  - 信用卡使用率: {customer_agg['card_usage_ratio'].mean():.1%}")
    print(f"  - 小費給予率: {customer_agg['tip_frequency'].mean():.1%}")

    return customer_agg


def select_features_for_clustering(customer_features):
    """選擇用於集群分析的特徵"""
    # 選擇數值特徵進行集群
    feature_cols = [
        'transaction_count',       # 交易次數
        'total_spending',          # 總消費
        'avg_spending',            # 平均消費
        'purchase_frequency',      # 購買頻率
        'card_usage_ratio',        # 信用卡使用率
        'tip_frequency',           # 小費給予率
        'avg_tip',                 # 平均小費
        'weekend_ratio'            # 週末消費比例
    ]

    X = customer_features[feature_cols].copy()

    # 處理無限值和缺失值
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(0, inplace=True)

    return X, feature_cols


def find_optimal_k(X, max_k=10):
    """使用肘部法則確定最佳集群數"""
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
    plt.xlabel('集群數 (k)', fontsize=12, fontproperties=chinese_font_prop)
    plt.ylabel('慣性 (Inertia)', fontsize=12, fontproperties=chinese_font_prop)
    plt.title('肘部法則 - 確定最佳集群數', fontsize=14, fontproperties=chinese_font_prop, fontweight='bold')
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
              fontproperties=chinese_font_prop, fontsize=12)
    plt.ylabel(f'第二主成分 (解釋變異: {pca.explained_variance_ratio_[1]:.2%})',
              fontproperties=chinese_font_prop, fontsize=12)
    plt.title('客戶集群分析 - PCA 視覺化', fontproperties=chinese_font_prop,
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

            # 設置標題 - 使用中文字體
            title_text = col.replace('_', ' ').title()
            axes[idx].set_title(title_text, fontproperties=chinese_font_prop, fontsize=10)
            axes[idx].grid(True, alpha=0.3)

            # 設置 x 軸標籤
            for label in axes[idx].get_xticklabels():
                label.set_fontproperties(chinese_font_prop)

    # 隱藏多餘的子圖
    for idx in range(len(feature_cols), len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle('各集群特徵分佈比較', fontproperties=chinese_font_prop,
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/charts/cluster_features_boxplot.png', dpi=300, bbox_inches='tight')
    print(f"✓ 特徵分佈箱型圖已保存")
    plt.close()

    # 3. 集群大小餅圖
    cluster_counts = pd.Series(clusters).value_counts().sort_index()
    plt.figure(figsize=(10, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_counts)))

    # 創建標籤
    labels = [f'集群 {i}\n({count} 人)' for i, count in enumerate(cluster_counts)]

    wedges, texts, autotexts = plt.pie(
        cluster_counts,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )

    # 設置所有文字使用中文字體
    for text in texts:
        text.set_fontproperties(chinese_font_prop)
    for autotext in autotexts:
        autotext.set_fontproperties(chinese_font_prop)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.title('客戶集群分佈', fontproperties=chinese_font_prop, fontsize=14, fontweight='bold')
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
            'avg_purchase_frequency': float(cluster_data['purchase_frequency'].mean()),
            'avg_card_usage_ratio': float(cluster_data['card_usage_ratio'].mean()),
            'avg_tip_frequency': float(cluster_data['tip_frequency'].mean()),
            'avg_tip': float(cluster_data['avg_tip'].mean()),
            'avg_weekend_ratio': float(cluster_data['weekend_ratio'].mean()),
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
        print(f"  - 平均購買頻率: {profile['avg_purchase_frequency']:.4f} 次/天")
        print(f"  - 信用卡使用率: {profile['avg_card_usage_ratio']:.2%}")
        print(f"  - 小費給予率: {profile['avg_tip_frequency']:.2%}")
        print(f"  - 平均小費: ${profile['avg_tip']:.2f}")
        print(f"  - 週末消費比例: {profile['avg_weekend_ratio']:.2%}")

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
    cluster_summary.to_csv(f'{OUTPUT_DIR}/data/cluster_summary_{timestamp}.csv', encoding='utf-8-sig')
    print(f"✓ 集群摘要已保存至: {OUTPUT_DIR}/data/cluster_summary_{timestamp}.csv")

    # 保存客戶集群分配
    customer_clusters = customer_features_with_clusters[['customer_id', 'Cluster']].copy()
    customer_clusters['Cluster_Name'] = customer_clusters['Cluster'].map(
        {k: v['cluster_name'] for k, v in cluster_profiles.items()}
    )
    customer_clusters.to_csv(f'{OUTPUT_DIR}/data/customer_clusters_{timestamp}.csv', index=False, encoding='utf-8-sig')
    print(f"✓ 客戶集群分配已保存至: {OUTPUT_DIR}/data/customer_clusters_{timestamp}.csv")

    # 生成 Markdown 報告
    generate_markdown_report(results, cluster_summary, timestamp)

    return timestamp


def generate_markdown_report(results, cluster_summary, timestamp):
    """生成 Markdown 分析報告"""
    report = f"""# 客戶集群分析報告

**生成時間**: {timestamp}
**分析客戶總數**: {results['total_customers']}
**集群數量**: {results['n_clusters']}
**數據來源**: all_payments.json (Square API)

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
- 購買頻率: {profile['avg_purchase_frequency']:.4f} 次/天
- 信用卡使用率: {profile['avg_card_usage_ratio']:.1%}
- 小費給予率: {profile['avg_tip_frequency']:.1%}
- 平均小費金額: ${profile['avg_tip']:.2f}
- 週末消費比例: {profile['avg_weekend_ratio']:.1%}

**營銷建議**:
"""

        # 根據集群特徵提供建議
        if 'VIP' in profile['cluster_name'] or '高價值' in profile['cluster_name']:
            report += """- 提供 VIP 會員專屬優惠和服務
- 定期發送個性化推薦和新品資訊
- 邀請參加專屬活動或品鑑會
- 建立積分回饋計劃，增強忠誠度
- 優先處理訂單和特殊要求
"""
        elif '常客' in profile['cluster_name']:
            report += """- 推出累積消費優惠活動
- 提供集點卡或會員卡制度
- 鼓勵嘗試新產品和高價值商品
- 定期發送促銷資訊和特別優惠
- 建立推薦獎勵機制
"""
        elif '新客戶' in profile['cluster_name'] or '偶爾' in profile['cluster_name']:
            report += """- 提供首購優惠吸引回購
- 發送歡迎優惠券和新客禮包
- 透過 Email/SMS 保持定期聯繫
- 推薦熱門商品和套餐組合
- 收集反饋改善服務體驗
"""
        else:
            report += """- 提供中等價位的套餐優惠
- 定期促銷活動提升購買頻率
- 推薦多樣化產品選擇
- 建立忠誠度計劃鼓勵升級
- 個性化推薦提升客單價
"""

        report += "\n---\n"

    report += f"""
## 分析方法

本分析使用 **K-means 集群演算法**，基於以下客戶特徵進行分群：

1. **交易次數** (transaction_count): 客戶累計交易次數
2. **總消費金額** (total_spending): 客戶累計消費總額
3. **平均消費** (avg_spending): 每次交易的平均消費金額
4. **購買頻率** (purchase_frequency): 每天的平均交易次數
5. **信用卡使用率** (card_usage_ratio): 使用信用卡支付的交易比例
6. **小費給予率** (tip_frequency): 給予小費的交易比例
7. **平均小費** (avg_tip): 每次交易的平均小費金額
8. **週末消費比例** (weekend_ratio): 週末進行交易的比例

### 數據處理流程

1. 從 Square API 支付記錄提取客戶交易數據
2. 轉換金額單位（cents → dollars）
3. 時區轉換（UTC → America/New_York）
4. 按客戶 ID 聚合計算特徵
5. 特徵標準化（StandardScaler）
6. K-means 集群分析（K=4）
7. PCA 降維視覺化

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

**分析工具**: Python (pandas, scikit-learn, matplotlib, seaborn, pytz)
**演算法**: K-means Clustering + PCA 降維
**數據來源**: Square API Payments (all_payments.json)
"""

    with open(f'{OUTPUT_DIR}/cluster_analysis_report_{timestamp}.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ 分析報告已保存至: {OUTPUT_DIR}/cluster_analysis_report_{timestamp}.md")


def main():
    """主函數"""
    print("=" * 60)
    print("客戶集群分析系統 - JSON 版本")
    print("=" * 60)

    # 1. 載入 JSON 數據
    df_payments = load_payments_json(DATA_FILE)

    # 2. 預處理數據
    df_processed = preprocess_payments_data(df_payments, start_date='2025-01-01', end_date='2025-11-16')

    # 3. 特徵工程
    customer_features = engineer_customer_features_from_payments(df_processed)

    # 4. 選擇特徵
    X, feature_cols = select_features_for_clustering(customer_features)

    # 5. 尋找最佳集群數
    inertias = find_optimal_k(X, max_k=8)

    # 6. 執行集群分析 (使用 k=4)
    optimal_k = 4
    clusters, kmeans, scaler, X_scaled = perform_clustering(X, n_clusters=optimal_k)

    # 7. 視覺化
    visualize_clusters(X, clusters, feature_cols, customer_features)

    # 8. 分析集群特徵
    cluster_profiles, cluster_summary, customer_features_with_clusters = analyze_cluster_characteristics(
        customer_features, clusters, feature_cols
    )

    # 9. 保存結果
    timestamp = save_results(cluster_profiles, cluster_summary, customer_features_with_clusters)

    print("\n" + "=" * 60)
    print("✅ 集群分析完成!")
    print(f"✅ 報告時間戳: {timestamp}")
    print("=" * 60)

    return timestamp


if __name__ == '__main__':
    main()
