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

from scripts.build_sales_enablement_bundle import main as build_sales_enablement_bundle  # noqa: E402


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "deal-room"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    deal_name = os.getenv("DEAL_NAME", os.getenv("PROPOSAL_CLIENT_NAME", "Flagship Client"))
    room_slug = _slugify(deal_name)

    build_sales_enablement_bundle()

    deal_room_dir = DIST_DIR / "deal-rooms" / room_slug
    sales_bundle_dir = deal_room_dir / "sales-enablement"
    exports_dir = sales_bundle_dir / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    crm_handoff = _load_json(sales_bundle_dir / "crm_handoff.json")
    manifest = _load_json(deal_room_dir / "manifest.json")

    hubspot_payload = {
        "properties": {
            "dealname": crm_handoff["deal_name"],
            "pipeline": "analytics-platform",
            "dealstage": "proposal",
            "amount": crm_handoff["setup_fee"],
            "description": crm_handoff["recommended_next_step"],
            "industry": crm_handoff["industry"],
            "analytics_package": crm_handoff["package"],
        }
    }
    (exports_dir / "hubspot_deal_payload.json").write_text(
        json.dumps(hubspot_payload, indent=2), encoding="utf-8"
    )

    salesforce_payload = {
        "Opportunity": {
            "Name": crm_handoff["deal_name"],
            "StageName": "Proposal/Price Quote",
            "CloseDate": "2026-12-31",
            "Amount": crm_handoff["setup_fee"],
            "Description": crm_handoff["recommended_next_step"],
            "Industry__c": crm_handoff["industry"],
            "Solution_Package__c": crm_handoff["package"],
        }
    }
    (exports_dir / "salesforce_opportunity_payload.json").write_text(
        json.dumps(salesforce_payload, indent=2), encoding="utf-8"
    )

    notion_payload = {
        "parent": {"database_id": "replace-with-notion-database-id"},
        "properties": {
            "Name": {"title": [{"text": {"content": crm_handoff["deal_name"]}}]},
            "Client": {"rich_text": [{"text": {"content": crm_handoff["client_name"]}}]},
            "Package": {"rich_text": [{"text": {"content": crm_handoff["package"]}}]},
            "Next Step": {"rich_text": [{"text": {"content": crm_handoff["recommended_next_step"]}}]},
        },
    }
    (exports_dir / "notion_page_payload.json").write_text(
        json.dumps(notion_payload, indent=2), encoding="utf-8"
    )

    microsite_publish_manifest = {
        "site_slug": room_slug,
        "source": str((deal_room_dir / "microsite.html").relative_to(ROOT)),
        "target_hint": f"/sites/{room_slug}/index.html",
        "publish_targets": ["github_pages", "s3_static_site", "netlify_drop"],
        "linked_assets": [artifact["name"] for artifact in manifest["artifacts"]],
    }
    (exports_dir / "microsite_publish_manifest.json").write_text(
        json.dumps(microsite_publish_manifest, indent=2), encoding="utf-8"
    )

    print(f"GTM exports generated in {exports_dir}")


if __name__ == "__main__":
    main()
