"""
Weather Tools
=============

Open-Meteo API 工具，用於獲取歷史天氣和預報數據。

優點:
- 完全免費
- 不需要 API Key
- 支援 CSV 直接下載
- 歷史數據從 1940 年起
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# API 端點
ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_API = "https://api.open-meteo.com/v1/forecast"

# 預設位置 (New York)
DEFAULT_LAT = 40.7128
DEFAULT_LON = -74.0060
DEFAULT_TIMEZONE = "America/New_York"

# WMO 天氣代碼對照
WMO_WEATHER_CODES = {
    0: ("Clear", 0),
    1: ("Mainly Clear", -0.02),
    2: ("Partly Cloudy", -0.05),
    3: ("Overcast", -0.08),
    45: ("Fog", -0.10),
    48: ("Depositing Fog", -0.10),
    51: ("Light Drizzle", -0.10),
    53: ("Moderate Drizzle", -0.12),
    55: ("Dense Drizzle", -0.15),
    61: ("Slight Rain", -0.15),
    63: ("Moderate Rain", -0.20),
    65: ("Heavy Rain", -0.25),
    66: ("Light Freezing Rain", -0.20),
    67: ("Heavy Freezing Rain", -0.30),
    71: ("Slight Snow", -0.25),
    73: ("Moderate Snow", -0.35),
    75: ("Heavy Snow", -0.50),
    77: ("Snow Grains", -0.20),
    80: ("Slight Rain Showers", -0.15),
    81: ("Moderate Rain Showers", -0.18),
    82: ("Violent Rain Showers", -0.25),
    85: ("Slight Snow Showers", -0.30),
    86: ("Heavy Snow Showers", -0.45),
    95: ("Thunderstorm", -0.35),
    96: ("Thunderstorm with Hail", -0.40),
    99: ("Thunderstorm with Heavy Hail", -0.50),
}


def get_weather_description(code: int) -> str:
    """將 WMO 代碼轉換為天氣描述"""
    return WMO_WEATHER_CODES.get(code, ("Unknown", 0))[0]


def get_weather_impact(code: int) -> float:
    """獲取天氣對營收的影響係數"""
    return WMO_WEATHER_CODES.get(code, ("Unknown", 0))[1]


def fetch_historical_weather(
    start_date: str,
    end_date: str,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    timezone: str = DEFAULT_TIMEZONE
) -> pd.DataFrame:
    """
    獲取歷史天氣數據 (使用 Open-Meteo Archive API)

    Args:
        start_date: 起始日期 (YYYY-MM-DD)
        end_date: 結束日期 (YYYY-MM-DD)
        lat: 緯度
        lon: 經度
        timezone: 時區

    Returns:
        DataFrame: 每日天氣數據
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "rain_sum",
            "snowfall_sum",
            "wind_speed_10m_max",
            "weather_code"
        ],
        "timezone": timezone
    }

    try:
        response = requests.get(ARCHIVE_API, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        # 解析每日數據
        daily = data.get("daily", {})
        if not daily:
            print("警告：API 回傳空數據")
            return pd.DataFrame()

        df = pd.DataFrame({
            "date": daily.get("time", []),
            "temp_high": daily.get("temperature_2m_max", []),
            "temp_low": daily.get("temperature_2m_min", []),
            "temp_avg": daily.get("temperature_2m_mean", []),
            "precipitation": daily.get("precipitation_sum", []),
            "rain": daily.get("rain_sum", []),
            "snow": daily.get("snowfall_sum", []),
            "wind_speed": daily.get("wind_speed_10m_max", []),
            "weather_code": daily.get("weather_code", [])
        })

        # 添加天氣描述和影響係數
        df["condition"] = df["weather_code"].apply(get_weather_description)
        df["weather_impact"] = df["weather_code"].apply(get_weather_impact)

        # 轉換溫度從攝氏到華氏 (如果需要)
        # df["temp_high"] = df["temp_high"] * 9/5 + 32
        # df["temp_low"] = df["temp_low"] * 9/5 + 32
        # df["temp_avg"] = df["temp_avg"] * 9/5 + 32

        return df

    except requests.exceptions.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return pd.DataFrame()


def fetch_weather_forecast(
    days: int = 7,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    timezone: str = DEFAULT_TIMEZONE
) -> pd.DataFrame:
    """
    獲取未來天氣預報 (使用 Open-Meteo Forecast API)

    Args:
        days: 預報天數 (1-16)
        lat: 緯度
        lon: 經度
        timezone: 時區

    Returns:
        DataFrame: 每日預報數據
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "rain_sum",
            "snowfall_sum",
            "wind_speed_10m_max",
            "weather_code"
        ],
        "timezone": timezone,
        "forecast_days": min(days, 16)
    }

    try:
        response = requests.get(FORECAST_API, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        if not daily:
            return pd.DataFrame()

        df = pd.DataFrame({
            "date": daily.get("time", []),
            "temp_high": daily.get("temperature_2m_max", []),
            "temp_low": daily.get("temperature_2m_min", []),
            "temp_avg": [(h + l) / 2 for h, l in zip(
                daily.get("temperature_2m_max", []),
                daily.get("temperature_2m_min", [])
            )],
            "precipitation": daily.get("precipitation_sum", []),
            "rain": daily.get("rain_sum", []),
            "snow": daily.get("snowfall_sum", []),
            "wind_speed": daily.get("wind_speed_10m_max", []),
            "weather_code": daily.get("weather_code", [])
        })

        # 添加天氣描述和影響係數
        df["condition"] = df["weather_code"].apply(get_weather_description)
        df["weather_impact"] = df["weather_code"].apply(get_weather_impact)

        # 添加預測日期和信心度
        df["forecast_date"] = datetime.now().strftime("%Y-%m-%d")
        df["confidence"] = [1.0 - (i * 0.03) for i in range(len(df))]

        return df

    except requests.exceptions.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return pd.DataFrame()


def batch_download_weather(
    start_date: str,
    end_date: str,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    output_path: Optional[str] = None,
    timezone: str = DEFAULT_TIMEZONE
) -> pd.DataFrame:
    """
    批次下載歷史天氣數據

    Open-Meteo 可以一次請求整個日期範圍，不需要逐日呼叫。

    Args:
        start_date: 起始日期 (YYYY-MM-DD)
        end_date: 結束日期 (YYYY-MM-DD)
        lat: 緯度
        lon: 經度
        output_path: 輸出 CSV 路徑 (可選)
        timezone: 時區

    Returns:
        DataFrame: 歷史天氣數據
    """
    print(f"下載 {start_date} 至 {end_date} 的天氣數據...")

    df = fetch_historical_weather(start_date, end_date, lat, lon, timezone)

    if df.empty:
        print("警告：未獲取到任何數據")
        return df

    print(f"成功獲取 {len(df)} 天的天氣數據")

    # 儲存 CSV
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"已儲存至 {output_path}")

    return df


def check_existing_data(file_path: str) -> Optional[str]:
    """
    檢查現有數據的最後日期

    Args:
        file_path: CSV 檔案路徑

    Returns:
        str: 最後日期，或 None 如果檔案不存在
    """
    if not Path(file_path).exists():
        return None

    df = pd.read_csv(file_path)
    if 'date' in df.columns and len(df) > 0:
        return df['date'].max()
    return None


def update_weather_data(
    file_path: str,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    timezone: str = DEFAULT_TIMEZONE
) -> pd.DataFrame:
    """
    增量更新天氣數據

    Args:
        file_path: 現有 CSV 檔案路徑
        lat: 緯度
        lon: 經度
        timezone: 時區

    Returns:
        DataFrame: 更新後的完整數據
    """
    last_date = check_existing_data(file_path)

    if last_date:
        # 從最後日期的下一天開始
        start = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
        start_date = start.strftime("%Y-%m-%d")
    else:
        # 預設從 2024-04-01 開始
        start_date = "2024-04-01"

    # Open-Meteo 歷史數據有 5 天延遲
    end_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

    if start_date > end_date:
        print("數據已是最新")
        if Path(file_path).exists():
            return pd.read_csv(file_path)
        return pd.DataFrame()

    print(f"下載 {start_date} 至 {end_date} 的天氣數據...")

    new_data = fetch_historical_weather(start_date, end_date, lat, lon, timezone)

    if new_data.empty:
        print("未獲取到新數據")
        if Path(file_path).exists():
            return pd.read_csv(file_path)
        return pd.DataFrame()

    if Path(file_path).exists():
        existing_data = pd.read_csv(file_path)
        combined = pd.concat([existing_data, new_data], ignore_index=True)
        combined = combined.drop_duplicates(subset=['date'], keep='last')
        combined = combined.sort_values('date')
    else:
        combined = new_data

    combined.to_csv(file_path, index=False)
    print(f"已更新 {file_path}，共 {len(combined)} 筆記錄")

    return combined


def download_complete_weather(
    output_path: str = "weather/data/raw/weather_history.csv",
    start_date: str = "2024-04-01",
    include_forecast: bool = True
) -> Dict[str, pd.DataFrame]:
    """
    下載完整的天氣數據（歷史 + 預報）

    Args:
        output_path: 歷史數據輸出路徑
        start_date: 歷史數據起始日期
        include_forecast: 是否包含預報數據

    Returns:
        dict: {"history": DataFrame, "forecast": DataFrame}
    """
    result = {}

    # 下載歷史數據
    end_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    print("=" * 60)
    print("下載紐約歷史天氣數據")
    print("=" * 60)

    history = batch_download_weather(
        start_date=start_date,
        end_date=end_date,
        output_path=output_path
    )
    result["history"] = history

    # 下載預報數據
    if include_forecast:
        print("\n" + "=" * 60)
        print("下載未來 7 天天氣預報")
        print("=" * 60)

        forecast = fetch_weather_forecast(days=7)
        if not forecast.empty:
            forecast_path = output_path.replace("history", "forecast")
            Path(forecast_path).parent.mkdir(parents=True, exist_ok=True)
            forecast.to_csv(forecast_path, index=False)
            print(f"已儲存預報至 {forecast_path}")
        result["forecast"] = forecast

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Open-Meteo Weather Tools 測試")
    print("=" * 60)

    # 測試歷史天氣（最近 7 天）
    end = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d")

    print(f"\n測試歷史天氣 ({start} ~ {end})...")
    history = fetch_historical_weather(start, end)
    if not history.empty:
        print(history.head())
        print(f"\n成功獲取 {len(history)} 天歷史數據")
    else:
        print("無法獲取歷史數據")

    # 測試預報
    print("\n測試天氣預報...")
    forecast = fetch_weather_forecast(days=3)
    if not forecast.empty:
        print(forecast)
        print(f"\n成功獲取 {len(forecast)} 天預報")
    else:
        print("無法獲取預報數據")

    print("\n" + "=" * 60)
    print("Weather Tools 載入成功！")
    print("=" * 60)
