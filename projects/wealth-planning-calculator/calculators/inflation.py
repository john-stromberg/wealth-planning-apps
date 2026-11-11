"""
Inflation impact analysis.
"""

def calculate_future_value_with_inflation(present_value, inflation_rate, years):
    """
    Calculate the purchasing power of a present value in the future.

    Returns:
        dict with future_nominal_value, future_real_value, purchasing_power_lost
    """
    future_nominal = present_value
    future_real = present_value / ((1 + inflation_rate) ** years)

    purchasing_power_lost = ((present_value - future_real) / present_value) * 100

    return {
        'future_nominal_value': round(future_nominal, 2),
        'future_real_value': round(future_real, 2),
        'purchasing_power_lost_pct': round(purchasing_power_lost, 1),
        'years': years,
        'inflation_rate': inflation_rate * 100
    }


def calculate_required_return_for_goal(current_portfolio, annual_contribution, 
                                      goal_amount, years):
    """
    Solve for the required annual return to reach a goal.
    Uses simplified iterative approach.

    Returns:
        dict with required_return, feasible, portfolio_at_goal
    """
    # Binary search for required return
    low_return = 0.0
    high_return = 0.5  # 50% max
    tolerance = 0.0001

    while high_return - low_return > tolerance:
        mid_return = (low_return + high_return) / 2

        portfolio = current_portfolio
        for _ in range(years):
            portfolio = portfolio * (1 + mid_return) + annual_contribution

        if portfolio < goal_amount:
            low_return = mid_return
        else:
            high_return = mid_return

    required_return = (low_return + high_return) / 2

    # Verify
    portfolio = current_portfolio
    for _ in range(years):
        portfolio = portfolio * (1 + required_return) + annual_contribution

    feasible = portfolio >= goal_amount

    return {
        'required_annual_return': round(required_return * 100, 2),
        'feasible': feasible,
        'portfolio_at_goal': round(portfolio, 2),
        'goal_amount': goal_amount,
        'years': years
    }


def calculate_inflation_adjusted_expenses(annual_expense, inflation_rate, years):
    """
    Project annual expenses accounting for inflation.

    Returns:
        list of dicts with year, nominal_expense, cumulative_total
    """
    expenses = []
    cumulative = 0

    for year in range(1, years + 1):
        nominal_expense = annual_expense * ((1 + inflation_rate) ** year)
        cumulative += nominal_expense
        expenses.append({
            'year': year,
            'nominal_expense': round(nominal_expense, 2),
            'cumulative_total': round(cumulative, 2)
        })

    return expenses
