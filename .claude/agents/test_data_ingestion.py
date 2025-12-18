#!/usr/bin/env python3
"""
數據攝取測試腳本
按照 data-ingestion.md 規格執行數據載入和預處理
"""

import pandas as pd
import pytz
import json
from pathlib import Path
from datetime import datetime


def load_and_preprocess_square_data(file_path: str) -> dict:
    """
    載入並預處理 Square 支付數據

    Args:
        file_path: CSV 檔案路徑

    Returns:
        dict: 包含 status, metadata, summary 的結果
    """
    try:
        # Step 1: 讀取 CSV 檔案
        print(f"[1/7] 讀取 CSV 檔案: {file_path}")
        df = pd.read_csv(file_path)
        rows_original = len(df)
        print(f"      ✓ 載入 {rows_original:,} 行數據")

        # Step 2: 驗證必要欄位
        print(f"[2/7] 驗證必要欄位")
        required_columns = ['created_at', 'amount', 'status']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return {
                "status": "error",
                "error": f"缺少必要欄位: {missing_columns}",
                "columns_found": list(df.columns)
            }

        print(f"      ✓ 所有必要欄位存在: {required_columns}")

        # Step 3: 過濾狀態（只保留 COMPLETED）
        print(f"[3/7] 過濾交易狀態")
        df = df[df['status'] == 'COMPLETED'].copy()
        print(f"      ✓ 過濾後保留 {len(df):,} 筆 COMPLETED 交易")

        # Step 4: 轉換時間欄位為 America/New_York 時區
        print(f"[4/7] 轉換時區")
        df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
        ny_tz = pytz.timezone('America/New_York')
        df['DateTime'] = df['created_at'].dt.tz_convert(ny_tz)

        # 提取時間維度
        df['Year'] = df['DateTime'].dt.year
        df['Month'] = df['DateTime'].dt.month
        df['Day'] = df['DateTime'].dt.day
        df['Hour'] = df['DateTime'].dt.hour
        df['DayOfWeek'] = df['DateTime'].dt.dayofweek
        df['YearMonth'] = df['DateTime'].dt.to_period('M')
        print(f"      ✓ 時區轉換完成 (UTC → America/New_York)")

        # Step 5: 應用業務規則過濾
        print(f"[5/7] 應用業務規則過濾")

        # 營業日：週一(0)、週二(1)、週五(4)、週六(5)
        operating_days = [0, 1, 4, 5]
        df = df[df['DayOfWeek'].isin(operating_days)]
        print(f"      ✓ 營業日過濾: {len(df):,} 行")

        # 排除六月(6)、七月(7)
        closed_months = [6, 7]
        df = df[~df['Month'].isin(closed_months)]
        print(f"      ✓ 月份過濾: {len(df):,} 行")

        rows_after_filter = len(df)

        # Step 6: 計算淨營收（NYC 稅率 8.875%）
        print(f"[6/7] 計算淨營收")
        NYC_TAX = 0.08875

        # amount 是以美元為單位（已經含稅）
        df['Net_Revenue'] = df['amount'] / (1 + NYC_TAX)
        print(f"      ✓ 淨營收計算完成 (稅率: 8.875%)")

        # Step 7: 生成摘要統計
        print(f"[7/7] 生成摘要統計")
        total_revenue = df['Net_Revenue'].sum()
        total_transactions = len(df)
        unique_days = df['DateTime'].dt.date.nunique()

        date_range = {
            "start": df['DateTime'].min().strftime('%Y-%m-%d'),
            "end": df['DateTime'].max().strftime('%Y-%m-%d')
        }

        print(f"      ✓ 統計完成")
        print(f"\n{'='*60}")
        print(f"處理完成摘要:")
        print(f"  原始行數: {rows_original:,}")
        print(f"  過濾後行數: {rows_after_filter:,}")
        print(f"  保留比例: {rows_after_filter/rows_original*100:.1f}%")
        print(f"  日期範圍: {date_range['start']} ~ {date_range['end']}")
        print(f"  總營收 (淨額): ${total_revenue:,.2f}")
        print(f"  交易筆數: {total_transactions:,}")
        print(f"  營業天數: {unique_days}")
        print(f"  平均日營收: ${total_revenue/unique_days:,.2f}")
        print(f"{'='*60}\n")

        # 返回結果
        return {
            "status": "success",
            "rows_original": rows_original,
            "rows_after_filter": rows_after_filter,
            "columns": list(df.columns),
            "date_range": date_range,
            "summary": {
                "total_revenue": round(total_revenue, 2),
                "total_transactions": total_transactions,
                "unique_days": unique_days,
                "avg_daily_revenue": round(total_revenue / unique_days, 2)
            },
            "metadata": {
                "timezone": "America/New_York",
                "tax_rate": NYC_TAX,
                "operating_days": operating_days,
                "closed_months": closed_months,
                "business_rules_applied": True,
                "timestamp": datetime.now().isoformat()
            }
        }

    except FileNotFoundError:
        return {
            "status": "error",
            "error": f"檔案不存在: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"處理錯誤: {str(e)}",
            "error_type": type(e).__name__
        }


def main():
    # 數據來源
    data_file = "/Users/lunhsiangyuan/Desktop/square/data/all_payments/all_payments.csv"

    print("=" * 60)
    print("數據攝取測試")
    print("規格來源: .claude/agents/data-ingestion.md")
    print("=" * 60)
    print()

    # 執行數據載入和預處理
    result = load_and_preprocess_square_data(data_file)

    # 輸出 JSON 結果
    print("JSON 輸出結果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 儲存結果
    output_dir = Path("/Users/lunhsiangyuan/Desktop/square/.claude/agents/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"data_ingestion_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n結果已儲存至: {output_file}")


if __name__ == "__main__":
    main()
