# Showcase Use Case

## Official Use Case

Reduce revenue churn in B2B customers by prioritizing retention actions with financial impact.

## Target User

- Revenue Lead
- Retention Ops
- CRM/CSM managers

## Decision Questions

1. Which accounts represent the highest revenue at risk this week?
2. Which action should be executed first for each risk cluster?
3. How much revenue can be recovered under each uplift scenario?

## Inputs

- Sales transactions from `modules/analise-vendas-python/dados_processados/vendas_simples.csv`
- Customer behavior from `modules/revenue-intelligence/data/raw/E-commerce Customer Behavior - Sheet1.csv`
- Model metrics from `modules/revenue-intelligence/data/processed/metrics_report.json`

## Outputs

- Executive KPI board with telemetry-backed revenue, NRR, churn, and value at risk.
- Top retention priorities with expected recovery per account.
- Weekly leadership action plan.

## Success Criteria

- Leadership can identify top-risk accounts in under 5 minutes.
- Action list is prioritized by financial impact, not only by model score.
- Scenario controls (uplift/budget) produce transparent ROI assumptions.
