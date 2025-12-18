#!/usr/bin/env python3
"""
Download Square payments for 2025 (Jan 1 to Nov 29)
"""
import os
import json
import csv
import requests
from pathlib import Path
from datetime import datetime
import time

# Configuration
ACCESS_TOKEN = "EAAAlxAXyAX2g8wHL4fpggE4yv5-4S3mO8rFH756zst3fLf_lPPPhuI1LR0CNc7a"
LOCATION_ID = "LMDN6Z5DKNJ2P"
START_DATE = "2025-01-01T00:00:00Z"
END_DATE = "2025-11-29T23:59:59Z"

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "all_payments"
OUTPUT_JSON = OUTPUT_DIR / "payments_2025_01_to_11.json"
OUTPUT_CSV = OUTPUT_DIR / "payments_2025_01_to_11.csv"

def download_payments():
    headers = {
        "Square-Version": "2025-10-16",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = "https://connect.squareup.com/v2/payments"
    
    all_payments = []
    cursor = None
    page = 1
    
    print(f"Starting download from {START_DATE} to {END_DATE}...")
    
    while True:
        params = {
            "location_id": LOCATION_ID,
            "begin_time": START_DATE,
            "end_time": END_DATE,
            "sort_order": "ASC",
            "limit": 100
        }
        
        if cursor:
            params["cursor"] = cursor
            
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            payments = data.get("payments", [])
            if not payments:
                break
                
            all_payments.extend(payments)
            print(f"Page {page}: Retrieved {len(payments)} records (Total: {len(all_payments)})")
            
            cursor = data.get("cursor")
            if not cursor:
                break
                
            page += 1
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error: {e}")
            break
            
    return all_payments

def flatten_payment(payment):
    amount_money = payment.get('amount_money', {})
    total_money = payment.get('total_money', {})
    card_details = payment.get('card_details', {}).get('card', {})
    
    return {
        'id': payment.get('id'),
        'created_at': payment.get('created_at'),
        'status': payment.get('status'),
        'amount': amount_money.get('amount', 0) / 100.0,
        'currency': amount_money.get('currency'),
        'total_amount': total_money.get('amount', 0) / 100.0,
        'card_brand': card_details.get('card_brand'),
        'card_last_4': card_details.get('last_4'),
        'order_id': payment.get('order_id')
    }

def save_data(payments):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({"payments": payments, "count": len(payments)}, f, indent=2)
    print(f"Saved JSON to {OUTPUT_JSON}")
    
    # Save CSV
    if payments:
        flat_payments = [flatten_payment(p) for p in payments]
        fieldnames = flat_payments[0].keys()
        
        with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_payments)
        print(f"Saved CSV to {OUTPUT_CSV}")

if __name__ == "__main__":
    payments = download_payments()
    if payments:
        save_data(payments)
        print(f"Successfully downloaded {len(payments)} payments.")
    else:
        print("No payments found or download failed.")
