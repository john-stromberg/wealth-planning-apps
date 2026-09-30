"""
Report generation for wealth planning scenarios.
"""

import pandas as pd
from datetime import datetime

def generate_scenario_report(client_name, current_age, retirement_age, 
                            current_portfolio, annual_income, annual_expense,
                            annual_return, inflation_rate, retirement_data):
    """
    Generate a comprehensive retirement scenario report.

    Returns:
        str: formatted report text
    """
    report = f"""
WEALTH PLANNING SCENARIO REPORT
Generated: {datetime.now().strftime('%B %d, %Y')}

CLIENT INFORMATION
==================
Name: {client_name}
Current Age: {current_age}
Target Retirement Age: {retirement_age}
Years to Retirement: {retirement_age - current_age}

CURRENT FINANCIAL POSITION
===========================
Portfolio Value: ${current_portfolio:,.2f}
Annual Income: ${annual_income:,.2f}
Annual Expenses: ${annual_expense:,.2f}
Annual Savings: ${annual_income - annual_expense:,.2f}

MARKET ASSUMPTIONS
===================
Expected Annual Return: {annual_return * 100:.1f}%
Expected Inflation Rate: {inflation_rate * 100:.1f}%

RETIREMENT PROJECTION (BASE CASE)
==================================
Portfolio at Retirement: ${retirement_data['portfolio_at_retirement']:,.2f}
Years to Retirement: {retirement_data['years_to_retirement']}
Annual Expense Needs: ${retirement_data['annual_expense']:,.2f}

SUSTAINABILITY ANALYSIS
=======================
Safe Withdrawal Rate: {retirement_data.get('swr', 'N/A')}%
Status: {retirement_data.get('status', 'Needs calculation')}

RECOMMENDATIONS
================
- Review and rebalance portfolio annually
- Consider tax-loss harvesting strategies
- Plan for Social Security optimization
- Evaluate healthcare costs pre-65

This report is for planning purposes only and should not be considered investment advice.
Consult with a qualified financial advisor for personalized recommendations.
"""
    return report


def export_projection_csv(projection_data, filename):
    """
    Export detailed year-by-year projection to CSV.

    Returns:
        pd.DataFrame
    """
    df = pd.DataFrame(projection_data)
    # Format currency columns
    currency_cols = ['Portfolio', 'Annual Savings', 'Investment Growth']
    for col in currency_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"${x:,.2f}")

    return df
