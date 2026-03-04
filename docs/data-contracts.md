# Data Contracts

## Purpose

Define contratos minimos entre camadas para evitar quebra silenciosa em pipelines e modelos.

## Contract: `gold.customer_snapshot`

| Column | Type | Rule |
|---|---|---|
| customer_id | string | not null, unique |
| snapshot_date | date | not null |
| recency_days | int | >= 0 |
| frequency_90d | int | >= 0 |
| monetary_90d | float | >= 0 |
| churn_label | int | in {0, 1} |
| segment | string | in approved taxonomy |

## Contract: `gold.sales_kpi_daily`

| Column | Type | Rule |
|---|---|---|
| date | date | not null |
| channel | string | not null |
| gross_revenue | float | >= 0 |
| orders | int | >= 0 |
| avg_ticket | float | >= 0 |

## Validation Path

- Define schema em `platform/quality/contracts.py`.
- Rodar validacao no fim da camada silver e antes da gold.
- Bloquear deploy de dashboard/modelo quando contrato falhar.

## Versioning

- Mudancas breaking exigem novo ADR.
- Contratos versionados por release tag.
