# Case Study 01 - Churn Retention Prioritization

## Context

Retention teams had limited bandwidth and no unified ranking of accounts by financial risk.

## Business Problem

High-value customers at risk were not consistently prioritized, reducing retention efficiency.

## Decision

Deploy a churn prioritization layer combining:

- churn score
- revenue exposure
- actionability rules

## Execution

- Consolidated customer snapshot in gold layer.
- Applied quality checks before model scoring.
- Exposed ranked action list in executive dashboard.

## Outcome (Initial Baseline)

- Clear ranking of top at-risk accounts by value.
- Faster weekly retention planning cycle.
- Governance-ready audit trail from data to recommendation.

## Risks and Mitigation

- Risk: low action adoption by commercial teams.
- Mitigation: owner assignment per recommendation and weekly follow-up.
