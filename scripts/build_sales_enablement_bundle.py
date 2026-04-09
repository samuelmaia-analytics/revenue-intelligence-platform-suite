from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_deal_room import main as build_deal_room  # noqa: E402


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "deal-room"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    deal_name = os.getenv("DEAL_NAME", os.getenv("PROPOSAL_CLIENT_NAME", "Flagship Client"))
    room_slug = _slugify(deal_name)

    build_deal_room()

    deal_room_dir = DIST_DIR / "deal-rooms" / room_slug
    proposal = _load_json(deal_room_dir / "client_proposal.json")
    manifest = _load_json(deal_room_dir / "manifest.json")
    approval_workflow = _load_json(deal_room_dir / "approvals" / "approval_workflow.json")

    bundle_dir = deal_room_dir / "sales-enablement"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    crm_handoff = {
        "deal_name": manifest["deal_name"],
        "client_name": proposal["proposal_client_name"],
        "industry": proposal["solution_profile"]["industry"],
        "buyer": proposal["solution_profile"]["executive_buyer"],
        "package": proposal["solution_profile"]["package"]["name"],
        "setup_fee": proposal["commercial_structure"]["setup_fee"],
        "monthly_service": proposal["commercial_structure"]["monthly_service"],
        "timeline": proposal["commercial_structure"]["timeline"],
        "value_at_risk_usd": proposal["summary"]["total_value_at_risk_usd"],
        "quality_score": proposal["scorecard"]["overall_score"],
        "top_insight": proposal["insights"]["insights"][0]["headline"]
        if proposal["insights"]["insights"]
        else "",
        "approval_stage_count": approval_workflow["stage_count"],
        "approved_stage_count": approval_workflow["approved_stage_count"],
        "ready_for_client_delivery": approval_workflow["ready_for_client_delivery"],
        "recommended_next_step": "Run executive walkthrough and confirm scope + connector priorities.",
    }

    crm_json_path = bundle_dir / "crm_handoff.json"
    crm_json_path.write_text(json.dumps(crm_handoff, indent=2), encoding="utf-8")

    crm_csv_path = bundle_dir / "crm_handoff.csv"
    pd.DataFrame([crm_handoff]).to_csv(crm_csv_path, index=False)

    tasklist = pd.DataFrame(
        [
            {"stage": "Discovery", "task": "Confirm executive sponsor and KPI owners"},
            {"stage": "Proposal", "task": "Review proposal pack and approve commercial structure"},
            {"stage": "Approval", "task": "Complete formal sign-off workflow and record approver evidence"},
            {"stage": "Technical", "task": "Validate connectors and source-system feasibility"},
            {"stage": "Delivery", "task": "Schedule executive board rollout and telemetry instrumentation"},
        ]
    )
    tasklist_path = bundle_dir / "implementation_tasklist.csv"
    tasklist.to_csv(tasklist_path, index=False)

    one_pager_path = bundle_dir / "sales_one_pager.md"
    one_pager_path.write_text(
        "\n".join(
            [
                "# Sales One Pager",
                "",
                f"Deal: {crm_handoff['deal_name']}",
                f"Client: {crm_handoff['client_name']}",
                f"Buyer: {crm_handoff['buyer']}",
                f"Package: {crm_handoff['package']}",
                "",
                "## Why This Deal Matters",
                f"- Current value at risk: ${crm_handoff['value_at_risk_usd']:,.0f}",
                f"- Quality score: {crm_handoff['quality_score']:.1f}",
                f"- Top executive signal: {crm_handoff['top_insight']}",
                "",
                "## Commercial Structure",
                f"- Setup fee: {crm_handoff['setup_fee']}",
                f"- Monthly recurring service: {crm_handoff['monthly_service']}",
                f"- Timeline: {crm_handoff['timeline']}",
                "",
                "## Approval Readiness",
                f"- Approved stages: {crm_handoff['approved_stage_count']}/{crm_handoff['approval_stage_count']}",
                f"- Ready for client delivery: {crm_handoff['ready_for_client_delivery']}",
                "",
                "## Next Step",
                f"- {crm_handoff['recommended_next_step']}",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Sales enablement bundle generated in {bundle_dir}")


if __name__ == "__main__":
    main()
