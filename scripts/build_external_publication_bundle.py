from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_formal_approval_pack import main as build_formal_approval_pack  # noqa: E402
from scripts.build_gtm_exports import main as build_gtm_exports  # noqa: E402


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "deal-room"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    proposal_client_name = os.getenv("PROPOSAL_CLIENT_NAME", "Flagship Client")
    deal_name = os.getenv("DEAL_NAME", proposal_client_name)
    publish_target = os.getenv("PUBLISH_TARGET", "static_bundle").strip().lower()
    publish_base_url = os.getenv("PUBLISH_BASE_URL", "https://demo.example.com").rstrip("/")
    room_slug = _slugify(deal_name)

    build_formal_approval_pack()
    build_gtm_exports()

    deal_room_dir = DIST_DIR / "deal-rooms" / room_slug
    publish_dir = deal_room_dir / "publication"
    site_dir = publish_dir / "site"
    site_dir.mkdir(parents=True, exist_ok=True)

    files_to_publish = {
        "index.html": deal_room_dir / "microsite.html",
        "executive_review_pack.html": deal_room_dir / "executive_review_pack.html",
        "client_proposal.html": deal_room_dir / "client_proposal.html",
    }

    published_assets: list[dict[str, str]] = []
    for target_name, source_path in files_to_publish.items():
        destination_path = site_dir / target_name
        shutil.copy2(source_path, destination_path)
        published_assets.append(
            {
                "file_name": target_name,
                "source": str(source_path.relative_to(ROOT)),
                "published_path": str(destination_path.relative_to(ROOT)),
                "public_url": f"{publish_base_url}/{room_slug}/{target_name}",
            }
        )

    manifest = _load_json(deal_room_dir / "manifest.json")
    approval_workflow = _load_json(deal_room_dir / "approvals" / "approval_workflow.json")
    microsite_publish_manifest = _load_json(
        deal_room_dir / "sales-enablement" / "exports" / "microsite_publish_manifest.json"
    )

    publication_manifest = {
        "deal_name": deal_name,
        "proposal_client_name": proposal_client_name,
        "room_slug": room_slug,
        "publish_target": publish_target,
        "publish_base_url": publish_base_url,
        "landing_url": f"{publish_base_url}/{room_slug}/index.html",
        "ready_for_external_publication": approval_workflow["ready_for_client_delivery"],
        "approval_status": manifest.get("approval_status", {}),
        "published_assets": published_assets,
        "exposure_policy": {
            "allowed_assets": [asset["file_name"] for asset in published_assets],
            "restricted_assets": [
                "client_proposal.json",
                "executive_review_pack.json",
                "release-evidence-pack",
                "crm_handoff.json",
            ],
            "copyright_notice": (
                "Copyright (c) 2026 Samuel Maia. Public visibility does not grant reuse, "
                "redistribution, sublicensing, or derivative rights."
            ),
        },
        "publication_targets": microsite_publish_manifest.get("publish_targets", []),
    }
    (publish_dir / "publication_manifest.json").write_text(
        json.dumps(publication_manifest, indent=2),
        encoding="utf-8",
    )

    summary_lines = [
        "# External Publication Bundle",
        "",
        f"Deal: {deal_name}",
        f"Client: {proposal_client_name}",
        f"Publish target: {publish_target}",
        f"Landing URL: {publication_manifest['landing_url']}",
        "",
        "## Publication Readiness",
        f"- Ready for external publication: {publication_manifest['ready_for_external_publication']}",
        f"- Approved stages: {approval_workflow['approved_stage_count']}/{approval_workflow['stage_count']}",
        "",
        "## Published Assets",
    ]
    for asset in published_assets:
        summary_lines.append(f"- {asset['file_name']}: {asset['public_url']}")
    summary_lines.extend(
        [
            "",
            "## Exposure Policy",
            "- Only presentation-layer HTML assets are included in the publication bundle.",
            "- Proposal JSON, review JSON, release evidence, and CRM exports remain restricted.",
            "- Public visibility does not grant reuse rights.",
        ]
    )
    (publish_dir / "README.md").write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"External publication bundle generated in {publish_dir}")


if __name__ == "__main__":
    main()
