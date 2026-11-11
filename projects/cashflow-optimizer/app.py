"""
Cashflow Optimizer - Advisor cashflow allocation tool.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from calculators.allocation import AllocationInputs, recommended_allocation
from calculators.scenarios import compare_allocation_strategies


st.set_page_config(page_title="Cashflow Optimizer", page_icon="💸", layout="wide")

st.title("💸 Cashflow Optimizer")
st.markdown("Optimize monthly cashflow across emergency reserves, debt payoff, and investing.")

st.sidebar.header("Household Inputs")
monthly_income = st.sidebar.number_input("Monthly Income ($)", min_value=1000, max_value=200000, value=15000, step=500)
fixed_expenses = st.sidebar.number_input("Fixed Expenses ($)", min_value=0, max_value=150000, value=7000, step=250)
variable_expenses = st.sidebar.number_input("Variable Expenses ($)", min_value=0, max_value=150000, value=2500, step=250)

st.sidebar.subheader("Emergency Fund")
emergency_current = st.sidebar.number_input("Current Emergency Fund ($)", min_value=0, max_value=2000000, value=15000, step=1000)
emergency_months_target = st.sidebar.slider("Target Months of Expenses", min_value=1, max_value=12, value=6, step=1)

st.sidebar.subheader("Debt")
debt_balance = st.sidebar.number_input("High-Interest Debt Balance ($)", min_value=0, max_value=2000000, value=25000, step=1000)
debt_apr = st.sidebar.slider("Debt APR (%)", min_value=0.0, max_value=40.0, value=18.0, step=0.5)

st.sidebar.subheader("Policy")
retirement_match_pct = st.sidebar.slider("Retirement Match Contribution (%)", min_value=0.0, max_value=15.0, value=6.0, step=0.5)
base_investing_pct = st.sidebar.slider("Base Investing Target (%)", min_value=0.0, max_value=30.0, value=10.0, step=0.5)

if st.sidebar.button("Run Optimization", use_container_width=True):
    inputs = AllocationInputs(
        monthly_income=monthly_income,
        fixed_expenses=fixed_expenses,
        variable_expenses=variable_expenses,
        emergency_fund_current=emergency_current,
        emergency_fund_target_months=emergency_months_target,
        high_interest_debt_balance=debt_balance,
        high_interest_debt_apr=debt_apr,
        retirement_match_pct=retirement_match_pct,
        base_investing_pct=base_investing_pct,
    )
    result = recommended_allocation(inputs)
    st.session_state.result = result
    st.session_state.inputs = inputs

if "result" in st.session_state:
    result = st.session_state.result
    inputs = st.session_state.inputs

    st.header("Recommended Monthly Allocation")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monthly Surplus", f"${result['monthly_surplus']:,.0f}")
    c2.metric("Emergency Target", f"${result['emergency_target']:,.0f}")
    c3.metric("Emergency Gap", f"${result['emergency_gap']:,.0f}")
    c4.metric("Discretionary Remaining", f"${result['discretionary']:,.0f}")

    alloc_df = pd.DataFrame(
        {
            "Bucket": [
                "Retirement Match",
                "Emergency Fund",
                "Debt Paydown",
                "Investing",
                "Discretionary",
            ],
            "Amount": [
                result["retirement_match_contrib"],
                result["emergency_contrib"],
                result["debt_paydown"],
                result["investing"],
                result["discretionary"],
            ],
        }
    )

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.dataframe(alloc_df, use_container_width=True)
    with col_right:
        fig = px.pie(alloc_df, names="Bucket", values="Amount", title="Allocation Mix")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("What-if Strategy Comparison")

    strategy_a = {
        "emergency_contrib": result["emergency_contrib"],
        "debt_paydown": result["debt_paydown"],
    }

    # Alternate strategy: shift 20% from debt to emergency (if debt allocation exists)
    shift = result["debt_paydown"] * 0.20
    strategy_b = {
        "emergency_contrib": result["emergency_contrib"] + shift,
        "debt_paydown": max(0.0, result["debt_paydown"] - shift),
    }

    comparison = compare_allocation_strategies(
        emergency_current=inputs.emergency_fund_current,
        emergency_target=result["emergency_target"],
        debt_balance=inputs.high_interest_debt_balance,
        debt_apr=inputs.high_interest_debt_apr,
        strategy_a=strategy_a,
        strategy_b=strategy_b,
    )

    compare_df = pd.DataFrame(
        {
            "Metric": ["Emergency Fund Completion (months)", "Debt Payoff (months)"],
            "Recommended Strategy": [
                comparison["strategy_a"]["emergency_fund_months"],
                comparison["strategy_a"]["debt_payoff_months"],
            ],
            "Alt Strategy (more emergency)": [
                comparison["strategy_b"]["emergency_fund_months"],
                comparison["strategy_b"]["debt_payoff_months"],
            ],
        }
    )

    st.dataframe(compare_df, use_container_width=True)
else:
    st.info("Configure inputs in the sidebar and click Run Optimization.")
