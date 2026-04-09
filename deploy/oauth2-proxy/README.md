# OAuth2 Proxy Deployment Notes

## Google Workspace Example
Use `google-workspace.env.example` as the starting point for local protected demos with Google Workspace.

Recommended process:
1. Copy `deploy/oauth2-proxy/google-workspace.env.example` to a private env file outside version control.
2. Fill `OAUTH2_PROXY_CLIENT_ID`, `OAUTH2_PROXY_CLIENT_SECRET`, and `OAUTH2_PROXY_COOKIE_SECRET`.
3. Set `OAUTH2_PROXY_EMAIL_DOMAINS` to your Workspace domain.
4. If you need group-based restriction, configure:
   - `OAUTH2_PROXY_GOOGLE_ADMIN_EMAIL`
   - `OAUTH2_PROXY_GOOGLE_GROUP`
   - a service account JSON with Admin SDK delegation

The repository does not ship live identity credentials.
