# Deal Room

## Purpose
Generate a single packaged folder for a client opportunity that combines proposal, executive review, microsite, benchmark, and evidence artifacts.

## Command

```bash
PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" python scripts/build_deal_room.py
```

## Outputs
- `dist/deal-rooms/<deal-slug>/README.md`
- `dist/deal-rooms/<deal-slug>/manifest.json`
- `dist/deal-rooms/<deal-slug>/approvals/approval_workflow.json`
- `dist/deal-room-<deal-slug>.tar.gz`

## Typical Use
- pre-sales handoff between consultant and technical lead
- executive follow-up after discovery or demo
- packaging materials for proposal review and steering committees
- formal sign-off tracking before client delivery or onboarding
