"""
Tax-aware portfolio growth calculations.
"""

def calculate_tax_aware_growth(initial_portfolio, annual_contribution, annual_return,
                              tax_bracket, years, capital_gains_tax_rate=0.15):
    """
    Project portfolio growth accounting for capital gains taxes.

    Returns:
        dict with after_tax_portfolio, pre_tax_portfolio, taxes_paid, effective_return
    """
    pre_tax_portfolio = initial_portfolio
    after_tax_portfolio = initial_portfolio
    total_taxes = 0

    for year in range(years):
        # Pre-tax growth
        pre_tax_growth = pre_tax_portfolio * annual_return
        pre_tax_portfolio += pre_tax_growth + annual_contribution

        # After-tax growth (simplified: tax on gains only)
        after_tax_growth = after_tax_portfolio * annual_return * (1 - capital_gains_tax_rate)
        after_tax_portfolio += after_tax_growth + annual_contribution
        total_taxes += after_tax_growth * (capital_gains_tax_rate / (1 - capital_gains_tax_rate))

    effective_return = (annual_return * (1 - capital_gains_tax_rate)) * 100

    return {
        'pre_tax_portfolio': round(pre_tax_portfolio, 2),
        'after_tax_portfolio': round(after_tax_portfolio, 2),
        'total_taxes_paid': round(total_taxes, 2),
        'tax_drag': round(pre_tax_portfolio - after_tax_portfolio, 2),
        'effective_after_tax_return': round(effective_return, 2)
    }


def calculate_tax_bracket_impact(annual_income, investment_gains, tax_brackets):
    """
    Calculate federal tax liability and impact of investment gains.
    Simplified US tax model for MVP.

    Returns:
        dict with tax_liability, marginal_rate, effective_rate
    """
    # Simplified 2024-ish brackets (single filer)
    default_brackets = [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ]

    brackets = tax_brackets or default_brackets
    taxable_income = annual_income + (investment_gains * 0.15)  # Simplified long-term cap gains

    tax = 0
    previous_limit = 0
    marginal_rate = 0.10

    for limit, rate in brackets:
        if taxable_income > limit:
            tax += (limit - previous_limit) * rate
            marginal_rate = rate
            previous_limit = limit
        else:
            tax += (taxable_income - previous_limit) * rate
            break

    effective_rate = (tax / taxable_income * 100) if taxable_income > 0 else 0

    return {
        'total_tax_liability': round(tax, 2),
        'marginal_tax_rate': round(marginal_rate * 100, 1),
        'effective_tax_rate': round(effective_rate, 2),
        'after_tax_income': round(annual_income - tax, 2)
    }
