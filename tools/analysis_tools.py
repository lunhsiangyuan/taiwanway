"""
分析工具
提供銷售、客戶和財務分析功能。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from collections import Counter
import logging

logger = logging.getLogger(__name__)

# 業務規則常量
VIP_VISIT_THRESHOLD = 10
VIP_SPENDING_THRESHOLD = 200
REGULAR_VISIT_THRESHOLD = 3


# =============================================================================
# 銷售分析工具
# =============================================================================

def analyze_hourly_sales(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析每小時銷售模式

    使用日平均法避免營業日數不均的影響：
    Avg_Daily_Revenue(hour) = Sum(Revenue) / Count(unique_days)

    參數:
        df: 包含 Hour, YearMonth, Net Sales 欄位的 DataFrame

    返回:
        每小時分析結果
    """
    if 'Hour' not in df.columns:
        return {"status": "error", "message": "缺少 Hour 欄位"}

    result = {"status": "success", "data": [], "summary": {}}

    try:
        # 按月份和小時分組
        if 'YearMonth' in df.columns and 'Net Sales' in df.columns:
            # 計算每個月份-小時組合的統計
            hourly = df.groupby(['YearMonth', 'Hour']).agg({
                'Net Sales': 'sum',
                'DateTime': lambda x: x.dt.date.nunique() if hasattr(x, 'dt') else 1
            }).reset_index()

            hourly.columns = ['YearMonth', 'Hour', 'Revenue', 'Days']
            hourly['Avg_Daily_Revenue'] = hourly['Revenue'] / hourly['Days']

            # 計算交易數
            transaction_col = 'Transaction ID' if 'Transaction ID' in df.columns else None
            if transaction_col:
                trans_hourly = df.groupby(['YearMonth', 'Hour'])[transaction_col].count().reset_index()
                trans_hourly.columns = ['YearMonth', 'Hour', 'Transactions']
                hourly = hourly.merge(trans_hourly, on=['YearMonth', 'Hour'], how='left')

            result["data"] = hourly.to_dict('records')

            # 整體小時統計
            overall_hourly = df.groupby('Hour').agg({
                'Net Sales': ['sum', 'count']
            }).reset_index()
            overall_hourly.columns = ['Hour', 'Total_Revenue', 'Transactions']

            result["summary"] = {
                "busiest_hour": int(overall_hourly.loc[overall_hourly['Transactions'].idxmax(), 'Hour']),
                "highest_revenue_hour": int(overall_hourly.loc[overall_hourly['Total_Revenue'].idxmax(), 'Hour']),
                "avg_hourly_revenue": float(overall_hourly['Total_Revenue'].mean()),
                "avg_hourly_transactions": float(overall_hourly['Transactions'].mean())
            }

        logger.info(f"小時分析完成，共 {len(result['data'])} 筆資料")
        return result

    except Exception as e:
        logger.error(f"小時分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_daily_sales(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析每日銷售模式

    參數:
        df: 包含 DateTime, Net Sales 欄位的 DataFrame

    返回:
        每日分析結果
    """
    if 'DateTime' not in df.columns:
        return {"status": "error", "message": "缺少 DateTime 欄位"}

    result = {"status": "success", "data": [], "summary": {}}

    try:
        df = df.copy()
        df['Date'] = df['DateTime'].dt.date

        # 每日統計
        daily = df.groupby('Date').agg({
            'Net Sales': 'sum'
        }).reset_index()

        daily.columns = ['Date', 'Revenue']

        # 添加交易數
        if 'Transaction ID' in df.columns:
            trans_daily = df.groupby('Date')['Transaction ID'].count().reset_index()
            trans_daily.columns = ['Date', 'Transactions']
            daily = daily.merge(trans_daily, on='Date', how='left')
            daily['AOV'] = daily['Revenue'] / daily['Transactions']

        daily['Date'] = daily['Date'].astype(str)

        result["data"] = daily.to_dict('records')

        # 摘要
        result["summary"] = {
            "avg_daily_revenue": float(daily['Revenue'].mean()),
            "max_daily_revenue": float(daily['Revenue'].max()),
            "min_daily_revenue": float(daily['Revenue'].min()),
            "total_days": len(daily),
            "best_day": daily.loc[daily['Revenue'].idxmax()].to_dict(),
            "worst_day": daily.loc[daily['Revenue'].idxmin()].to_dict()
        }

        if 'Transactions' in daily.columns:
            result["summary"]["avg_daily_transactions"] = float(daily['Transactions'].mean())

        logger.info(f"每日分析完成，共 {len(daily)} 天")
        return result

    except Exception as e:
        logger.error(f"每日分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_monthly_sales(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析月度銷售趨勢

    參數:
        df: 包含 YearMonth, Net Sales 欄位的 DataFrame

    返回:
        月度分析結果
    """
    if 'YearMonth' not in df.columns:
        return {"status": "error", "message": "缺少 YearMonth 欄位"}

    result = {"status": "success", "data": [], "summary": {}}

    try:
        # 月度統計
        monthly = df.groupby('YearMonth').agg({
            'Net Sales': 'sum'
        }).reset_index()

        monthly.columns = ['YearMonth', 'Revenue']

        # 添加交易數
        if 'Transaction ID' in df.columns:
            trans_monthly = df.groupby('YearMonth')['Transaction ID'].count().reset_index()
            trans_monthly.columns = ['YearMonth', 'Transactions']
            monthly = monthly.merge(trans_monthly, on='YearMonth', how='left')
            monthly['AOV'] = monthly['Revenue'] / monthly['Transactions']

        # 計算成長率
        monthly['Revenue_Growth'] = monthly['Revenue'].pct_change() * 100
        monthly['Revenue_Growth'] = monthly['Revenue_Growth'].replace([np.inf, -np.inf], 0).fillna(0)

        result["data"] = monthly.to_dict('records')

        # 摘要
        result["summary"] = {
            "avg_monthly_revenue": float(monthly['Revenue'].mean()),
            "best_month": monthly.loc[monthly['Revenue'].idxmax()].to_dict(),
            "worst_month": monthly.loc[monthly['Revenue'].idxmin()].to_dict(),
            "total_months": len(monthly)
        }

        logger.info(f"月度分析完成，共 {len(monthly)} 個月")
        return result

    except Exception as e:
        logger.error(f"月度分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_categories(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析產品類別銷售表現

    參數:
        df: 包含 Category, Net Sales 欄位的 DataFrame

    返回:
        類別分析結果
    """
    if 'Category' not in df.columns:
        return {"status": "error", "message": "缺少 Category 欄位"}

    result = {"status": "success", "data": [], "summary": {}}

    try:
        # 類別統計
        agg_dict = {'Net Sales': 'sum'} if 'Net Sales' in df.columns else {}

        if 'Qty' in df.columns:
            agg_dict['Qty'] = 'sum'

        if 'Transaction ID' in df.columns:
            agg_dict['Transaction ID'] = 'count'

        category_stats = df.groupby('Category').agg(agg_dict).reset_index()

        # 重命名欄位
        rename_map = {'Transaction ID': 'Transactions'}
        category_stats = category_stats.rename(columns=rename_map)

        # 計算佔比
        if 'Net Sales' in category_stats.columns:
            total_revenue = category_stats['Net Sales'].sum()
            category_stats['Revenue_Share'] = (category_stats['Net Sales'] / total_revenue * 100).round(2)
            category_stats = category_stats.sort_values('Net Sales', ascending=False)

        result["data"] = category_stats.to_dict('records')

        result["summary"] = {
            "total_categories": len(category_stats),
            "top_category": category_stats.iloc[0].to_dict() if len(category_stats) > 0 else {}
        }

        logger.info(f"類別分析完成，共 {len(category_stats)} 個類別")
        return result

    except Exception as e:
        logger.error(f"類別分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_products(df: pd.DataFrame, top_n: int = 10) -> Dict[str, Any]:
    """
    分析個別產品銷售表現

    參數:
        df: 包含 Item, Net Sales 欄位的 DataFrame
        top_n: 返回前 N 名產品

    返回:
        產品分析結果
    """
    if 'Item' not in df.columns:
        return {"status": "error", "message": "缺少 Item 欄位"}

    result = {"status": "success", "top_products": [], "bottom_products": [], "summary": {}}

    try:
        # 產品統計
        agg_dict = {}

        if 'Net Sales' in df.columns:
            agg_dict['Net Sales'] = 'sum'

        if 'Qty' in df.columns:
            agg_dict['Qty'] = 'sum'

        if 'Transaction ID' in df.columns:
            agg_dict['Transaction ID'] = 'count'

        product_stats = df.groupby('Item').agg(agg_dict).reset_index()

        # 重命名欄位
        rename_map = {'Transaction ID': 'Transactions', 'Net Sales': 'Revenue'}
        product_stats = product_stats.rename(columns=rename_map)

        # 排序
        sort_col = 'Revenue' if 'Revenue' in product_stats.columns else 'Transactions'
        product_stats = product_stats.sort_values(sort_col, ascending=False)

        # 計算佔比
        if 'Revenue' in product_stats.columns:
            total_revenue = product_stats['Revenue'].sum()
            product_stats['Revenue_Share'] = (product_stats['Revenue'] / total_revenue * 100).round(2)

        # Top N 和 Bottom N
        result["top_products"] = product_stats.head(top_n).to_dict('records')
        result["bottom_products"] = product_stats.tail(top_n).to_dict('records')

        result["summary"] = {
            "total_products": len(product_stats),
            "best_seller": product_stats.iloc[0].to_dict() if len(product_stats) > 0 else {}
        }

        logger.info(f"產品分析完成，共 {len(product_stats)} 個產品")
        return result

    except Exception as e:
        logger.error(f"產品分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def identify_peak_hours(df: pd.DataFrame, top_n: int = 3) -> Dict[str, Any]:
    """
    識別尖峰時段

    參數:
        df: 包含 Hour, Net Sales 欄位的 DataFrame
        top_n: 返回前 N 個尖峰時段

    返回:
        尖峰時段資訊
    """
    if 'Hour' not in df.columns:
        return {"status": "error", "message": "缺少 Hour 欄位"}

    result = {"status": "success", "peak_traffic_hours": [], "peak_revenue_hours": []}

    try:
        # 交易量尖峰
        hourly_traffic = df.groupby('Hour').size()
        result["peak_traffic_hours"] = [
            {"hour": int(hour), "transactions": int(count)}
            for hour, count in hourly_traffic.nlargest(top_n).items()
        ]

        # 營收尖峰
        if 'Net Sales' in df.columns:
            hourly_revenue = df.groupby('Hour')['Net Sales'].sum()
            result["peak_revenue_hours"] = [
                {"hour": int(hour), "revenue": round(float(revenue), 2)}
                for hour, revenue in hourly_revenue.nlargest(top_n).items()
            ]

        logger.info(f"尖峰時段識別完成")
        return result

    except Exception as e:
        logger.error(f"尖峰時段識別失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_growth_trends(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析成長趨勢

    參數:
        df: 包含 YearMonth, Net Sales 欄位的 DataFrame

    返回:
        成長趨勢分析結果
    """
    if 'YearMonth' not in df.columns:
        return {"status": "error", "message": "缺少 YearMonth 欄位"}

    result = {"status": "success", "monthly_growth": [], "summary": {}}

    try:
        # 月度統計
        monthly = df.groupby('YearMonth').agg({
            'Net Sales': 'sum'
        }).reset_index()

        monthly.columns = ['YearMonth', 'Revenue']

        # 添加交易數
        if 'Transaction ID' in df.columns:
            trans = df.groupby('YearMonth')['Transaction ID'].count().reset_index()
            trans.columns = ['YearMonth', 'Transactions']
            monthly = monthly.merge(trans, on='YearMonth', how='left')

        # 計算成長率
        monthly['Revenue_Growth'] = monthly['Revenue'].pct_change() * 100

        if 'Transactions' in monthly.columns:
            monthly['Transaction_Growth'] = monthly['Transactions'].pct_change() * 100

        # 清理無效值
        monthly = monthly.replace([np.inf, -np.inf], 0).fillna(0)

        result["monthly_growth"] = monthly.to_dict('records')

        # 摘要
        result["summary"] = {
            "avg_revenue_growth": round(float(monthly['Revenue_Growth'].mean()), 2),
            "max_revenue_growth": round(float(monthly['Revenue_Growth'].max()), 2),
            "min_revenue_growth": round(float(monthly['Revenue_Growth'].min()), 2)
        }

        if 'Transaction_Growth' in monthly.columns:
            result["summary"]["avg_transaction_growth"] = round(float(monthly['Transaction_Growth'].mean()), 2)

        logger.info(f"成長趨勢分析完成")
        return result

    except Exception as e:
        logger.error(f"成長趨勢分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# 客戶分析工具
# =============================================================================

def analyze_customer_segments(
    df: pd.DataFrame,
    vip_visits: int = VIP_VISIT_THRESHOLD,
    vip_spending: float = VIP_SPENDING_THRESHOLD,
    regular_visits: int = REGULAR_VISIT_THRESHOLD
) -> Dict[str, Any]:
    """
    分析客戶分群

    分群條件：
    - VIP：造訪 >10 次 或 消費 >$200
    - Regular：造訪 ≥3 次
    - Occasional：造訪 <3 次

    參數:
        df: 包含 customer_id 或 Customer ID 欄位的 DataFrame
        vip_visits: VIP 造訪閾值
        vip_spending: VIP 消費閾值
        regular_visits: 常客造訪閾值

    返回:
        客戶分群結果
    """
    # 找出客戶 ID 欄位
    customer_col = None
    for col in ['customer_id', 'Customer ID', 'CustomerID']:
        if col in df.columns:
            customer_col = col
            break

    if customer_col is None:
        return {"status": "error", "message": "缺少客戶 ID 欄位"}

    result = {"status": "success", "segments": {}, "summary": {}}

    try:
        # 計算每位客戶的統計
        customer_stats = df.groupby(customer_col).agg({
            'Net Sales': 'sum'
        }).reset_index()

        # 計算造訪次數
        visit_counts = df.groupby(customer_col).size().reset_index(name='Visits')
        customer_stats = customer_stats.merge(visit_counts, on=customer_col, how='left')

        customer_stats.columns = ['CustomerID', 'Total_Spending', 'Visits']

        # 分群
        def segment_customer(row):
            if row['Visits'] > vip_visits or row['Total_Spending'] > vip_spending:
                return 'VIP'
            elif row['Visits'] >= regular_visits:
                return 'Regular'
            else:
                return 'Occasional'

        customer_stats['Segment'] = customer_stats.apply(segment_customer, axis=1)

        # 計算各分群統計
        for segment in ['VIP', 'Regular', 'Occasional']:
            segment_data = customer_stats[customer_stats['Segment'] == segment]
            result["segments"][segment.lower()] = {
                "count": len(segment_data),
                "percentage": round(len(segment_data) / len(customer_stats) * 100, 2),
                "total_revenue": round(float(segment_data['Total_Spending'].sum()), 2),
                "avg_spending": round(float(segment_data['Total_Spending'].mean()), 2) if len(segment_data) > 0 else 0,
                "avg_visits": round(float(segment_data['Visits'].mean()), 2) if len(segment_data) > 0 else 0
            }

        # 計算營收佔比
        total_revenue = customer_stats['Total_Spending'].sum()
        for segment in result["segments"]:
            result["segments"][segment]["revenue_share"] = round(
                result["segments"][segment]["total_revenue"] / total_revenue * 100, 2
            ) if total_revenue > 0 else 0

        result["summary"] = {
            "total_customers": len(customer_stats),
            "vip_count": result["segments"]["vip"]["count"],
            "vip_revenue_share": result["segments"]["vip"]["revenue_share"]
        }

        logger.info(f"客戶分群完成，共 {len(customer_stats)} 位客戶")
        return result

    except Exception as e:
        logger.error(f"客戶分群失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_dining_preferences(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析用餐偏好（內用 vs 外帶 vs 外送）

    參數:
        df: 包含 Dining Option 欄位的 DataFrame

    返回:
        用餐偏好分析結果
    """
    # 找出用餐選項欄位
    dining_col = None
    for col in ['Dining Option', 'dining_option', 'DiningOption']:
        if col in df.columns:
            dining_col = col
            break

    if dining_col is None:
        return {"status": "error", "message": "缺少用餐選項欄位"}

    result = {"status": "success", "distribution": {}, "by_hour": {}, "summary": {}}

    try:
        # 整體分布
        dining_counts = df[dining_col].value_counts()
        total = len(df)

        for option, count in dining_counts.items():
            result["distribution"][option] = {
                "count": int(count),
                "percentage": round(count / total * 100, 2)
            }

        # 按小時分析
        if 'Hour' in df.columns:
            hourly_dining = df.groupby(['Hour', dining_col]).size().unstack(fill_value=0)
            result["by_hour"] = hourly_dining.to_dict()

        result["summary"] = {
            "most_popular": dining_counts.idxmax(),
            "most_popular_percentage": round(dining_counts.max() / total * 100, 2)
        }

        logger.info(f"用餐偏好分析完成")
        return result

    except Exception as e:
        logger.error(f"用餐偏好分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# 財務分析工具
# =============================================================================

def analyze_revenue_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析營收指標

    參數:
        df: 包含 Net Sales 欄位的 DataFrame

    返回:
        營收指標分析結果
    """
    result = {"status": "success", "metrics": {}}

    try:
        if 'Net Sales' in df.columns:
            result["metrics"]["total_revenue"] = round(float(df['Net Sales'].sum()), 2)
            result["metrics"]["avg_revenue_per_transaction"] = round(float(df['Net Sales'].mean()), 2)
            result["metrics"]["median_revenue_per_transaction"] = round(float(df['Net Sales'].median()), 2)
            result["metrics"]["revenue_std"] = round(float(df['Net Sales'].std()), 2)
            result["metrics"]["min_revenue"] = round(float(df['Net Sales'].min()), 2)
            result["metrics"]["max_revenue"] = round(float(df['Net Sales'].max()), 2)

        if 'Gross Sales' in df.columns:
            result["metrics"]["total_gross_sales"] = round(float(df['Gross Sales'].sum()), 2)

        if 'Discounts' in df.columns:
            result["metrics"]["total_discounts"] = round(float(df['Discounts'].sum()), 2)

        if 'Tax' in df.columns:
            result["metrics"]["total_tax"] = round(float(df['Tax'].sum()), 2)

        # 月度營收
        if 'YearMonth' in df.columns and 'Net Sales' in df.columns:
            monthly_revenue = df.groupby('YearMonth')['Net Sales'].sum().to_dict()
            result["monthly_revenue"] = {str(k): round(v, 2) for k, v in monthly_revenue.items()}

        logger.info(f"營收指標分析完成")
        return result

    except Exception as e:
        logger.error(f"營收指標分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_transactions(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析交易統計

    參數:
        df: DataFrame

    返回:
        交易統計分析結果
    """
    result = {"status": "success", "stats": {}}

    try:
        result["stats"]["total_transactions"] = len(df)

        if 'Transaction ID' in df.columns:
            result["stats"]["unique_transactions"] = int(df['Transaction ID'].nunique())

        # 月度交易數
        if 'YearMonth' in df.columns:
            monthly_trans = df.groupby('YearMonth').size().to_dict()
            result["monthly_transactions"] = {str(k): int(v) for k, v in monthly_trans.items()}

        # 每日統計
        if 'DateTime' in df.columns:
            result["stats"]["date_range"] = {
                "start": str(df['DateTime'].min()),
                "end": str(df['DateTime'].max()),
                "days": int((df['DateTime'].max() - df['DateTime'].min()).days)
            }

            daily_trans = df.groupby(df['DateTime'].dt.date).size()
            result["stats"]["avg_daily_transactions"] = round(float(daily_trans.mean()), 2)
            result["stats"]["max_daily_transactions"] = int(daily_trans.max())
            result["stats"]["min_daily_transactions"] = int(daily_trans.min())

        logger.info(f"交易統計分析完成")
        return result

    except Exception as e:
        logger.error(f"交易統計分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_tax(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析稅務指標

    參數:
        df: 包含 Tax, Net Sales 欄位的 DataFrame

    返回:
        稅務分析結果
    """
    if 'Tax' not in df.columns:
        return {"status": "error", "message": "缺少 Tax 欄位"}

    result = {"status": "success", "tax_analysis": {}}

    try:
        result["tax_analysis"]["total_tax_collected"] = round(float(df['Tax'].sum()), 2)
        result["tax_analysis"]["avg_tax_per_transaction"] = round(float(df['Tax'].mean()), 2)

        # 有效稅率
        if 'Net Sales' in df.columns:
            total_sales = df['Net Sales'].sum()
            total_tax = df['Tax'].sum()
            if total_sales > 0:
                result["tax_analysis"]["effective_tax_rate"] = round(float((total_tax / total_sales) * 100), 2)

        # 月度稅金
        if 'YearMonth' in df.columns:
            monthly_tax = df.groupby('YearMonth')['Tax'].sum().to_dict()
            result["monthly_tax"] = {str(k): round(v, 2) for k, v in monthly_tax.items()}

        logger.info(f"稅務分析完成")
        return result

    except Exception as e:
        logger.error(f"稅務分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_aov_trends(df: pd.DataFrame) -> Dict[str, Any]:
    """
    分析平均訂單價值（AOV）趨勢

    參數:
        df: 包含 Net Sales 欄位的 DataFrame

    返回:
        AOV 趨勢分析結果
    """
    if 'Net Sales' not in df.columns:
        return {"status": "error", "message": "缺少 Net Sales 欄位"}

    result = {"status": "success", "aov_trends": {}}

    try:
        # 整體 AOV
        result["aov_trends"]["overall_aov"] = round(float(df['Net Sales'].mean()), 2)

        # 月度 AOV
        if 'YearMonth' in df.columns:
            monthly_aov = df.groupby('YearMonth')['Net Sales'].mean()
            result["aov_trends"]["monthly_aov"] = {str(k): round(v, 2) for k, v in monthly_aov.to_dict().items()}

            # AOV 成長率
            aov_growth = monthly_aov.pct_change() * 100
            result["aov_trends"]["monthly_aov_growth"] = {
                str(k): round(v, 2) for k, v in aov_growth.replace([np.inf, -np.inf], 0).fillna(0).to_dict().items()
            }

        # 星期 AOV
        if 'DayName' in df.columns:
            weekday_aov = df.groupby('DayName')['Net Sales'].mean()
            result["aov_trends"]["weekday_aov"] = {k: round(v, 2) for k, v in weekday_aov.to_dict().items()}

        # 小時 AOV
        if 'Hour' in df.columns:
            hourly_aov = df.groupby('Hour')['Net Sales'].mean()
            result["aov_trends"]["hourly_aov"] = {int(k): round(v, 2) for k, v in hourly_aov.to_dict().items()}

        logger.info(f"AOV 趨勢分析完成")
        return result

    except Exception as e:
        logger.error(f"AOV 趨勢分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def analyze_revenue_concentration(df: pd.DataFrame, pareto_threshold: int = 80) -> Dict[str, Any]:
    """
    分析營收集中度（Pareto 分析）

    參數:
        df: 包含 Item, Net Sales 欄位的 DataFrame
        pareto_threshold: Pareto 閾值（預設 80%）

    返回:
        營收集中度分析結果
    """
    if 'Item' not in df.columns or 'Net Sales' not in df.columns:
        return {"status": "error", "message": "缺少 Item 或 Net Sales 欄位"}

    result = {"status": "success", "concentration": {}}

    try:
        # 計算產品營收
        product_revenue = df.groupby('Item')['Net Sales'].sum().sort_values(ascending=False)

        if len(product_revenue) == 0:
            return {"status": "error", "message": "無產品營收數據"}

        # 累積百分比
        total_revenue = product_revenue.sum()
        cumulative_pct = product_revenue.cumsum() / total_revenue * 100

        # Pareto 分析
        pareto_products = cumulative_pct[cumulative_pct <= pareto_threshold].count() + 1
        pareto_percentage = (pareto_products / len(product_revenue)) * 100

        # Top 10 產品
        top_10 = product_revenue.head(10)
        top_10_contribution = (top_10.sum() / total_revenue) * 100

        result["concentration"] = {
            "total_products": len(product_revenue),
            "pareto_threshold": pareto_threshold,
            "pareto_products": int(pareto_products),
            "pareto_percentage": round(float(pareto_percentage), 2),
            "top_10_contribution": round(float(top_10_contribution), 2),
            "top_products": [
                {
                    "item": str(item),
                    "revenue": round(float(revenue), 2),
                    "percentage": round(float(revenue / total_revenue * 100), 2)
                }
                for item, revenue in top_10.items()
            ]
        }

        logger.info(f"營收集中度分析完成")
        return result

    except Exception as e:
        logger.error(f"營收集中度分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}
