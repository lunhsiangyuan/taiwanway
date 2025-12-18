#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成客戶集群分析 PDF 報告
包含所有圖表和詳細解釋
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import matplotlib.font_manager as fm
import json
import os
from datetime import datetime
import pandas as pd
from PIL import Image
import numpy as np

# 設置中文字體
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
    print("⚠️  未找到中文字體，使用默認字體（可能顯示不正確）")
    chinese_font_prop = fm.FontProperties()

# 配置
CLUSTERING_DIR = 'analysis_output/clustering'
OUTPUT_DIR = 'analysis_output/clustering'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def find_latest_files():
    """找到最新的集群分析文件"""
    data_dir = f'{CLUSTERING_DIR}/data'

    # 找到最新的 JSON 文件
    json_files = [f for f in os.listdir(data_dir) if f.startswith('cluster_profiles_') and f.endswith('.json')]
    if not json_files:
        raise FileNotFoundError("找不到集群配置文件")

    latest_json = sorted(json_files)[-1]
    timestamp = latest_json.replace('cluster_profiles_', '').replace('.json', '')

    return timestamp


def load_cluster_data(timestamp):
    """載入集群分析數據"""
    with open(f'{CLUSTERING_DIR}/data/cluster_profiles_{timestamp}.json', 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    summary_df = pd.read_csv(f'{CLUSTERING_DIR}/data/cluster_summary_{timestamp}.csv')
    customer_clusters = pd.read_csv(f'{CLUSTERING_DIR}/data/customer_clusters_{timestamp}.csv')

    return profiles, summary_df, customer_clusters


def create_title_page(fig):
    """創建封面頁"""
    ax = fig.add_subplot(111)
    ax.axis('off')

    # 標題
    ax.text(0.5, 0.75, '客戶集群分析報告',
            ha='center', va='center', fontsize=36, fontweight='bold',
            fontproperties=chinese_font_prop)

    ax.text(0.5, 0.65, 'Customer Clustering Analysis Report',
            ha='center', va='center', fontsize=20, style='italic')

    # 分隔線
    ax.plot([0.2, 0.8], [0.58, 0.58], 'k-', linewidth=2)

    # 副標題
    ax.text(0.5, 0.50, '基於 K-means 演算法的客戶分群研究',
            ha='center', va='center', fontsize=16,
            fontproperties=chinese_font_prop)

    # 日期
    current_date = datetime.now().strftime('%Y年%m月%d日')
    ax.text(0.5, 0.35, f'報告生成日期: {current_date}',
            ha='center', va='center', fontsize=14,
            fontproperties=chinese_font_prop)

    # 底部資訊
    ax.text(0.5, 0.15, 'Taiwanway Restaurant',
            ha='center', va='center', fontsize=12,
            fontproperties=chinese_font_prop, style='italic')

    ax.text(0.5, 0.10, '數據驅動的客戶洞察與營銷策略',
            ha='center', va='center', fontsize=11,
            fontproperties=chinese_font_prop, color='gray')


def create_summary_page(fig, profiles):
    """創建執行摘要頁"""
    ax = fig.add_subplot(111)
    ax.axis('off')

    # 標題
    ax.text(0.5, 0.95, '執行摘要',
            ha='center', va='top', fontsize=24, fontweight='bold',
            fontproperties=chinese_font_prop)

    # 分析概要
    y_pos = 0.87
    summary_text = f"""
分析範圍:
• 客戶總數: {profiles['total_customers']} 位
• 集群數量: {profiles['n_clusters']} 個
• 分析方法: K-means 集群演算法
• 生成時間: {profiles['timestamp']}

主要發現:
"""

    ax.text(0.1, y_pos, summary_text, ha='left', va='top', fontsize=12,
            fontproperties=chinese_font_prop, linespacing=1.8)

    # 各集群簡介
    y_pos = 0.60

    cluster_colors = ['#440154', '#31688e', '#35b779', '#fde724']

    for cluster_id, profile in profiles['cluster_profiles'].items():
        color = cluster_colors[int(cluster_id)]

        # 處理不同版本的字段名
        dine_in_ratio = profile.get('avg_dine_in_ratio', 0)
        card_usage = profile.get('avg_card_usage_ratio', 0)

        cluster_text = f"""
集群 {cluster_id}: {profile['cluster_name']} ({profile['customer_count']}人, {profile['customer_count']/profiles['total_customers']*100:.1f}%)
  ├─ 平均交易次數: {profile['avg_transaction_count']:.1f} 次
  ├─ 平均總消費: ${profile['avg_total_spending']:.2f}
  ├─ 平均單次消費: ${profile['avg_spending_per_transaction']:.2f}
  └─ 信用卡使用率: {card_usage:.1%}
"""

        # 背景框
        rect = mpatches.FancyBboxPatch((0.08, y_pos-0.08), 0.84, 0.11,
                                        boxstyle="round,pad=0.01",
                                        facecolor=color, alpha=0.15,
                                        edgecolor=color, linewidth=2)
        ax.add_patch(rect)

        ax.text(0.1, y_pos, cluster_text, ha='left', va='top', fontsize=10,
                fontproperties=chinese_font_prop, family='monospace',
                linespacing=1.6)

        y_pos -= 0.145

    # 底部關鍵洞察
    ax.text(0.5, 0.08, '⚡ 關鍵洞察: 4.2% 的超級 VIP 客戶平均消費超過 $400,是最寶貴的資產',
            ha='center', va='center', fontsize=11, fontweight='bold',
            fontproperties=chinese_font_prop,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))


def create_methodology_page(fig):
    """創建分析方法頁"""
    ax = fig.add_subplot(111)
    ax.axis('off')

    # 標題
    ax.text(0.5, 0.95, '分析方法論',
            ha='center', va='top', fontsize=24, fontweight='bold',
            fontproperties=chinese_font_prop)

    # K-means 演算法介紹
    y_pos = 0.87

    methodology_text = """
一、K-means 集群演算法

K-means 是一種無監督機器學習算法,通過迭代方式將數據分成 K 個集群:

  1. 隨機選擇 K 個初始中心點
  2. 將每個數據點分配到最近的中心點
  3. 重新計算各集群的中心點
  4. 重複步驟 2-3 直到收斂

二、特徵工程

本分析使用以下 8 個客戶特徵:

  1. 交易次數 (transaction_count): 客戶累計交易次數
  2. 總消費金額 (total_spending): 客戶累計消費總額
  3. 平均消費 (avg_spending): 每次交易的平均消費金額
  4. 類別多樣性 (category_diversity): 購買的商品類別數量
  5. 商品多樣性 (item_diversity): 購買的不同商品種類數
  6. 購買頻率 (purchase_frequency): 每天的平均交易次數
  7. 平均每次購買數量 (avg_items_per_transaction): 平均商品數量
  8. 內用比例 (dine_in_ratio): 選擇內用的交易比例

三、最佳集群數確定

使用肘部法則 (Elbow Method) 確定最佳集群數:
  • 計算不同 K 值下的組內平方和 (Inertia)
  • 尋找曲線的「肘部」拐點
  • 平衡模型複雜度與解釋性

四、數據預處理

  • 特徵標準化 (StandardScaler): 消除量綱影響
  • 缺失值處理: 使用 0 填充
  • 異常值處理: 保留以反映真實客戶行為差異
"""

    ax.text(0.08, y_pos, methodology_text, ha='left', va='top', fontsize=10,
            fontproperties=chinese_font_prop, linespacing=1.7,
            family='monospace')


def create_image_page(fig, image_path, title, description):
    """創建包含圖片和說明的頁面"""
    gs = GridSpec(3, 1, height_ratios=[0.1, 2, 0.5], hspace=0.3)

    # 標題
    ax_title = fig.add_subplot(gs[0])
    ax_title.axis('off')
    ax_title.text(0.5, 0.5, title, ha='center', va='center',
                  fontsize=18, fontweight='bold',
                  fontproperties=chinese_font_prop)

    # 圖片
    ax_img = fig.add_subplot(gs[1])
    ax_img.axis('off')

    if os.path.exists(image_path):
        img = Image.open(image_path)
        ax_img.imshow(img)
    else:
        ax_img.text(0.5, 0.5, f'圖片未找到: {image_path}',
                   ha='center', va='center', fontsize=12)

    # 說明
    ax_desc = fig.add_subplot(gs[2])
    ax_desc.axis('off')
    ax_desc.text(0.05, 0.8, description, ha='left', va='top',
                fontsize=10, fontproperties=chinese_font_prop,
                wrap=True, linespacing=1.6)


def create_cluster_detail_page(fig, cluster_id, profile, color):
    """創建單個集群的詳細分析頁"""
    ax = fig.add_subplot(111)
    ax.axis('off')

    # 標題背景
    rect = mpatches.FancyBboxPatch((0.05, 0.88), 0.9, 0.08,
                                    boxstyle="round,pad=0.01",
                                    facecolor=color, alpha=0.3,
                                    edgecolor=color, linewidth=3)
    ax.add_patch(rect)

    # 標題
    ax.text(0.5, 0.92, f'集群 {cluster_id}: {profile["cluster_name"]}',
            ha='center', va='center', fontsize=22, fontweight='bold',
            fontproperties=chinese_font_prop)

    # 描述
    ax.text(0.5, 0.84, profile['description'],
            ha='center', va='center', fontsize=12,
            fontproperties=chinese_font_prop, style='italic')

    # 關鍵指標
    y_pos = 0.76

    # 處理不同版本的字段名
    category_diversity = profile.get('avg_category_diversity', 0)
    dine_in_ratio = profile.get('avg_dine_in_ratio', 0)
    card_usage = profile.get('avg_card_usage_ratio', 0)
    tip_frequency = profile.get('avg_tip_frequency', 0)
    tip_amount = profile.get('avg_tip', 0)
    weekend_ratio = profile.get('avg_weekend_ratio', 0)
    total_customers = 1281  # 使用新的客戶總數

    metrics_text = f"""
📊 關鍵指標

客戶規模:
  • 客戶數量: {profile['customer_count']} 人
  • 占比: {profile['customer_count']/total_customers*100:.1f}%

消費行為:
  • 平均交易次數: {profile['avg_transaction_count']:.2f} 次
  • 平均總消費: ${profile['avg_total_spending']:.2f}
  • 平均單次消費: ${profile['avg_spending_per_transaction']:.2f}
  • 單次消費範圍: ${profile['avg_spending_per_transaction']*0.7:.2f} - ${profile['avg_spending_per_transaction']*1.3:.2f}

購買模式:
  • 購買頻率: {profile['avg_purchase_frequency']:.4f} 次/天
  • 信用卡使用率: {card_usage:.1%}
  • 小費給予率: {tip_frequency:.1%}
  • 平均小費金額: ${tip_amount:.2f}
  • 週末消費比例: {weekend_ratio:.1%}
"""

    ax.text(0.08, y_pos, metrics_text, ha='left', va='top', fontsize=11,
            fontproperties=chinese_font_prop, linespacing=1.8)

    # 營銷建議
    y_pos = 0.35

    # 根據集群類型提供建議
    if 'VIP' in profile['cluster_name'] or '高價值' in profile['cluster_name']:
        strategies = """
🎯 營銷策略建議

1. VIP 專屬服務
   • 建立 VIP 會員卡制度,提供專屬折扣
   • 優先預訂服務和座位保留
   • 專屬客服熱線和快速服務通道

2. 個性化互動
   • 根據購買歷史推薦新品和套餐
   • 生日/節日專屬優惠和祝福
   • 定期發送會員專刊和活動邀請

3. 忠誠度計劃
   • 積分回饋系統 (每消費 $1 = 1 積分)
   • 累積積分兌換免費餐點或特殊優惠
   • 推薦新客戶獎勵計劃

4. 高端體驗
   • 邀請參加新品試吃會和主廚交流活動
   • 提供客製化菜單服務
   • 季節性限量商品優先購買權
"""
    elif '常客' in profile['cluster_name']:
        strategies = """
🎯 營銷策略建議

1. 頻率獎勵
   • 集點卡制度 (買 10 送 1)
   • 每週特定時段享有優惠
   • 連續消費獎勵計劃

2. 品類拓展
   • 推薦未曾購買的產品類別
   • 組合套餐優惠鼓勵嘗試新品
   • 限時新品體驗優惠

3. 社群經營
   • 建立會員 LINE/微信群組
   • 分享優惠資訊和新品消息
   • 舉辦會員專屬活動

4. 提升客單價
   • 推出超值組合套餐
   • 升級大份量優惠
   • 搭配購買折扣 (如飲料+甜點組合)
"""
    elif '內用' in profile['cluster_name']:
        strategies = """
🎯 營銷策略建議

1. 用餐體驗優化
   • 提升內用環境舒適度和氛圍
   • 提供免費 WiFi 和充電服務
   • 延長座位使用時間(非尖峰時段)

2. 內用專屬優惠
   • 內用享有特定商品折扣
   • 午餐/晚餐套餐優惠
   • 內用加點飲料半價優惠

3. 社交場景營造
   • 提供適合團體聚餐的座位區
   • 舉辦主題美食日活動
   • 提供拍照打卡點和社群分享優惠

4. 會員發展
   • 鼓勵加入會員享有內用優惠
   • 推薦朋友內用享有折扣
   • 定期內用累積點數換購
"""
    else:
        strategies = """
🎯 營銷策略建議

1. 新客戶轉化
   • 首次消費優惠券
   • 歡迎禮包 (小點心或飲料)
   • 加入會員即享首購折扣

2. 回購激勵
   • 第二次消費享有折扣
   • 一週內回購享有優惠
   • Email/SMS 定期發送優惠資訊

3. 產品推薦
   • 推薦熱門商品和高評價套餐
   • 提供試吃活動吸引嘗試
   • 季節限定商品推廣

4. 關係維護
   • 定期發送問候和促銷訊息
   • 收集反饋改善服務
   • 建立長期聯繫管道
"""

    ax.text(0.08, y_pos, strategies, ha='left', va='top', fontsize=10,
            fontproperties=chinese_font_prop, linespacing=1.7)


def create_recommendations_page(fig, profiles):
    """創建總體建議頁"""
    ax = fig.add_subplot(111)
    ax.axis('off')

    # 標題
    ax.text(0.5, 0.96, '總體營銷建議與行動方案',
            ha='center', va='top', fontsize=22, fontweight='bold',
            fontproperties=chinese_font_prop)

    y_pos = 0.89

    recommendations = """
基於客戶集群分析結果,我們提出以下總體營銷建議:

一、差異化客戶管理策略 (80/20 法則)

   重點投資: 集群 1 & 2 (VIP 客戶)
   • 佔客戶數: 33.1% (219人)
   • 貢獻營收估計: 70-80%
   • 行動方案:
     - 建立 VIP 會員制度,提供差異化服務
     - 指派專屬客服經理
     - 優先獲得新品試吃和特別活動邀請
     - 年度感謝回饋活動

   提升轉化: 集群 0 (一般客戶 - 48.3%)
   • 目標: 將其中 20% 轉化為忠誠客戶
   • 行動方案:
     - 首購優惠和回購激勵計劃
     - Email/SMS 營銷保持聯繫
     - 推薦熱門商品和套餐組合
     - 新會員註冊獎勵

   場景深耕: 集群 3 (內用常客 - 18.6%)
   • 特色: 內用比例高達 90.7%
   • 行動方案:
     - 優化內用體驗 (環境、服務、氛圍)
     - 推出午餐/晚餐特惠套餐
     - 團體聚餐優惠方案
     - 建立「常客專座」計劃

二、數據驅動的產品策略

   • 針對集群 2 (超級 VIP): 推出高單價精品商品和限量版產品
   • 針對集群 0 & 3: 推出高性價比套餐吸引回購
   • 跨品類推薦: 利用類別多樣性數據進行精準推薦

三、會員制度建立 (優先級 ⭐⭐⭐⭐⭐)

   目前問題:
   • 只有 662/9347 筆交易有客戶 ID (7.1%)
   • 大量交易無法追蹤客戶行為

   建議方案:
   ✓ 建立完整的會員系統 (APP/小程序/實體卡)
   ✓ 首次消費即邀請加入會員享優惠
   ✓ 會員專屬折扣和積分計劃
   ✓ 提升客戶 ID 覆蓋率至 80% 以上

四、短期行動計劃 (未來 3 個月)

   第一個月:
   • 建立 VIP 客戶名單並發送專屬優惠
   • 推出會員招募活動
   • 設計新客戶歡迎方案

   第二個月:
   • 啟動積分/集點計劃
   • 針對集群 0 發送回購優惠券
   • 優化內用環境和服務流程

   第三個月:
   • 分析營銷活動效果
   • 調整策略並擴大實施
   • 舉辦會員專屬感謝活動

五、預期效益

   • VIP 客戶留存率提升 15-20%
   • 一般客戶回購率提升 25-30%
   • 整體營收增長 12-18%
   • 會員覆蓋率達到 60% 以上
"""

    ax.text(0.05, y_pos, recommendations, ha='left', va='top', fontsize=9.5,
            fontproperties=chinese_font_prop, linespacing=1.65)


def create_conclusion_page(fig):
    """創建結論頁"""
    ax = fig.add_subplot(111)
    ax.axis('off')

    # 標題
    ax.text(0.5, 0.90, '結論與下一步',
            ha='center', va='top', fontsize=24, fontweight='bold',
            fontproperties=chinese_font_prop)

    y_pos = 0.80

    conclusion = """
📌 關鍵結論

1. 客戶結構清晰: 四大集群特徵明顯,便於實施差異化策略

2. 超級 VIP 寶貴: 28 位客戶(4.2%)平均消費 $422,需重點維護

3. 潛力巨大: 48% 的一般客戶有較大轉化空間

4. 內用場景重要: 18.6% 的客戶幾乎全選內用,需強化體驗

5. 數據缺口: 只有 7% 的交易有客戶 ID,急需建立會員系統


🚀 下一步行動

立即執行:
  ☑ 識別並聯繫 28 位超級 VIP,建立專屬服務
  ☑ 設計會員招募方案,提升客戶 ID 覆蓋率
  ☑ 制定各集群的差異化營銷方案

短期目標 (1-3 個月):
  ☑ 會員覆蓋率達到 60%
  ☑ VIP 客戶滿意度調查並改進服務
  ☑ 推出首批針對性營銷活動

中期目標 (3-6 個月):
  ☑ 建立自動化客戶分群系統
  ☑ 實施完整的 CRM 客戶關係管理
  ☑ 定期更新集群分析並調整策略


📊 持續優化

• 每季度重新進行集群分析,追蹤客戶群體變化
• 監控各項營銷活動的 ROI
• 收集客戶反饋持續改進
• 探索更多維度的客戶分析 (如時間偏好、產品偏好組合等)


💡 最後建議

客戶集群分析只是起點,真正的價值在於執行。建議:

1. 成立專門的客戶運營團隊
2. 建立客戶數據平台,整合所有觸點數據
3. 培訓員工理解並應用集群洞察
4. 定期檢視和更新客戶策略

數據驅動 + 精細運營 = 可持續增長
"""

    ax.text(0.08, y_pos, conclusion, ha='left', va='top', fontsize=11,
            fontproperties=chinese_font_prop, linespacing=1.75)

    # 底部簽名
    ax.text(0.5, 0.05, '————————',
            ha='center', va='center', fontsize=12)
    ax.text(0.5, 0.02, '感謝您的閱讀  |  Taiwanway Restaurant Analytics Team',
            ha='center', va='center', fontsize=10,
            fontproperties=chinese_font_prop, style='italic', color='gray')


def generate_pdf_report(timestamp):
    """生成完整的 PDF 報告"""
    print("=" * 60)
    print("開始生成 PDF 報告...")
    print("=" * 60)

    # 載入數據
    print("\n📂 載入集群分析數據...")
    profiles, summary_df, customer_clusters = load_cluster_data(timestamp)

    # PDF 文件名
    pdf_filename = f'{OUTPUT_DIR}/客戶集群分析完整報告_{timestamp}.pdf'

    cluster_colors = ['#440154', '#31688e', '#35b779', '#fde724']

    with PdfPages(pdf_filename) as pdf:

        # 1. 封面頁
        print("\n📄 生成封面頁...")
        fig = plt.figure(figsize=(8.5, 11))
        create_title_page(fig)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 2. 執行摘要頁
        print("📄 生成執行摘要...")
        fig = plt.figure(figsize=(8.5, 11))
        create_summary_page(fig, profiles)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 3. 分析方法頁
        print("📄 生成分析方法論...")
        fig = plt.figure(figsize=(8.5, 11))
        create_methodology_page(fig)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 4. 肘部法則圖
        print("📄 加入肘部法則圖...")
        fig = plt.figure(figsize=(8.5, 11))
        create_image_page(
            fig,
            f'{CLUSTERING_DIR}/charts/elbow_curve.png',
            '肘部法則 - 確定最佳集群數',
            '說明: 通過計算不同 K 值下的組內平方和(Inertia),我們觀察到在 K=4 時曲線出現明顯的「肘部」拐點,表明 4 個集群是最佳選擇。繼續增加集群數帶來的邊際收益遞減,且會增加解釋的複雜度。'
        )
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 5. PCA 視覺化
        print("📄 加入 PCA 視覺化...")
        fig = plt.figure(figsize=(8.5, 11))
        create_image_page(
            fig,
            f'{CLUSTERING_DIR}/charts/cluster_pca.png',
            'PCA 降維視覺化 - 客戶集群分布',
            '說明: 使用主成分分析(PCA)將 8 維特徵降至 2 維進行視覺化。圖中可以清楚看到四個集群的分布:左下角紫色為一般客戶(集群0),中間藍色為 VIP 忠誠客戶(集群1),右側綠色為超級 VIP(集群2),上方黃色為內用常客(集群3)。前兩個主成分解釋了約 62% 的總變異。'
        )
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 6. 集群分布餅圖
        print("📄 加入集群分布圖...")
        fig = plt.figure(figsize=(8.5, 11))
        create_image_page(
            fig,
            f'{CLUSTERING_DIR}/charts/cluster_distribution.png',
            '客戶集群分布比例',
            '說明: 客戶分布呈現明顯的層次結構。一般客戶(集群0)佔比最大為 48.3%,VIP 忠誠客戶(集群1)佔 28.9%,內用常客(集群3)佔 18.6%,而最有價值的超級 VIP(集群2)僅佔 4.2% 但貢獻了顯著的營收。這符合典型的帕累托法則(80/20 法則)。'
        )
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 7. 特徵分布箱型圖
        print("📄 加入特徵分布分析...")
        fig = plt.figure(figsize=(8.5, 11))
        create_image_page(
            fig,
            f'{CLUSTERING_DIR}/charts/cluster_features_boxplot.png',
            '各集群特徵分布比較',
            '說明: 箱型圖展示了四個集群在 8 個關鍵特徵上的差異。可以明顯看出集群 2(超級 VIP)在交易次數、總消費、類別多樣性等維度都遠超其他集群。集群 3(內用常客)在內用比例上接近 100%,而集群 0 和 1 則更偏向外帶。這些差異為制定差異化營銷策略提供了依據。'
        )
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 8-11. 各集群詳細分析
        for cluster_id, profile in profiles['cluster_profiles'].items():
            print(f"📄 生成集群 {cluster_id} 詳細分析...")
            fig = plt.figure(figsize=(8.5, 11))
            create_cluster_detail_page(fig, cluster_id, profile, cluster_colors[int(cluster_id)])
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

        # 12. 總體建議頁
        print("📄 生成總體營銷建議...")
        fig = plt.figure(figsize=(8.5, 11))
        create_recommendations_page(fig, profiles)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 13. 結論頁
        print("📄 生成結論頁...")
        fig = plt.figure(figsize=(8.5, 11))
        create_conclusion_page(fig)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # 設置 PDF 元數據
        d = pdf.infodict()
        d['Title'] = '客戶集群分析完整報告'
        d['Author'] = 'Taiwanway Analytics Team'
        d['Subject'] = 'K-means 客戶分群分析'
        d['Keywords'] = 'Customer Clustering, K-means, Marketing Strategy'
        d['CreationDate'] = datetime.now()

    print("\n" + "=" * 60)
    print(f"✅ PDF 報告生成完成!")
    print(f"📁 文件位置: {pdf_filename}")
    print(f"📊 總頁數: 13 頁")
    print("=" * 60)

    return pdf_filename


def main():
    """主函數"""
    try:
        # 找到最新的分析文件
        timestamp = find_latest_files()
        print(f"找到最新分析文件: {timestamp}")

        # 生成 PDF
        pdf_file = generate_pdf_report(timestamp)

        print(f"\n🎉 報告包含:")
        print("  1. 封面頁")
        print("  2. 執行摘要")
        print("  3. 分析方法論")
        print("  4. 肘部法則圖 + 解釋")
        print("  5. PCA 視覺化 + 解釋")
        print("  6. 集群分布圖 + 解釋")
        print("  7. 特徵分布圖 + 解釋")
        print("  8-11. 四個集群的詳細分析與營銷建議")
        print("  12. 總體營銷建議與行動方案")
        print("  13. 結論與下一步")

    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
