# External Publication

## Purpose
Generate a controlled publication bundle for a deal room without pushing directly to an external host. This keeps the repository production-minded while avoiding hardcoded deployment credentials.

## What It Generates
- `dist/deal-rooms/<deal-slug>/publication/site/index.html`
- `dist/deal-rooms/<deal-slug>/publication/site/client_proposal.html`
- `dist/deal-rooms/<deal-slug>/publication/site/executive_review_pack.html`
- `dist/deal-rooms/<deal-slug>/publication/publication_manifest.json`
- `dist/deal-rooms/<deal-slug>/publication/README.md`
- `dist/github-pages/<deal-slug>/` when preparing a GitHub Pages target

## Command
```bash
make publish-bundle PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" PUBLISH_BASE_URL="https://demo.example.com"
make prepare-pages PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" PUBLISH_BASE_URL="https://your-user.github.io/your-repo"
```

## Publication Policy
- only HTML presentation assets are included
- JSON artifacts, CRM exports, and evidence bundles stay restricted
- publication readiness is tied to the formal approval workflow
- the manifest includes a landing URL and per-asset public URLs

## API Surface
- `/executive/deal-room/{deal_slug}/publication`

## GitHub Pages
The repository now includes a real publication workflow in [publish-deal-room-pages.yml](../.github/workflows/publish-deal-room-pages.yml).

Behavior:
- builds the publication bundle
- blocks deployment if `ready_for_external_publication=false`
- uploads `dist/github-pages/` as the Pages artifact
- deploys only the approved HTML presentation layer

For local preparation without GitHub Actions:
```bash
make prepare-pages PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" PUBLISH_BASE_URL="https://your-user.github.io/your-repo"
```

## Why This Matters
This creates a clean bridge between commercial assets and future automated publishing to GitHub Pages, S3, Netlify, Vercel, or controlled client portals.
