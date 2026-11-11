"""
Retirement planning calculations.
"""

def calculate_retirement_date(current_age, retirement_age, current_portfolio, annual_savings,
                             annual_return, inflation_rate, annual_expense):
    """
    Calculate when retirement is feasible based on portfolio growth and expense needs.

    Returns:
        dict with retirement_year, portfolio_at_retirement, years_to_retirement
    """
    portfolio = current_portfolio
    age = current_age
    year = 0

    while age < retirement_age and year < 70:
        # Annual growth
        growth = portfolio * annual_return
        portfolio += growth + annual_savings
        age += 1
        year += 1

    return {
        'retirement_year': int(current_age + year),
        'portfolio_at_retirement': round(portfolio, 2),
        'years_to_retirement': year,
        'annual_expense': annual_expense
    }


def calculate_safe_withdrawal_rate(portfolio, annual_expense, years_in_retirement=30):
    """
    Calculate if portfolio supports withdrawal needs (4% rule proxy).

    Returns:
        dict with swr, is_sustainable, remaining_at_end
    """
    annual_withdrawal = annual_expense
    swr = (annual_withdrawal / portfolio) * 100 if portfolio > 0 else 0

    # Simplified: assume 5% returns in retirement
    growth_rate = 0.05
    inflation = 0.03

    remaining = portfolio
    for year in range(years_in_retirement):
        remaining -= annual_withdrawal
        remaining *= (1 + growth_rate)
        annual_withdrawal *= (1 + inflation)

    return {
        'safe_withdrawal_rate': round(swr, 2),
        'is_sustainable': swr <= 4.0,
        'remaining_at_end': round(remaining, 2),
        'swr_status': 'SAFE' if swr <= 4.0 else 'AT RISK' if swr <= 5.0 else 'UNSUSTAINABLE'
    }
