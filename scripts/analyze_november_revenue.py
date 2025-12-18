#!/usr/bin/env python3
"""
Analyze November 2025 revenue:
- Revenue by time slot (hourly)
- Number of people (transactions) by time slot
- Total revenue
"""
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from zoneinfo import ZoneInfo

def analyze_november(input_file):
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File {input_file} not found.")
        return

    print(f"Reading from {input_path}...")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        payments = data.get('payments', [])

    target_year = 2025
    target_month = 11
    
    # Define timezones
    utc_zone = ZoneInfo("UTC")
    ny_zone = ZoneInfo("America/New_York")
    
    hourly_stats = defaultdict(lambda: {'count': 0, 'revenue': 0.0})
    total_revenue = 0.0
    total_count = 0
    
    print(f"Analyzing data for {target_year}-{target_month:02d} (New York Time)...")
    
    for p in payments:
        created_at = p.get('created_at')
        if not created_at:
            continue
        
        try:
            # Parse datetime as UTC
            dt_utc = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            # Convert to New York time
            dt_ny = dt_utc.astimezone(ny_zone)
            
            # Filter for November 2025 (based on NY time)
            if dt_ny.year == target_year and dt_ny.month == target_month:
                # Get amount
                amount_money = p.get('amount_money', {})
                amount = amount_money.get('amount', 0)
                
                # Square amounts are usually in cents, check if we need to divide by 100
                amount_val = amount / 100.0 if isinstance(amount, (int, float)) else 0
                
                # Group by hour (NY time)
                hour = dt_ny.hour
                hourly_stats[hour]['count'] += 1
                hourly_stats[hour]['revenue'] += amount_val
                
                total_revenue += amount_val
                total_count += 1
                
        except ValueError:
            continue

    print("\n--- November 2025 Revenue Analysis (New York Time) ---")
    print(f"Total Transactions: {total_count}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print("\n--- Hourly Breakdown (NY Time) ---")
    print(f"{'Hour':<10} | {'Transactions':<15} | {'Revenue':<15}")
    print("-" * 45)
    
    sorted_hours = sorted(hourly_stats.keys())
    for hour in sorted_hours:
        stats = hourly_stats[hour]
        time_slot = f"{hour:02d}:00-{hour:02d}:59"
        print(f"{time_slot:<10} | {stats['count']:<15} | ${stats['revenue']:,.2f}")

if __name__ == "__main__":
    INPUT_FILE = "data/all_payments/payments_2025_01_to_11.json"
    analyze_november(INPUT_FILE)
