"""
Forecast Tools
==============

預測模型工具，用於訓練、預測和驗證。
"""

import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

# scikit-learn
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import TimeSeriesSplit, cross_val_score
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.preprocessing import MinMaxScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("警告: scikit-learn 未安裝")


def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    計算 Mean Absolute Percentage Error

    Args:
        y_true: 實際值
        y_pred: 預測值

    Returns:
        float: MAPE (百分比)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    計算所有評估指標

    Args:
        y_true: 實際值
        y_pred: 預測值

    Returns:
        dict: 指標字典
    """
    if not HAS_SKLEARN:
        return {"error": "scikit-learn not installed"}

    return {
        "mape": calculate_mape(y_true, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
    }


def train_linear_model(
    X: pd.DataFrame,
    y: pd.Series,
    feature_names: Optional[List[str]] = None
) -> Tuple[Any, Dict]:
    """
    訓練線性迴歸模型

    Args:
        X: 特徵 DataFrame
        y: 目標變數
        feature_names: 特徵名稱列表

    Returns:
        tuple: (模型, 訓練資訊)
    """
    if not HAS_SKLEARN:
        raise ImportError("scikit-learn not installed")

    model = LinearRegression()
    model.fit(X, y)

    # 計算訓練指標
    y_pred = model.predict(X)
    metrics = calculate_metrics(y, y_pred)

    # 特徵係數
    if feature_names is None:
        feature_names = X.columns.tolist() if hasattr(X, 'columns') else [f"f{i}" for i in range(X.shape[1])]

    coefficients = dict(zip(feature_names, model.coef_))

    info = {
        "model_type": "LinearRegression",
        "n_features": X.shape[1],
        "n_samples": X.shape[0],
        "training_metrics": metrics,
        "coefficients": coefficients,
        "intercept": float(model.intercept_),
        "trained_at": datetime.now().isoformat(),
    }

    return model, info


def predict_with_interval(
    model: Any,
    X: pd.DataFrame,
    confidence: float = 0.95,
    residual_std: Optional[float] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    預測並計算信賴區間

    Args:
        model: 訓練好的模型
        X: 特徵 DataFrame
        confidence: 信賴水準 (預設 0.95)
        residual_std: 殘差標準差 (可選，若未提供則估計)

    Returns:
        tuple: (預測值, 下限, 上限)
    """
    from scipy import stats

    predictions = model.predict(X)

    # 估計殘差標準差
    if residual_std is None:
        residual_std = np.std(predictions) * 0.15  # 簡化估計

    # 計算信賴區間
    z = stats.norm.ppf((1 + confidence) / 2)
    lower = predictions - z * residual_std
    upper = predictions + z * residual_std

    return predictions, lower, upper


def cross_validate(
    model_class: Any,
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5
) -> Dict[str, Any]:
    """
    時間序列交叉驗證

    Args:
        model_class: 模型類別
        X: 特徵
        y: 目標
        n_splits: 分割數

    Returns:
        dict: 交叉驗證結果
    """
    if not HAS_SKLEARN:
        raise ImportError("scikit-learn not installed")

    tscv = TimeSeriesSplit(n_splits=n_splits)
    cv_results = []

    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train = X.iloc[train_idx] if hasattr(X, 'iloc') else X[train_idx]
        X_test = X.iloc[test_idx] if hasattr(X, 'iloc') else X[test_idx]
        y_train = y.iloc[train_idx] if hasattr(y, 'iloc') else y[train_idx]
        y_test = y.iloc[test_idx] if hasattr(y, 'iloc') else y[test_idx]

        model = model_class()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        metrics = calculate_metrics(y_test, y_pred)
        metrics['fold'] = fold + 1
        cv_results.append(metrics)

    # 計算統計
    mape_values = [r['mape'] for r in cv_results]
    r2_values = [r['r2'] for r in cv_results]

    return {
        "n_splits": n_splits,
        "fold_results": cv_results,
        "mape_mean": np.mean(mape_values),
        "mape_std": np.std(mape_values),
        "r2_mean": np.mean(r2_values),
        "r2_std": np.std(r2_values),
        "stability": np.std(mape_values) / np.mean(mape_values) if np.mean(mape_values) > 0 else 0,
    }


def save_model(model: Any, path: str, info: Optional[Dict] = None) -> None:
    """
    儲存模型

    Args:
        model: 模型物件
        path: 儲存路徑
        info: 模型資訊 (可選)
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'wb') as f:
        pickle.dump({'model': model, 'info': info}, f)

    print(f"模型已儲存至 {path}")


def load_model(path: str) -> Tuple[Any, Optional[Dict]]:
    """
    載入模型

    Args:
        path: 模型路徑

    Returns:
        tuple: (模型, 資訊)
    """
    with open(path, 'rb') as f:
        data = pickle.load(f)

    if isinstance(data, dict):
        return data.get('model'), data.get('info')
    else:
        return data, None


def prepare_features(
    df: pd.DataFrame,
    feature_columns: List[str],
    target_column: str
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    準備訓練和預測數據

    Args:
        df: 完整 DataFrame
        feature_columns: 特徵欄位
        target_column: 目標欄位

    Returns:
        tuple: (訓練特徵, 訓練目標, 預測特徵)
    """
    # 分離有目標和無目標的數據
    has_target = df[target_column].notna()

    train_df = df[has_target]
    predict_df = df[~has_target]

    X_train = train_df[feature_columns]
    y_train = train_df[target_column]
    X_predict = predict_df[feature_columns]

    return X_train, y_train, X_predict


def scale_features(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'minmax'
) -> Tuple[pd.DataFrame, Any]:
    """
    特徵縮放

    Args:
        df: DataFrame
        columns: 要縮放的欄位
        method: 縮放方法 ('minmax' or 'standard')

    Returns:
        tuple: (縮放後的 DataFrame, scaler)
    """
    if not HAS_SKLEARN:
        raise ImportError("scikit-learn not installed")

    df = df.copy()

    if method == 'minmax':
        scaler = MinMaxScaler()
    else:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()

    # 保留原始值
    for col in columns:
        df[f'{col}_raw'] = df[col]

    # 縮放
    df[columns] = scaler.fit_transform(df[columns])

    return df, scaler


def encode_categorical(
    df: pd.DataFrame,
    columns: List[str],
    method: str = 'onehot'
) -> pd.DataFrame:
    """
    類別編碼

    Args:
        df: DataFrame
        columns: 要編碼的欄位
        method: 編碼方法 ('onehot' or 'label')

    Returns:
        DataFrame: 編碼後的 DataFrame
    """
    df = df.copy()

    if method == 'onehot':
        df = pd.get_dummies(df, columns=columns, prefix=columns)
    else:
        from sklearn.preprocessing import LabelEncoder
        for col in columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    return df


def merge_datasets(
    weather_df: pd.DataFrame,
    holiday_df: pd.DataFrame,
    sales_df: pd.DataFrame
) -> pd.DataFrame:
    """
    合併天氣、假日、銷售數據

    Args:
        weather_df: 天氣 DataFrame
        holiday_df: 假日 DataFrame
        sales_df: 銷售 DataFrame

    Returns:
        DataFrame: 合併後的 DataFrame
    """
    # 確保日期欄位格式一致
    for df in [weather_df, holiday_df, sales_df]:
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # 以 sales 為基準 LEFT JOIN
    merged = sales_df.merge(weather_df, on='date', how='left')
    merged = merged.merge(holiday_df, on='date', how='left')

    return merged


def create_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    生成衍生特徵

    Args:
        df: 原始 DataFrame

    Returns:
        DataFrame: 含衍生特徵的 DataFrame
    """
    df = df.copy()

    # 日期轉換
    if 'date' in df.columns:
        df['date_dt'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date_dt'].dt.dayofweek
        df['month'] = df['date_dt'].dt.month
        df['day_of_month'] = df['date_dt'].dt.day

        # 季節
        def get_season(month):
            if month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            elif month in [9, 10, 11]:
                return 'Fall'
            else:
                return 'Winter'

        df['season'] = df['month'].apply(get_season)

        # 是否週末 (對於 Taiwanway: 週五六)
        df['is_weekend'] = df['day_of_week'].isin([4, 5]).astype(int)

    # 天氣特徵
    if 'temp_avg' in df.columns:
        df['temp_category'] = pd.cut(
            df['temp_avg'],
            bins=[-float('inf'), 40, 70, float('inf')],
            labels=['Cold', 'Mild', 'Hot']
        )

    if 'precipitation' in df.columns:
        df['is_rainy'] = (df['precipitation'] > 0.1).astype(int)

    if 'temp_high' in df.columns and 'temp_low' in df.columns:
        df['temp_delta'] = df['temp_high'] - df['temp_low']

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    處理缺失值

    Args:
        df: DataFrame

    Returns:
        DataFrame: 處理後的 DataFrame
    """
    df = df.copy()

    # 天氣欄位: 插值
    weather_cols = ['temp_high', 'temp_low', 'temp_avg', 'precipitation', 'humidity']
    for col in weather_cols:
        if col in df.columns:
            df[col] = df[col].interpolate(method='linear')

    # 布林欄位: 填 False
    bool_cols = ['is_holiday', 'is_long_weekend', 'is_school_break', 'is_rainy']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].fillna(False)

    # 假日欄位
    if 'holiday_type' in df.columns:
        df['holiday_type'] = df['holiday_type'].fillna('none')

    if 'days_to_next_holiday' in df.columns:
        df['days_to_next_holiday'] = df['days_to_next_holiday'].fillna(30)

    # 天氣狀況
    if 'condition' in df.columns:
        df['condition'] = df['condition'].fillna('Clear')

    return df


def get_feature_importance(
    model: Any,
    feature_names: List[str],
    top_n: int = 10
) -> List[Dict]:
    """
    獲取特徵重要性

    Args:
        model: 訓練好的模型
        feature_names: 特徵名稱
        top_n: 返回前 N 個

    Returns:
        list: 特徵重要性列表
    """
    if hasattr(model, 'coef_'):
        # 線性模型
        importance = np.abs(model.coef_)
    elif hasattr(model, 'feature_importances_'):
        # 樹模型
        importance = model.feature_importances_
    else:
        return []

    # 正規化
    importance = importance / importance.sum()

    # 排序
    sorted_idx = np.argsort(importance)[::-1]

    result = []
    for i, idx in enumerate(sorted_idx[:top_n]):
        result.append({
            "rank": i + 1,
            "feature": feature_names[idx],
            "importance": float(importance[idx]),
        })

    return result


if __name__ == "__main__":
    print("測試 Forecast Tools...")

    # 測試基本功能
    if HAS_SKLEARN:
        # 生成測試數據
        np.random.seed(42)
        X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
        })
        y = pd.Series(X['feature1'] * 2 + X['feature2'] * 3 + np.random.randn(100) * 0.1)

        # 訓練模型
        model, info = train_linear_model(X, y)
        print(f"訓練完成: R² = {info['training_metrics']['r2']:.4f}")

        # 預測
        pred, lower, upper = predict_with_interval(model, X)
        print(f"預測範圍: {pred.min():.2f} ~ {pred.max():.2f}")

    print("Forecast Tools 載入成功")
