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
