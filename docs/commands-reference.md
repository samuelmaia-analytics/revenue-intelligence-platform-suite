# Commands Reference

## Purpose
Quick reference for the platform's most important operating commands.

## Environment Setup
```bash
python -m pip install -e ".[dev]"
```

## Core Runtime
```bash
make showcase
make app
make api
make demo-stack
make protected-demo-stack
make google-workspace-demo-stack
```

## Validation
```bash
make lint
make test
make validate
make tenant-secrets-check
```

## Executive And Commercial Assets
```bash
make review-pack
make proposal-pack PROPOSAL_CLIENT_NAME="Acme Corp"
make microsite PROPOSAL_CLIENT_NAME="Acme Corp"
make deal-room PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26"
make approval-pack PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26"
make publish-bundle PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" PUBLISH_BASE_URL="https://demo.example.com"
make prepare-pages PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" PUBLISH_BASE_URL="https://your-user.github.io/your-repo"
make sales-bundle PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26"
make gtm-exports PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26"
make evidence-pack RELEASE_TAG=v1.0.0
```

## Industry Assets
```bash
make industry-packs
make benchmark
```
