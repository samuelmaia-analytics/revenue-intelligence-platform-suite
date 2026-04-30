# Revenue Intelligence Architecture

## Layered design

- `src/ingestion`: raw source normalization and Bronze materialization.
- `src/transform`: Silver standardization and feature creation.
- `src/analytics`: semantic KPI layer, recommendation logic, executive reporting.
- `src/models`: churn and next-purchase model training/scoring.
- `src/orchestration`: end-to-end pipeline execution and stage logging.
- `src/dashboard`: backend service consumed by Streamlit.
- `app/streamlit_app.py`: presentation layer only.

## End-to-end flow

1. `run_pipeline.py` or `main.py` loads centralized configuration from environment variables.
2. Ingestion reads the Kaggle CSV or generates deterministic synthetic data.
3. Bronze stores auditable copies with source metadata and ingestion timestamp.
4. Silver applies schema checks, null handling, deduplication and referential consistency validation.
5. Feature engineering creates customer-level attributes used by ML and analytics.
6. Gold star schema publishes `dim_customers`, `dim_date`, `dim_channel`, and `fact_orders`.
7. Semantic layer computes Revenue, Growth Rate, ARPU, Retention, Churn, LTV/CAC and action priorities.
8. Reporting publishes executive artifacts and the dashboard service reads them without re-implementing business logic.

## Data quality controls

- Required columns validation on Bronze and Silver.
- Null checks for business-critical columns.
- Duplicate checks on primary identifiers.
- Referential consistency between orders and customers.
- Non-negative marketing spend and positive order value rules.
- JSON quality report emitted to `data/processed/data_quality_report.json`.

## Observability

- Structured JSON logs are emitted for each pipeline stage.
- File output: `logs/pipeline.log`
- Key stages: `ingestion`, `transformation`, `analytics_prep`, `modeling`, `warehouse`, `analytics`, `pipeline`
