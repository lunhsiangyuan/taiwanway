#!/usr/bin/env python3
"""
Extract monthly data from the full payments JSON/CSV.
"""
import json
import csv
import sys
from pathlib import Path
from datetime import datetime

def extract_month(input_file, target_year, target_month):
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File {input_file} not found.")
        return

    output_dir = input_path.parent
    output_csv = output_dir / f"payments_{target_year}_{target_month:02d}.csv"
    
    print(f"Reading from {input_path}...")
    
    payments = []
    if input_path.suffix == '.json':
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            payments = data.get('payments', [])
    elif input_path.suffix == '.csv':
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            payments = list(reader)
            
    filtered_payments = []
    for p in payments:
        created_at = p.get('created_at')
        if not created_at:
            continue
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            if dt.year == target_year and dt.month == target_month:
                filtered_payments.append(p)
        except ValueError:
            continue
            
    print(f"Found {len(filtered_payments)} records for {target_year}-{target_month:02d}.")
    
    if filtered_payments:
        # Flatten if necessary (for JSON input)
        if input_path.suffix == '.json':
            flat_payments = []
            for p in filtered_payments:
                amount_money = p.get('amount_money', {})
                total_money = p.get('total_money', {})
                card_details = p.get('card_details', {}).get('card', {})
                flat_payments.append({
                    'id': p.get('id'),
                    'created_at': p.get('created_at'),
                    'status': p.get('status'),
                    'amount': amount_money.get('amount', 0) / 100.0 if isinstance(amount_money.get('amount'), (int, float)) else 0,
                    'currency': amount_money.get('currency'),
                    'total_amount': total_money.get('amount', 0) / 100.0 if isinstance(total_money.get('amount'), (int, float)) else 0,
                    'card_brand': card_details.get('card_brand'),
                    'card_last_4': card_details.get('last_4'),
                    'order_id': p.get('order_id')
                })
            filtered_payments = flat_payments

        fieldnames = filtered_payments[0].keys()
        with open(output_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_payments)
        print(f"Saved to {output_csv}")
    else:
        print("No records found.")

if __name__ == "__main__":
    # Hardcoded for this task
    INPUT_FILE = "data/all_payments/payments_2025_01_to_11.json"
    YEAR = 2025
    
    # Check May
    MONTH = 5
    print(f"Extracting month {MONTH}...")
    extract_month(INPUT_FILE, YEAR, MONTH)
