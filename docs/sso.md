# SSO

## Purpose
This platform now supports an enterprise-ready SSO enforcement layer without coupling the repository to a single identity provider. The implementation is designed for deployment behind an identity-aware proxy or ingress that injects trusted user headers after OIDC or SAML authentication.

## Supported Pattern
Current mode:
- `trusted_header`

The platform expects a reverse proxy, gateway, or identity-aware access layer to authenticate the user and inject headers such as:
- `X-Auth-Request-Email`
- `X-Auth-Request-User`
- `X-Auth-Request-Groups`

## Environment Variables
- `PLATFORM_SSO_MODE`
- `PLATFORM_SSO_HEADER_USER`
- `PLATFORM_SSO_HEADER_NAME`
- `PLATFORM_SSO_HEADER_GROUPS`
- `PLATFORM_SSO_REQUIRED_GROUPS`

For Google Workspace with the local protected stack, the relevant `oauth2-proxy` variables are:
- `OAUTH2_PROXY_PROVIDER=google`
- `OAUTH2_PROXY_REDIRECT_URL`
- `OAUTH2_PROXY_CLIENT_ID`
- `OAUTH2_PROXY_CLIENT_SECRET`
- `OAUTH2_PROXY_COOKIE_SECRET`
- `OAUTH2_PROXY_EMAIL_DOMAINS`
- optional: `OAUTH2_PROXY_GOOGLE_ADMIN_EMAIL`
- optional: `OAUTH2_PROXY_GOOGLE_GROUP`
- optional: `OAUTH2_PROXY_GOOGLE_SERVICE_ACCOUNT_JSON`

Example:
```bash
PLATFORM_SSO_MODE=trusted_header
PLATFORM_SSO_REQUIRED_GROUPS=analytics-admin,executive-viewer
PLATFORM_SSO_HEADER_USER=x-auth-request-email
PLATFORM_SSO_HEADER_NAME=x-auth-request-user
PLATFORM_SSO_HEADER_GROUPS=x-auth-request-groups
```

## API Behavior
- `/health`, `/docs`, `/openapi.json`, and `/redoc` remain accessible for platform diagnostics
- business endpoints return `401` when trusted identity headers are missing
- business endpoints return `403` when the identity is authenticated but not in one of the required groups
- `/auth/config` exposes non-sensitive SSO configuration
- `/auth/me` returns the resolved identity for the current request

## Streamlit Behavior
The executive dashboard and pages use the same SSO policy:
- when SSO is disabled, the app behaves normally
- when SSO is enabled and no trusted identity is present, the app blocks access
- when SSO is enabled and the user is authenticated, the app displays a lightweight session caption

## Why This Matters
This gives the repository a credible path to enterprise access control:
- private client portals behind corporate identity
- API access with group-based authorization
- clean separation between public showcase mode and protected client environments

## Operational Note
Streamlit Community Cloud is still better suited to public demos than enterprise SSO. For protected client deployments, run Streamlit and the API behind a gateway such as NGINX, Cloudflare Access, Azure AD Application Proxy, or another identity-aware reverse proxy.

## Local Protected Stack
The repository now includes a concrete local pattern with Docker Compose:
- `oauth2-proxy` for OIDC login
- `NGINX` for `auth_request` header propagation
- `trusted_header` enforcement inside the API and Streamlit apps

Start it with:
```bash
make protected-demo-stack
```

Reference docs:
- [docker-compose.md](./docker-compose.md)
- [../deploy/nginx/executive-proxy.conf](../deploy/nginx/executive-proxy.conf)
- [../deploy/oauth2-proxy/google-workspace.env.example](../deploy/oauth2-proxy/google-workspace.env.example)

## Google Workspace
The repository now ships a Google Workspace example for the protected local stack.

What it covers:
- Google OAuth client login through `oauth2-proxy`
- Workspace domain restriction using `OAUTH2_PROXY_EMAIL_DOMAINS`
- optional group-based restriction through Google Admin SDK
- trusted-header propagation into Streamlit and FastAPI

Use:
```bash
make google-workspace-demo-stack
```

Optional group restriction requires a Google service account with Admin SDK delegation. This is an inference from the `oauth2-proxy` Google provider documentation, which describes group restriction through `google-group`, `google-admin-email`, and a service account credential.
