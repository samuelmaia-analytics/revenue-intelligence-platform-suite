# Data Retention Matrix

## Purpose
Provide a baseline retention and classification reference for datasets, executive artifacts, and client-facing deliverables.

| Asset Type | Example | Classification | Default Retention | Owner | Notes |
|---|---|---|---|---|---|
| Showcase sample data | bundled demo CSV files | sanitized demo data | keep while relevant to showcase | Analytics Engineering | must remain anonymized or synthetic |
| Operational client extracts | CRM, billing, product usage exports | confidential client data | defined per client agreement | Client Data Owner + Data Platform | legal basis and retention policy required |
| Semantic metric definitions | `config/semantic_metrics.json` | internal governance artifact | persistent | Analytics Engineering | version with releases |
| Executive scorecards | `data_quality_scorecard.json` | internal/client governance artifact | 12 months minimum | Analytics Engineering | may be included in proof packs |
| Proposal packs | `dist/client-proposal-pack/` | client-facing commercial artifact | until deal close or refresh cycle | Revenue Lead | must avoid raw personal data |
| Deal rooms | `dist/deal-rooms/<deal>/` | client-facing commercial artifact | per deal cycle | Revenue Lead + Analytics Engineering | archive or delete after close decision |
| GTM exports | CRM and Notion payload JSONs | internal commercial ops artifact | per RevOps policy | Revenue Operations | no sensitive raw records |
| Release evidence packs | `dist/release-evidence-pack-*.tar.gz` | internal governance artifact | 12 months minimum | Analytics Engineering | supports auditability and quarterly review |

## Review Rule
Retention policy should be confirmed during onboarding and reviewed quarterly for active client deployments.
