# Sales Enablement Bundle

## Purpose
Generate CRM-ready and proposal-ops-ready handoff artifacts from the deal room.

## Command

```bash
PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" python scripts/build_sales_enablement_bundle.py
```

## Outputs
- `crm_handoff.json`
- `crm_handoff.csv`
- `implementation_tasklist.csv`
- `sales_one_pager.md`

## Use Cases
- CRM handoff after demo or discovery
- alignment between sales, consulting, and delivery
- lightweight next-step package for account progression
