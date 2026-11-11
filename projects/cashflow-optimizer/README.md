# Cashflow Optimizer

Practical advisor tool for monthly cashflow allocation across emergency reserves, debt reduction, retirement match capture, and investing.

## Features
- Monthly surplus calculation
- Rule-based recommended allocation
- Emergency fund target and gap tracking
- Debt payoff prioritization for high-interest balances
- What-if comparison of alternative allocation mix
- Interactive Streamlit UI with charts and tables

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Install
```bash
git clone https://github.com/john-stromberg/cashflow-optimizer.git
cd cashflow-optimizer
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

## Project Structure
- `app.py` - Streamlit UI
- `calculators/allocation.py` - core allocation rule engine
- `calculators/scenarios.py` - scenario timeline and comparison helpers

## Notes
This is an MVP intended for advisor workflow support. Results are illustrative and not financial advice.
