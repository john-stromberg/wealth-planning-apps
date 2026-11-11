"""
Load layer for writing curated outputs.
"""

import os
import pandas as pd


def write_curated_csv(df: pd.DataFrame, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
