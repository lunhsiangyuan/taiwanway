#!/usr/bin/env python3
"""
詳細的資料完整性比對分析
生成缺少的 Payment ID 清單和日期分布報告
"""
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import pytz

def main():
    """主函數"""
    # 檔案路徑
    all_payments_path = Path("data/all_payments/all_payments.csv")
    items_path = Path("/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv")
    
    print("載入資料...")
    all_payments_df = pd.read_csv(all_payments_path)
    items_df = pd.read_csv(items_path)
    
    # 處理 all_payments
    all_payments_df['payment_id'] = all_payments_df['id']
    all_payments_df['created_at'] = pd.to_datetime(all_payments_df['created_at'], utc=True)
    ny_tz = pytz.timezone('America/New_York')
    all_payments_df['datetime_ny'] = all_payments_df['created_at'].dt.tz_convert(ny_tz)
    all_payments_df['date'] = all_payments_df['datetime_ny'].dt.date
    
    # 處理 items
    items_df['datetime_str'] = items_df['Date'].astype(str) + ' ' + items_df['Time'].astype(str)
    items_df['datetime'] = pd.to_datetime(items_df['datetime_str'])
    items_df['date'] = items_df['datetime'].dt.date
    
    # 提取 Payment ID
    all_payments_ids = set(all_payments_df['payment_id'].dropna().unique())
    items_payment_ids = set(items_df['Payment ID'].dropna().unique())
    
    # 找出缺少的 Payment ID
    missing_ids = items_payment_ids - all_payments_ids
    
    print(f"\n缺少的 Payment ID 總數: {len(missing_ids)}")
    
    # 分析缺少的 Payment ID 的日期分布
    missing_items = items_df[items_df['Payment ID'].isin(missing_ids)]
    
    # 按日期分組統計
    missing_by_date = missing_items.groupby('date').agg({
        'Payment ID': 'nunique',
        'Net Sales': lambda x: x.replace('[\$,]', '', regex=True).astype(float).sum()
    }).reset_index()
    missing_by_date.columns = ['date', 'payment_count', 'total_amount']
    missing_by_date = missing_by_date.sort_values('date')
    
    # 輸出報告
    output_dir = Path("data/comparison_report")
    output_dir.mkdir(exist_ok=True)
    
    # 1. 缺少的 Payment ID 清單
    missing_payment_ids_df = pd.DataFrame({
        'payment_id': sorted(list(missing_ids))
    })
    missing_payment_ids_df.to_csv(output_dir / "missing_payment_ids.csv", index=False)
    print(f"✅ 已儲存缺少的 Payment ID 清單: {output_dir / 'missing_payment_ids.csv'}")
    
    # 2. 按日期統計缺少的資料
    missing_by_date.to_csv(output_dir / "missing_data_by_date.csv", index=False)
    print(f"✅ 已儲存按日期統計: {output_dir / 'missing_data_by_date.csv'}")
    
    # 3. 詳細的缺少記錄（包含 Payment ID、日期、金額）
    missing_details = missing_items[['Payment ID', 'Date', 'Time', 'Net Sales', 'Item', 'Qty']].copy()
    missing_details = missing_details.sort_values(['Date', 'Payment ID'])
    missing_details.to_csv(output_dir / "missing_records_details.csv", index=False)
    print(f"✅ 已儲存詳細缺少記錄: {output_dir / 'missing_records_details.csv'}")
    
    # 4. 按 Payment ID 分組的缺少資料統計
    missing_by_payment = missing_items.groupby('Payment ID').agg({
        'Date': 'first',
        'Net Sales': lambda x: x.replace('[\$,]', '', regex=True).astype(float).sum(),
        'Item': 'count'
    }).reset_index()
    missing_by_payment.columns = ['payment_id', 'date', 'total_amount', 'item_count']
    missing_by_payment = missing_by_payment.sort_values('date')
    missing_by_payment.to_csv(output_dir / "missing_data_by_payment.csv", index=False)
    print(f"✅ 已儲存按 Payment ID 統計: {output_dir / 'missing_data_by_payment.csv'}")
    
    # 顯示統計摘要
    print("\n" + "="*60)
    print("📊 缺少資料統計摘要")
    print("="*60)
    print(f"缺少的 Payment ID 總數: {len(missing_ids):,}")
    print(f"缺少的日期數: {len(missing_by_date):,}")
    print(f"缺少的總金額: ${missing_by_date['total_amount'].sum():,.2f}")
    print(f"\n缺少資料最多的前10個日期:")
    top_missing = missing_by_date.nlargest(10, 'payment_count')
    for _, row in top_missing.iterrows():
        print(f"   {row['date']}: {int(row['payment_count'])} 筆 Payment, ${row['total_amount']:.2f}")
    
    # 檢查日期範圍
    print(f"\n缺少資料的日期範圍: {missing_by_date['date'].min()} 至 {missing_by_date['date'].max()}")

if __name__ == "__main__":
    main()



