# Publish v1.0.0

## 1) Commit
```bash
git add .
git commit -m "feat(platform): ship flagship v1.0.0 with telemetry, contracts, CI and observability"
```

## 2) Tag
```bash
git tag -a v1.0.0 -m "Revenue-Intelligence-Platform-Suite v1.0.0"
```

## 3) Push
```bash
git push origin main
git push origin v1.0.0
```

## 4) GitHub Release (CLI)
```bash
gh release create v1.0.0 \
  --title "v1.0.0 - Flagship Platform Baseline" \
  --notes-file docs/releases/v1.0.0.md
```

## 5) Quarterly cadence (after v1.0.0)
```bash
# every quarter, create/update the quarter note from template
cp docs/releases/QUARTERLY_TEMPLATE.md docs/releases/2026-Q2.md

# publish release tag + note for quarter milestone
git add docs/releases/2026-Q2.md
git commit -m "docs(release): add 2026-Q2 release notes"
git push origin main
```

Automation:
- `.github/workflows/quarterly-release-reminder.yml` opens the quarterly release issue.
- `.github/workflows/showcase-monitoring.yml` generates drift/adoption artifacts weekly and on-demand.
