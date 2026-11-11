"""
Extraction layer for raw source files.
"""

import pandas as pd


def load_market_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_economic_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_client_cashflows(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
