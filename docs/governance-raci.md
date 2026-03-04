# Governance RACI

## Purpose

Define who is accountable for business outcomes and who operates each platform domain.

## RACI Matrix

| Domain | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|
| Executive KPI scorecard | Analytics Eng | Revenue Lead | Retention Lead, Growth Lead | Stakeholders |
| Data contracts and schema changes | Data Platform | Data Platform | Analytics Eng, ML Lead | Stakeholders |
| Churn model lifecycle | ML Lead | Retention Lead | Data Platform, CRM Ops | Stakeholders |
| Recommendation playbooks | CRM Ops | Growth Lead | Revenue Lead, ML Lead | Stakeholders |
| Pipeline orchestration reliability | Data Platform | Data Platform | Analytics Eng | Stakeholders |
| Executive dashboard narrative | Analytics Eng | Revenue Lead | Growth Lead | Stakeholders |

## Ownership by Repository Area

- `platform/`: Data Platform
- `packages/common/`: Analytics Eng
- `apps/executive-dashboard/`: Analytics Eng
- `apps/sales-analytics/`: Analytics Eng
- `modules/revenue-intelligence/`: Revenue Lead + Analytics Eng
- `modules/churn-prediction/`: Retention Lead + ML Lead
- `modules/amazon-sales-analysis/`: Growth Lead + Analytics Eng
- `modules/analise-vendas-python/`: Analytics Eng
- `modules/data-senior-analytics/`: Analytics Eng

## Escalation Path

1. Owner triage within 24h.
2. Data Platform/ML review for technical incidents.
3. Revenue Lead decision for scope and priority conflicts.
