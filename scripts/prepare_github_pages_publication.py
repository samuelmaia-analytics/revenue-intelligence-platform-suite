from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_external_publication_bundle import main as build_external_publication_bundle  # noqa: E402


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "deal-room"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    proposal_client_name = os.getenv("PROPOSAL_CLIENT_NAME", "Flagship Client")
    deal_name = os.getenv("DEAL_NAME", proposal_client_name)
    room_slug = _slugify(deal_name)
    pages_base_url = os.getenv(
        "PUBLISH_BASE_URL",
        "https://example.github.io/revenue-intelligence-platform-suite",
    ).rstrip("/")
    allow_unapproved = os.getenv("ALLOW_UNAPPROVED_PUBLICATION", "0").strip() == "1"

    os.environ["PUBLISH_TARGET"] = "github_pages"
    os.environ["PUBLISH_BASE_URL"] = pages_base_url
    build_external_publication_bundle()

    publication_manifest = _load_json(
        DIST_DIR / "deal-rooms" / room_slug / "publication" / "publication_manifest.json"
    )
    if not publication_manifest["ready_for_external_publication"] and not allow_unapproved:
        raise SystemExit(
            "GitHub Pages publication blocked because ready_for_external_publication=false. "
            "Complete the formal approval workflow or set ALLOW_UNAPPROVED_PUBLICATION=1 for internal testing."
        )

    pages_dir = DIST_DIR / "github-pages" / room_slug
    pages_dir.mkdir(parents=True, exist_ok=True)
    site_dir = DIST_DIR / "deal-rooms" / room_slug / "publication" / "site"
    for source in site_dir.iterdir():
        target = pages_dir / source.name
        target.write_bytes(source.read_bytes())

    root_index = DIST_DIR / "github-pages" / "index.html"
    root_index.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Published Deal Rooms</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #122033; }}
    .wrap {{ max-width: 960px; margin: 0 auto; padding: 48px 24px 64px; }}
    .card {{ background: #fff; padding: 24px; border-radius: 20px; box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08); }}
    a {{ color: #0f766e; font-weight: 700; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Published Deal Rooms</h1>
      <p>Latest prepared publication target:</p>
      <p><a href="./{room_slug}/index.html">{proposal_client_name} | {deal_name}</a></p>
      <p>Copyright (c) 2026 Samuel Maia. Public visibility does not grant reuse, redistribution, sublicensing, or derivative rights.</p>
    </div>
  </div>
</body>
</html>""",
        encoding="utf-8",
    )

    print(f"GitHub Pages bundle prepared in {DIST_DIR / 'github-pages'}")


if __name__ == "__main__":
    main()
