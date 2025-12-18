#!/usr/bin/env python3
"""
產生營業時間（10:00-20:00）對月份的熱力圖
X軸：營業時間（10點到晚上8點）
Y軸：月份
"""

import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 設定
OUTPUT_DIR = "../analysis_output"
DATA_DIR_HOURLY = os.path.join(OUTPUT_DIR, "data", "hourly")
CHARTS_DIR_HOURLY = os.path.join(OUTPUT_DIR, "charts", "hourly")

# 營業時間：10:00-20:00（小時 10-20）
BUSINESS_HOURS = list(range(10, 21))  # [10, 11, 12, ..., 20]

def ensure_output_dir():
    """確保輸出目錄存在"""
    os.makedirs(CHARTS_DIR_HOURLY, exist_ok=True)

def load_hourly_data():
    """載入所有月份的小時分析數據"""
    monthly_hourly_data = defaultdict(dict)
    
    # 查找所有小時分析文件
    for filename in os.listdir(DATA_DIR_HOURLY):
        if filename.startswith('hourly_analysis_') and filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR_HOURLY, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 提取月份
                if len(data) > 0:
                    month = data[0].get('month')
                    if month:
                        # 建立 hour -> revenue 的映射
                        for entry in data:
                            hour = entry.get('hour')
                            revenue = entry.get('revenue', 0.0)
                            if hour is not None:
                                monthly_hourly_data[month][hour] = revenue
                        
                        print(f"✓ 載入 {month}: {len(monthly_hourly_data[month])} 個小時的數據")
            except Exception as e:
                print(f"⚠ 讀取 {filename} 時發生錯誤: {e}")
    
    return monthly_hourly_data

def create_heatmap(monthly_hourly_data):
    """創建營業時間對月份的熱力圖"""
    # 設定中文字體
    font_path = '/System/Library/Fonts/Hiragino Sans GB.ttc'
    chinese_font_prop = None
    if os.path.exists(font_path):
        chinese_font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = [chinese_font_prop.get_name(), 'DejaVu Sans', 'Arial']
        print(f"✓ 使用中文字體: {chinese_font_prop.get_name()}")
    else:
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'STHeiti', 'Arial Unicode MS', 'DejaVu Sans', 'Arial']
    
    plt.rcParams['axes.unicode_minus'] = False
    
    # 準備數據
    months = sorted(monthly_hourly_data.keys())
    hours = BUSINESS_HOURS
    
    if len(months) == 0:
        print("⚠ 沒有數據可視覺化")
        return
    
    # 創建矩陣數據（月份 x 小時）
    data_matrix = []
    for month in months:
        month_row = []
        for hour in hours:
            revenue = monthly_hourly_data[month].get(hour, 0.0)
            month_row.append(revenue)
        data_matrix.append(month_row)
    
    data_array = np.array(data_matrix)
    
    # 創建熱力圖
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # 使用 YlOrRd 顏色映射（黃-橙-紅）
    im = ax.imshow(data_array, cmap='YlOrRd', aspect='auto', interpolation='nearest')
    
    # 設置刻度標籤
    hour_labels = [f"{h:02d}:00" for h in hours]
    ax.set_xticks(range(len(hour_labels)))
    ax.set_xticklabels(hour_labels, fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    ax.set_yticks(range(len(months)))
    ax.set_yticklabels(months, fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    # 添加數值標籤（如果數值不為0）
    for i in range(len(months)):
        for j in range(len(hours)):
            value = data_array[i, j]
            if value > 0:
                # 根據背景顏色選擇文字顏色
                text_color = "white" if value > data_array.max() * 0.5 else "black"
                text = ax.text(j, i, f'${value:.0f}',
                              ha="center", va="center", 
                              color=text_color, fontsize=9,
                              fontweight='bold' if value > data_array.max() * 0.7 else 'normal')
    
    # 設置標題和標籤
    ax.set_title('各月份營業時間消費金額熱力圖', fontsize=16, fontweight='bold',
                fontproperties=chinese_font_prop if chinese_font_prop else None, pad=20)
    ax.set_xlabel('營業時間', fontsize=14, fontproperties=chinese_font_prop if chinese_font_prop else None)
    ax.set_ylabel('月份', fontsize=14, fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    # 添加顏色條
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('消費金額 ($)', fontsize=12,
                   fontproperties=chinese_font_prop if chinese_font_prop else None)
    
    # 添加網格線（可選）
    ax.set_xticks(np.arange(len(hours)) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(months)) - 0.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5, alpha=0.3)
    ax.tick_params(which="minor", size=0)
    
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR_HOURLY, 'hourly_revenue_heatmap_by_month.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 儲存熱力圖: hourly_revenue_heatmap_by_month.png")
    plt.close()

def print_statistics(monthly_hourly_data):
    """列印統計資訊"""
    print("\n" + "=" * 60)
    print("各月份營業時間消費金額統計")
    print("=" * 60)
    
    for month in sorted(monthly_hourly_data.keys()):
        print(f"\n{month}:")
        month_data = monthly_hourly_data[month]
        total_revenue = 0.0
        for hour in BUSINESS_HOURS:
            revenue = month_data.get(hour, 0.0)
            total_revenue += revenue
            if revenue > 0:
                print(f"  {hour:02d}:00: ${revenue:.2f}")
        print(f"  營業時間總計: ${total_revenue:.2f}")

def main():
    """主函數"""
    print("=" * 60)
    print("產生營業時間對月份的熱力圖")
    print("=" * 60)
    
    ensure_output_dir()
    
    # 載入數據
    print("\n載入小時分析數據...")
    monthly_hourly_data = load_hourly_data()
    
    if len(monthly_hourly_data) == 0:
        print("⚠ 沒有找到小時分析數據")
        return
    
    # 列印統計
    print_statistics(monthly_hourly_data)
    
    # 繪製熱力圖
    print("\n繪製熱力圖...")
    create_heatmap(monthly_hourly_data)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print(f"結果儲存在: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)

if __name__ == "__main__":
    main()

