"""
Weather Prediction Tools
========================

MCP 工具集合，供天氣預測系統 Subagents 使用。

模組:
- weather_tools: 天氣 API 工具
- holiday_tools: 假日日曆工具
- forecast_tools: 預測模型工具
- gcp_ml_tools: GCP ML 工具
"""

from .weather_tools import (
    fetch_historical_weather,
    fetch_weather_forecast,
    batch_download_weather,
)

from .holiday_tools import (
    get_us_federal_holidays,
    get_ny_school_breaks,
    get_chinese_holidays,
    calculate_days_to_holiday,
)

from .forecast_tools import (
    train_linear_model,
    predict_with_interval,
    save_model,
    load_model,
    calculate_metrics,
    cross_validate,
)

from .gcp_ml_tools import (
    upload_to_gcs,
    create_bqml_model,
    train_automl_model,
    predict_with_bqml,
    predict_with_automl,
)

__all__ = [
    # Weather
    'fetch_historical_weather',
    'fetch_weather_forecast',
    'batch_download_weather',
    # Holiday
    'get_us_federal_holidays',
    'get_ny_school_breaks',
    'get_chinese_holidays',
    'calculate_days_to_holiday',
    # Forecast
    'train_linear_model',
    'predict_with_interval',
    'save_model',
    'load_model',
    'calculate_metrics',
    'cross_validate',
    # GCP
    'upload_to_gcs',
    'create_bqml_model',
    'train_automl_model',
    'predict_with_bqml',
    'predict_with_automl',
]
