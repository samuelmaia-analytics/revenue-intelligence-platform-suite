# Data Contracts

## Purpose
Define minimum, versioned contracts between ingestion, curated metrics, and executive outputs so that the platform can scale to multiple clients without silent breakage.

## Contract Layers

### Source Contracts
Used to validate inbound client or showcase datasets before promotion to curated layers.

### Metric Contracts
Used to stabilize KPI definitions across domains and dashboards.

### Executive Output Contracts
Used to validate artifacts consumed by decision-support applications and external delivery packs.

## Example Curated Contracts

### `gold.customer_snapshot`
| Column | Type | Rule |
|---|---|---|
| customer_id | string | not null, unique |
| snapshot_date | date | not null |
| recency_days | int | >= 0 |
| frequency_90d | int | >= 0 |
| monetary_90d | float | >= 0 |
| churn_label | int | in {0, 1} |
| segment | string | in approved taxonomy |

### `gold.sales_kpi_daily`
| Column | Type | Rule |
|---|---|---|
| date | date | not null |
| channel | string | not null |
| gross_revenue | float | >= 0 |
| orders | int | >= 0 |
| avg_ticket | float | >= 0 |

## Root Executive Contracts
- `packages/common/contracts/showcase_summary.schema.json`
- `packages/common/contracts/showcase_summary.v1.schema.json`
- `packages/common/contracts/action_adoption_event.schema.json`
- `packages/common/contracts/action_adoption_event.v1.schema.json`
- `packages/common/contracts/executive_insight_report.v1.schema.json`

## Validation Path
- validate source and silver promotions before gold publication
- validate executive output artifacts before app consumption or release packaging
- block publish or release workflows when breaking changes are introduced without version updates

## Versioning Rules
- backward-compatible changes may remain in the same major contract version
- breaking changes require a new versioned schema and release-note entry
- contract versions should be referenced in release docs and client implementation notes
