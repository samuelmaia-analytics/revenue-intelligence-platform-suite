# Security Policy

## Supported Scope

This repository contains analytics and machine learning assets for business decision support.
Security controls apply to:

- Source code and CI workflows
- Sample datasets and generated artifacts
- Dashboard and API integration points

## Reporting a Vulnerability

Please report security issues privately by email:

- `smaia2@gmail.com`

Include:

- Affected file/path
- Reproduction steps
- Potential impact
- Suggested remediation (if available)

Do not open public issues for sensitive vulnerabilities.

## Security Baseline

- Do not commit secrets or access tokens.
- Use environment variables for credentials.
- Keep dependencies updated and pinned where possible.
- Restrict datasets to anonymized/sanitized samples in-repo.
- Review CI workflows for least-privilege permissions.

## Data Handling

- PII should not be committed to this repository.
- Any customer-like data must be anonymized before local or CI usage.
- Contracts and quality checks should reject invalid/sensitive payloads where applicable.
