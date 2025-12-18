#!/usr/bin/env python3
"""
Analyze Sep, Oct, Nov 2025 revenue:
- Compare months
- Metrics: Total, Average (Daily), Median (Daily) per hour
- Visualizations: Bar charts
"""
import json
import statistics
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import numpy as np

def analyze_fall_revenue(input_file):
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File {input_file} not found.")
        return

    print(f"Reading from {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        payments = data.get('payments', [])

    # Config
    target_year = 2025
    target_months = [9, 10, 11]
    month_names = {9: 'Sep', 10: 'Oct', 11: 'Nov'}
    
    ny_zone = ZoneInfo("America/New_York")
    
    # Data structure: stats[month][day][hour] = revenue
    # We use this to calculate daily stats per hour
    daily_hourly_revenue = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    
    print("Processing data...")
    for p in payments:
        created_at = p.get('created_at')
        if not created_at:
            continue
        
        try:
            dt_utc = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            dt_ny = dt_utc.astimezone(ny_zone)
            
            if dt_ny.year == target_year and dt_ny.month in target_months:
                amount = p.get('amount_money', {}).get('amount', 0)
                amount_val = amount / 100.0 if isinstance(amount, (int, float)) else 0
                
                month = dt_ny.month
                day = dt_ny.date()
                hour = dt_ny.hour
                
                daily_hourly_revenue[month][day][hour] += amount_val
                
        except ValueError:
            continue

    # Calculate metrics per month per hour
    # hours range from 0 to 23
    hours = range(24)
    
    # Structure: results[month][hour] = {'total': X, 'avg': Y, 'median': Z}
    results = defaultdict(lambda: defaultdict(dict))
    
    for month in target_months:
        # Get all days that had any data in this month? 
        # Or should we consider all days in the month?
        # Usually for "Average Daily", we divide by number of days in month, 
        # or number of days *open*. Let's assume number of days with *any* sales 
        # to avoid skewing if they are closed on weekends, 
        # BUT user might want to know "per day of month".
        # Let's use "days with data" for now as a proxy for "open days".
        days_with_data = daily_hourly_revenue[month].keys()
        num_days = len(days_with_data) if days_with_data else 1
        
        for hour in hours:
            # Collect revenue for this hour across all active days
            revenues = []
            for day in days_with_data:
                rev = daily_hourly_revenue[month][day].get(hour, 0.0)
                revenues.append(rev)
            
            total = sum(revenues)
            avg = total / num_days if num_days > 0 else 0
            med = statistics.median(revenues) if revenues else 0
            
            results[month][hour] = {
                'total': total,
                'avg': avg,
                'median': med
            }

    # Generate Table
    print("\n--- Hourly Revenue Analysis (Sep - Nov 2025) ---")
    header = f"{'Hour':<5} | " + " | ".join([f"{month_names[m]:^26}" for m in target_months])
    print(header)
    sub_header = f"{'':<5} | " + " | ".join([f"{'Total':<8} {'Avg':<8} {'Med':<8}" for _ in target_months])
    print(sub_header)
    print("-" * len(sub_header))
    
    # Filter hours to show only relevant ones (e.g. 10am to 10pm) or all?
    # Let's show all where at least one month has non-zero total
    active_hours = []
    for h in hours:
        if any(results[m][h]['total'] > 0 for m in target_months):
            active_hours.append(h)
    
    for h in active_hours:
        row = f"{h:02d}:00 | "
        for m in target_months:
            r = results[m][h]
            row += f"${r['total']:<7.0f} ${r['avg']:<7.0f} ${r['median']:<7.0f} | "
        print(row)

    # Generate Plots
    generate_plots(results, target_months, month_names, active_hours)

def generate_plots(results, target_months, month_names, active_hours):
    # Prepare data for plotting
    # We'll focus on the active hours range for better visualization
    if not active_hours:
        print("No data to plot.")
        return

    min_h = min(active_hours)
    max_h = max(active_hours)
    plot_hours = range(min_h, max_h + 1)
    
    x = np.arange(len(plot_hours))
    width = 0.25
    
    # Plot 1: Total Revenue
    plt.figure(figsize=(12, 6))
    for i, month in enumerate(target_months):
        totals = [results[month][h]['total'] for h in plot_hours]
        plt.bar(x + i*width, totals, width, label=month_names[month])
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Total Revenue ($)')
    plt.title('Total Revenue per Hour (Sep - Nov 2025)')
    plt.xticks(x + width, [f"{h:02d}:00" for h in plot_hours])
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_total = 'analysis_output/revenue_hourly_total_sep_nov.png'
    Path(output_total).parent.mkdir(exist_ok=True)
    plt.savefig(output_total)
    print(f"\nSaved Total Revenue plot to {output_total}")
    
    # Plot 2: Median Revenue
    plt.figure(figsize=(12, 6))
    for i, month in enumerate(target_months):
        medians = [results[month][h]['median'] for h in plot_hours]
        plt.bar(x + i*width, medians, width, label=month_names[month])
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Median Daily Revenue ($)')
    plt.title('Median Daily Revenue per Hour (Sep - Nov 2025)')
    plt.xticks(x + width, [f"{h:02d}:00" for h in plot_hours])
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_median = 'analysis_output/revenue_hourly_median_sep_nov.png'
    plt.savefig(output_median)
    print(f"Saved Median Revenue plot to {output_median}")

if __name__ == "__main__":
    INPUT_FILE = "data/all_payments/payments_2025_01_to_11.json"
    analyze_fall_revenue(INPUT_FILE)
