"""
Wealth Planning Calculator - Streamlit App
Multi-scenario analysis for retirement, FIRE, tax-aware growth, and inflation.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from calculators.retirement import calculate_retirement_date, calculate_safe_withdrawal_rate
from calculators.fire import calculate_fire_number, calculate_fire_timeline, calculate_fire_savings_rate
from calculators.tax_aware_growth import calculate_tax_aware_growth, calculate_tax_bracket_impact
from calculators.inflation import calculate_inflation_adjusted_expenses, calculate_future_value_with_inflation

st.set_page_config(page_title="Wealth Planning Calculator", layout="wide")

st.title("💰 Wealth Planning Calculator")
st.write("Comprehensive retirement and wealth scenario modeling for advisors.")

# Sidebar inputs
st.sidebar.header("Client Profile")
current_age = st.sidebar.slider("Current Age", 20, 75, 45)
retirement_age = st.sidebar.slider("Target Retirement Age", 50, 80, 65)
current_portfolio = st.sidebar.number_input("Current Portfolio ($)", 0, 5000000, 500000)
annual_income = st.sidebar.number_input("Annual Income ($)", 0, 1000000, 150000)
annual_expense = st.sidebar.number_input("Annual Living Expenses ($)", 0, 500000, 60000)
annual_savings = annual_income - annual_expense

st.sidebar.header("Market Assumptions")
annual_return = st.sidebar.slider("Expected Annual Return (%)", 2.0, 12.0, 7.0) / 100
inflation_rate = st.sidebar.slider("Expected Inflation (%)", 1.0, 5.0, 3.0) / 100
tax_bracket = st.sidebar.slider("Federal Tax Bracket (%)", 10, 37, 24)
capital_gains_tax = st.sidebar.slider("Long-Term Capital Gains Rate (%)", 0, 20, 15) / 100

years_to_project = retirement_age - current_age

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Retirement Planning",
    "FIRE Analysis",
    "Tax-Aware Growth",
    "Inflation Impact"
])

# ============ TAB 1: Retirement Planning ============
with tab1:
    st.header("Retirement Planning")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Retirement Feasibility")

        # Calculate retirement scenarios
        base_case = calculate_retirement_date(
            current_age, retirement_age, current_portfolio,
            annual_savings, annual_return, inflation_rate, annual_expense
        )

        optimistic_case = calculate_retirement_date(
            current_age, retirement_age, current_portfolio,
            annual_savings, annual_return * 1.2, inflation_rate, annual_expense
        )

        pessimistic_case = calculate_retirement_date(
            current_age, retirement_age, current_portfolio,
            annual_savings, annual_return * 0.8, inflation_rate, annual_expense
        )

        # Display key metrics
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Base Case Portfolio", f"${base_case['portfolio_at_retirement']:,.0f}")
        with col_b:
            st.metric("Optimistic Portfolio", f"${optimistic_case['portfolio_at_retirement']:,.0f}")
        with col_c:
            st.metric("Pessimistic Portfolio", f"${pessimistic_case['portfolio_at_retirement']:,.0f}")

        # Safe withdrawal rate analysis
        swr_base = calculate_safe_withdrawal_rate(
            base_case['portfolio_at_retirement'],
            annual_expense,
            30
        )

        st.subheader("Safe Withdrawal Rate Analysis")
        st.metric("SWR Status", swr_base['swr_status'], swr_base['safe_withdrawal_rate'])
        st.write(f"**Annual Withdrawal Rate:** {swr_base['safe_withdrawal_rate']:.2f}%")
        st.write(f"**Sustainability:** {swr_base['is_sustainable'] and '✅ Sustainable' or '❌ At Risk'}")
        st.write(f"**Portfolio Remaining (30 years):** ${swr_base['remaining_at_end']:,.0f}")

    with col2:
        # Portfolio growth chart
        scenarios = {
            'Base Case': base_case['portfolio_at_retirement'],
            'Optimistic': optimistic_case['portfolio_at_retirement'],
            'Pessimistic': pessimistic_case['portfolio_at_retirement']
        }

        fig = go.Figure(data=[
            go.Bar(x=list(scenarios.keys()), y=list(scenarios.values()),
                   marker_color=['#1f77b4', '#2ca02c', '#d62728'])
        ])
        fig.update_layout(
            title="Portfolio at Retirement by Scenario",
            yaxis_title="Portfolio Value ($)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    # Year-by-year projection
    st.subheader("Detailed Projection (Base Case)")
    projection_data = []
    portfolio = current_portfolio
    for year in range(years_to_project + 1):
        age = current_age + year
        growth = portfolio * annual_return
        portfolio += growth + annual_savings
        projection_data.append({
            'Year': year,
            'Age': age,
            'Portfolio': portfolio,
            'Annual Savings': annual_savings,
            'Investment Growth': growth
        })

    df_projection = pd.DataFrame(projection_data)
    st.dataframe(df_projection, use_container_width=True)

# ============ TAB 2: FIRE Analysis ============
with tab2:
    st.header("FIRE (Financial Independence, Retire Early) Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("FIRE Number Calculation")

        fire_metrics = calculate_fire_number(annual_expense, 0.04)
        fire_timeline = calculate_fire_timeline(
            current_portfolio, annual_savings, annual_return, fire_metrics['fire_number']
        )
        savings_rate = calculate_fire_savings_rate(annual_income, annual_expense)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("FIRE Number (4% Rule)", f"${fire_metrics['fire_number']:,.0f}")
        with col_b:
            st.metric("Current Portfolio", f"${current_portfolio:,.0f}")

        progress = (current_portfolio / fire_metrics['fire_number']) * 100
        st.progress(min(progress / 100, 1.0))
        st.write(f"**Progress to FIRE:** {progress:.1f}%")

        st.subheader("Savings Rate Analysis")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Annual Savings", f"${annual_savings:,.0f}")
        with col_b:
            st.metric("Savings Rate", f"{savings_rate['savings_rate_pct']:.1f}%")
        with col_c:
            st.metric("Est. Years to FIRE", f"{savings_rate['years_to_fire_estimate']:.1f}")

    with col2:
        st.subheader("Years to FIRE Goal")
        years_to_fire = fire_timeline['years_to_fire']
        fire_age = current_age + years_to_fire

        if fire_timeline['fire_achieved']:
            st.success(f"✅ FIRE achievable in **{years_to_fire} years** (age {fire_age})")
        else:
            st.warning(f"⚠️ FIRE not achievable within 60 years with current assumptions")

        st.metric("Final Portfolio", f"${fire_timeline['final_portfolio']:,.0f}")

        # Milestone chart
        if fire_timeline['milestones']:
            milestones_df = pd.DataFrame(fire_timeline['milestones'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=milestones_df['year'],
                y=milestones_df['portfolio'],
                mode='lines+markers',
                name='Portfolio Growth',
                line=dict(color='#1f77b4', width=2)
            ))
            fig.add_hline(y=fire_metrics['fire_number'], line_dash='dash', 
                         line_color='#2ca02c', annotation_text="FIRE Number")
            fig.update_layout(
                title="Path to FIRE",
                xaxis_title="Years",
                yaxis_title="Portfolio ($)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

# ============ TAB 3: Tax-Aware Growth ============
with tab3:
    st.header("Tax-Aware Portfolio Growth")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Projection with Tax Impact")

        tax_result = calculate_tax_aware_growth(
            current_portfolio, annual_savings, annual_return,
            tax_bracket / 100, years_to_project, capital_gains_tax
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Pre-Tax Portfolio", f"${tax_result['pre_tax_portfolio']:,.0f}")
        with col_b:
            st.metric("After-Tax Portfolio", f"${tax_result['after_tax_portfolio']:,.0f}")

        st.metric("Total Tax Drag", f"${tax_result['tax_drag']:,.0f}")
        st.write(f"**Effective After-Tax Return:** {tax_result['effective_after_tax_return']:.2f}%")

        st.subheader("Tax Bracket Analysis")
        tax_impact = calculate_tax_bracket_impact(annual_income, 0, None)
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Tax Liability", f"${tax_impact['total_tax_liability']:,.0f}")
        with col_b:
            st.metric("Effective Rate", f"{tax_impact['effective_tax_rate']:.2f}%")

    with col2:
        st.subheader("Tax Impact Comparison")

        tax_comparison = {
            'Pre-Tax': tax_result['pre_tax_portfolio'],
            'After-Tax': tax_result['after_tax_portfolio']
        }

        fig = go.Figure(data=[
            go.Bar(
                x=['Portfolio Value'],
                y=[tax_comparison['Pre-Tax']],
                name='Pre-Tax',
                marker_color='#2ca02c'
            ),
            go.Bar(
                x=['Portfolio Value'],
                y=[tax_comparison['After-Tax']],
                name='After-Tax',
                marker_color='#d62728'
            )
        ])
        fig.update_layout(
            barmode='group',
            title="Pre-Tax vs After-Tax Growth",
            yaxis_title="Portfolio Value ($)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 4: Inflation Impact ============
with tab4:
    st.header("Inflation Impact Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Purchasing Power Erosion")

        inflation_impact = calculate_future_value_with_inflation(
            current_portfolio, inflation_rate, years_to_project
        )

        st.metric("Future Nominal Value", f"${current_portfolio:,.0f}")
        st.metric("Future Real Value (inflation-adjusted)", 
                 f"${inflation_impact['future_real_value']:,.0f}")
        st.metric("Purchasing Power Lost", 
                 f"{inflation_impact['purchasing_power_lost_pct']:.1f}%")

        st.subheader("Inflation-Adjusted Expenses")
        expense_projection = calculate_inflation_adjusted_expenses(
            annual_expense, inflation_rate, min(years_to_project, 30)
        )

        years_shown = min(10, len(expense_projection))
        expense_df = pd.DataFrame(expense_projection[:years_shown])
        st.dataframe(expense_df, use_container_width=True)

    with col2:
        st.subheader("Expense Growth Over Time")

        expense_df_full = pd.DataFrame(expense_projection)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=expense_df_full['year'],
            y=expense_df_full['nominal_expense'],
            mode='lines',
            name='Annual Expense',
            line=dict(color='#ff7f0e', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=expense_df_full['year'],
            y=expense_df_full['cumulative_total'],
            mode='lines',
            name='Cumulative Expense',
            line=dict(color='#d62728', width=2, dash='dash')
        ))
        fig.update_layout(
            title="Inflation-Adjusted Expense Projection",
            xaxis_title="Years",
            yaxis_title="Amount ($)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.write("""
**Disclaimer:** This calculator uses simplified models for demonstration purposes. 
Actual retirement planning should incorporate professional advice, detailed tax analysis, 
and comprehensive financial planning. All results are hypothetical and based on the 
assumptions provided.
""")
