# GTM Exports

## Purpose
Generate ready-to-adapt payloads for CRM and proposal tooling without requiring live credentials.

## Command

```bash
PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" python scripts/build_gtm_exports.py
```

## Outputs
- `hubspot_deal_payload.json`
- `salesforce_opportunity_payload.json`
- `notion_page_payload.json`
- `microsite_publish_manifest.json`

For publication-ready static assets, see [docs/external-publication.md](./external-publication.md).

## Why This Matters
- speeds up CRM handoff
- creates a bridge from pre-sales assets to system-of-record workflows
- gives proposal-ops and RevOps a clean starting point for automation

## Copyright Note
These exports are generated from proprietary platform assets. They are intended for controlled commercial handoff, not unrestricted redistribution.
