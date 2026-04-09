# Tenant Secrets

## Purpose
This directory defines the repository convention for tenant-specific secrets without committing live credentials.

## Layering Order
Secrets resolve in this order:
1. `config/secrets/global.json`
2. `config/secrets/environments/<deployment_env>.json`
3. `config/secrets/clients/<client_profile>.json`
4. `config/secrets/tenants/<deployment_env>/<client_profile>.json`
5. environment overrides using `TENANT_SECRET__...`

Later layers override earlier ones.

## What Is Versioned
Only templates are versioned in Git:
- `config/secrets/templates/global.template.json`
- `config/secrets/templates/environments/*.template.json`
- `config/secrets/templates/clients/*.template.json`

These templates define the required shape and expected keys for operational readiness.

## What Must Stay Out Of Git
Never commit live credentials to:
- `config/secrets/global.json`
- `config/secrets/environments/*.json`
- `config/secrets/clients/*.json`
- `config/secrets/tenants/**/*.json`

These paths are ignored by `.gitignore`.

## Environment Variable Overrides
Environment overrides use nested keys:

```bash
TENANT_SECRET__CRM__API_TOKEN=abc123
TENANT_SECRET__OBSERVABILITY__SLACK_WEBHOOK_URL=https://hooks.slack.com/...
TENANT_SECRET__STORAGE__SIGNED_URL_TTL_SECONDS=3600
```

## Validation
Generate masked readiness output:

```bash
python scripts/check_tenant_secrets.py
CLIENT_PROFILE=healthtech_growth DEPLOYMENT_ENV=production python scripts/check_tenant_secrets.py
```

This validation reports completeness against templates without printing secret values.
