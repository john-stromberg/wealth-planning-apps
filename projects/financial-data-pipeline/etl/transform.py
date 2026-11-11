"""
Transformation logic for aligning market/economic/client datasets.
"""

import pandas as pd


def normalize_dates(df: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    out = df.copy()
    out[column] = pd.to_datetime(out[column])
    return out


def build_monthly_feature_set(market_df: pd.DataFrame, econ_df: pd.DataFrame, cashflow_df: pd.DataFrame) -> pd.DataFrame:
    market = normalize_dates(market_df, "date")
    econ = normalize_dates(econ_df, "date")
    cash = normalize_dates(cashflow_df, "date")

    merged = market.merge(econ, on="date", how="left").merge(cash, on="date", how="left")

    merged = merged.sort_values("date").reset_index(drop=True)
    merged["sp500_return_1m"] = merged["sp500_level"].pct_change().fillna(0.0)
    merged["bond_return_1m"] = merged["bond_index"].pct_change().fillna(0.0)
    merged["net_flow"] = merged["inflows"].fillna(0.0) - merged["outflows"].fillna(0.0)

    return merged
