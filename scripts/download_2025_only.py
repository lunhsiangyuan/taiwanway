#!/usr/bin/env python3
"""
生成 MCP Square 命令以下载 2025 年 payments 数据 (2025-01-01 至 2025-11-15)

使用方法:
    python3 scripts/download_2025_only.py

输出:
    - 11 个月的 MCP Square 命令
    - 每个月一个命令，最后一个月只到 11-15
    - 格式化的命令可直接复制到 MCP Square 使用
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Taiwanway Location ID
LOCATION_ID = "LMDN6Z5DKNJ2P"

# 日期范围
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 11, 15)

def generate_monthly_commands():
    """生成按月份的 MCP Square 命令"""

    print("=" * 80)
    print("  MCP Square Commands - Download 2025 Payments (2025-01-01 to 2025-11-15)")
    print("=" * 80)
    print()
    print("Location ID: LMDN6Z5DKNJ2P")
    print("Date Range: 2025-01-01 to 2025-11-15")
    print()
    print("营业规则:")
    print("  - 营业日: 周一、周二、周五、周六")
    print("  - 不营业月份: 六月、七月")
    print("  - 特殊假期: 圣诞节 (12月25日)")
    print()
    print("=" * 80)
    print()

    current_date = START_DATE
    command_count = 0

    while current_date <= END_DATE:
        # 计算当前月份的结束日期
        if current_date.year == END_DATE.year and current_date.month == END_DATE.month:
            # 最后一个月，只到 11-15
            month_end = END_DATE
        else:
            # 其他月份，到月底
            next_month = current_date + relativedelta(months=1)
            month_end = next_month - timedelta(days=1)

        # 生成 begin_time 和 end_time
        begin_time = f"{current_date.strftime('%Y-%m-%d')}T00:00:00Z"
        end_time = f"{month_end.strftime('%Y-%m-%d')}T23:59:59Z"

        command_count += 1

        # 格式化输出
        month_name = current_date.strftime('%Y-%m')
        note = ""

        if current_date.month in [6, 7]:
            note = "  # 注意: 六、七月通常不营业（暑期休息），数据可能为空"

        print(f"# ───────────────────────────────────────────────────────")
        print(f"# Command #{command_count}: {month_name}")
        print(f"# Date Range: {current_date.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}")
        print(f"# ───────────────────────────────────────────────────────")
        print()
        print(f"service: payments")
        print(f"method: list")
        print(f"request: {{")
        print(f"    \"location_id\": \"{LOCATION_ID}\",")
        print(f"    \"begin_time\": \"{begin_time}\",")
        print(f"    \"end_time\": \"{end_time}\",")
        print(f"    \"sort_order\": \"ASC\",")
        print(f"    \"limit\": 100")
        print(f"}}")

        if note:
            print(note)

        print()
        print()

        # 移动到下个月
        current_date = current_date + relativedelta(months=1)

    print("=" * 80)
    print(f"  总共生成 {command_count} 个下载命令")
    print("=" * 80)
    print()
    print("使用说明:")
    print("1. 复制上面的每个命令到 MCP Square")
    print("2. 依次执行每个月份的命令")
    print("3. 如果返回结果中有 'cursor' 字段，表示还有更多数据")
    print("4. 使用 cursor 继续下载（参见下面的 cursor 命令格式）")
    print()
    print("Cursor 下载命令格式:")
    print("─" * 80)
    print("service: payments")
    print("method: list")
    print("request: {")
    print(f"    \"location_id\": \"{LOCATION_ID}\",")
    print("    \"cursor\": \"<从上次响应中获取的 cursor>\",")
    print("    \"limit\": 100,")
    print("    \"sort_order\": \"ASC\"")
    print("}")
    print("─" * 80)
    print()
    print("下载后:")
    print("1. MCP 会自动保存文件到:")
    print("   ~/.cursor/projects/Users-lunhsiangyuan-Desktop-square/agent-tools/")
    print("2. 运行合并脚本: python3 scripts/download_all_payments_mcp.py")
    print("3. 转换为 CSV: python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json")
    print("4. 生成报告: python3 scripts/generate_html_report.py data/all_payments/all_payments.csv")
    print()

def generate_command_summary():
    """生成命令摘要"""
    print("\n" + "=" * 80)
    print("  按月份摘要")
    print("=" * 80)
    print()

    months_info = [
        ("2025-01", "January", "2025-01-01 至 2025-01-31", "冬季营业"),
        ("2025-02", "February", "2025-02-01 至 2025-02-28", "冬季营业"),
        ("2025-03", "March", "2025-03-01 至 2025-03-31", "春季营业"),
        ("2025-04", "April", "2025-04-01 至 2025-04-30", "春季营业"),
        ("2025-05", "May", "2025-05-01 至 2025-05-31", "春季营业"),
        ("2025-06", "June", "2025-06-01 至 2025-06-30", "⚠️ 暑期休息，应该无数据"),
        ("2025-07", "July", "2025-07-01 至 2025-07-31", "⚠️ 暑期休息，应该无数据"),
        ("2025-08", "August", "2025-08-01 至 2025-08-31", "秋季营业"),
        ("2025-09", "September", "2025-09-01 至 2025-09-30", "秋季营业"),
        ("2025-10", "October", "2025-10-01 至 2025-10-31", "秋季营业"),
        ("2025-11", "November", "2025-11-01 至 2025-11-15", "秋季营业（前15天）"),
    ]

    for month_code, month_name, date_range, note in months_info:
        print(f"{month_code} ({month_name:9s}): {date_range:30s} - {note}")

    print()
    print("=" * 80)
    print()

if __name__ == "__main__":
    generate_monthly_commands()
    generate_command_summary()

    print("✅ 命令生成完成！")
    print()
    print("下一步:")
    print("  1. 使用上面的命令在 MCP Square 中下载数据")
    print("  2. 下载完成后，运行: python3 scripts/download_all_payments_mcp.py")
    print()
