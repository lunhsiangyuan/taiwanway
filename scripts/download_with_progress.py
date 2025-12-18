#!/usr/bin/env python3
"""
Download Square payments with Progress Bar and ETA.
"""
import os
import json
import csv
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Try to import tqdm, fallback if not available
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Configuration
ACCESS_TOKEN = "EAAAlxAXyAX2g8wHL4fpggE4yv5-4S3mO8rFH756zst3fLf_lPPPhuI1LR0CNc7a"
LOCATION_ID = "LMDN6Z5DKNJ2P"
# Default to full year if not specified
START_DATE = "2025-01-01T00:00:00Z"
END_DATE = datetime.utcnow().isoformat() + "Z"

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "all_payments"
OUTPUT_JSON = OUTPUT_DIR / "payments_downloaded.json"

def download_payments_with_progress():
    headers = {
        "Square-Version": "2025-10-16",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = "https://connect.squareup.com/v2/payments"
    
    all_payments = []
    cursor = None
    page = 0
    start_time = time.time()
    
    print(f"Starting download from {START_DATE}...")
    
    # Initial request to check connection and start
    # We don't know total count upfront with cursor pagination, 
    # so we'll estimate or just show count.
    
    pbar = None
    if tqdm:
        pbar = tqdm(desc="Downloading Records", unit=" payments")
        
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
                
            count = len(payments)
            all_payments.extend(payments)
            page += 1
            
            if pbar:
                pbar.update(count)
            else:
                # Manual progress
                elapsed = time.time() - start_time
                rate = len(all_payments) / elapsed if elapsed > 0 else 0
                print(f"\rDownloaded {len(all_payments)} records... (Rate: {rate:.1f} rec/s)", end="")
                sys.stdout.flush()
            
            cursor = data.get("cursor")
            if not cursor:
                break
                
            # Rate limiting sleep
            time.sleep(0.2)
            
        except Exception as e:
            print(f"\nError: {e}")
            break
            
    if pbar:
        pbar.close()
    else:
        print() # Newline
        
    return all_payments

def save_data(payments):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"payments_download_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"payments": payments, "count": len(payments)}, f, indent=2)
    print(f"Saved {len(payments)} records to {output_file}")

if __name__ == "__main__":
    if not tqdm:
        print("Tip: Install 'tqdm' for a better progress bar: pip install tqdm")
        
    payments = download_payments_with_progress()
    if payments:
        save_data(payments)
        print(f"Download complete. Total records: {len(payments)}")
    else:
        print("No payments found.")
