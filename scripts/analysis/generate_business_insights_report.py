#!/usr/bin/env python3
"""
以營運顧問視角，將 Square 支付紀錄整併分析並輸出 HTML 互動報告。

遵循專案全域 AGENTS.md 指南：
- 語言：繁體中文（技術名詞保留英文）
- 報告：輸出至 reports/，檔名含時間戳記 report_YYYYMMDD_HHMMSS.html
- 結構：container/header/main 響應式版面
- 可視化：使用 Plotly 產生互動圖表
- 記錄：將分析過程寫入 logs/ 檔案

資料來源（會自動偵測是否存在）：
- data/all_payments/all_payments.csv（部分欄位為分/cent）
- data/all_payments/all_payments.json（包含 processing_fee，可估計手續費）
- data/2025_08_11/taiwanway_payments.csv（金額為美元）

輸出內容：
- KPI 總覽（總營收、交易數、平均客單、Tip 率、退款率、營業天數、日均）
- 月度趨勢、週間分佈、時段分佈、時段×週間熱力圖
- 支付結構（Entry Method、Card Brand）
- 具體營運建議（人力、餐期、品項與組合、促銷與會員、資料治理）
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import pytz
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


# -----------------------------
# 基本設定與常數
# -----------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
LOGS_DIR = ROOT / "logs"
TEMP_DIR = ROOT / "temp"

NY_TZ = pytz.timezone("America/New_York")

# 營業日（可依需求調整）：週一、週二、週五、週六
BUSINESS_DAYS = {0, 1, 4, 5}  # Monday=0 ... Sunday=6


def ensure_dirs():
    """確保必要的資料夾存在。"""
    for d in [REPORTS_DIR, LOGS_DIR, TEMP_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def setup_logging() -> Path:
    """設定 logging 並回傳日誌檔案路徑。"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"analysis_{ts}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.info("Logging initialized: %s", log_path)
    return log_path


# -----------------------------
# 輔助：金額解析與時間處理
# -----------------------------
def _to_float(val) -> Optional[float]:
    """嘗試將值轉為 float，失敗回傳 None。"""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        s = str(val).strip()
        if s == "" or s.lower() == "nan":
            return None
        # 移除可能的逗號
        s = s.replace(",", "")
        return float(s)
    except Exception:
        return None


def parse_money_auto(series: pd.Series) -> pd.Series:
    """自動判斷金額單位（美元或分）並轉為美元 float。

    規則（保守版）：
    - 只要樣本中出現小數點（如 "12.34"），視為「已是美元」；
    - 否則一律視為「分（cent）」再除以 100。

    設計理由：Square 匯出常見情境為整數分或小數美元，
    避免因平均值閾值造成誤判（例如 603 分被誤判為 603 美元）。
    """
    # 先嘗試轉 float
    s = series.map(_to_float)
    if s.dropna().empty:
        return s

    has_decimal_like = any("." in str(v) for v in series.head(200))
    if has_decimal_like:
        return s
    return s / 100.0


def to_local_dt(iso_utc: str) -> Optional[datetime]:
    """ISO UTC（含Z）字串轉為紐約時區 datetime。"""
    if not iso_utc:
        return None
    try:
        dt_utc = datetime.fromisoformat(str(iso_utc).replace("Z", "+00:00"))
        return dt_utc.astimezone(NY_TZ)
    except Exception:
        return None


# -----------------------------
# 讀取與整併資料
# -----------------------------
def load_all_payments_csv(csv_path: Path) -> pd.DataFrame:
    """讀取 data/all_payments/all_payments.csv（部分欄位為分）。"""
    df = pd.read_csv(csv_path)
    df.rename(columns=lambda c: c.strip(), inplace=True)

    # 金額欄位處理
    for col in ["amount", "tip", "total_amount", "approved_amount", "refunded_amount"]:
        if col in df.columns:
            df[col] = parse_money_auto(df[col])
        else:
            df[col] = np.nan

    # 時間處理
    df["local_dt"] = df["created_at"].map(to_local_dt)
    df = df[df["local_dt"].notna()].copy()
    df["date"] = df["local_dt"].dt.date
    df["hour"] = df["local_dt"].dt.hour
    df["dow"] = df["local_dt"].dt.weekday
    df["month"] = df["local_dt"].dt.strftime("%Y-%m")

    # 費用不可用（CSV 無 processing_fee），以 NaN 表示
    df["fee"] = np.nan

    # 欄位對齊
    for col in ["entry_method", "card_brand", "card_type", "source_type", "status"]:
        if col not in df.columns:
            df[col] = None

    df["id"] = df.get("id")
    return df


def load_taiwanway_2025_csv(csv_path: Path) -> pd.DataFrame:
    """讀取 data/2025_08_11/taiwanway_payments.csv（金額已為美元）。"""
    df = pd.read_csv(csv_path)
    df.rename(columns=lambda c: c.strip(), inplace=True)

    for col in ["amount", "tip", "total_amount", "approved_amount"]:
        if col in df.columns:
            df[col] = parse_money_auto(df[col])  # 應為美元，不會被除以100（函式會自動判斷）
        else:
            df[col] = np.nan

    if "refunded_amount" not in df.columns:
        df["refunded_amount"] = np.nan

    df["local_dt"] = df["created_at"].map(to_local_dt)
    df = df[df["local_dt"].notna()].copy()
    df["date"] = df["local_dt"].dt.date
    df["hour"] = df["local_dt"].dt.hour
    df["dow"] = df["local_dt"].dt.weekday
    df["month"] = df["local_dt"].dt.strftime("%Y-%m")
    df["fee"] = np.nan

    for col in ["entry_method", "card_brand", "card_type", "source_type", "status"]:
        if col not in df.columns:
            df[col] = None

    df["id"] = df.get("id")
    return df


def load_all_payments_json(json_path: Path) -> pd.DataFrame:
    """讀取 data/all_payments/all_payments.json，含 processing_fee。"""
    with open(json_path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    payments = obj.get("payments", [])
    rows = []
    for p in payments:
        try:
            created_at = p.get("created_at")
            local_dt = to_local_dt(created_at)
            if not local_dt:
                continue
            amount = _to_float(p.get("amount_money", {}).get("amount"))
            tip = _to_float(p.get("tip_money", {}).get("amount"))
            total = _to_float(p.get("total_money", {}).get("amount"))
            approved = _to_float(p.get("approved_money", {}).get("amount"))

            # 以分為單位，轉美元
            amount = (amount or 0.0) / 100.0
            tip = (tip or 0.0) / 100.0
            total = (total or 0.0) / 100.0
            approved = (approved or 0.0) / 100.0

            # 手續費：加總 processing_fee 陣列
            fee_cents = 0.0
            for pf in p.get("processing_fee", []) or []:
                fee_cents += _to_float(pf.get("amount_money", {}).get("amount")) or 0.0
            fee = fee_cents / 100.0

            card_details = p.get("card_details", {}) or {}
            card = card_details.get("card", {}) or {}

            rows.append(
                {
                    "id": p.get("id"),
                    "created_at": created_at,
                    "status": p.get("status"),
                    "source_type": p.get("source_type"),
                    "entry_method": card_details.get("entry_method"),
                    "card_brand": card.get("card_brand"),
                    "card_type": card.get("card_type"),
                    "amount": amount,
                    "tip": tip,
                    "total_amount": total,
                    "approved_amount": approved,
                    "refunded_amount": np.nan,  # JSON此處無直接提供
                    "local_dt": local_dt,
                    "date": local_dt.date(),
                    "hour": local_dt.hour,
                    "dow": local_dt.weekday(),
                    "month": local_dt.strftime("%Y-%m"),
                    "fee": fee,
                }
            )
        except Exception as e:
            logging.exception("JSON payment parse error: %s", e)
    return pd.DataFrame(rows)


def load_all_sources() -> pd.DataFrame:
    """讀取並整併所有可用來源。"""
    frames: List[pd.DataFrame] = []

    csv1 = DATA_DIR / "all_payments" / "all_payments.csv"
    if csv1.exists():
        logging.info("Loading CSV: %s", csv1)
        frames.append(load_all_payments_csv(csv1))
    else:
        logging.warning("Missing: %s", csv1)

    json1 = DATA_DIR / "all_payments" / "all_payments.json"
    if json1.exists():
        logging.info("Loading JSON: %s", json1)
        frames.append(load_all_payments_json(json1))
    else:
        logging.warning("Missing: %s", json1)

    csv2 = DATA_DIR / "2025_08_11" / "taiwanway_payments.csv"
    if csv2.exists():
        logging.info("Loading CSV: %s", csv2)
        frames.append(load_taiwanway_2025_csv(csv2))
    else:
        logging.warning("Missing: %s", csv2)

    if not frames:
        raise FileNotFoundError("未找到任何支付資料來源。")

    df = pd.concat(frames, ignore_index=True, sort=False)
    # 以 id + created_at 去重
    df.sort_values(by=["created_at"], inplace=True)
    df.drop_duplicates(subset=["id", "created_at"], keep="last", inplace=True)
    df.reset_index(drop=True, inplace=True)
    logging.info("Unified payments: %d rows", len(df))
    return df


# -----------------------------
# 指標計算
# -----------------------------
@dataclass
class KPI:
    total_txn: int
    gross_revenue: float
    tip_revenue: float
    tip_rate: float
    avg_order_value: float
    refunds: float
    days_active: int
    avg_daily_revenue: float
    est_net_revenue: Optional[float]  # 以 processing_fee 估算，若缺則 None


def compute_kpi(df: pd.DataFrame) -> KPI:
    df_ok = df.copy()
    df_ok = df_ok[df_ok.get("status", "COMPLETED") == "COMPLETED"]

    total_txn = len(df_ok)
    amt = df_ok["amount"].fillna(0.0)
    tip = df_ok["tip"].fillna(0.0)
    total = df_ok["total_amount"].fillna(0.0)
    refunds = df_ok.get("refunded_amount", pd.Series([0.0] * len(df_ok))).fillna(0.0)

    gross_revenue = float(total.sum()) if total.sum() > 0 else float(amt.sum() + tip.sum())
    tip_revenue = float(tip.sum())
    denom_for_tip = float(amt.sum()) if amt.sum() > 0 else max(gross_revenue - tip_revenue, 1e-9)
    tip_rate = tip_revenue / denom_for_tip if denom_for_tip > 0 else 0.0
    avg_order_value = gross_revenue / total_txn if total_txn else 0.0
    total_refunds = float(refunds.sum())
    days_active = df_ok["date"].nunique()
    avg_daily_revenue = gross_revenue / days_active if days_active else 0.0

    # 估算淨收入（若有 fee）
    fee_series = df_ok.get("fee")
    est_net_revenue = None
    if fee_series is not None and fee_series.notna().any():
        est_net_revenue = gross_revenue - float(fee_series.fillna(0.0).sum())

    return KPI(
        total_txn=total_txn,
        gross_revenue=round(gross_revenue, 2),
        tip_revenue=round(tip_revenue, 2),
        tip_rate=round(tip_rate, 4),
        avg_order_value=round(avg_order_value, 2),
        refunds=round(total_refunds, 2),
        days_active=int(days_active),
        avg_daily_revenue=round(avg_daily_revenue, 2),
        est_net_revenue=round(est_net_revenue, 2) if est_net_revenue is not None else None,
    )


def summary_by_month(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("month").agg(
        txn=("id", "count"),
        revenue=("total_amount", "sum"),
        tip=("tip", "sum"),
    )
    g = g.sort_index()
    g["aov"] = g["revenue"] / g["txn"]
    return g.reset_index()


def summary_by_dow(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("dow").agg(
        txn=("id", "count"),
        revenue=("total_amount", "sum"),
    )
    g["dow_name"] = g.index.map(["週一", "週二", "週三", "週四", "週五", "週六", "週日"].__getitem__)
    g = g.sort_index()
    return g.reset_index(drop=True)


def summary_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("hour").agg(
        txn=("id", "count"),
        revenue=("total_amount", "sum"),
    )
    g = g.sort_index()
    g["aov"] = g["revenue"] / g["txn"]
    return g.reset_index()


def heatmap_dow_hour(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["dow", "hour"]).agg(revenue=("total_amount", "sum")).reset_index()
    # 轉換成 Pivot：rows=dow, cols=hour，並補齊所有小時與星期
    pivot = g.pivot(index="dow", columns="hour", values="revenue").fillna(0.0)
    # 補齊 0..6 與 0..23
    pivot = pivot.reindex(index=range(7), fill_value=0.0)
    pivot = pivot.reindex(columns=range(24), fill_value=0.0)
    pivot.index = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    return pivot


def payment_structure(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    entry = (
        df.groupby("entry_method")["id"].count().sort_values(ascending=False).reset_index(name="count")
    )
    brand = (
        df.groupby("card_brand")["id"].count().sort_values(ascending=False).reset_index(name="count")
    )
    return entry, brand


# -----------------------------
# 視覺化（Plotly）
# -----------------------------
def fig_monthly_revenue(df_month: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_month,
        x="month",
        y="revenue",
        text_auto=".2s",
        title="月度營收趨勢",
        labels={"month": "月份", "revenue": "營收 (USD)"},
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig


def fig_dow_revenue(df_dow: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_dow,
        x="dow_name",
        y="revenue",
        text_auto=".2s",
        title="週間營收分佈",
        labels={"dow_name": "星期", "revenue": "營收 (USD)"},
        color="dow_name",
    )
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=60, b=20))
    return fig


def fig_hour_revenue(df_hour: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df_hour,
        x="hour",
        y="revenue",
        markers=True,
        title="時段營收分佈",
        labels={"hour": "小時", "revenue": "營收 (USD)"},
    )
    fig.update_layout(xaxis=dict(dtick=1), margin=dict(l=20, r=20, t=60, b=20))
    return fig


def fig_heatmap(pivot: pd.DataFrame) -> go.Figure:
    fig = px.imshow(
        pivot.values,
        x=list(range(24)),
        y=list(pivot.index),
        color_continuous_scale="Greens",
        labels=dict(x="小時", y="星期", color="營收"),
        title="週間×時段 營收熱力圖",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig


def fig_pie_entry(entry_df: pd.DataFrame) -> go.Figure:
    fig = px.pie(entry_df, names="entry_method", values="count", title="支付方式（Entry Method）占比")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def fig_brand_bar(brand_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(brand_df, x="card_brand", y="count", title="Card Brand 分佈", text_auto=True)
    fig.update_layout(xaxis_title="Card Brand", yaxis_title="交易數")
    return fig


# -----------------------------
# 報告輸出（HTML）
# -----------------------------
def build_html_report(
    kpi: KPI,
    df_month: pd.DataFrame,
    df_dow: pd.DataFrame,
    df_hour: pd.DataFrame,
    heatmap_df: pd.DataFrame,
    entry_df: pd.DataFrame,
    brand_df: pd.DataFrame,
    data_links: List[Tuple[str, str]],
) -> str:
    """組裝完整 HTML（含 Plotly 互動圖表）。"""
    # 產生圖表 HTML 片段
    figs = [
        fig_monthly_revenue(df_month),
        fig_dow_revenue(df_dow),
        fig_hour_revenue(df_hour),
        fig_heatmap(heatmap_df),
        fig_pie_entry(entry_df),
        fig_brand_bar(brand_df),
    ]
    fig_htmls = [
        pio.to_html(fig, include_plotlyjs=False, full_html=False, default_height="480px") for fig in figs
    ]

    # 下載連結（若存在）
    links_html = "".join(
        f'<li><a href="{href}" download>{label}</a></li>' for label, href in data_links
    )

    ts_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 注意：外部載入 Plotly CDN，確保互動
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Taiwanway 營運洞察報告</title>
  <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
  <style>
    :root {{ --bg:#0b0c0f; --fg:#111; --card:#fff; --muted:#6b7280; --primary:#0ea5e9; --accent:#22c55e; }}
    body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft JhengHei",sans-serif; background:#f3f4f6; color:#111; }}
    .container {{ max-width:1200px; margin:0 auto; padding:16px; }}
    header {{ background:white; position:sticky; top:0; z-index:10; border-bottom:1px solid #e5e7eb; }}
    header .inner {{ max-width:1200px; margin:0 auto; padding:16px; display:flex; align-items:center; justify-content:space-between; }}
    header h1 {{ margin:0; font-size:20px; }}
    main {{ padding:16px; }}
    .grid {{ display:grid; grid-template-columns:1fr; gap:16px; }}
    @media (min-width: 900px) {{ .grid-2 {{ grid-template-columns:1fr 1fr; }} }}
    .card {{ background:white; border:1px solid #e5e7eb; border-radius:10px; box-shadow:0 1px 2px rgba(0,0,0,0.04); overflow:hidden; }}
    .card header {{ background:linear-gradient(90deg, rgba(34,197,94,0.1), rgba(14,165,233,0.1)); padding:12px 16px; border-bottom:1px solid #e5e7eb; }}
    .card h2 {{ margin:0; font-size:16px; }}
    .card .body {{ padding:16px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:12px; }}
    @media (min-width: 900px) {{ .kpis {{ grid-template-columns:repeat(4, minmax(0,1fr)); }} }}
    .kpi {{ background:#f8fafc; padding:12px; border-radius:8px; border:1px solid #e5e7eb; }}
    .kpi .label {{ color:#6b7280; font-size:12px; }}
    .kpi .value {{ font-weight:700; font-size:20px; }}
    ul.links {{ margin:0; padding-left:18px; }}
    footer {{ color:#6b7280; font-size:12px; padding:24px 0; text-align:center; }}
  </style>
  <!-- 容器/header/main 結構 -->
</head>
<body>
  <header>
    <div class="inner">
      <h1>Taiwanway 營運洞察報告</h1>
      <div class="time">生成時間：{ts_human}</div>
    </div>
  </header>
  <div class="container">
    <main>
      <section class="card">
        <header><h2>指標總覽</h2></header>
        <div class="body">
          <div class="kpis">
            <div class="kpi"><div class="label">總營收</div><div class="value">${kpi.gross_revenue:,.2f}</div></div>
            <div class="kpi"><div class="label">交易數</div><div class="value">{kpi.total_txn:,d}</div></div>
            <div class="kpi"><div class="label">平均客單價</div><div class="value">${kpi.avg_order_value:,.2f}</div></div>
            <div class="kpi"><div class="label">日均營收</div><div class="value">${kpi.avg_daily_revenue:,.2f}</div></div>
            <div class="kpi"><div class="label">小費金額</div><div class="value">${kpi.tip_revenue:,.2f}</div></div>
            <div class="kpi"><div class="label">小費率（Tip/銷售）</div><div class="value">{kpi.tip_rate*100:.1f}%</div></div>
            <div class="kpi"><div class="label">退款金額</div><div class="value">${kpi.refunds:,.2f}</div></div>
            <div class="kpi"><div class="label">營業天數</div><div class="value">{kpi.days_active:d}</div></div>
          </div>
          {f'<p style="margin-top:8px;color:#6b7280">（含手續費估算之淨營收：約 ${kpi.est_net_revenue:,.2f}）</p>' if kpi.est_net_revenue is not None else ''}
        </div>
      </section>

      <section class="grid grid-2" style="margin-top:16px;">
        <div class="card"><header><h2>月度營收趨勢</h2></header><div class="body">{fig_htmls[0]}</div></div>
        <div class="card"><header><h2>週間營收分佈</h2></header><div class="body">{fig_htmls[1]}</div></div>
        <div class="card"><header><h2>時段營收分佈</h2></header><div class="body">{fig_htmls[2]}</div></div>
        <div class="card"><header><h2>週間×時段 熱力圖</h2></header><div class="body">{fig_htmls[3]}</div></div>
      </section>

      <section class="grid grid-2" style="margin-top:16px;">
        <div class="card"><header><h2>支付方式占比（Entry Method）</h2></header><div class="body">{fig_htmls[4]}</div></div>
        <div class="card"><header><h2>Card Brand 分佈</h2></header><div class="body">{fig_htmls[5]}</div></div>
      </section>

      <section class="card" style="margin-top:16px;">
        <header><h2>資料下載</h2></header>
        <div class="body">
          <ul class="links">{links_html}</ul>
          <p style="color:#6b7280; font-size:12px; margin-top:8px;">提示：部分來源不含手續費/退款欄位，金額解讀以報表說明為準。</p>
        </div>
      </section>

      <section class="card" style="margin-top:16px;">
        <header><h2>營運建議（依據目前營收紀錄）</h2></header>
        <div class="body">
          <ol style="margin:0; padding-left:18px; line-height:1.6;">
            <li><b>餐期與人力排班：</b>強化高峰時段（通常為傍晚至晚餐前後）的前場點單與後場出餐人力，於低谷時段（如平日下午）安排備料與訓練。</li>
            <li><b>提高客單價（AOV）：</b>設計<b>牛肉麵/滷肉飯 + 珍奶</b>的固定價位<b>Combo</b>，並於點餐介面（Square Register）預設推薦，促進加購。</li>
            <li><b>尖離峰價格與促銷：</b>週一/週二與下午 2–5 點可導入限時優惠（第二杯半價、學生證 10% off），拉抬離峰銷量與翻桌率。</li>
            <li><b>小費策略：</b>在無壓迫感的前提下，於 Contactless/EMV 付款畫面提供清楚的<b>15/18/20%</b>快捷選項與文案（例：支持家庭小店），目前小費率約 <b>{kpi.tip_rate*100:.1f}%</b> 尚可、仍有提升空間。</li>
            <li><b>支付體驗優化：</b>CONTACTLESS 佔比較高時，確保讀卡機位置與站位動線順暢；若 EMV 比例偏高且尖峰排隊，建議增設第二台終端或優化收銀流程。</li>
            <li><b>菜單工程：</b>依據毛利與動銷將品項分為 <i>Stars</i>/<i>Plowhorses</i>/<i>Puzzles</i>/<i>Dogs</i>；目前無品項明細，建議於 Square Catalog 綁定類別，後續導出明細分析。</li>
            <li><b>營業時段調整：</b>若上午/午後長期低谷，可考慮週末延後關門或特定日提前開門，並配合社群宣傳與 Google 商家同步。</li>
            <li><b>社群與社區合作：</b>針對附近學校/社區活動推出團體訂購與預訂折扣，主打 <b>珍奶 + 台式熱食</b>的一站式體驗。</li>
            <li><b>資料治理：</b>持續下載 Payments 與 Orders Itemization，補齊<b>費用（processing_fee）</b>與<b>品項</b>資料；另可串接 <b>Settlements</b> 估算實際入帳。</li>
          </ol>
        </div>
      </section>

    </main>
    <footer>© {datetime.now().year} Taiwanway — 內部營運報告（保密）</footer>
  </div>
</body>
</html>
"""
    return html


def main():
    ensure_dirs()
    log_path = setup_logging()
    logging.info("Project root: %s", ROOT)

    # 載入並整併資料
    df = load_all_sources()

    # 僅統計完成交易
    df = df[(df.get("status").isna()) | (df.get("status") == "COMPLETED")].copy()

    # 填補 total_amount（若缺）
    if df["total_amount"].isna().any():
        df.loc[df["total_amount"].isna(), "total_amount"] = (
            df["amount"].fillna(0) + df["tip"].fillna(0)
        )

    # KPI 與摘要
    kpi = compute_kpi(df)
    logging.info("KPI: %s", kpi)

    df_month = summary_by_month(df)
    df_dow = summary_by_dow(df)
    df_hour = summary_by_hour(df)
    heatmap_df = heatmap_dow_hour(df)
    entry_df, brand_df = payment_structure(df)

    # 準備下載連結（若檔案存在）
    links: List[Tuple[str, str]] = []
    for label, rel in [
        ("All Payments (CSV)", "data/all_payments/all_payments.csv"),
        ("All Payments Monthly (CSV)", "data/all_payments/all_payments_monthly_report.csv"),
        ("Taiwanway 2025 Payments (CSV)", "data/2025_08_11/taiwanway_payments.csv"),
    ]:
        if (ROOT / rel).exists():
            links.append((label, rel))

    # 生成 HTML
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = REPORTS_DIR / f"report_{ts}.html"
    html = build_html_report(kpi, df_month, df_dow, df_hour, heatmap_df, entry_df, brand_df, links)
    out_path.write_text(html, encoding="utf-8")
    logging.info("HTML report written: %s", out_path)

    # 輸出部分彙總至 temp 供後續擴充
    df_month.to_csv(TEMP_DIR / f"monthly_summary_{ts}.csv", index=False)
    df_dow.to_csv(TEMP_DIR / f"dow_summary_{ts}.csv", index=False)
    df_hour.to_csv(TEMP_DIR / f"hour_summary_{ts}.csv", index=False)

    print(f"✅ 互動式營運報告已輸出：{out_path}")
    print(f"📝 日誌：{log_path}")


if __name__ == "__main__":
    main()
