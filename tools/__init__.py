"""
MCP Tools for Taiwanway Revenue Analysis System

這些工具提供數據處理、分析和記憶功能，供 Claude Agent SDK 的 Subagent 使用。
"""

from .data_tools import (
    load_square_data,
    preprocess_data,
    validate_data,
    filter_by_business_rules
)

from .analysis_tools import (
    analyze_hourly_sales,
    analyze_daily_sales,
    analyze_monthly_sales,
    analyze_categories,
    analyze_products,
    identify_peak_hours,
    analyze_growth_trends,
    analyze_customer_segments,
    analyze_dining_preferences,
    analyze_revenue_metrics,
    analyze_transactions,
    analyze_tax,
    analyze_aov_trends,
    analyze_revenue_concentration
)

from .memory_tools import (
    remember,
    recall,
    get_experience,
    record_analysis,
    clear_memory,
    get_memory_summary
)

from .visualization_tools import (
    generate_hourly_chart,
    generate_daily_chart,
    generate_monthly_chart,
    generate_heatmap,
    generate_category_chart
)

from .break_even_tools import (
    calculate_break_even,
    sensitivity_analysis,
    profit_target_analysis,
    generate_break_even_report
)

__all__ = [
    # Data tools
    'load_square_data',
    'preprocess_data',
    'validate_data',
    'filter_by_business_rules',
    # Analysis tools
    'analyze_hourly_sales',
    'analyze_daily_sales',
    'analyze_monthly_sales',
    'analyze_categories',
    'analyze_products',
    'identify_peak_hours',
    'analyze_growth_trends',
    'analyze_customer_segments',
    'analyze_dining_preferences',
    'analyze_revenue_metrics',
    'analyze_transactions',
    'analyze_tax',
    'analyze_aov_trends',
    'analyze_revenue_concentration',
    # Memory tools
    'remember',
    'recall',
    'get_experience',
    'record_analysis',
    'clear_memory',
    'get_memory_summary',
    # Visualization tools
    'generate_hourly_chart',
    'generate_daily_chart',
    'generate_monthly_chart',
    'generate_heatmap',
    'generate_category_chart',
    # Break-even tools
    'calculate_break_even',
    'sensitivity_analysis',
    'profit_target_analysis',
    'generate_break_even_report'
]
