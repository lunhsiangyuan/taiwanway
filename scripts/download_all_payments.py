#!/usr/bin/env python3
"""
使用 Square API 下載 Taiwanway 所有的 payment histories
從開店到現在（2024-02-08 開始）
並轉換成 CSV 檔並檢核數據
"""
import json
import csv
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional
import pytz

try:
    import requests
except ImportError:
    print("⚠️  需要安裝 requests 套件: pip install requests")
    sys.exit(1)

# 營業日設定：週一、週二、週五、週六
BUSINESS_DAYS = {0, 1, 4, 5}  # Monday=0, Tuesday=1, Friday=4, Saturday=5

# 不營業的月份：六月、七月
CLOSED_MONTHS = {6, 7}  # June=6, July=7

# 聖誕節日期
CHRISTMAS_DAY = 25


def flatten_payment(payment: Dict) -> Dict:
    """將 Square Payment 物件扁平化為 CSV 行"""
    # 基本資訊
    row = {
        'id': payment.get('id', ''),
        'created_at': payment.get('created_at', ''),
        'updated_at': payment.get('updated_at', ''),
        'status': payment.get('status', ''),
        'source_type': payment.get('source_type', ''),
        'location_id': payment.get('location_id', ''),
        'order_id': payment.get('order_id', ''),
        'customer_id': payment.get('customer_id', ''),
        'receipt_number': payment.get('receipt_number', ''),
        'receipt_url': payment.get('receipt_url', ''),
    }
    
    # 金額資訊
    amount_money = payment.get('amount_money', {})
    row['amount'] = amount_money.get('amount', 0)
    row['amount_currency'] = amount_money.get('currency', '')
    
    tip_money = payment.get('tip_money', {})
    row['tip'] = tip_money.get('amount', 0)
    row['tip_currency'] = tip_money.get('currency', '')
    
    total_money = payment.get('total_money', {})
    row['total_amount'] = total_money.get('amount', 0)
    row['total_currency'] = total_money.get('currency', '')
    
    approved_money = payment.get('approved_money', {})
    row['approved_amount'] = approved_money.get('amount', 0)
    row['approved_currency'] = approved_money.get('currency', '')
    
    refunded_money = payment.get('refunded_money', {})
    row['refunded_amount'] = refunded_money.get('amount', 0)
    row['refunded_currency'] = refunded_money.get('currency', '')
    
    # 卡片資訊
    card_details = payment.get('card_details', {})
    if card_details:
        card = card_details.get('card', {})
        row['card_brand'] = card.get('card_brand', '')
        row['card_last_4'] = card.get('last_4', '')
        row['card_type'] = card.get('card_type', '')
        row['entry_method'] = card_details.get('entry_method', '')
    else:
        row['card_brand'] = ''
        row['card_last_4'] = ''
        row['card_type'] = ''
        row['entry_method'] = ''
    
    # 設備資訊
    device_details = payment.get('device_details', {})
    row['device_id'] = device_details.get('device_id', '')
    row['device_name'] = device_details.get('device_name', '')
    
    return row


def validate_business_day(date_str: str) -> tuple[bool, str]:
    """
    檢核是否為營業日
    返回: (is_valid, reason)
    """
    try:
        # 解析 UTC 時間
        dt_utc = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        # 轉換為紐約時區
        ny_tz = pytz.timezone('America/New_York')
        dt_ny = dt_utc.astimezone(ny_tz)
        
        # 檢查星期幾（0=Monday, 6=Sunday）
        weekday = dt_ny.weekday()
        if weekday not in BUSINESS_DAYS:
            weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                           'Friday', 'Saturday', 'Sunday']
            return False, f"非營業日: {weekday_names[weekday]}"
        
        # 檢查月份（六月、七月不營業）
        month = dt_ny.month
        if month in CLOSED_MONTHS:
            month_names = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return False, f"不營業月份: {month_names[month]}"
        
        # 檢查聖誕節（12月25日）
        if month == 12 and dt_ny.day == CHRISTMAS_DAY:
            return False, "聖誕節放假"
        
        return True, "正常營業日"
    
    except Exception as e:
        return False, f"日期解析錯誤: {str(e)}"


def download_payments_via_api(begin_time: str, location_id: str, 
                              access_token: Optional[str] = None) -> List[Dict]:
    """
    透過 Square API 下載所有 payments（使用分頁）
    
    注意：此函數需要 Square API access token
    可以通過環境變量 SQUARE_ACCESS_TOKEN 設定
    或通過參數傳入
    """
    import os
    import requests
    
    # 取得 access token
    if not access_token:
        access_token = os.getenv('SQUARE_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ 錯誤：需要 Square API access token")
        print("請設定環境變量 SQUARE_ACCESS_TOKEN 或修改腳本")
        return []
    
    all_payments = []
    cursor = None
    page = 1
    base_url = "https://connect.squareup.com/v2/payments"
    
    print(f"開始下載 payments（從 {begin_time} 開始）...")
    
    while True:
        # 準備請求參數
        params = {
            'location_id': location_id,
            'begin_time': begin_time,
            'sort_order': 'ASC',  # 從舊到新
            'limit': 100,  # 每頁最多 100 筆
        }
        
        if cursor:
            params['cursor'] = cursor
        
        # 發送請求
        headers = {
            'Square-Version': '2025-10-16',
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if 'errors' in data:
                print(f"❌ API 錯誤: {data['errors']}")
                break
            
            payments = data.get('payments', [])
            if not payments:
                print("沒有更多 payments")
                break
            
            all_payments.extend(payments)
            print(f"  頁面 {page}: 取得 {len(payments)} 筆記錄（總計: {len(all_payments)} 筆）")
            
            # 檢查是否有下一頁
            cursor = data.get('cursor')
            if not cursor:
                print("已取得所有記錄")
                break
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 請求錯誤: {e}")
            break
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
            break
    
    return all_payments


def save_to_csv(payments: List[Dict], output_path: Path):
    """將 payments 儲存為 CSV 檔案"""
    if not payments:
        print("沒有 payment 數據可儲存")
        return
    
    # 取得所有欄位
    fieldnames = list(flatten_payment(payments[0]).keys())
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for payment in payments:
            row = flatten_payment(payment)
            writer.writerow(row)
    
    print(f"✅ 已儲存 {len(payments)} 筆記錄到 {output_path}")


def validate_payments(payments: List[Dict]) -> Dict:
    """檢核所有 payments 的數據"""
    validation_results = {
        'total': len(payments),
        'valid_business_days': 0,
        'invalid_business_days': [],
        'june_july_payments': [],
        'christmas_payments': [],
    }
    
    for payment in payments:
        created_at = payment.get('created_at', '')
        if not created_at:
            continue
        
        is_valid, reason = validate_business_day(created_at)
        
        if is_valid:
            validation_results['valid_business_days'] += 1
        else:
            validation_results['invalid_business_days'].append({
                'id': payment.get('id', ''),
                'created_at': created_at,
                'reason': reason
            })
            
            # 檢查是否為六月或七月
            try:
                dt_utc = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                ny_tz = pytz.timezone('America/New_York')
                dt_ny = dt_utc.astimezone(ny_tz)
                if dt_ny.month in CLOSED_MONTHS:
                    validation_results['june_july_payments'].append({
                        'id': payment.get('id', ''),
                        'created_at': created_at,
                        'date_ny': dt_ny.strftime('%Y-%m-%d %H:%M:%S %Z')
                    })
                
                # 檢查是否為聖誕節
                if dt_ny.month == 12 and dt_ny.day == CHRISTMAS_DAY:
                    validation_results['christmas_payments'].append({
                        'id': payment.get('id', ''),
                        'created_at': created_at,
                        'date_ny': dt_ny.strftime('%Y-%m-%d %H:%M:%S %Z')
                    })
            except:
                pass
    
    return validation_results


def print_validation_report(results: Dict):
    """列印檢核報告"""
    print("\n" + "="*80)
    print("數據檢核報告")
    print("="*80)
    print(f"總記錄數: {results['total']}")
    print(f"正常營業日記錄數: {results['valid_business_days']}")
    print(f"異常記錄數: {len(results['invalid_business_days'])}")
    
    if results['invalid_business_days']:
        print("\n⚠️  異常記錄詳情（前 20 筆）：")
        for i, record in enumerate(results['invalid_business_days'][:20], 1):
            print(f"  {i}. {record['created_at']} - {record['reason']}")
        if len(results['invalid_business_days']) > 20:
            print(f"  ... 還有 {len(results['invalid_business_days']) - 20} 筆異常記錄")
    
    if results['june_july_payments']:
        print(f"\n⚠️  六月/七月有 {len(results['june_july_payments'])} 筆記錄（應該沒有營業）：")
        for i, record in enumerate(results['june_july_payments'][:10], 1):
            print(f"  {i}. {record['date_ny']} - ID: {record['id']}")
    
    if results['christmas_payments']:
        print(f"\n⚠️  聖誕節有 {len(results['christmas_payments'])} 筆記錄（應該放假）：")
        for i, record in enumerate(results['christmas_payments'], 1):
            print(f"  {i}. {record['date_ny']} - ID: {record['id']}")
    
    print("="*80)


def main():
    """主函數"""
    # 設定參數
    location_id = 'LMDN6Z5DKNJ2P'  # Taiwanway location ID
    begin_time = '2024-02-08T00:00:00Z'  # 最早的記錄時間
    end_time = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # 輸出檔案路徑
    output_dir = Path(__file__).parent.parent / 'data' / 'all_payments'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / 'taiwanway_all_payments.csv'
    
    print("="*80)
    print("Taiwanway Payment Histories 下載工具")
    print("="*80)
    print(f"Location ID: {location_id}")
    print(f"開始時間: {begin_time}")
    print(f"結束時間: {end_time}")
    print(f"輸出檔案: {output_csv}")
    print("="*80)
    
    # 下載 payments
    print("\n正在下載 payment histories...")
    payments = download_payments_via_api(begin_time, location_id)
    
    if not payments:
        print("\n❌ 無法下載數據")
        print("\n請確認：")
        print("1. 已設定環境變量 SQUARE_ACCESS_TOKEN")
        print("2. 或使用 MCP Square 工具手動下載數據")
        print("3. 或修改腳本以使用其他認證方式")
        return
    
    # 儲存為 CSV
    print(f"\n正在儲存 {len(payments)} 筆記錄到 CSV...")
    save_to_csv(payments, output_csv)
    
    # 檢核數據
    print("\n正在檢核數據...")
    validation_results = validate_payments(payments)
    print_validation_report(validation_results)
    
    print(f"\n✅ 完成！數據已儲存至 {output_csv}")


if __name__ == "__main__":
    main()

