#!/usr/bin/env python3
"""
訓練預測模型
============

使用 feature_matrix.csv 訓練三個預測模型：
1. 營收預測模型 (total_revenue)
2. 來客數預測模型 (visitor_count)
3. 便當量預測模型 (bento_estimate)
"""

import sys
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime
import json

from weather.tools.forecast_tools import (
    train_linear_model,
    cross_validate,
    save_model,
    calculate_metrics,
    get_feature_importance,
    predict_with_interval,
)
from sklearn.linear_model import LinearRegression

# 路徑設定
FEATURE_MATRIX_PATH = project_root / "weather/data/processed/feature_matrix.csv"
WEATHER_FORECAST_PATH = project_root / "weather/data/raw/weather_forecast.csv"
HOLIDAY_PATH = project_root / "weather/data/raw/holidays.csv"
MODEL_DIR = project_root / "weather/models/local"
PREDICTION_DIR = project_root / "weather/predictions"

# 確保目錄存在
MODEL_DIR.mkdir(parents=True, exist_ok=True)
PREDICTION_DIR.mkdir(parents=True, exist_ok=True)

# 特徵欄位定義
NUMERIC_FEATURES = [
    'day_of_week',
    'month',
    'is_weekend',
    'temp_avg',
    'temp_delta',
    'precipitation',
    'wind_speed',
    'weather_impact',
    'is_holiday',
    'is_long_weekend',
    'days_to_next_holiday',
    'is_school_break',
    'is_rainy',
]

# 目標變數
TARGETS = {
    'revenue': 'total_revenue',
    'visitor': 'visitor_count',
    'bento': 'bento_estimate',
}


def load_and_prepare_data():
    """載入並準備訓練數據"""
    print("=" * 60)
    print("載入特徵矩陣...")
    print("=" * 60)

    df = pd.read_csv(FEATURE_MATRIX_PATH)
    print(f"原始記錄數: {len(df)}")

    # 轉換布林值
    bool_cols = ['is_weekend', 'is_holiday', 'is_long_weekend', 'is_school_break', 'is_rainy']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)

    # 過濾有效數據（有營收的日期）
    df_train = df[df['total_revenue'].notna() & (df['total_revenue'] > 0)].copy()
    print(f"有效訓練記錄: {len(df_train)}")

    # 處理缺失值
    for col in NUMERIC_FEATURES:
        if col in df_train.columns:
            if df_train[col].isna().any():
                df_train[col] = df_train[col].fillna(df_train[col].median())

    return df_train


def train_single_model(X, y, model_name, target_name):
    """訓練單一模型"""
    print(f"\n{'─' * 40}")
    print(f"訓練 {model_name} ({target_name})")
    print(f"{'─' * 40}")

    # 訓練模型
    model, info = train_linear_model(X, y, feature_names=X.columns.tolist())

    # 交叉驗證
    cv_results = cross_validate(LinearRegression, X, y, n_splits=5)

    # 打印結果
    print(f"\n📊 訓練結果:")
    print(f"  - 樣本數: {info['n_samples']}")
    print(f"  - 特徵數: {info['n_features']}")
    print(f"\n📈 訓練指標:")
    print(f"  - R²: {info['training_metrics']['r2']:.4f}")
    print(f"  - MAPE: {info['training_metrics']['mape']:.2f}%")
    print(f"  - RMSE: {info['training_metrics']['rmse']:.2f}")

    print(f"\n🔄 交叉驗證 (5-fold):")
    print(f"  - R² (平均): {cv_results['r2_mean']:.4f} ± {cv_results['r2_std']:.4f}")
    print(f"  - MAPE (平均): {cv_results['mape_mean']:.2f}% ± {cv_results['mape_std']:.2f}%")

    # 特徵重要性
    importance = get_feature_importance(model, X.columns.tolist(), top_n=5)
    print(f"\n🏆 Top 5 重要特徵:")
    for item in importance:
        print(f"  {item['rank']}. {item['feature']}: {item['importance']:.4f}")

    # 儲存模型
    model_path = MODEL_DIR / f"{model_name}_model.pkl"
    model_info = {
        **info,
        'cross_validation': cv_results,
        'feature_importance': importance,
    }
    save_model(model, str(model_path), model_info)

    return model, model_info


def generate_future_predictions(models, model_infos):
    """生成未來 7 天預測"""
    print("\n" + "=" * 60)
    print("生成未來 7 天預測")
    print("=" * 60)

    # 載入天氣預報
    forecast_df = pd.read_csv(WEATHER_FORECAST_PATH)
    print(f"天氣預報天數: {len(forecast_df)}")

    # 載入假日數據
    holiday_df = pd.read_csv(HOLIDAY_PATH)

    # 準備預測數據
    forecast_df['date'] = pd.to_datetime(forecast_df['date'])
    forecast_df['day_of_week'] = forecast_df['date'].dt.dayofweek
    forecast_df['month'] = forecast_df['date'].dt.month
    forecast_df['is_weekend'] = forecast_df['day_of_week'].isin([4, 5]).astype(int)
    forecast_df['is_rainy'] = (forecast_df['precipitation'] > 0.1).astype(int)
    forecast_df['temp_delta'] = forecast_df['temp_high'] - forecast_df['temp_low']

    # 合併假日資訊
    holiday_df['date'] = pd.to_datetime(holiday_df['date'])
    forecast_df = forecast_df.merge(
        holiday_df[['date', 'is_holiday', 'is_long_weekend', 'days_to_next_holiday', 'is_school_break']],
        on='date',
        how='left'
    )

    # 填充缺失值
    forecast_df['is_holiday'] = forecast_df['is_holiday'].fillna(False).astype(int)
    forecast_df['is_long_weekend'] = forecast_df['is_long_weekend'].fillna(False).astype(int)
    forecast_df['is_school_break'] = forecast_df['is_school_break'].fillna(False).astype(int)
    forecast_df['days_to_next_holiday'] = forecast_df['days_to_next_holiday'].fillna(30)

    # 準備特徵
    available_features = [f for f in NUMERIC_FEATURES if f in forecast_df.columns]
    X_future = forecast_df[available_features].copy()

    # 確保所有特徵都有值
    for col in available_features:
        if X_future[col].isna().any():
            X_future[col] = X_future[col].fillna(0)

    # 生成預測
    predictions = []

    for i, row in forecast_df.iterrows():
        pred = {
            'date': row['date'].strftime('%Y-%m-%d'),
            'day_name': row['date'].strftime('%A'),
            'temp_high': row['temp_high'],
            'temp_low': row['temp_low'],
            'condition': row['condition'],
            'is_holiday': bool(row['is_holiday']),
        }

        # 預測各指標
        X_row = X_future.iloc[[i]]

        for model_name, model in models.items():
            y_pred, y_lower, y_upper = predict_with_interval(
                model, X_row,
                residual_std=model_infos[model_name]['training_metrics']['rmse']
            )
            pred[f'{model_name}_pred'] = max(0, float(y_pred[0]))
            pred[f'{model_name}_lower'] = max(0, float(y_lower[0]))
            pred[f'{model_name}_upper'] = max(0, float(y_upper[0]))

        predictions.append(pred)

    # 儲存預測結果
    predictions_df = pd.DataFrame(predictions)
    timestamp = datetime.now().strftime('%Y%m%d')
    output_path = PREDICTION_DIR / f"predictions_{timestamp}.csv"
    predictions_df.to_csv(output_path, index=False)
    print(f"\n✅ 預測結果已儲存至: {output_path}")

    # 打印預測摘要
    print("\n📅 未來 7 天預測摘要:")
    print("─" * 80)
    print(f"{'日期':<12} {'星期':<10} {'天氣':<15} {'營收':<15} {'來客':<10} {'便當':<10}")
    print("─" * 80)

    for pred in predictions:
        print(f"{pred['date']:<12} {pred['day_name']:<10} {pred['condition']:<15} "
              f"${pred['revenue_pred']:>7.0f}      {pred['visitor_pred']:>5.0f}     {pred['bento_pred']:>5.0f}")

    print("─" * 80)

    # 計算週總計
    weekly_revenue = sum(p['revenue_pred'] for p in predictions)
    weekly_visitors = sum(p['visitor_pred'] for p in predictions)
    weekly_bento = sum(p['bento_pred'] for p in predictions)

    print(f"{'週總計':<22} {'':<15} ${weekly_revenue:>7.0f}      {weekly_visitors:>5.0f}     {weekly_bento:>5.0f}")

    return predictions_df


def generate_validation_report(model_infos):
    """生成驗證報告"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'models': {}
    }

    for name, info in model_infos.items():
        report['models'][name] = {
            'target': TARGETS.get(name, name),
            'training_metrics': info['training_metrics'],
            'cross_validation': {
                'r2_mean': info['cross_validation']['r2_mean'],
                'r2_std': info['cross_validation']['r2_std'],
                'mape_mean': info['cross_validation']['mape_mean'],
                'mape_std': info['cross_validation']['mape_std'],
            },
            'top_features': info['feature_importance'][:5],
        }

    # 儲存報告
    report_path = PREDICTION_DIR / "validation_metrics.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 驗證報告已儲存至: {report_path}")

    return report


def main():
    """主程式"""
    print("\n" + "=" * 60)
    print("🚀 天氣預測模型訓練系統")
    print("=" * 60)

    # 載入數據
    df = load_and_prepare_data()

    # 準備特徵矩陣
    available_features = [f for f in NUMERIC_FEATURES if f in df.columns]
    X = df[available_features]

    print(f"\n使用特徵 ({len(available_features)} 個):")
    for f in available_features:
        print(f"  - {f}")

    # 訓練模型
    models = {}
    model_infos = {}

    # 1. 營收模型
    y_revenue = df['total_revenue']
    models['revenue'], model_infos['revenue'] = train_single_model(
        X, y_revenue, 'revenue', '營收預測'
    )

    # 2. 來客數模型
    y_visitor = df['visitor_count']
    models['visitor'], model_infos['visitor'] = train_single_model(
        X, y_visitor, 'visitor', '來客數預測'
    )

    # 3. 便當量模型
    y_bento = df['bento_estimate']
    models['bento'], model_infos['bento'] = train_single_model(
        X, y_bento, 'bento', '便當量預測'
    )

    # 生成未來預測
    predictions = generate_future_predictions(models, model_infos)

    # 生成驗證報告
    report = generate_validation_report(model_infos)

    # 總結
    print("\n" + "=" * 60)
    print("✅ 模型訓練完成！")
    print("=" * 60)
    print(f"\n📁 輸出檔案:")
    print(f"  - 營收模型: weather/models/local/revenue_model.pkl")
    print(f"  - 來客模型: weather/models/local/visitor_model.pkl")
    print(f"  - 便當模型: weather/models/local/bento_model.pkl")
    print(f"  - 預測結果: weather/predictions/predictions_{datetime.now().strftime('%Y%m%d')}.csv")
    print(f"  - 驗證報告: weather/predictions/validation_metrics.json")

    print("\n📊 模型品質摘要:")
    print("─" * 50)
    print(f"{'模型':<15} {'R²':<10} {'MAPE':<15} {'評價'}")
    print("─" * 50)

    for name, info in model_infos.items():
        r2 = info['training_metrics']['r2']
        mape = info['training_metrics']['mape']

        if mape < 15:
            rating = "✅ 優秀"
        elif mape < 20:
            rating = "🟡 良好"
        elif mape < 30:
            rating = "🟠 尚可"
        else:
            rating = "🔴 需改進"

        print(f"{name:<15} {r2:.4f}     {mape:.2f}%          {rating}")

    print("─" * 50)


if __name__ == "__main__":
    main()
