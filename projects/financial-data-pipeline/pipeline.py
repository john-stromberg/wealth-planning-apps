"""
Financial Data Pipeline MVP runner.
"""

from pathlib import Path

from etl.extract import load_client_cashflows, load_economic_data, load_market_data
from etl.load import write_curated_csv
from etl.quality import run_quality_checks
from etl.transform import build_monthly_feature_set


def run_pipeline(base_dir: Path):
    raw_dir = base_dir / "data" / "raw"
    curated_dir = base_dir / "data" / "curated"

    market = load_market_data(str(raw_dir / "market_data.csv"))
    econ = load_economic_data(str(raw_dir / "economic_data.csv"))
    cash = load_client_cashflows(str(raw_dir / "client_cashflows.csv"))

    feature_set = build_monthly_feature_set(market, econ, cash)

    quality = run_quality_checks(feature_set)
    output_path = curated_dir / "monthly_feature_set.csv"
    write_curated_csv(feature_set, str(output_path))

    return {
        "output_path": str(output_path),
        "quality": quality,
        "row_count": len(feature_set),
    }


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    result = run_pipeline(base)

    print("Pipeline completed")
    print(f"Output: {result['output_path']}")
    print(f"Rows: {result['row_count']}")
    print(f"Quality passed: {result['quality']['passed']}")
    if result["quality"]["missing_columns"]:
        print(f"Missing columns: {result['quality']['missing_columns']}")
    if result["quality"]["null_threshold_violations"]:
        print(f"Null threshold violations: {result['quality']['null_threshold_violations']}")
