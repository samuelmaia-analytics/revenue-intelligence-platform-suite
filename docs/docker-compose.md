# Docker Compose Demo

## Purpose
Run the executive dashboard and executive API together as a local commercial demo stack.

## Services
- `executive-api`: serves executive artifacts and client profiles on port `8000`
- `executive-dashboard`: serves the Streamlit app on port `8501`
- `oauth2-proxy`: optional OIDC-aware auth proxy for protected environments
- `executive-edge-proxy`: optional NGINX entrypoint that forwards trusted identity headers

## Command

```bash
docker compose up --build
```

Protected stack with SSO enforcement:

```bash
PLATFORM_SSO_MODE=trusted_header docker compose --profile protected up --build
```

Google Workspace example:

```bash
docker compose --profile protected --env-file deploy/oauth2-proxy/google-workspace.env.example up --build
```

## Recommended Flow
1. Generate showcase artifacts with `make showcase`
2. Start the stack with `make demo-stack`
3. Open `http://localhost:8501` for the dashboard
4. Open `http://localhost:8000/docs` for the API docs

Protected flow:
1. Configure OIDC values for `oauth2-proxy`
2. Start the protected stack with `make protected-demo-stack`
3. Open `http://localhost:8080` for the SSO-protected dashboard
4. Open `http://localhost:8080/api/docs` for the protected API docs

Google Workspace flow:
1. Create a Google OAuth client with redirect URI `http://localhost:8080/oauth2/callback`
2. Copy the example env file from `deploy/oauth2-proxy/google-workspace.env.example`
3. Fill client id, client secret, cookie secret, and Workspace domain
4. Run `make google-workspace-demo-stack`
5. Open `http://localhost:8080`

## Environment Variables
- `CLIENT_PROFILE`
- `DEPLOYMENT_ENV`
- `SOLUTION_PACKAGE`
- `PLATFORM_SSO_MODE`
- `PLATFORM_SSO_REQUIRED_GROUPS`
- `OAUTH2_PROXY_REDIRECT_URL`
- `OAUTH2_PROXY_CLIENT_ID`
- `OAUTH2_PROXY_CLIENT_SECRET`
- `OAUTH2_PROXY_COOKIE_SECRET`
- `OAUTH2_PROXY_EMAIL_DOMAINS`
- `OAUTH2_PROXY_GOOGLE_ADMIN_EMAIL`
- `OAUTH2_PROXY_GOOGLE_GROUP`

## Protected Pattern
The protected profile uses:
- `oauth2-proxy` to authenticate against Google Workspace or another configured provider
- `NGINX auth_request` to validate the session
- trusted headers `X-Auth-Request-Email`, `X-Auth-Request-User`, and `X-Auth-Request-Groups`
- application-level enforcement from `docs/sso.md`

The NGINX configuration lives in [deploy/nginx/executive-proxy.conf](../deploy/nginx/executive-proxy.conf).

For the Google Workspace-specific setup, see [sso.md](./sso.md) and [../deploy/oauth2-proxy/google-workspace.env.example](../deploy/oauth2-proxy/google-workspace.env.example).
