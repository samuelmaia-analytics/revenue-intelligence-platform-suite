# dbt Layer (Modern Data Stack)

This dbt project adds an Analytics Engineering layer to `revenue-intelligence`.

## Layers

- `staging`: source standardization
- `intermediate`: reusable business transformations
- `marts`: KPI-ready data products

## Warehouse targets

- BigQuery (`target: dev`)
- Snowflake (`target: snowflake`)

## Quick start

```bash
cd modules/revenue-intelligence/dbt
cp profiles.yml.example ~/.dbt/profiles.yml
dbt debug --target dev
dbt run --target dev
dbt test --target dev
```

For Snowflake:

```bash
dbt debug --target snowflake
dbt run --target snowflake
dbt test --target snowflake
```

## Raw expectations

The following raw tables must exist in your warehouse schema:

- `customers`
- `orders`
- `marketing_spend`

You can create/load them from the Python pipeline using `RIP_WAREHOUSE_PROVIDER` in `main.py`.

## dbt Docs (Published)

GitHub Pages publication is automated by:
- `.github/workflows/dbt-docs.yml`

Expected URL pattern:
- `https://<github-user>.github.io/revenue-intelligence-platform-suite/`

Required GitHub repository secrets:
- `DBT_BIGQUERY_PROJECT`
- `DBT_BIGQUERY_DATASET`
- `DBT_BIGQUERY_LOCATION`
- `DBT_BIGQUERY_KEYFILE_JSON`

Local docs generation:

```bash
cd modules/revenue-intelligence/dbt
dbt parse --target dev
dbt docs generate --target dev
dbt docs serve --port 8080
```
