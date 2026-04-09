# Formal Approval Workflow

## Purpose
This workflow adds explicit sign-off control to proposal, onboarding, and client-delivery readiness. It is designed to support enterprise-style reviews without introducing heavy process tooling into the repository.

## What It Generates
For each deal room, the platform now creates:
- `approvals/approval_workflow.json`
- `approvals/approval_log.csv`
- `approvals/approval_summary.md`

These artifacts record:
- required approval stages
- responsible roles
- current approval status
- approver identity
- decision timestamp
- notes and evidence expectations

## Default Approval Gates
The default workflow includes:
1. Commercial Review
2. Privacy And LGPD Review
3. Technical Readiness Review
4. Executive Sponsor Sign-off

This gives the platform a formal bridge between pre-sales, governance, delivery, and client-side sponsorship.

## Commands
```bash
make deal-room PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26"
make approval-pack PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26"
```

## Recording Sign-offs
Optional sign-offs can be injected with `APPROVAL_SIGNOFFS` as JSON:

```bash
APPROVAL_SIGNOFFS='{"commercial_review":{"status":"approved","approver_name":"Samuel Maia","decision_at":"2026-04-08T14:00:00Z"}}' make approval-pack
```

## API Surface
The executive API exposes:
- `/executive/deal-room/{deal_slug}`
- `/executive/deal-room/{deal_slug}/approvals`

This allows client-delivery readiness and sign-off status to be consumed by external workflow tools later.

## Why This Matters
This layer improves:
- commercial governance
- client onboarding discipline
- auditability of approval decisions
- readiness for recurring enterprise delivery
