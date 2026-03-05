# Contributing Guide

Thanks for contributing to the Revenue-Intelligence-Platform-Suite.

## Development setup
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -e ".[dev]"
```
3. Generate showcase artifacts:
```bash
python scripts/run_showcase_demo.py
```

## Quality gates
Run before opening a PR:
```bash
ruff check apps platform platform_connectors platform_observability packages scripts tests main.py
pytest
```

## Branch and commit conventions
- Branches: `feat/<scope>`, `fix/<scope>`, `docs/<scope>`, `chore/<scope>`
- Commits: follow Conventional Commits, for example:
  - `feat(platform): add duckdb telemetry fallback`
  - `fix(executive-app): guard empty monitoring report`
  - `docs(release): update v1.0.0 notes`

## Pull request checklist
- Keep scope focused and describe user/business impact.
- Update docs if behavior, contracts, or workflows changed.
- Add or update tests for changed behavior.
- Include evidence (logs, screenshots, generated artifacts) when relevant.

## Contracts and observability
- Do not break schemas in `packages/common/contracts` without versioning and migration notes.
- If you change monitoring or telemetry outputs, update:
  - `tests/test_monitoring_outputs.py`
  - `docs/proof.md`
  - release notes in `docs/releases/`

## Security
- Never commit secrets, tokens, or customer-sensitive data.
- Follow [SECURITY.md](./SECURITY.md) for reporting vulnerabilities.
