"""
Cashflow allocation engine for advisor workflows.
"""

from dataclasses import dataclass


@dataclass
class AllocationInputs:
    monthly_income: float
    fixed_expenses: float
    variable_expenses: float
    emergency_fund_current: float
    emergency_fund_target_months: int
    high_interest_debt_balance: float
    high_interest_debt_apr: float
    retirement_match_pct: float
    base_investing_pct: float


def calculate_monthly_surplus(monthly_income: float, fixed_expenses: float, variable_expenses: float) -> float:
    return max(0.0, monthly_income - fixed_expenses - variable_expenses)


def recommended_allocation(inputs: AllocationInputs):
    """
    Advisor-friendly rule set:
    1) Ensure retirement match capture
    2) Build emergency fund to target
    3) Accelerate high-interest debt payoff
    4) Allocate remainder to long-term investing and discretionary
    """
    surplus = calculate_monthly_surplus(inputs.monthly_income, inputs.fixed_expenses, inputs.variable_expenses)

    # Emergency fund target
    emergency_target = (inputs.fixed_expenses + inputs.variable_expenses) * inputs.emergency_fund_target_months
    emergency_gap = max(0.0, emergency_target - inputs.emergency_fund_current)

    # Step 1: retirement match capture
    retirement_match_contrib = inputs.monthly_income * max(0.0, inputs.retirement_match_pct / 100.0)
    retirement_match_contrib = min(retirement_match_contrib, surplus)
    remaining = max(0.0, surplus - retirement_match_contrib)

    # Step 2: emergency fund priority
    emergency_contrib = 0.0
    if emergency_gap > 0 and remaining > 0:
        emergency_contrib = min(remaining * 0.50, emergency_gap)
        remaining -= emergency_contrib

    # Step 3: high-interest debt payoff priority
    debt_paydown = 0.0
    if inputs.high_interest_debt_balance > 0 and remaining > 0:
        debt_paydown = min(remaining * 0.70, inputs.high_interest_debt_balance)
        remaining -= debt_paydown

    # Step 4: base investing and discretionary split
    target_investing = inputs.monthly_income * max(0.0, inputs.base_investing_pct / 100.0)
    investing = min(target_investing, remaining)
    remaining -= investing

    discretionary = remaining

    return {
        "monthly_surplus": surplus,
        "emergency_target": emergency_target,
        "emergency_gap": emergency_gap,
        "retirement_match_contrib": retirement_match_contrib,
        "emergency_contrib": emergency_contrib,
        "debt_paydown": debt_paydown,
        "investing": investing,
        "discretionary": discretionary,
    }
