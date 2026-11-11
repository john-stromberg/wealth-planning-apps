"""
Basic data quality checks.
"""

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "sp500_level",
    "bond_index",
    "cpi_yoy",
    "fed_funds_rate",
    "inflows",
    "outflows",
]


def validate_required_columns(df: pd.DataFrame) -> list[str]:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing


def validate_null_threshold(df: pd.DataFrame, threshold: float = 0.10) -> dict:
    ratios = df.isnull().mean().to_dict()
    violations = {k: v for k, v in ratios.items() if v > threshold}
    return violations


def run_quality_checks(df: pd.DataFrame) -> dict:
    missing = validate_required_columns(df)
    null_violations = validate_null_threshold(df)

    return {
        "row_count": len(df),
        "missing_columns": missing,
        "null_threshold_violations": null_violations,
        "passed": len(missing) == 0 and len(null_violations) == 0,
    }
