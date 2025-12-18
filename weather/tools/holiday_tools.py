"""
Holiday Tools
=============

假日日曆工具，用於獲取美國聯邦假日、紐約學校假期和華人節日。
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# 嘗試導入農曆轉換庫
try:
    from lunarcalendar import Converter, Lunar
    HAS_LUNAR = True
except ImportError:
    HAS_LUNAR = False
    print("警告: lunarcalendar 未安裝，農曆轉換功能不可用")


def get_nth_weekday(year: int, month: int, weekday: int, n: int) -> datetime:
    """
    獲取某月的第 n 個星期幾

    Args:
        year: 年份
        month: 月份
        weekday: 星期幾 (0=Monday, 6=Sunday)
        n: 第幾個 (1, 2, 3, 4, -1 表示最後一個)

    Returns:
        datetime: 日期
    """
    if n > 0:
        # 從月初開始找
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        days_to_add = (weekday - first_weekday + 7) % 7 + (n - 1) * 7
        return first_day + timedelta(days=days_to_add)
    else:
        # 從月末開始找
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        last_weekday = last_day.weekday()
        days_to_sub = (last_weekday - weekday + 7) % 7 + (-n - 1) * 7
        return last_day - timedelta(days=days_to_sub)


def get_us_federal_holidays(year: int) -> List[Dict]:
    """
    獲取美國聯邦假日

    Args:
        year: 年份

    Returns:
        list: 假日列表
    """
    holidays = []

    # 固定日期假日
    fixed_holidays = [
        ("01-01", "New Year's Day", "high"),
        ("07-04", "Independence Day", "high"),
        ("11-11", "Veterans Day", "low"),
        ("12-25", "Christmas Day", "high"),
    ]

    for date_str, name, impact in fixed_holidays:
        holidays.append({
            "date": f"{year}-{date_str}",
            "holiday_name": name,
            "holiday_type": "federal",
            "impact_level": impact,
        })

    # 浮動假日
    floating_holidays = [
        # (月, 星期幾, 第幾個, 名稱, 影響程度)
        (1, 0, 3, "Martin Luther King Jr. Day", "medium"),  # 1月第3個週一
        (2, 0, 3, "Presidents' Day", "low"),                # 2月第3個週一
        (5, 0, -1, "Memorial Day", "medium"),               # 5月最後一個週一
        (9, 0, 1, "Labor Day", "medium"),                   # 9月第1個週一
        (10, 0, 2, "Columbus Day", "low"),                  # 10月第2個週一
        (11, 3, 4, "Thanksgiving", "high"),                 # 11月第4個週四
    ]

    for month, weekday, n, name, impact in floating_holidays:
        dt = get_nth_weekday(year, month, weekday, n)
        holidays.append({
            "date": dt.strftime("%Y-%m-%d"),
            "holiday_name": name,
            "holiday_type": "federal",
            "impact_level": impact,
        })

    return holidays


def get_ny_school_breaks(year: int) -> List[Dict]:
    """
    獲取紐約學校假期

    Args:
        year: 年份

    Returns:
        list: 假期列表
    """
    breaks = []

    # 寒假 (約 12/23 - 1/2)
    breaks.extend([
        {"date": f"{year-1}-12-23", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-24", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-26", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-27", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-28", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-29", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-30", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year-1}-12-31", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year}-01-01", "school_break_name": "Winter Break", "is_school_break": True},
        {"date": f"{year}-01-02", "school_break_name": "Winter Break", "is_school_break": True},
    ])

    # 二月假期 (約第3週)
    feb_break_start = get_nth_weekday(year, 2, 0, 3)  # 2月第3個週一
    for i in range(5):
        dt = feb_break_start + timedelta(days=i)
        breaks.append({
            "date": dt.strftime("%Y-%m-%d"),
            "school_break_name": "Mid-Winter Break",
            "is_school_break": True,
        })

    # 春假 (約4月中)
    spring_break_start = get_nth_weekday(year, 4, 0, 2)  # 4月第2個週一
    for i in range(5):
        dt = spring_break_start + timedelta(days=i)
        breaks.append({
            "date": dt.strftime("%Y-%m-%d"),
            "school_break_name": "Spring Break",
            "is_school_break": True,
        })

    # 暑假 (6月底 - 9月初)
    summer_start = datetime(year, 6, 26)
    summer_end = datetime(year, 9, 5)
    current = summer_start
    while current <= summer_end:
        breaks.append({
            "date": current.strftime("%Y-%m-%d"),
            "school_break_name": "Summer Break",
            "is_school_break": True,
        })
        current += timedelta(days=1)

    return breaks


def get_chinese_holidays(year: int) -> List[Dict]:
    """
    獲取華人節日 (農曆轉公曆)

    Args:
        year: 年份

    Returns:
        list: 節日列表
    """
    holidays = []

    # 預定義的農曆節日日期 (如果沒有農曆庫)
    # 這些是近幾年的實際日期
    predefined_chinese_new_year = {
        2024: "2024-02-10",
        2025: "2025-01-29",
        2026: "2026-02-17",
    }

    predefined_mid_autumn = {
        2024: "2024-09-17",
        2025: "2025-10-06",
        2026: "2026-09-25",
    }

    predefined_dragon_boat = {
        2024: "2024-06-10",
        2025: "2025-05-31",
        2026: "2026-06-19",
    }

    # 春節 (農曆正月初一，持續 15 天)
    if year in predefined_chinese_new_year:
        cny_date = datetime.strptime(predefined_chinese_new_year[year], "%Y-%m-%d")
        for i in range(15):
            dt = cny_date + timedelta(days=i)
            holidays.append({
                "date": dt.strftime("%Y-%m-%d"),
                "holiday_name": f"Chinese New Year Day {i+1}",
                "holiday_type": "chinese",
                "impact_level": "very_high" if i < 3 else "high",
            })

    # 中秋節
    if year in predefined_mid_autumn:
        holidays.append({
            "date": predefined_mid_autumn[year],
            "holiday_name": "Mid-Autumn Festival",
            "holiday_type": "chinese",
            "impact_level": "high",
        })

    # 端午節
    if year in predefined_dragon_boat:
        holidays.append({
            "date": predefined_dragon_boat[year],
            "holiday_name": "Dragon Boat Festival",
            "holiday_type": "chinese",
            "impact_level": "medium",
        })

    # 清明節 (約 4 月 4-6 日)
    holidays.append({
        "date": f"{year}-04-05",
        "holiday_name": "Qingming Festival",
        "holiday_type": "chinese",
        "impact_level": "low",
    })

    return holidays


def calculate_days_to_holiday(date: str, holidays_df: pd.DataFrame) -> int:
    """
    計算距離下一個假日的天數

    Args:
        date: 日期 (YYYY-MM-DD)
        holidays_df: 假日 DataFrame

    Returns:
        int: 天數
    """
    dt = datetime.strptime(date, "%Y-%m-%d")

    # 過濾出未來的假日
    holidays_df['date_dt'] = pd.to_datetime(holidays_df['date'])
    future_holidays = holidays_df[holidays_df['date_dt'] > dt]

    if len(future_holidays) == 0:
        return 365  # 無未來假日

    next_holiday = future_holidays['date_dt'].min()
    return (next_holiday - dt).days


def is_long_weekend(date: str, holidays_df: pd.DataFrame) -> bool:
    """
    判斷是否為連假

    Args:
        date: 日期 (YYYY-MM-DD)
        holidays_df: 假日 DataFrame

    Returns:
        bool: 是否為連假
    """
    dt = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = dt.weekday()

    # 檢查該日期是否為假日
    is_holiday = date in holidays_df['date'].values

    if not is_holiday:
        return False

    # 週五假日 → 週五六日連假
    if day_of_week == 4:
        return True

    # 週一假日 → 週六日一連假
    if day_of_week == 0:
        return True

    # 週四假日 → 可能形成 4 天連假
    if day_of_week == 3:
        return True

    return False


def generate_holiday_calendar(
    start_year: int,
    end_year: int,
    output_path: Optional[str] = None
) -> pd.DataFrame:
    """
    生成完整的假日日曆

    Args:
        start_year: 起始年份
        end_year: 結束年份
        output_path: 輸出 CSV 路徑 (可選)

    Returns:
        DataFrame: 完整日曆
    """
    all_holidays = []

    for year in range(start_year, end_year + 1):
        # 聯邦假日
        all_holidays.extend(get_us_federal_holidays(year))
        # 華人節日
        all_holidays.extend(get_chinese_holidays(year))

    # 轉換為 DataFrame
    holidays_df = pd.DataFrame(all_holidays)
    holidays_df['date'] = pd.to_datetime(holidays_df['date'])

    # 生成完整日期範圍
    date_range = pd.date_range(
        start=f"{start_year}-01-01",
        end=f"{end_year}-12-31",
        freq='D'
    )

    calendar_df = pd.DataFrame({'date': date_range})
    calendar_df['date_str'] = calendar_df['date'].dt.strftime('%Y-%m-%d')

    # 合併假日資訊
    holidays_df['date_str'] = holidays_df['date'].dt.strftime('%Y-%m-%d')
    calendar_df = calendar_df.merge(
        holidays_df[['date_str', 'holiday_name', 'holiday_type', 'impact_level']],
        on='date_str',
        how='left'
    )

    # 填入預設值
    calendar_df['is_holiday'] = calendar_df['holiday_name'].notna()
    calendar_df['holiday_type'] = calendar_df['holiday_type'].fillna('none')
    calendar_df['impact_level'] = calendar_df['impact_level'].fillna('none')

    # 學校假期
    school_breaks = []
    for year in range(start_year, end_year + 1):
        school_breaks.extend(get_ny_school_breaks(year))

    school_df = pd.DataFrame(school_breaks)
    if len(school_df) > 0:
        school_df['date_str'] = school_df['date']
        calendar_df = calendar_df.merge(
            school_df[['date_str', 'school_break_name', 'is_school_break']],
            on='date_str',
            how='left'
        )
        calendar_df['is_school_break'] = calendar_df['is_school_break'].fillna(False)
        calendar_df['school_break_name'] = calendar_df['school_break_name'].fillna('')
    else:
        calendar_df['is_school_break'] = False
        calendar_df['school_break_name'] = ''

    # 計算距離假日天數
    holiday_dates = calendar_df[calendar_df['is_holiday']]['date'].tolist()

    def calc_days_to_holiday(row):
        current_date = row['date']
        future_holidays = [h for h in holiday_dates if h > current_date]
        if future_holidays:
            return (min(future_holidays) - current_date).days
        return 365

    calendar_df['days_to_next_holiday'] = calendar_df.apply(calc_days_to_holiday, axis=1)

    # 計算是否連假
    def calc_long_weekend(row):
        if not row['is_holiday']:
            return False
        dow = row['date'].weekday()
        return dow in [0, 3, 4]  # 週一、週四、週五

    calendar_df['is_long_weekend'] = calendar_df.apply(calc_long_weekend, axis=1)

    # 整理輸出欄位
    result_df = calendar_df[[
        'date_str', 'is_holiday', 'holiday_name', 'holiday_type',
        'is_long_weekend', 'days_to_next_holiday',
        'is_school_break', 'school_break_name', 'impact_level'
    ]].copy()
    result_df.columns = [
        'date', 'is_holiday', 'holiday_name', 'holiday_type',
        'is_long_weekend', 'days_to_next_holiday',
        'is_school_break', 'school_break_name', 'impact_level'
    ]

    # 儲存 CSV
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        result_df.to_csv(output_path, index=False)
        print(f"已儲存至 {output_path}")

    return result_df


if __name__ == "__main__":
    # 測試範例
    print("測試 Holiday Tools...")

    # 測試聯邦假日
    holidays_2025 = get_us_federal_holidays(2025)
    print(f"2025 年聯邦假日: {len(holidays_2025)} 個")
    for h in holidays_2025[:3]:
        print(f"  - {h['date']}: {h['holiday_name']}")

    # 測試華人節日
    chinese_2025 = get_chinese_holidays(2025)
    print(f"2025 年華人節日: {len(chinese_2025)} 個")

    print("Holiday Tools 載入成功")
