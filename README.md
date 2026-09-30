# Wealth Planning Calculator

Professional wealth planning and retirement scenario modeling tool for financial advisors.

## Features

### Retirement Planning
- Projected portfolio growth to retirement date
- Safe withdrawal rate (SWR) analysis using 4% rule
- Base case, optimistic, and pessimistic scenarios
- Year-by-year detailed projections

### FIRE Analysis
- Financial Independence Retire Early number calculation
- Timeline to FIRE goal achievement
- Savings rate and progress tracking
- Milestone visualization

### Tax-Aware Growth
- After-tax portfolio projections accounting for capital gains taxes
- Federal tax bracket analysis
- Tax drag visualization
- Effective after-tax return calculations

### Inflation Impact
- Purchasing power erosion analysis
- Inflation-adjusted expense projections
- Cumulative expense tracking
- Multi-year scenario planning

## Stack
- Python 3.9+
- Streamlit 1.28+
- Pandas, NumPy for calculations
- Plotly for interactive visualizations

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage Workflow

1. **Set Client Profile**
   - Adjust current age, target retirement age
   - Input current portfolio and annual income/expenses

2. **Set Market Assumptions**
   - Expected returns, inflation, tax rates

3. **Explore Scenarios**
   - Review retirement planning across 3 scenarios
   - Analyze FIRE feasibility and timeline
   - Examine tax impact on wealth
   - Project inflation effects on expenses

4. **Share Results**
   - Export charts and data for client meetings
   - Use for proposal conversations

## Key Calculations

### 4% Safe Withdrawal Rule
Assumes you can safely withdraw 4% of your portfolio annually in retirement.

### FIRE Number
Portfolio size needed to support annual expenses in perpetuity = Annual Expense / 0.04

### Tax-Aware Growth
Accounts for capital gains taxes (15% long-term assumed) reducing effective returns.

### Inflation Adjustment
Compounds expenses annually by inflation rate to show future nominal costs.

## Limitations (MVP)

- Simplified tax models (does not cover all deductions, credits, AMT)
- Fixed allocation strategy (does not rebalance)
- No Monte Carlo distribution analysis (see Portfolio Risk Lab for that)
- No integration with live market data (can add via financial-data-pipeline)

## Future Enhancements

- Integration with real market data feeds
- Monte Carlo simulation for probability analysis
- Roth vs. Traditional IRA optimization
- Social Security planning
- Sequence of returns risk analysis
- PDF report generation

## Integration

This tool is part of the **Advisory Workflow Dashboard** suite. Access from:
- Dashboard Hub: https://github.com/john-stromberg/advisory-workflow-dashboard
- Module Registry: Listed as `wealth-planning-calculator`

## Development

### Adding a New Calculator
1. Create module in `calculators/` folder
2. Import and use in relevant tab in `app.py`
3. Test with sample inputs

### Extending the UI
- Add new tabs for additional features
- Use Streamlit widgets (sliders, inputs, etc.)
- Display results with st.metric() and plotly charts

## Support

For issues or feature requests, open an issue on GitHub.
