# dbt Docs Publishing (GitHub Pages)

This project publishes dbt documentation for `modules/revenue-intelligence/dbt` using:
- `.github/workflows/dbt-docs.yml`

## 1. Enable GitHub Pages

In repository settings:
1. Open `Settings -> Pages`
2. In `Build and deployment`, set `Source` to `GitHub Actions`

## 2. Add repository secrets

Create these repository secrets:
- `DBT_BIGQUERY_PROJECT`
- `DBT_BIGQUERY_DATASET`
- `DBT_BIGQUERY_LOCATION`
- `DBT_BIGQUERY_KEYFILE_JSON`

Notes:
- `DBT_BIGQUERY_KEYFILE_JSON` must be the full JSON content of a BigQuery service account key.
- Service account needs permissions to read/write the target dataset.

## 3. Run the workflow

Option A:
- Trigger `dbt-docs` manually from `Actions -> dbt-docs -> Run workflow`

Option B:
- Push to `main` changing files under `modules/revenue-intelligence/dbt/**`

## 4. Verify publication

After a successful run, open:
- `https://<github-user>.github.io/revenue-intelligence-platform-suite/`

If publication fails, check:
- Pages source configuration
- missing/invalid secrets
- BigQuery permissions for the service account
