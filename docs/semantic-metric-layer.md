# Semantic Metric Layer

## Purpose
Make KPI definitions explicit, versionable, and reusable across dashboards, API responses, and client implementations.

## Current Root Catalog
The root semantic catalog lives in `config/semantic_metrics.json` and is exposed via:
- `packages/common/semantic_metrics.py`
- `apps/executive_api/main.py` at `/semantic-metrics`
- the executive dashboard semantic layer section

## Why This Matters Commercially
- reduces ambiguity during executive reviews
- makes client adaptation faster
- supports governance conversations with buyers who care about trust and accountability
- strengthens the platform story beyond visualization and model outputs

## Current Core Metrics
- latest revenue
- NRR
- gross revenue churn
- total value at risk
- action adoption rate
- data quality score

## Next Step
Promote client-specific semantic overrides and align the catalog with dbt model contracts where appropriate.
