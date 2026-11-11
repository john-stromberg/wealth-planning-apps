"""
Scenario and timeline calculations for cashflow goals.
"""

import math


def months_to_fund_goal(current_balance: float, target_balance: float, monthly_contribution: float) -> int | None:
    gap = max(0.0, target_balance - current_balance)
    if gap <= 0:
        return 0
    if monthly_contribution <= 0:
        return None
    return math.ceil(gap / monthly_contribution)


def months_to_payoff_debt(balance: float, apr_percent: float, monthly_payment: float) -> int | None:
    if balance <= 0:
        return 0
    if monthly_payment <= 0:
        return None

    monthly_rate = max(0.0, apr_percent / 100.0 / 12.0)
    if monthly_rate == 0:
        return math.ceil(balance / monthly_payment)

    # If payment does not cover monthly interest, payoff is impossible.
    if monthly_payment <= balance * monthly_rate:
        return None

    # Amortization formula
    months = -math.log(1 - (balance * monthly_rate / monthly_payment)) / math.log(1 + monthly_rate)
    return math.ceil(months)


def compare_allocation_strategies(
    emergency_current: float,
    emergency_target: float,
    debt_balance: float,
    debt_apr: float,
    strategy_a: dict,
    strategy_b: dict,
):
    """
    Compare two allocations by timeline outputs.
    Expected keys: emergency_contrib, debt_paydown
    """
    a_emergency_months = months_to_fund_goal(emergency_current, emergency_target, strategy_a.get("emergency_contrib", 0.0))
    b_emergency_months = months_to_fund_goal(emergency_current, emergency_target, strategy_b.get("emergency_contrib", 0.0))

    a_debt_months = months_to_payoff_debt(debt_balance, debt_apr, strategy_a.get("debt_paydown", 0.0))
    b_debt_months = months_to_payoff_debt(debt_balance, debt_apr, strategy_b.get("debt_paydown", 0.0))

    return {
        "strategy_a": {
            "emergency_fund_months": a_emergency_months,
            "debt_payoff_months": a_debt_months,
        },
        "strategy_b": {
            "emergency_fund_months": b_emergency_months,
            "debt_payoff_months": b_debt_months,
        },
    }
