> This repository is part of the **Revenue-Intelligence-Platform-Suite**
> Main platform: ../../README.md

# Amazon Sales Analysis

Commercial analytics project focused on discount leakage, revenue protection, category prioritization, and executive business framing.

## Language

- English: [docs/README.en.md](docs/README.en.md)
- Portugues (BR): [docs/README.pt-BR.md](docs/README.pt-BR.md)
- Portugues (PT): [docs/README.pt-PT.md](docs/README.pt-PT.md)

## Executive Summary

This repository addresses a practical revenue efficiency problem: discounting can preserve volume while quietly eroding value.
The project is structured to show how commercial analytics can move beyond descriptive reporting and become a decision-support asset for Revenue Operations, Sales Leadership, and Category Management.

North Star metric:

- **Net Revenue Retained (NRR)** = `net revenue / gross revenue before discounts`

Current baseline from the processed dataset:

- Net revenue: **$32.87M**
- Discount leakage: **$5.05M**
- Net Revenue Retained: **86.69%**
- Upside at 5% leakage recovery: **+$252.3K**

## Business Context

Marketplace-style operations often optimize for sales volume while losing value through uncontrolled discounts.
This repository is built to answer three business questions:

1. Where is discount leakage eroding revenue most?
2. Which categories represent the highest recoverable value?
3. What is the financial upside of tighter discount governance?

## What This Repository Proves

- Business-facing KPI design for revenue protection
- Reproducible analytics pipeline for discount leakage analysis
- Data quality enforcement before business outputs
- Category-level prioritization instead of generic reporting
- Executive framing for commercial decision-making

## Business Metrics Snapshot

- Net Revenue: **$32.87M**
- Discount Leakage: **$5.05M**
- North Star (NRR): **86.69%**
- Upside at 5% leakage recovery: **+$252.3K**

## Dataset

- Source: Kaggle (`aliiihussain/amazon-sales-dataset`)
- Link: https://www.kaggle.com/datasets/aliiihussain/amazon-sales-dataset
- Scope: 50,000 transactions
- Main entities: order, product category, price, discount, region, payment method, rating

## Analytical Approach

1. Data ingestion with fallback logic for local execution
2. Data quality enforcement through schema checks, clipping, and invalid-row removal
3. Feature engineering for business metrics such as `gross_revenue`, `discount_value`, and `NRR`
4. Opportunity ranking by category-level discount leakage
5. Executive dashboard outputs and artifacts for decision support

## Repository Structure

```text
amazon-sales-analysis/
|-- app/
|   `-- streamlit_app.py
|-- assets/
|   |-- amazon_logo.svg
|   `-- custom.css
|-- data/
|   |-- raw/
|   `-- processed/
|-- docs/
|   |-- README.en.md
|   `-- README.pt-BR.md
|-- notebooks/
|-- reports/
|   |-- figures/
|   `-- tables/
|-- scripts/
|   `-- run_pipeline.py
|-- src/amazon_sales_analysis/
|   |-- analytics.py
|   |-- config.py
|   |-- data_ingestion.py
|   |-- data_preprocessing.py
|   |-- eda.py
|   |-- evaluation.py
|   |-- feature_engineering.py
|   |-- logging_config.py
|   |-- modeling.py
|   `-- visualization.py
|-- tests/
|-- main.py
|-- pyproject.toml
|-- requirements.txt
`-- Dockerfile
```

## Results

- Net revenue retained baseline: **86.69%**
- Discount leakage identified: **$5.05M**
- Highest-revenue category: **Beauty ($5.55M)**
- Prioritized opportunities exported to `reports/tables/discount_opportunities.csv`

## Business Impact

- 5% leakage recovery scenario: **+$252.3K** net revenue
- 10% leakage recovery scenario: **+$504.7K** net revenue
- Decision impact: supports discount policy redesign by category and promotional channel

Business framing:

**Recovering only 5% of discount leakage can add roughly $252K without increasing acquisition spend.**

## Recommendations

- Cap discount depth for high-leakage categories and monitor weekly NRR
- Shift campaign strategy from blanket discounts to category-specific thresholds
- Track `discount_to_revenue_ratio` as a governance KPI in leadership reviews
- Pilot policy changes in top leakage categories before broader rollout

## Quality, Contracts, and CI

- Raw data contract: `contracts/sales_dataset.contract.json`
- Product metrics contract: `contracts/product_metrics.contract.json`
- Quality gates enforce schema integrity, invalid-value removal, and metrics generation

Local quality commands:

```bash
pip install -r requirements-dev.txt
black --check .
isort --check-only .
ruff check .
mypy src scripts
pytest
```

CI baseline:

- Workflow: `.github/workflows/ci.yml`
- Gates: formatting, lint, type checking, tests, and coverage threshold (`>=70%`)
- Metrics artifacts exported in `reports/metrics/`

## How to Run

### Local

```bash
git clone https://github.com/samuelmaia-analytics/amazon-sales-analysis.git
cd amazon-sales-analysis
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

### Docker

```bash
docker build -t amazon-sales-analytics .
docker run --rm -p 8501:8501 amazon-sales-analytics
```

## Release Process

1. Update `CHANGELOG.md`
2. Bump version with `python scripts/bump_version.py <version>`
3. Commit, tag, and push
4. Let the release workflow validate version and changelog consistency

## Future Improvements

- Add scenario simulation for category discount policy changes
- Add anomaly detection on discount spikes
- Expose metrics through a FastAPI endpoint for BI integration

## Where It Fits in the Platform

- Layer: Pipeline + App + Quality
- Inputs: Amazon sales raw files, pricing, discount, and channel data
- Outputs: KPI tables, leakage analysis, Streamlit views, and tested data contracts

## Author

Samuel Maia

- GitHub: https://github.com/samuelmaia-analytics
- LinkedIn: https://linkedin.com/in/samuelmaia-analytics
- Email: smaia2@gmail.com
