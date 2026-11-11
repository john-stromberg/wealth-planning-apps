# Financial Data Pipeline

Lightweight ETL MVP for advisor workflows: market, economic, and client cashflow data ingestion into a curated monthly feature set.

## Features
- Raw CSV ingestion (market, economic, client cashflows)
- Date normalization and dataset merge
- Derived monthly features (equity return, bond return, net flow)
- Data quality checks (required columns + null threshold)
- Curated output export to `data/curated/monthly_feature_set.csv`

## Project Structure
- `pipeline.py` - pipeline runner
- `etl/extract.py` - extraction helpers
- `etl/transform.py` - transform/feature engineering
- `etl/quality.py` - quality checks
- `etl/load.py` - curated output writer
- `data/raw/*.csv` - sample input datasets

## Setup
```bash
git clone https://github.com/john-stromberg/financial-data-pipeline.git
cd financial-data-pipeline
pip install -r requirements.txt
python pipeline.py
```

## Output
After running, curated data is written to:
- `data/curated/monthly_feature_set.csv`

## Notes
This MVP uses sample CSV inputs and is intended for workflow prototyping.
