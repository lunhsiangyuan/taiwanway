#!/usr/bin/env python3
"""
Merge May 2025 data with existing dataset and check for duplicates.
"""
import csv
import json
from pathlib import Path
from collections import defaultdict

# File paths
DATA_DIR = Path(__file__).parent.parent / "data" / "all_payments"
EXISTING_CSV = DATA_DIR / "all_payments.csv"
MAY_CSV = DATA_DIR / "payments_2025_05.csv"
OUTPUT_CSV = DATA_DIR / "all_payments_merged.csv"
BACKUP_CSV = DATA_DIR / "all_payments_backup.csv"

def read_csv_payments(file_path):
    """Read payments from CSV file."""
    payments = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            payments.append(row)
    return payments

def merge_and_deduplicate(existing_payments, new_payments):
    """Merge payments and remove duplicates based on ID."""
    # Use dict to automatically handle duplicates (last one wins)
    payment_dict = {}
    
    # Track statistics
    stats = {
        'existing_count': len(existing_payments),
        'new_count': len(new_payments),
        'duplicates_found': 0,
        'final_count': 0
    }
    
    # Add existing payments
    for payment in existing_payments:
        payment_id = payment.get('id', '')
        if payment_id:
            payment_dict[payment_id] = payment
    
    # Add new payments and count duplicates
    for payment in new_payments:
        payment_id = payment.get('id', '')
        if payment_id:
            if payment_id in payment_dict:
                stats['duplicates_found'] += 1
            payment_dict[payment_id] = payment
    
    stats['final_count'] = len(payment_dict)
    
    return list(payment_dict.values()), stats

def main():
    print("=" * 80)
    print("Merging May 2025 Data")
    print("=" * 80)
    
    # Read existing data
    print(f"\n1. Reading existing data from {EXISTING_CSV}...")
    existing_payments = read_csv_payments(EXISTING_CSV)
    print(f"   Found {len(existing_payments)} existing records")
    
    # Read May data
    print(f"\n2. Reading May data from {MAY_CSV}...")
    may_payments = read_csv_payments(MAY_CSV)
    print(f"   Found {len(may_payments)} May records")
    
    # Merge and deduplicate
    print("\n3. Merging and checking for duplicates...")
    merged_payments, stats = merge_and_deduplicate(existing_payments, may_payments)
    
    # Print statistics
    print("\n" + "=" * 80)
    print("Merge Statistics:")
    print("=" * 80)
    print(f"Existing records:     {stats['existing_count']:,}")
    print(f"May records:          {stats['new_count']:,}")
    print(f"Duplicates found:     {stats['duplicates_found']:,}")
    print(f"Final unique records: {stats['final_count']:,}")
    print(f"Net new records:      {stats['final_count'] - stats['existing_count']:,}")
    print("=" * 80)
    
    # Backup existing file
    print(f"\n4. Creating backup: {BACKUP_CSV}...")
    import shutil
    shutil.copy2(EXISTING_CSV, BACKUP_CSV)
    
    # Save merged data
    print(f"\n5. Saving merged data to {OUTPUT_CSV}...")
    if merged_payments:
        # Collect all unique fieldnames from all payments
        all_fieldnames = set()
        for payment in merged_payments:
            all_fieldnames.update(payment.keys())
        fieldnames = sorted(all_fieldnames)
        
        with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merged_payments)
        print(f"   ✅ Saved {len(merged_payments):,} records")
        
        # Replace original file with merged file
        print(f"\n6. Replacing {EXISTING_CSV} with merged data...")
        shutil.move(str(OUTPUT_CSV), str(EXISTING_CSV))
        print("   ✅ Complete!")
    
    print("\n" + "=" * 80)
    print("Merge Complete!")
    print("=" * 80)
    print(f"\nBackup saved at: {BACKUP_CSV}")
    print(f"Merged file: {EXISTING_CSV}")
    
    return stats

if __name__ == "__main__":
    main()
