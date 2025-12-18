"""
視覺化工具
提供圖表生成功能，支援繁體中文顯示。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# 嘗試導入 matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("matplotlib 未安裝，視覺化功能將不可用")

# 嘗試導入 seaborn
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    logger.warning("seaborn 未安裝，部分視覺化功能將受限")

# 預設輸出目錄
DEFAULT_OUTPUT_DIR = "agents/output/charts"

# 中文字體路徑（macOS）
CHINESE_FONT_PATHS = [
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    '/System/Library/Fonts/PingFang.ttc',
]


def _setup_chinese_font() -> Optional[fm.FontProperties]:
    """設置中文字體"""
    if not MATPLOTLIB_AVAILABLE:
        return None

    for font_path in CHINESE_FONT_PATHS:
        if Path(font_path).exists():
            return fm.FontProperties(fname=font_path)

    logger.warning("未找到中文字體，圖表中文可能無法正確顯示")
    return None


def _ensure_output_dir(output_dir: str) -> Path:
    """確保輸出目錄存在"""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_hourly_chart(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    title: str = "每小時銷售分析",
    figsize: Tuple[int, int] = (12, 6)
) -> Dict[str, Any]:
    """
    生成每小時銷售圖表

    參數:
        df: 包含 Hour 和 Revenue/Transactions 欄位的 DataFrame
        output_path: 輸出路徑（None 則使用預設）
        title: 圖表標題
        figsize: 圖表尺寸

    返回:
        生成結果
    """
    if not MATPLOTLIB_AVAILABLE:
        return {"status": "error", "message": "matplotlib 未安裝"}

    if 'Hour' not in df.columns:
        return {"status": "error", "message": "缺少 Hour 欄位"}

    try:
        # 設置
        plt.rcParams['text.usetex'] = False
        chinese_font = _setup_chinese_font()

        fig, ax = plt.subplots(figsize=figsize)

        # 數據準備
        if 'Avg_Daily_Revenue' in df.columns:
            hourly_data = df.groupby('Hour')['Avg_Daily_Revenue'].mean()
            ylabel = "日均營收 ($)"
        elif 'Revenue' in df.columns:
            hourly_data = df.groupby('Hour')['Revenue'].sum()
            ylabel = "總營收 ($)"
        else:
            hourly_data = df.groupby('Hour').size()
            ylabel = "交易數"

        # 繪圖
        bars = ax.bar(hourly_data.index, hourly_data.values, color='steelblue', edgecolor='white')

        # 標記尖峰時段
        peak_hour = hourly_data.idxmax()
        peak_idx = list(hourly_data.index).index(peak_hour)
        bars[peak_idx].set_color('coral')

        # 設置標籤
        if chinese_font:
            ax.set_xlabel('小時', fontproperties=chinese_font)
            ax.set_ylabel(ylabel, fontproperties=chinese_font)
            ax.set_title(title, fontproperties=chinese_font, fontsize=14)
        else:
            ax.set_xlabel('Hour')
            ax.set_ylabel(ylabel)
            ax.set_title(title, fontsize=14)

        ax.set_xticks(range(int(hourly_data.index.min()), int(hourly_data.index.max()) + 1))
        ax.grid(axis='y', alpha=0.3)

        # 添加數值標籤
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        # 保存
        if output_path is None:
            output_dir = _ensure_output_dir(DEFAULT_OUTPUT_DIR)
            output_path = output_dir / "hourly_sales.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        logger.info(f"每小時圖表已生成：{output_path}")

        return {
            "status": "success",
            "path": str(output_path),
            "peak_hour": int(peak_hour),
            "peak_value": float(hourly_data.max())
        }

    except Exception as e:
        logger.error(f"生成每小時圖表失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def generate_daily_chart(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    title: str = "每日銷售趨勢",
    figsize: Tuple[int, int] = (14, 6)
) -> Dict[str, Any]:
    """
    生成每日銷售趨勢圖

    參數:
        df: 包含 Date 和 Revenue 欄位的 DataFrame
        output_path: 輸出路徑
        title: 圖表標題
        figsize: 圖表尺寸

    返回:
        生成結果
    """
    if not MATPLOTLIB_AVAILABLE:
        return {"status": "error", "message": "matplotlib 未安裝"}

    try:
        plt.rcParams['text.usetex'] = False
        chinese_font = _setup_chinese_font()

        fig, ax = plt.subplots(figsize=figsize)

        # 數據準備
        if 'Date' in df.columns:
            df = df.sort_values('Date')
            x = pd.to_datetime(df['Date'])
        else:
            x = range(len(df))

        if 'Revenue' in df.columns:
            y = df['Revenue']
            ylabel = "營收 ($)"
        else:
            y = df.iloc[:, 1] if len(df.columns) > 1 else range(len(df))
            ylabel = "數值"

        # 繪圖
        ax.plot(x, y, marker='o', markersize=4, linewidth=2, color='steelblue')
        ax.fill_between(x, y, alpha=0.3)

        # 添加移動平均線
        if len(y) >= 7:
            ma = pd.Series(y.values).rolling(window=7).mean()
            ax.plot(x, ma, linestyle='--', color='coral', label='7日移動平均')
            ax.legend()

        # 設置標籤
        if chinese_font:
            ax.set_xlabel('日期', fontproperties=chinese_font)
            ax.set_ylabel(ylabel, fontproperties=chinese_font)
            ax.set_title(title, fontproperties=chinese_font, fontsize=14)
        else:
            ax.set_xlabel('Date')
            ax.set_ylabel(ylabel)
            ax.set_title(title, fontsize=14)

        ax.grid(alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 保存
        if output_path is None:
            output_dir = _ensure_output_dir(DEFAULT_OUTPUT_DIR)
            output_path = output_dir / "daily_trend.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        logger.info(f"每日趨勢圖已生成：{output_path}")

        return {
            "status": "success",
            "path": str(output_path)
        }

    except Exception as e:
        logger.error(f"生成每日圖表失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def generate_monthly_chart(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    title: str = "月度銷售分析",
    figsize: Tuple[int, int] = (10, 6)
) -> Dict[str, Any]:
    """
    生成月度銷售圖表

    參數:
        df: 包含 YearMonth 和 Revenue 欄位的 DataFrame
        output_path: 輸出路徑
        title: 圖表標題
        figsize: 圖表尺寸

    返回:
        生成結果
    """
    if not MATPLOTLIB_AVAILABLE:
        return {"status": "error", "message": "matplotlib 未安裝"}

    if 'YearMonth' not in df.columns:
        return {"status": "error", "message": "缺少 YearMonth 欄位"}

    try:
        plt.rcParams['text.usetex'] = False
        chinese_font = _setup_chinese_font()

        fig, ax1 = plt.subplots(figsize=figsize)

        # 數據準備
        df = df.sort_values('YearMonth')
        x = df['YearMonth'].astype(str)
        revenue = df['Revenue'] if 'Revenue' in df.columns else df.iloc[:, 1]

        # 主軸：營收柱狀圖
        bars = ax1.bar(x, revenue, color='steelblue', alpha=0.8, label='營收')

        if chinese_font:
            ax1.set_xlabel('月份', fontproperties=chinese_font)
            ax1.set_ylabel('營收 ($)', fontproperties=chinese_font, color='steelblue')
            ax1.set_title(title, fontproperties=chinese_font, fontsize=14)
        else:
            ax1.set_xlabel('Month')
            ax1.set_ylabel('Revenue ($)', color='steelblue')
            ax1.set_title(title, fontsize=14)

        ax1.tick_params(axis='y', labelcolor='steelblue')

        # 副軸：成長率
        if 'Revenue_Growth' in df.columns:
            ax2 = ax1.twinx()
            growth = df['Revenue_Growth']
            ax2.plot(x, growth, color='coral', marker='o', linewidth=2, label='成長率')
            ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

            if chinese_font:
                ax2.set_ylabel('成長率 (%)', fontproperties=chinese_font, color='coral')
            else:
                ax2.set_ylabel('Growth Rate (%)', color='coral')

            ax2.tick_params(axis='y', labelcolor='coral')

        plt.xticks(rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        # 保存
        if output_path is None:
            output_dir = _ensure_output_dir(DEFAULT_OUTPUT_DIR)
            output_path = output_dir / "monthly_sales.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        logger.info(f"月度圖表已生成：{output_path}")

        return {
            "status": "success",
            "path": str(output_path)
        }

    except Exception as e:
        logger.error(f"生成月度圖表失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def generate_heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    output_path: Optional[str] = None,
    title: str = "熱力圖",
    figsize: Tuple[int, int] = (12, 8),
    cmap: str = "YlOrRd"
) -> Dict[str, Any]:
    """
    生成熱力圖

    參數:
        df: DataFrame
        x_col: X 軸欄位
        y_col: Y 軸欄位
        value_col: 數值欄位
        output_path: 輸出路徑
        title: 圖表標題
        figsize: 圖表尺寸
        cmap: 色彩映射

    返回:
        生成結果
    """
    if not MATPLOTLIB_AVAILABLE:
        return {"status": "error", "message": "matplotlib 未安裝"}

    if x_col not in df.columns or y_col not in df.columns or value_col not in df.columns:
        return {"status": "error", "message": f"缺少必要欄位：{x_col}, {y_col}, {value_col}"}

    try:
        plt.rcParams['text.usetex'] = False
        chinese_font = _setup_chinese_font()

        # 創建樞紐表
        pivot = df.pivot_table(values=value_col, index=y_col, columns=x_col, aggfunc='mean')

        fig, ax = plt.subplots(figsize=figsize)

        if SEABORN_AVAILABLE:
            sns.heatmap(pivot, annot=True, fmt='.0f', cmap=cmap, ax=ax,
                        linewidths=0.5, cbar_kws={'label': value_col})
        else:
            im = ax.imshow(pivot.values, cmap=cmap, aspect='auto')
            plt.colorbar(im, ax=ax, label=value_col)
            ax.set_xticks(range(len(pivot.columns)))
            ax.set_yticks(range(len(pivot.index)))
            ax.set_xticklabels(pivot.columns)
            ax.set_yticklabels(pivot.index)

        if chinese_font:
            ax.set_title(title, fontproperties=chinese_font, fontsize=14)
        else:
            ax.set_title(title, fontsize=14)

        plt.tight_layout()

        # 保存
        if output_path is None:
            output_dir = _ensure_output_dir(DEFAULT_OUTPUT_DIR)
            output_path = output_dir / "heatmap.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        logger.info(f"熱力圖已生成：{output_path}")

        return {
            "status": "success",
            "path": str(output_path)
        }

    except Exception as e:
        logger.error(f"生成熱力圖失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def generate_category_chart(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    title: str = "類別銷售分析",
    figsize: Tuple[int, int] = (10, 8),
    top_n: int = 10
) -> Dict[str, Any]:
    """
    生成類別銷售圖表（橫向柱狀圖）

    參數:
        df: 包含 Category 和 Revenue/Net Sales 欄位的 DataFrame
        output_path: 輸出路徑
        title: 圖表標題
        figsize: 圖表尺寸
        top_n: 顯示前 N 個類別

    返回:
        生成結果
    """
    if not MATPLOTLIB_AVAILABLE:
        return {"status": "error", "message": "matplotlib 未安裝"}

    category_col = 'Category' if 'Category' in df.columns else None
    revenue_col = 'Net Sales' if 'Net Sales' in df.columns else ('Revenue' if 'Revenue' in df.columns else None)

    if category_col is None:
        return {"status": "error", "message": "缺少 Category 欄位"}

    try:
        plt.rcParams['text.usetex'] = False
        chinese_font = _setup_chinese_font()

        # 數據準備
        if revenue_col:
            category_data = df.groupby(category_col)[revenue_col].sum().sort_values(ascending=True)
        else:
            category_data = df[category_col].value_counts().sort_values(ascending=True)

        # 取前 N 個
        category_data = category_data.tail(top_n)

        fig, ax = plt.subplots(figsize=figsize)

        # 繪圖
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(category_data)))
        bars = ax.barh(category_data.index, category_data.values, color=colors)

        # 添加數值標籤
        for bar in bars:
            width = bar.get_width()
            label = f'${width:,.0f}' if revenue_col else f'{width:,.0f}'
            ax.annotate(label,
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0),
                        textcoords="offset points",
                        ha='left', va='center', fontsize=9)

        if chinese_font:
            ax.set_xlabel('營收 ($)' if revenue_col else '數量', fontproperties=chinese_font)
            ax.set_title(title, fontproperties=chinese_font, fontsize=14)
        else:
            ax.set_xlabel('Revenue ($)' if revenue_col else 'Count')
            ax.set_title(title, fontsize=14)

        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()

        # 保存
        if output_path is None:
            output_dir = _ensure_output_dir(DEFAULT_OUTPUT_DIR)
            output_path = output_dir / "category_sales.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        logger.info(f"類別圖表已生成：{output_path}")

        return {
            "status": "success",
            "path": str(output_path),
            "top_category": str(category_data.index[-1]),
            "top_value": float(category_data.values[-1])
        }

    except Exception as e:
        logger.error(f"生成類別圖表失敗：{str(e)}")
        return {"status": "error", "message": str(e)}
