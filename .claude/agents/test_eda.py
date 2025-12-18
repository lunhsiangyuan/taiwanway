#!/usr/bin/env python3
"""
EDA Agent 測試腳本

按照 .claude/agents/eda.md 規格執行探索性數據分析：
1. 摘要統計
2. 分佈分析
3. 相關性分析
4. 離群值偵測
5. 生成圖表需求列表
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from datetime import datetime


def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """載入並預處理數據"""
    print("=" * 80)
    print("步驟 1: 數據載入與預處理")
    print("=" * 80)

    # 載入原始數據
    df = pd.read_csv(file_path)
    print(f"✅ 載入數據：{len(df)} 行, {len(df.columns)} 欄")

    # 預處理
    # 1. 只保留 COMPLETED 交易
    df = df[df['status'] == 'COMPLETED'].copy()
    print(f"✅ 過濾 COMPLETED：{len(df)} 筆交易")

    # 2. 解析時間
    df['DateTime'] = pd.to_datetime(df['created_at'], utc=True)

    # 3. 提取時間欄位
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek
    df['Month'] = df['DateTime'].dt.month
    df['YearMonth'] = df['DateTime'].dt.to_period('M')

    # 4. 計算淨營收（去除稅）
    TAX_RATE = 0.08875
    df['Net_Revenue'] = df['amount'] / (1 + TAX_RATE)

    # 5. 過濾營業日（Mon=0, Tue=1, Fri=4, Sat=5）
    operating_days = [0, 1, 4, 5]
    df = df[df['DayOfWeek'].isin(operating_days)].copy()
    print(f"✅ 過濾營業日：{len(df)} 筆交易")

    print(f"\n數據預覽：")
    print(df[['DateTime', 'Hour', 'DayOfWeek', 'YearMonth', 'Net_Revenue']].head())

    return df


def compute_summary_stats(df: pd.DataFrame, columns: list) -> dict:
    """計算摘要統計"""
    print("\n" + "=" * 80)
    print("步驟 2: 摘要統計")
    print("=" * 80)

    stats_dict = {}
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            stats_dict[col] = {
                "count": int(df[col].count()),
                "mean": round(df[col].mean(), 2),
                "std": round(df[col].std(), 2),
                "min": round(df[col].min(), 2),
                "25%": round(df[col].quantile(0.25), 2),
                "50%": round(df[col].quantile(0.50), 2),
                "75%": round(df[col].quantile(0.75), 2),
                "max": round(df[col].max(), 2)
            }

            print(f"\n{col}:")
            for k, v in stats_dict[col].items():
                print(f"  {k:8s}: {v}")

    return stats_dict


def analyze_distributions(df: pd.DataFrame, columns: list) -> dict:
    """分析數據分佈"""
    print("\n" + "=" * 80)
    print("步驟 3: 分佈分析")
    print("=" * 80)

    distributions = {}
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            data = df[col].dropna()

            # 計算偏態和峰態
            skewness = stats.skew(data)
            kurtosis = stats.kurtosis(data)

            # 常態性檢驗
            try:
                _, p_value = stats.normaltest(data)
                is_normal = p_value > 0.05
            except:
                is_normal = False
                p_value = 0.0

            # 建議轉換
            if skewness > 1:
                suggested_transform = "log"
            elif skewness < -1:
                suggested_transform = "reciprocal"
            else:
                suggested_transform = "none"

            distributions[col] = {
                "skewness": round(skewness, 2),
                "kurtosis": round(kurtosis, 2),
                "is_normal": is_normal,
                "normality_pvalue": round(p_value, 4),
                "suggested_transform": suggested_transform
            }

            print(f"\n{col}:")
            print(f"  偏態 (skewness):  {distributions[col]['skewness']}")
            print(f"  峰態 (kurtosis):  {distributions[col]['kurtosis']}")
            print(f"  常態性:           {'是' if is_normal else '否'} (p={distributions[col]['normality_pvalue']})")
            print(f"  建議轉換:         {distributions[col]['suggested_transform']}")

    return distributions


def compute_correlations(df: pd.DataFrame, columns: list) -> dict:
    """計算相關性"""
    print("\n" + "=" * 80)
    print("步驟 4: 相關性分析")
    print("=" * 80)

    # 只選數值欄位
    numeric_cols = [c for c in columns if pd.api.types.is_numeric_dtype(df[c])]
    corr_matrix = df[numeric_cols].corr()

    # 找出強相關（|r| > 0.3）
    strong_corrs = []
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            corr_val = corr_matrix.loc[col1, col2]
            if abs(corr_val) > 0.3:
                strong_corrs.append({
                    "pair": [col1, col2],
                    "value": round(corr_val, 3)
                })

    print("\n相關係數矩陣：")
    print(corr_matrix.round(3))

    print(f"\n強相關關係（|r| > 0.3）：")
    if strong_corrs:
        for corr in strong_corrs:
            print(f"  {corr['pair'][0]} ↔ {corr['pair'][1]}: {corr['value']}")
    else:
        print("  無強相關關係")

    # 轉換為可序列化格式
    matrix_dict = {}
    for col1 in numeric_cols:
        for col2 in numeric_cols:
            matrix_dict[f"{col1}_{col2}"] = round(corr_matrix.loc[col1, col2], 3)

    return {
        "matrix": matrix_dict,
        "strong_correlations": strong_corrs
    }


def detect_outliers(df: pd.DataFrame, column: str, method: str = "IQR") -> dict:
    """離群值偵測"""
    print("\n" + "=" * 80)
    print("步驟 5: 離群值偵測")
    print("=" * 80)

    data = df[column].dropna()

    if method == "IQR":
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
        outliers_df = df[outliers_mask]

        print(f"\nIQR 方法：")
        print(f"  Q1 (25%):        ${Q1:.2f}")
        print(f"  Q3 (75%):        ${Q3:.2f}")
        print(f"  IQR:             ${IQR:.2f}")
        print(f"  下界:            ${lower_bound:.2f}")
        print(f"  上界:            ${upper_bound:.2f}")

    elif method == "zscore":
        z_scores = np.abs(stats.zscore(data))
        outliers_mask = z_scores > 3
        outliers_df = df[outliers_mask]

        print(f"\nZ-score 方法（|z| > 3）：")

    outliers_count = len(outliers_df)
    outliers_pct = outliers_count / len(df) * 100

    print(f"  離群值數量:      {outliers_count}")
    print(f"  離群值比例:      {outliers_pct:.2f}%")

    # 顯示前 10 個離群值
    if outliers_count > 0:
        print(f"\n  前 10 個離群值：")
        for idx, row in outliers_df.head(10).iterrows():
            print(f"    {row['DateTime']}: ${row[column]:.2f}")

    return {
        "method": method,
        "count": outliers_count,
        "percentage": round(outliers_pct, 2),
        "indices": outliers_df.index.tolist()[:100],  # 最多 100 個
        "summary": f"發現 {outliers_count} 個離群值（{outliers_pct:.2f}%）"
    }


def generate_chart_requirements(df: pd.DataFrame, config: dict = None) -> list:
    """生成圖表需求列表"""
    print("\n" + "=" * 80)
    print("步驟 6: 生成圖表需求列表")
    print("=" * 80)

    requirements = []
    chart_id = 1

    # 圖表 1: 每小時平均營收（bar）
    if 'Hour' in df.columns and 'Net_Revenue' in df.columns:
        requirements.append({
            "chart_id": f"chart_{chart_id:03d}",
            "chart_type": "bar",
            "title": "每小時平均營收分布",
            "subtitle": "營業時間 10:00-20:00",
            "x_column": "Hour",
            "y_column": "Net_Revenue",
            "aggregation": "mean",
            "groupby": None,
            "color_by": None,
            "sort_by": "x",
            "priority": "high",
            "rationale": "識別營收高峰時段，用於人力配置優化"
        })
        print(f"✅ 圖表 {chart_id}: 每小時平均營收（bar）")
        chart_id += 1

    # 圖表 2: 營收熱力圖（heatmap）
    if 'Hour' in df.columns and 'DayOfWeek' in df.columns:
        requirements.append({
            "chart_id": f"chart_{chart_id:03d}",
            "chart_type": "heatmap",
            "title": "營收熱力圖（小時 × 星期）",
            "x_column": "Hour",
            "y_column": "DayOfWeek",
            "value_column": "Net_Revenue",
            "aggregation": "sum",
            "colormap": "YlOrRd",
            "priority": "high",
            "rationale": "識別營業高峰時段組合，發現週期性模式"
        })
        print(f"✅ 圖表 {chart_id}: 營收熱力圖（heatmap）")
        chart_id += 1

    # 圖表 3: 月度營收趨勢（line）
    if 'YearMonth' in df.columns:
        requirements.append({
            "chart_id": f"chart_{chart_id:03d}",
            "chart_type": "line",
            "title": "月度營收趨勢",
            "x_column": "YearMonth",
            "y_column": "Net_Revenue",
            "aggregation": "sum",
            "show_trend": True,
            "priority": "high",
            "rationale": "追蹤營收變化趨勢，評估業務成長"
        })
        print(f"✅ 圖表 {chart_id}: 月度營收趨勢（line）")
        chart_id += 1

    # 圖表 4: 各星期營收分布（boxplot）
    if 'DayOfWeek' in df.columns:
        requirements.append({
            "chart_id": f"chart_{chart_id:03d}",
            "chart_type": "boxplot",
            "title": "各星期營收分布",
            "x_column": "DayOfWeek",
            "y_column": "Net_Revenue",
            "priority": "medium",
            "rationale": "比較不同營業日的營收分布和離散程度"
        })
        print(f"✅ 圖表 {chart_id}: 各星期營收分布（boxplot）")
        chart_id += 1

    # 圖表 5: 交易金額分布（histogram）
    requirements.append({
        "chart_id": f"chart_{chart_id:03d}",
        "chart_type": "histogram",
        "title": "交易金額分布",
        "column": "Net_Revenue",
        "bins": 30,
        "show_kde": True,
        "priority": "medium",
        "rationale": "了解交易金額分布形狀，識別客單價模式"
    })
    print(f"✅ 圖表 {chart_id}: 交易金額分布（histogram）")
    chart_id += 1

    # 圖表 6: 各星期營收佔比（pie）
    if 'DayOfWeek' in df.columns:
        requirements.append({
            "chart_id": f"chart_{chart_id:03d}",
            "chart_type": "pie",
            "title": "各星期營收佔比",
            "labels_column": "DayOfWeek",
            "values_column": "Net_Revenue",
            "aggregation": "sum",
            "priority": "low",
            "rationale": "顯示各營業日貢獻比例"
        })
        print(f"✅ 圖表 {chart_id}: 各星期營收佔比（pie）")
        chart_id += 1

    print(f"\n總計生成 {len(requirements)} 個圖表需求")

    return requirements


def extract_insights(summary_stats: dict, distributions: dict,
                     correlations: dict, outliers: dict) -> list:
    """提取洞察"""
    print("\n" + "=" * 80)
    print("步驟 7: 提取洞察")
    print("=" * 80)

    insights = []

    # 分佈洞察
    for col, dist in distributions.items():
        if dist['skewness'] > 1:
            insights.append(f"{col} 呈右偏分佈（偏態={dist['skewness']}），存在少數高額交易")
        elif dist['skewness'] < -1:
            insights.append(f"{col} 呈左偏分佈（偏態={dist['skewness']}）")

        if not dist['is_normal']:
            insights.append(f"{col} 不符合常態分佈，建議使用 {dist['suggested_transform']} 轉換")

    # 相關性洞察
    for corr in correlations.get('strong_correlations', []):
        if corr['value'] > 0.5:
            insights.append(f"{corr['pair'][0]} 與 {corr['pair'][1]} 呈強正相關 (r={corr['value']})")
        elif corr['value'] < -0.5:
            insights.append(f"{corr['pair'][0]} 與 {corr['pair'][1]} 呈強負相關 (r={corr['value']})")
        elif abs(corr['value']) > 0.3:
            insights.append(f"{corr['pair'][0]} 與 {corr['pair'][1]} 呈中度相關 (r={corr['value']})")

    # 離群值洞察
    if outliers['percentage'] > 5:
        insights.append(f"發現 {outliers['percentage']}% 的離群值，建議進一步檢視異常交易")
    elif outliers['percentage'] > 1:
        insights.append(f"發現 {outliers['percentage']}% 的離群值，屬於正常範圍")

    # 統計洞察
    for col, stat in summary_stats.items():
        if col == 'Net_Revenue':
            cv = stat['std'] / stat['mean']  # 變異係數
            if cv > 0.5:
                insights.append(f"{col} 變異係數高（CV={cv:.2f}），表示營收波動較大")

    print("\n洞察摘要：")
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")

    return insights


def main():
    """主函數"""
    print("\n" + "=" * 80)
    print("EDA Agent 測試腳本")
    print("按照 .claude/agents/eda.md 規格執行")
    print("=" * 80)

    # 設定路徑
    data_path = "/Users/lunhsiangyuan/Desktop/square/data/all_payments/all_payments.csv"
    output_dir = Path("/Users/lunhsiangyuan/Desktop/square/.claude/agents/output/eda")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 執行分析
    df = load_and_preprocess_data(data_path)

    target_columns = ['Net_Revenue', 'Hour', 'DayOfWeek']

    summary_stats = compute_summary_stats(df, target_columns)
    distributions = analyze_distributions(df, target_columns)
    correlations = compute_correlations(df, target_columns)
    outliers = detect_outliers(df, 'Net_Revenue', method='IQR')
    chart_requirements = generate_chart_requirements(df)
    insights = extract_insights(summary_stats, distributions, correlations, outliers)

    # 組合結果
    result = {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data_summary": {
            "total_records": len(df),
            "date_range": f"{df['DateTime'].min()} ~ {df['DateTime'].max()}",
            "columns": list(df.columns)
        },
        "summary_statistics": summary_stats,
        "distributions": distributions,
        "correlations": correlations,
        "outliers": outliers,
        "chart_requirements": chart_requirements,
        "insights": insights
    }

    # 儲存結果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. 完整 JSON
    json_path = output_dir / f"eda_results_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n✅ 完整結果已儲存至：{json_path}")

    # 2. 圖表需求 JSON
    charts_path = output_dir / f"chart_requirements_{timestamp}.json"
    with open(charts_path, 'w', encoding='utf-8') as f:
        json.dump({"chart_requirements": chart_requirements}, f, ensure_ascii=False, indent=2)
    print(f"✅ 圖表需求已儲存至：{charts_path}")

    # 3. Markdown 摘要
    md_path = output_dir / f"eda_summary_{timestamp}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# EDA 分析摘要\n\n")
        f.write(f"**分析時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**數據範圍**: {len(df)} 筆交易\n\n")

        f.write("## 摘要統計\n\n")
        for col, stat in summary_stats.items():
            f.write(f"### {col}\n\n")
            f.write(f"- 數量: {stat['count']}\n")
            f.write(f"- 平均: ${stat['mean']:.2f}\n")
            f.write(f"- 標準差: ${stat['std']:.2f}\n")
            f.write(f"- 最小值: ${stat['min']:.2f}\n")
            f.write(f"- 中位數: ${stat['50%']:.2f}\n")
            f.write(f"- 最大值: ${stat['max']:.2f}\n\n")

        f.write("## 分佈分析\n\n")
        for col, dist in distributions.items():
            f.write(f"### {col}\n\n")
            f.write(f"- 偏態: {dist['skewness']}\n")
            f.write(f"- 峰態: {dist['kurtosis']}\n")
            f.write(f"- 常態性: {'是' if dist['is_normal'] else '否'}\n")
            f.write(f"- 建議轉換: {dist['suggested_transform']}\n\n")

        f.write("## 洞察\n\n")
        for i, insight in enumerate(insights, 1):
            f.write(f"{i}. {insight}\n")

        f.write(f"\n## 圖表需求\n\n")
        f.write(f"總計 {len(chart_requirements)} 個圖表需求：\n\n")
        for req in chart_requirements:
            f.write(f"- **{req['chart_id']}** ({req['priority']}): {req['title']}\n")
            f.write(f"  - 類型: {req['chart_type']}\n")
            f.write(f"  - 理由: {req['rationale']}\n\n")

    print(f"✅ Markdown 摘要已儲存至：{md_path}")

    # 顯示完整 JSON 結果
    print("\n" + "=" * 80)
    print("完整 JSON 結果")
    print("=" * 80)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    print("\n" + "=" * 80)
    print("EDA 測試完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
