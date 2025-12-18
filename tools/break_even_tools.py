"""
損益平衡分析工具
提供損益平衡點計算、敏感度分析和利潤目標分析功能。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 業務規則常量
DEFAULT_FIXED_COSTS = {
    "rent": 3100,        # 月租金
    "utilities": 700     # 水電瓦斯
}
DEFAULT_FIXED_COST_TOTAL = 3800  # 月固定成本

# 人力成本情境
LABOR_SCENARIOS = {
    "minimal": 100,      # 最低配置
    "standard": 160,     # 標準配置
    "busy": 200,         # 繁忙配置
    "peak": 250          # 尖峰配置
}

# 食材成本率情境
FOOD_COST_RATES = {
    "low": 0.30,         # 低成本率
    "medium": 0.35,      # 中成本率
    "high": 0.40         # 高成本率
}

# NYC 銷售稅率
NYC_TAX_RATE = 0.08875


def calculate_break_even(
    fixed_costs: float = DEFAULT_FIXED_COST_TOTAL,
    labor_cost_per_day: float = 160,
    food_cost_rate: float = 0.35,
    operating_days_per_month: int = 16,
    include_tax: bool = True
) -> Dict[str, Any]:
    """
    計算損益平衡點

    公式：
    損益平衡營收 = (固定成本 + 人力成本) / (1 - 食材成本率)

    參數:
        fixed_costs: 月固定成本（預設 $3,800）
        labor_cost_per_day: 每日人力成本
        food_cost_rate: 食材成本率（0-1）
        operating_days_per_month: 每月營業天數
        include_tax: 是否考慮稅金

    返回:
        損益平衡分析結果
    """
    try:
        # 計算月人力成本
        monthly_labor = labor_cost_per_day * operating_days_per_month

        # 計算總變動成本前的成本
        total_costs = fixed_costs + monthly_labor

        # 計算損益平衡營收
        contribution_margin = 1 - food_cost_rate
        break_even_revenue = total_costs / contribution_margin

        # 計算每日損益平衡
        daily_break_even = break_even_revenue / operating_days_per_month

        # 計算含稅金額
        if include_tax:
            daily_break_even_with_tax = daily_break_even * (1 + NYC_TAX_RATE)
        else:
            daily_break_even_with_tax = daily_break_even

        result = {
            "status": "success",
            "break_even": {
                "monthly_revenue": round(break_even_revenue, 2),
                "daily_revenue": round(daily_break_even, 2),
                "daily_revenue_with_tax": round(daily_break_even_with_tax, 2)
            },
            "cost_breakdown": {
                "fixed_costs": fixed_costs,
                "monthly_labor": round(monthly_labor, 2),
                "total_monthly_costs": round(total_costs, 2),
                "food_cost_rate": food_cost_rate,
                "contribution_margin": round(contribution_margin, 4)
            },
            "parameters": {
                "labor_cost_per_day": labor_cost_per_day,
                "operating_days": operating_days_per_month,
                "include_tax": include_tax,
                "tax_rate": NYC_TAX_RATE if include_tax else 0
            }
        }

        logger.info(f"損益平衡計算完成：月營收 ${break_even_revenue:,.2f}")
        return result

    except Exception as e:
        logger.error(f"損益平衡計算失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def sensitivity_analysis(
    base_fixed_costs: float = DEFAULT_FIXED_COST_TOTAL,
    labor_scenarios: Dict[str, float] = None,
    food_cost_scenarios: Dict[str, float] = None,
    operating_days: int = 16
) -> Dict[str, Any]:
    """
    敏感度分析

    分析不同人力成本和食材成本率組合下的損益平衡點

    參數:
        base_fixed_costs: 基礎固定成本
        labor_scenarios: 人力成本情境
        food_cost_scenarios: 食材成本率情境
        operating_days: 每月營業天數

    返回:
        敏感度分析矩陣
    """
    if labor_scenarios is None:
        labor_scenarios = LABOR_SCENARIOS

    if food_cost_scenarios is None:
        food_cost_scenarios = FOOD_COST_RATES

    try:
        # 建立敏感度矩陣
        matrix = {}

        for labor_name, labor_cost in labor_scenarios.items():
            matrix[labor_name] = {}
            for food_name, food_rate in food_cost_scenarios.items():
                result = calculate_break_even(
                    fixed_costs=base_fixed_costs,
                    labor_cost_per_day=labor_cost,
                    food_cost_rate=food_rate,
                    operating_days_per_month=operating_days
                )

                if result["status"] == "success":
                    matrix[labor_name][food_name] = {
                        "monthly_break_even": result["break_even"]["monthly_revenue"],
                        "daily_break_even": result["break_even"]["daily_revenue"]
                    }

        # 找出最佳和最差情境
        all_values = []
        for labor_name in matrix:
            for food_name in matrix[labor_name]:
                all_values.append({
                    "labor": labor_name,
                    "food_rate": food_name,
                    "daily_break_even": matrix[labor_name][food_name]["daily_break_even"]
                })

        all_values.sort(key=lambda x: x["daily_break_even"])

        result = {
            "status": "success",
            "sensitivity_matrix": matrix,
            "scenarios": {
                "labor": labor_scenarios,
                "food_cost_rates": food_cost_scenarios
            },
            "summary": {
                "best_case": all_values[0] if all_values else None,
                "worst_case": all_values[-1] if all_values else None,
                "range": {
                    "min_daily": all_values[0]["daily_break_even"] if all_values else 0,
                    "max_daily": all_values[-1]["daily_break_even"] if all_values else 0
                }
            }
        }

        logger.info(f"敏感度分析完成：{len(all_values)} 種情境")
        return result

    except Exception as e:
        logger.error(f"敏感度分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def profit_target_analysis(
    target_profit: float,
    fixed_costs: float = DEFAULT_FIXED_COST_TOTAL,
    labor_cost_per_day: float = 160,
    food_cost_rate: float = 0.35,
    operating_days_per_month: int = 16
) -> Dict[str, Any]:
    """
    利潤目標分析

    計算達成特定利潤目標所需的營收

    公式：
    目標營收 = (固定成本 + 人力成本 + 目標利潤) / (1 - 食材成本率)

    參數:
        target_profit: 月目標利潤
        fixed_costs: 月固定成本
        labor_cost_per_day: 每日人力成本
        food_cost_rate: 食材成本率
        operating_days_per_month: 每月營業天數

    返回:
        利潤目標分析結果
    """
    try:
        # 計算月人力成本
        monthly_labor = labor_cost_per_day * operating_days_per_month

        # 計算達成目標所需營收
        total_to_cover = fixed_costs + monthly_labor + target_profit
        contribution_margin = 1 - food_cost_rate
        required_revenue = total_to_cover / contribution_margin

        # 每日所需營收
        daily_required = required_revenue / operating_days_per_month

        # 計算與損益平衡的差距
        break_even_result = calculate_break_even(
            fixed_costs=fixed_costs,
            labor_cost_per_day=labor_cost_per_day,
            food_cost_rate=food_cost_rate,
            operating_days_per_month=operating_days_per_month
        )

        break_even_revenue = break_even_result["break_even"]["monthly_revenue"]
        revenue_above_break_even = required_revenue - break_even_revenue

        result = {
            "status": "success",
            "target_analysis": {
                "target_profit": target_profit,
                "required_monthly_revenue": round(required_revenue, 2),
                "required_daily_revenue": round(daily_required, 2),
                "break_even_revenue": round(break_even_revenue, 2),
                "revenue_above_break_even": round(revenue_above_break_even, 2),
                "revenue_increase_percentage": round((revenue_above_break_even / break_even_revenue) * 100, 2)
            },
            "cost_structure": {
                "fixed_costs": fixed_costs,
                "monthly_labor": round(monthly_labor, 2),
                "food_cost_at_target": round(required_revenue * food_cost_rate, 2),
                "total_costs_at_target": round(required_revenue * food_cost_rate + fixed_costs + monthly_labor, 2)
            },
            "metrics": {
                "gross_margin": round((1 - food_cost_rate) * 100, 2),
                "operating_margin_at_target": round((target_profit / required_revenue) * 100, 2)
            }
        }

        logger.info(f"利潤目標分析完成：目標 ${target_profit:,.2f}，所需月營收 ${required_revenue:,.2f}")
        return result

    except Exception as e:
        logger.error(f"利潤目標分析失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def scenario_comparison(
    actual_daily_revenue: float,
    scenarios: Optional[List[Dict[str, Any]]] = None,
    fixed_costs: float = DEFAULT_FIXED_COST_TOTAL,
    operating_days: int = 16
) -> Dict[str, Any]:
    """
    情境比較分析

    比較不同成本情境下的盈虧狀況

    參數:
        actual_daily_revenue: 實際日均營收
        scenarios: 情境列表，每個包含 labor_cost 和 food_cost_rate
        fixed_costs: 固定成本
        operating_days: 營業天數

    返回:
        情境比較結果
    """
    if scenarios is None:
        # 預設情境
        scenarios = [
            {"name": "保守", "labor_cost": 100, "food_cost_rate": 0.40},
            {"name": "標準", "labor_cost": 160, "food_cost_rate": 0.35},
            {"name": "積極", "labor_cost": 200, "food_cost_rate": 0.30},
        ]

    try:
        results = []
        monthly_revenue = actual_daily_revenue * operating_days

        for scenario in scenarios:
            labor_cost = scenario["labor_cost"]
            food_rate = scenario["food_cost_rate"]

            monthly_labor = labor_cost * operating_days
            food_cost = monthly_revenue * food_rate
            total_costs = fixed_costs + monthly_labor + food_cost
            profit = monthly_revenue - total_costs

            # 計算損益平衡
            be_result = calculate_break_even(
                fixed_costs=fixed_costs,
                labor_cost_per_day=labor_cost,
                food_cost_rate=food_rate,
                operating_days_per_month=operating_days
            )

            daily_break_even = be_result["break_even"]["daily_revenue"]
            margin = actual_daily_revenue - daily_break_even
            margin_percentage = (margin / daily_break_even) * 100 if daily_break_even > 0 else 0

            results.append({
                "scenario_name": scenario.get("name", f"情境 {len(results) + 1}"),
                "parameters": {
                    "labor_cost_per_day": labor_cost,
                    "food_cost_rate": food_rate
                },
                "financials": {
                    "monthly_revenue": round(monthly_revenue, 2),
                    "monthly_costs": round(total_costs, 2),
                    "monthly_profit": round(profit, 2),
                    "profit_margin": round((profit / monthly_revenue) * 100, 2) if monthly_revenue > 0 else 0
                },
                "break_even_analysis": {
                    "daily_break_even": round(daily_break_even, 2),
                    "actual_daily_revenue": actual_daily_revenue,
                    "margin": round(margin, 2),
                    "margin_percentage": round(margin_percentage, 2),
                    "is_profitable": profit > 0
                }
            })

        # 排序：按利潤降序
        results.sort(key=lambda x: x["financials"]["monthly_profit"], reverse=True)

        return {
            "status": "success",
            "actual_daily_revenue": actual_daily_revenue,
            "operating_days": operating_days,
            "scenarios": results,
            "summary": {
                "best_scenario": results[0]["scenario_name"] if results else None,
                "worst_scenario": results[-1]["scenario_name"] if results else None,
                "profitable_count": sum(1 for r in results if r["break_even_analysis"]["is_profitable"])
            }
        }

    except Exception as e:
        logger.error(f"情境比較失敗：{str(e)}")
        return {"status": "error", "message": str(e)}


def generate_break_even_report(
    daily_revenues: Dict[str, float],
    fixed_costs: float = DEFAULT_FIXED_COST_TOTAL,
    labor_scenarios: Dict[str, float] = None,
    food_cost_rate: float = 0.35,
    operating_days: int = 16,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    生成損益平衡分析報告

    參數:
        daily_revenues: 日營收情境（如 {"淡季": 640, "平均": 753, "旺季": 820}）
        fixed_costs: 固定成本
        labor_scenarios: 人力成本情境
        food_cost_rate: 食材成本率
        operating_days: 營業天數
        output_path: 報告輸出路徑

    返回:
        報告生成結果
    """
    if labor_scenarios is None:
        labor_scenarios = LABOR_SCENARIOS

    try:
        report = {
            "title": "損益平衡分析報告",
            "generated_at": datetime.now().isoformat(),
            "parameters": {
                "fixed_costs": fixed_costs,
                "food_cost_rate": food_cost_rate,
                "operating_days": operating_days,
                "labor_scenarios": labor_scenarios,
                "revenue_scenarios": daily_revenues
            },
            "analyses": {}
        }

        # 1. 基本損益平衡分析
        for labor_name, labor_cost in labor_scenarios.items():
            be_result = calculate_break_even(
                fixed_costs=fixed_costs,
                labor_cost_per_day=labor_cost,
                food_cost_rate=food_cost_rate,
                operating_days_per_month=operating_days
            )
            report["analyses"][f"break_even_{labor_name}"] = be_result

        # 2. 各營收情境下的盈虧
        revenue_analyses = {}
        for rev_name, daily_rev in daily_revenues.items():
            scenario_result = scenario_comparison(
                actual_daily_revenue=daily_rev,
                scenarios=[
                    {"name": name, "labor_cost": cost, "food_cost_rate": food_cost_rate}
                    for name, cost in labor_scenarios.items()
                ],
                fixed_costs=fixed_costs,
                operating_days=operating_days
            )
            revenue_analyses[rev_name] = scenario_result

        report["revenue_analysis"] = revenue_analyses

        # 3. 敏感度分析
        sensitivity_result = sensitivity_analysis(
            base_fixed_costs=fixed_costs,
            labor_scenarios=labor_scenarios,
            operating_days=operating_days
        )
        report["sensitivity"] = sensitivity_result

        # 4. 關鍵洞察
        insights = []

        # 找出最常見的損益平衡點
        avg_daily_be = np.mean([
            report["analyses"][f"break_even_{name}"]["break_even"]["daily_revenue"]
            for name in labor_scenarios
        ])
        insights.append(f"平均日損益平衡點：${avg_daily_be:.2f}")

        # 評估各營收情境
        for rev_name, daily_rev in daily_revenues.items():
            if daily_rev > avg_daily_be:
                margin = ((daily_rev - avg_daily_be) / avg_daily_be) * 100
                insights.append(f"{rev_name}營收（${daily_rev}）高於平均損益平衡點 {margin:.1f}%")
            else:
                gap = ((avg_daily_be - daily_rev) / avg_daily_be) * 100
                insights.append(f"{rev_name}營收（${daily_rev}）低於平均損益平衡點 {gap:.1f}%")

        report["insights"] = insights

        # 5. 建議
        recommendations = []

        # 根據敏感度分析提供建議
        if sensitivity_result["status"] == "success":
            best = sensitivity_result["summary"]["best_case"]
            if best:
                recommendations.append(
                    f"最佳情境：{best['labor']} 人力配置 + {best['food_rate']} 食材成本率，"
                    f"日損益平衡點 ${best['daily_break_even']:.2f}"
                )

        recommendations.append("在營收較低的月份考慮減少人力配置以降低損益平衡點")
        recommendations.append("監控食材成本率，維持在 35% 以下可顯著提升獲利能力")

        report["recommendations"] = recommendations

        # 保存報告
        if output_path:
            import json
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            report["output_path"] = str(path)

        logger.info(f"損益平衡報告生成完成")

        return {
            "status": "success",
            "report": report
        }

    except Exception as e:
        logger.error(f"報告生成失敗：{str(e)}")
        return {"status": "error", "message": str(e)}
