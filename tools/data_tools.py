"""
數據處理工具
負責載入、驗證和預處理 Square 支付數據。
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import pytz
import json
import logging

logger = logging.getLogger(__name__)

# 業務規則常量
NYC_TAX_RATE = 0.08875
OPERATING_DAYS = [0, 1, 4, 5]  # 週一、二、五、六
OPERATING_HOURS = (10, 20)     # 10:00-20:00
CLOSED_MONTHS = [6, 7]         # 六月、七月休息
TIMEZONE = 'America/New_York'


def load_square_data(
    file_path: str,
    file_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    載入 Square 支付數據

    參數:
        file_path: 數據檔案路徑（CSV 或 JSON）
        file_type: 檔案類型（自動偵測如未指定）

    返回:
        包含 DataFrame 和載入資訊的字典
    """
    path = Path(file_path)

    if not path.exists():
        return {
            "status": "error",
            "message": f"檔案不存在：{file_path}"
        }

    # 自動偵測檔案類型
    if file_type is None:
        file_type = path.suffix.lower().lstrip('.')

    try:
        if file_type == 'csv':
            df = pd.read_csv(path)
        elif file_type == 'json':
            df = pd.read_json(path)
        else:
            return {
                "status": "error",
                "message": f"不支援的檔案格式：{file_type}"
            }

        load_info = {
            "status": "success",
            "file_path": str(path),
            "file_type": file_type,
            "file_size_kb": path.stat().st_size / 1024,
            "rows": len(df),
            "columns": list(df.columns),
            "column_count": len(df.columns)
        }

        logger.info(f"成功載入 {len(df)} 筆記錄從 {path.name}")

        return {
            "status": "success",
            "data": df,
            "info": load_info
        }

    except Exception as e:
        logger.error(f"載入數據失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def validate_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    驗證數據品質和完整性

    參數:
        df: 輸入 DataFrame

    返回:
        驗證結果字典
    """
    validation = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "null_counts": {},
        "null_percentages": {},
        "duplicates": 0,
        "issues": [],
        "is_valid": True
    }

    # 檢查空值
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            validation["null_counts"][col] = int(count)
            validation["null_percentages"][col] = round(count / len(df) * 100, 2)

    # 檢查重複行
    validation["duplicates"] = int(df.duplicated().sum())

    # 檢查必要欄位
    required_cols = ['DateTime', 'Net Sales']
    alternative_datetime_cols = ['Date', 'Time', 'created_at']

    has_datetime = 'DateTime' in df.columns or \
                   all(col in df.columns for col in ['Date', 'Time']) or \
                   'created_at' in df.columns

    has_revenue = 'Net Sales' in df.columns or 'amount' in df.columns

    if not has_datetime:
        validation["issues"].append("缺少時間欄位（DateTime, Date/Time, 或 created_at）")
        validation["is_valid"] = False

    if not has_revenue:
        validation["issues"].append("缺少營收欄位（Net Sales 或 amount）")
        validation["is_valid"] = False

    # 計算整體缺失率
    total_cells = len(df) * len(df.columns)
    total_nulls = df.isnull().sum().sum()
    validation["overall_null_rate"] = round(total_nulls / total_cells * 100, 2)

    # 高缺失率警告
    if validation["overall_null_rate"] > 10:
        validation["issues"].append(f"數據缺失率較高（{validation['overall_null_rate']}%）")

    logger.info(f"數據驗證完成：{len(validation['issues'])} 個問題")

    return validation


def preprocess_data(
    df: pd.DataFrame,
    timezone: str = TIMEZONE,
    parse_money: bool = True,
    extract_time_components: bool = True
) -> Dict[str, Any]:
    """
    預處理 DataFrame

    參數:
        df: 輸入 DataFrame
        timezone: 目標時區
        parse_money: 是否解析金額欄位
        extract_time_components: 是否提取時間組件

    返回:
        包含預處理後 DataFrame 和處理資訊的字典
    """
    df = df.copy()
    processed = {
        "datetime_processed": False,
        "timezone_converted": False,
        "money_columns_parsed": [],
        "time_components_extracted": [],
        "rows_before": len(df),
        "rows_after": 0
    }

    try:
        # 1. 處理日期時間
        if 'Date' in df.columns and 'Time' in df.columns:
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
            processed["datetime_processed"] = True
        elif 'created_at' in df.columns:
            df['DateTime'] = pd.to_datetime(df['created_at'])
            processed["datetime_processed"] = True
        elif 'DateTime' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DateTime'])
            processed["datetime_processed"] = True

        # 2. 時區轉換
        if 'DateTime' in df.columns:
            ny_tz = pytz.timezone(timezone)

            if df['DateTime'].dt.tz is None:
                df['DateTime'] = df['DateTime'].dt.tz_localize('UTC')

            df['DateTime'] = df['DateTime'].dt.tz_convert(ny_tz)
            processed["timezone_converted"] = True
            processed["timezone"] = timezone

        # 3. 提取時間組件
        if extract_time_components and 'DateTime' in df.columns:
            df['Year'] = df['DateTime'].dt.year
            df['Month'] = df['DateTime'].dt.month
            df['Day'] = df['DateTime'].dt.day
            df['Hour'] = df['DateTime'].dt.hour
            df['DayOfWeek'] = df['DateTime'].dt.dayofweek
            df['DayName'] = df['DateTime'].dt.day_name()
            df['MonthName'] = df['DateTime'].dt.month_name()
            df['YearMonth'] = df['DateTime'].dt.to_period('M').astype(str)

            processed["time_components_extracted"] = [
                'Year', 'Month', 'Day', 'Hour',
                'DayOfWeek', 'DayName', 'MonthName', 'YearMonth'
            ]

        # 4. 解析金額欄位
        if parse_money:
            monetary_cols = ['Gross Sales', 'Net Sales', 'Tax', 'Discounts', 'Price']
            for col in monetary_cols:
                if col in df.columns:
                    df[col] = _parse_money_column(df[col])
                    processed["money_columns_parsed"].append(col)

            # 處理 amount 欄位（from API，以 cents 為單位）
            if 'amount' in df.columns:
                df['Net Sales'] = df['amount'] / 100 / (1 + NYC_TAX_RATE)
                df['Tax'] = df['amount'] / 100 - df['Net Sales']
                processed["money_columns_parsed"].extend(['Net Sales', 'Tax'])

        # 5. 解析數量欄位
        if 'Qty' in df.columns:
            df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0)

        # 6. 移除關鍵欄位缺失的行
        critical_cols = []
        if 'DateTime' in df.columns:
            critical_cols.append('DateTime')
        if 'Net Sales' in df.columns:
            critical_cols.append('Net Sales')

        if critical_cols:
            before_drop = len(df)
            df = df.dropna(subset=critical_cols)
            processed["rows_dropped"] = before_drop - len(df)

        processed["rows_after"] = len(df)
        processed["status"] = "success"

        logger.info(f"預處理完成：{processed['rows_before']} → {processed['rows_after']} 行")

        return {
            "status": "success",
            "data": df,
            "info": processed
        }

    except Exception as e:
        logger.error(f"預處理失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def filter_by_business_rules(
    df: pd.DataFrame,
    operating_days: List[int] = OPERATING_DAYS,
    operating_hours: tuple = OPERATING_HOURS,
    closed_months: List[int] = CLOSED_MONTHS,
    status_filter: Optional[str] = 'COMPLETED',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    根據業務規則過濾數據

    參數:
        df: 輸入 DataFrame
        operating_days: 營業日（0=週一, 6=週日）
        operating_hours: 營業時間範圍 (start, end)
        closed_months: 休息月份
        status_filter: 交易狀態過濾
        start_date: 開始日期
        end_date: 結束日期

    返回:
        包含過濾後 DataFrame 和過濾資訊的字典
    """
    df = df.copy()
    original_count = len(df)
    filters_applied = []

    try:
        # 1. 日期範圍過濾
        if start_date and 'DateTime' in df.columns:
            df = df[df['DateTime'] >= pd.to_datetime(start_date)]
            filters_applied.append(f"start_date >= {start_date}")

        if end_date and 'DateTime' in df.columns:
            df = df[df['DateTime'] <= pd.to_datetime(end_date)]
            filters_applied.append(f"end_date <= {end_date}")

        # 2. 營業日過濾
        if 'DayOfWeek' in df.columns and operating_days:
            df = df[df['DayOfWeek'].isin(operating_days)]
            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            days_str = ', '.join([day_names[d] for d in operating_days])
            filters_applied.append(f"營業日：{days_str}")

        # 3. 營業時間過濾
        if 'Hour' in df.columns and operating_hours:
            start_hour, end_hour = operating_hours
            df = df[(df['Hour'] >= start_hour) & (df['Hour'] < end_hour)]
            filters_applied.append(f"營業時間：{start_hour}:00-{end_hour}:00")

        # 4. 休息月份過濾
        if 'Month' in df.columns and closed_months:
            df = df[~df['Month'].isin(closed_months)]
            filters_applied.append(f"排除月份：{closed_months}")

        # 5. 交易狀態過濾
        if status_filter and 'status' in df.columns:
            df = df[df['status'] == status_filter]
            filters_applied.append(f"狀態：{status_filter}")

        filtered_count = len(df)

        filter_info = {
            "status": "success",
            "original_count": original_count,
            "filtered_count": filtered_count,
            "removed_count": original_count - filtered_count,
            "removal_rate": round((original_count - filtered_count) / original_count * 100, 2) if original_count > 0 else 0,
            "filters_applied": filters_applied
        }

        logger.info(f"過濾完成：{original_count} → {filtered_count} 行")

        return {
            "status": "success",
            "data": df,
            "info": filter_info
        }

    except Exception as e:
        logger.error(f"過濾失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def generate_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    生成數據摘要資訊

    參數:
        df: 輸入 DataFrame

    返回:
        數據摘要字典
    """
    summary = {
        "total_records": len(df),
        "columns": list(df.columns),
        "column_count": len(df.columns)
    }

    # 日期範圍
    if 'DateTime' in df.columns:
        summary["date_range"] = {
            "start": str(df['DateTime'].min()),
            "end": str(df['DateTime'].max()),
            "days": int((df['DateTime'].max() - df['DateTime'].min()).days)
        }

    # 營收摘要
    if 'Net Sales' in df.columns:
        summary["revenue_summary"] = {
            "total": round(float(df['Net Sales'].sum()), 2),
            "mean": round(float(df['Net Sales'].mean()), 2),
            "median": round(float(df['Net Sales'].median()), 2),
            "std": round(float(df['Net Sales'].std()), 2),
            "min": round(float(df['Net Sales'].min()), 2),
            "max": round(float(df['Net Sales'].max()), 2)
        }

    # 類別統計
    if 'Category' in df.columns:
        summary["categories"] = int(df['Category'].nunique())

    # 品項統計
    if 'Item' in df.columns:
        summary["items"] = int(df['Item'].nunique())

    # 交易統計
    if 'Transaction ID' in df.columns:
        summary["unique_transactions"] = int(df['Transaction ID'].nunique())

    return summary


def _parse_money_column(series: pd.Series) -> pd.Series:
    """
    解析金額欄位

    參數:
        series: 金額 Series

    返回:
        解析後的數值 Series
    """
    if series.dtype == 'object':
        # 移除 $ 和 , 符號
        series = series.str.replace('$', '', regex=False)
        series = series.str.replace(',', '', regex=False)

    return pd.to_numeric(series, errors='coerce').fillna(0)


def export_to_csv(
    df: pd.DataFrame,
    output_path: str,
    include_index: bool = False
) -> Dict[str, Any]:
    """
    匯出 DataFrame 為 CSV

    參數:
        df: 輸入 DataFrame
        output_path: 輸出路徑
        include_index: 是否包含索引

    返回:
        匯出結果字典
    """
    try:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(path, index=include_index, encoding='utf-8')

        return {
            "status": "success",
            "path": str(path),
            "rows": len(df),
            "size_kb": round(path.stat().st_size / 1024, 2)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
