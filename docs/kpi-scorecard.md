# KPI Scorecard

## How To Use
- update current values weekly
- review targets monthly with executive sponsors
- keep a named owner and action plan for every KPI outside guardrail

## Executive KPI Template
| KPI | Formula | Baseline | Target 6M | Target 12M | Current | Status | Owner |
|---|---|---:|---:|---:|---:|---|---|
| Net Revenue Retention | retained + expansion - contraction / starting revenue | 86.69% | 90.00% | 94.00% | 86.69% | Risk | Revenue Lead |
| Gross Revenue Churn | lost revenue / starting revenue | 13.31% | 10.50% | 8.00% | 13.31% | Risk | Retention Lead |
| Churn Precision@K | true churn in top-K / K | 0.62 | 0.70 | 0.78 | 0.62 | Risk | ML Lead |
| Action Adoption Rate | executed actions / recommended actions | 28% | 45% | 60% | 28% | Risk | CRM Ops |
| Incremental Revenue | observed uplift - control group | $0 | $120K | $350K | $0 | Off Track | Growth Lead |
| Time-to-Insight | time from ingestion to actionable output | 2 days | 8 hours | 2 hours | 2 days | Risk | Analytics Engineering |
| Data Contract Pass Rate | passed contracts / total contracts | 92% | 97% | 99% | 92% | Risk | Data Platform |
| Pipeline Reliability | successful runs / total runs | 95% | 98% | 99.5% | 95% | Risk | Data Platform |

## Notes
- baseline values are starter targets for executive steering
- replace them with production telemetry after the first operating cycle
- recommended cadence: weekly current-state review, monthly target review

## Weekly Review Template

### Wins
- executive KPI baseline is live
- monitoring and scorecard artifacts are publishable

### Risks
- some telemetry remains demo-oriented in showcase mode
- recommendation adoption still depends on process rollout in the client workflow

### Decisions Needed
- approve next-step investment in automation and connector depth
- confirm owners for KPI remediation where trust or freshness is below target

### Actions For The Next 7 Days
- connect scorecard metrics to recurring export and release evidence
- review action-adoption telemetry and close owner gaps
