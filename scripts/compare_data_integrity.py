#!/usr/bin/env python3
"""
比對 all_payments.csv 和 items-2025-01-01-2025-11-16.csv 的資料完整性
items-2025-01-01-2025-11-16.csv 是正確的參考檔案
"""
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import pytz

def load_all_payments(file_path: Path) -> pd.DataFrame:
    """載入 all_payments.csv"""
    print(f"📂 載入 {file_path.name}...")
    df = pd.read_csv(file_path)
    print(f"   總記錄數: {len(df):,}")
    print(f"   欄位數: {len(df.columns)}")
    
    # 提取 Payment ID (id 欄位)
    df['payment_id'] = df['id']
    
    # 解析日期
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
    ny_tz = pytz.timezone('America/New_York')
    df['datetime_ny'] = df['created_at'].dt.tz_convert(ny_tz)
    df['date'] = df['datetime_ny'].dt.date
    
    return df

def load_items(file_path: Path) -> pd.DataFrame:
    """載入 items CSV"""
    print(f"📂 載入 {file_path.name}...")
    df = pd.read_csv(file_path)
    print(f"   總記錄數: {len(df):,}")
    print(f"   欄位數: {len(df.columns)}")
    
    # 解析日期時間
    df['datetime_str'] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)
    df['datetime'] = pd.to_datetime(df['datetime_str'])
    df['date'] = df['datetime'].dt.date
    
    # 處理金額欄位（移除 $ 和逗號）
    if 'Net Sales' in df.columns:
        df['net_sales'] = df['Net Sales'].replace('[\$,]', '', regex=True).astype(float)
    
    return df

def compare_payment_ids(all_payments_df: pd.DataFrame, items_df: pd.DataFrame):
    """比對 Payment ID"""
    print("\n" + "="*60)
    print("🔍 Payment ID 比對分析")
    print("="*60)
    
    # 提取唯一的 Payment ID
    all_payments_ids = set(all_payments_df['payment_id'].dropna().unique())
    items_payment_ids = set(items_df['Payment ID'].dropna().unique())
    
    print(f"\n📊 Payment ID 統計:")
    print(f"   all_payments.csv 唯一 Payment ID 數: {len(all_payments_ids):,}")
    print(f"   items.csv 唯一 Payment ID 數: {len(items_payment_ids):,}")
    
    # 找出差異
    missing_in_all_payments = items_payment_ids - all_payments_ids
    extra_in_all_payments = all_payments_ids - items_payment_ids
    common_ids = all_payments_ids & items_payment_ids
    
    print(f"\n✅ 共同 Payment ID: {len(common_ids):,}")
    print(f"❌ items 中有但 all_payments 中缺少: {len(missing_in_all_payments):,}")
    print(f"⚠️  all_payments 中有但 items 中沒有: {len(extra_in_all_payments):,}")
    
    # 顯示缺少的 Payment ID 範例
    if missing_in_all_payments:
        print(f"\n❌ 缺少的 Payment ID 範例 (前10個):")
        missing_list = sorted(list(missing_in_all_payments))[:10]
        for pid in missing_list:
            # 找出這個 Payment ID 在 items 中的資訊
            item_info = items_df[items_df['Payment ID'] == pid].iloc[0]
            print(f"   {pid} - 日期: {item_info['Date']}, 金額: {item_info.get('Net Sales', 'N/A')}")
    
    # 顯示多餘的 Payment ID 範例
    if extra_in_all_payments:
        print(f"\n⚠️  多餘的 Payment ID 範例 (前10個):")
        extra_list = sorted(list(extra_in_all_payments))[:10]
        for pid in extra_list:
            # 找出這個 Payment ID 在 all_payments 中的資訊
            payment_info = all_payments_df[all_payments_df['payment_id'] == pid].iloc[0]
            print(f"   {pid} - 日期: {payment_info['date']}, 金額: ${payment_info.get('total_amount', 0)/100:.2f}")
    
    return {
        'missing_in_all_payments': missing_in_all_payments,
        'extra_in_all_payments': extra_in_all_payments,
        'common_ids': common_ids
    }

def compare_date_ranges(all_payments_df: pd.DataFrame, items_df: pd.DataFrame):
    """比對日期範圍"""
    print("\n" + "="*60)
    print("📅 日期範圍比對")
    print("="*60)
    
    all_payments_dates = set(all_payments_df['date'].dropna().unique())
    items_dates = set(items_df['date'].dropna().unique())
    
    print(f"\n📊 日期統計:")
    print(f"   all_payments.csv 日期範圍: {min(all_payments_dates)} 至 {max(all_payments_dates)}")
    print(f"   items.csv 日期範圍: {min(items_dates)} 至 {max(items_dates)}")
    print(f"   all_payments.csv 唯一日期數: {len(all_payments_dates):,}")
    print(f"   items.csv 唯一日期數: {len(items_dates):,}")
    
    # 找出差異日期
    missing_dates = items_dates - all_payments_dates
    extra_dates = all_payments_dates - items_dates
    
    if missing_dates:
        print(f"\n❌ items 中有但 all_payments 中缺少的日期 ({len(missing_dates)} 天):")
        missing_dates_sorted = sorted(list(missing_dates))[:20]
        for date in missing_dates_sorted:
            items_count = len(items_df[items_df['date'] == date])
            print(f"   {date}: {items_count} 筆記錄")
    
    if extra_dates:
        print(f"\n⚠️  all_payments 中有但 items 中沒有的日期 ({len(extra_dates)} 天):")
        extra_dates_sorted = sorted(list(extra_dates))[:20]
        for date in extra_dates_sorted:
            payments_count = len(all_payments_df[all_payments_df['date'] == date])
            print(f"   {date}: {payments_count} 筆記錄")

def compare_amounts(all_payments_df: pd.DataFrame, items_df: pd.DataFrame):
    """比對金額統計"""
    print("\n" + "="*60)
    print("💰 金額統計比對")
    print("="*60)
    
    # all_payments 金額（單位：分，需轉換為元）
    all_payments_df['total_amount_usd'] = all_payments_df['total_amount'] / 100
    all_payments_total = all_payments_df['total_amount_usd'].sum()
    
    # items 金額（已經是美元）
    items_total = items_df['net_sales'].sum()
    
    print(f"\n📊 總金額統計:")
    print(f"   all_payments.csv 總金額: ${all_payments_total:,.2f}")
    print(f"   items.csv 總金額: ${items_total:,.2f}")
    print(f"   差異: ${abs(all_payments_total - items_total):,.2f}")
    print(f"   差異百分比: {abs(all_payments_total - items_total) / items_total * 100:.2f}%")
    
    # 按 Payment ID 分組比較
    items_by_payment = items_df.groupby('Payment ID')['net_sales'].sum()
    all_payments_by_id = all_payments_df.groupby('payment_id')['total_amount_usd'].sum()
    
    # 找出共同 Payment ID 的金額差異
    common_ids = set(items_by_payment.index) & set(all_payments_by_id.index)
    if common_ids:
        differences = []
        for pid in common_ids:
            items_amount = items_by_payment[pid]
            payments_amount = all_payments_by_id[pid]
            diff = abs(items_amount - payments_amount)
            if diff > 0.01:  # 差異超過 1 分
                differences.append({
                    'payment_id': pid,
                    'items_amount': items_amount,
                    'payments_amount': payments_amount,
                    'difference': diff
                })
        
        if differences:
            print(f"\n⚠️  發現 {len(differences)} 個 Payment ID 金額不一致:")
            differences_sorted = sorted(differences, key=lambda x: x['difference'], reverse=True)[:10]
            for diff in differences_sorted:
                print(f"   Payment ID {diff['payment_id']}: items=${diff['items_amount']:.2f}, "
                      f"all_payments=${diff['payments_amount']:.2f}, 差異=${diff['difference']:.2f}")

def compare_status(all_payments_df: pd.DataFrame):
    """檢查 all_payments 的狀態分布"""
    print("\n" + "="*60)
    print("📊 all_payments.csv 狀態分布")
    print("="*60)
    
    status_counts = all_payments_df['status'].value_counts()
    print(f"\n狀態分布:")
    for status, count in status_counts.items():
        print(f"   {status}: {count:,} ({count/len(all_payments_df)*100:.1f}%)")
    
    # 只統計 COMPLETED 狀態
    completed_df = all_payments_df[all_payments_df['status'] == 'COMPLETED']
    print(f"\n✅ COMPLETED 狀態記錄數: {len(completed_df):,}")

def main():
    """主函數"""
    # 檔案路徑
    all_payments_path = Path("data/all_payments/all_payments.csv")
    items_path = Path("/Users/lunhsiangyuan/Desktop/square/data/items-2025-01-01-2025-11-16.csv")
    
    # 檢查檔案是否存在
    if not all_payments_path.exists():
        print(f"❌ 找不到檔案: {all_payments_path}")
        sys.exit(1)
    
    if not items_path.exists():
        print(f"❌ 找不到檔案: {items_path}")
        sys.exit(1)
    
    print("="*60)
    print("📋 資料完整性比對報告")
    print("="*60)
    print(f"參考檔案 (正確): {items_path.name}")
    print(f"比對檔案: {all_payments_path.name}")
    print("="*60)
    
    # 載入資料
    all_payments_df = load_all_payments(all_payments_path)
    items_df = load_items(items_path)
    
    # 執行各項比對
    payment_id_comparison = compare_payment_ids(all_payments_df, items_df)
    compare_date_ranges(all_payments_df, items_df)
    compare_amounts(all_payments_df, items_df)
    compare_status(all_payments_df)
    
    # 總結
    print("\n" + "="*60)
    print("📝 總結")
    print("="*60)
    print(f"✅ 共同 Payment ID: {len(payment_id_comparison['common_ids']):,}")
    print(f"❌ 缺少的 Payment ID: {len(payment_id_comparison['missing_in_all_payments']):,}")
    print(f"⚠️  多餘的 Payment ID: {len(payment_id_comparison['extra_in_all_payments']):,}")
    
    if payment_id_comparison['missing_in_all_payments']:
        print(f"\n⚠️  警告: all_payments.csv 缺少 {len(payment_id_comparison['missing_in_all_payments'])} 個 Payment ID")
        print("   建議檢查下載流程是否完整")
    
    if payment_id_comparison['extra_in_all_payments']:
        print(f"\nℹ️  資訊: all_payments.csv 有 {len(payment_id_comparison['extra_in_all_payments'])} 個額外的 Payment ID")
        print("   這些可能是 items.csv 日期範圍外的記錄")

if __name__ == "__main__":
    main()



