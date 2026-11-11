"""
FIRE (Financial Independence, Retire Early) calculations.
"""

def calculate_fire_number(annual_expense, safe_withdrawal_rate=0.04):
    """
    Calculate the portfolio needed to support annual expenses in perpetuity.

    Returns:
        dict with fire_number, monthly_expense_needed
    """
    fire_number = annual_expense / safe_withdrawal_rate

    return {
        'fire_number': round(fire_number, 2),
        'annual_expense': annual_expense,
        'safe_withdrawal_rate': safe_withdrawal_rate * 100
    }


def calculate_fire_timeline(current_portfolio, annual_savings, annual_return,
                           target_fire_number):
    """
    Calculate years until FIRE goal is reached.

    Returns:
        dict with years_to_fire, fire_age (if current age provided), portfolio_milestones
    """
    portfolio = current_portfolio
    year = 0
    milestones = []

    while portfolio < target_fire_number and year < 60:
        portfolio += annual_savings
        portfolio *= (1 + annual_return)
        year += 1

        if year % 5 == 0 or year == 1:
            milestones.append({
                'year': year,
                'portfolio': round(portfolio, 2),
                'progress_pct': round((portfolio / target_fire_number) * 100, 1)
            })

    return {
        'years_to_fire': year,
        'final_portfolio': round(portfolio, 2),
        'fire_achieved': portfolio >= target_fire_number,
        'milestones': milestones
    }


def calculate_fire_savings_rate(annual_income, annual_expense):
    """
    Calculate savings rate and years to FIRE assuming constant returns.

    Returns:
        dict with savings_rate, years_estimate (simplified)
    """
    savings_rate = ((annual_income - annual_expense) / annual_income) * 100 if annual_income > 0 else 0

    # Very rough estimate: 25 / savings_rate (Shania Johnson rule)
    years_estimate = 25 / (savings_rate + 1) if savings_rate > 0 else 0

    return {
        'savings_rate_pct': round(savings_rate, 1),
        'annual_savings': round(annual_income - annual_expense, 2),
        'years_to_fire_estimate': round(years_estimate, 1)
    }
