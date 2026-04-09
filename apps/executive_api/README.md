# Executive API

## Purpose
FastAPI serving layer for executive artifacts, client profiles, readiness checks, and commercial delivery assets.

## Run Locally

```bash
uvicorn apps.executive_api.main:app --reload
```

## Core Endpoints
- `/health`
- `/auth/config`
- `/auth/me`
- `/health`
- `/profiles`
- `/profiles/{profile_id}`
- `/profiles/{profile_id}/secret-status`
- `/semantic-metrics`
- `/executive/summary`
- `/executive/scorecard`
- `/executive/insights`
- `/executive/solution-profile`
- `/executive/review-pack`
- `/executive/review-pack/html`
- `/executive/proposal-pack`
- `/executive/microsite`
- `/executive/deal-room/{deal_slug}`
- `/executive/deal-room/{deal_slug}/approvals`
- `/executive/deal-room/{deal_slug}/publication`
- `/executive/sales-bundle/{deal_slug}`
- `/executive/gtm-export/{deal_slug}/{export_name}`

## Why It Matters
The API is not only a demo companion. It is the serving surface that turns showcase artifacts, governance controls, approval workflows, and commercial packs into consumable platform endpoints.

## Security And Access
- public diagnostics remain available through `/health`
- SSO can be enforced through the trusted-header pattern documented in [docs/sso.md](../../docs/sso.md)
- proprietary rights still apply even when endpoints are exposed in demo mode
