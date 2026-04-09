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
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from common import build_approval_workflow, load_approval_overrides  # noqa: E402
from scripts.build_deal_room import main as build_deal_room  # noqa: E402


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "deal-room"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    proposal_client_name = os.getenv("PROPOSAL_CLIENT_NAME", "Flagship Client")
    deal_name = os.getenv("DEAL_NAME", proposal_client_name)
    release_tag = os.getenv("RELEASE_TAG", "local")
    artifact_version = os.getenv("APPROVAL_ARTIFACT_VERSION", release_tag)
    room_slug = _slugify(deal_name)

    build_deal_room()

    deal_room_dir = DIST_DIR / "deal-rooms" / room_slug
    approvals_dir = deal_room_dir / "approvals"
    approvals_dir.mkdir(parents=True, exist_ok=True)

    workflow = build_approval_workflow(
        deal_name=deal_name,
        proposal_client_name=proposal_client_name,
        artifact_version=artifact_version,
        release_tag=release_tag,
        approval_overrides=load_approval_overrides(),
    )
    proposal = _load_json(deal_room_dir / "client_proposal.json")

    workflow_path = approvals_dir / "approval_workflow.json"
    workflow_path.write_text(json.dumps(workflow, indent=2), encoding="utf-8")

    approval_log = pd.DataFrame(workflow["stages"])[
        [
            "stage_id",
            "stage_name",
            "required_role",
            "owner_team",
            "status",
            "approved",
            "approver_name",
            "decision_at",
            "notes",
        ]
    ]
    approval_log_path = approvals_dir / "approval_log.csv"
    approval_log.to_csv(approval_log_path, index=False)

    summary_lines = [
        "# Formal Approval Pack",
        "",
        f"Deal: {workflow['deal_name']}",
        f"Client: {workflow['proposal_client_name']}",
        f"Artifact version: {workflow['artifact_version']}",
        f"Release tag: {workflow['release_tag']}",
        "",
        "## Status",
        f"- Approved stages: {workflow['approved_stage_count']}/{workflow['stage_count']}",
        f"- Ready for client delivery: {workflow['ready_for_client_delivery']}",
        "",
        "## Required Sign-offs",
    ]
    for stage in workflow["stages"]:
        summary_lines.append(
            f"- {stage['stage_name']}: {stage['status']} | role {stage['required_role']} | "
            f"approver {stage.get('approver_name') or 'pending'}"
        )
    summary_lines.extend(
        [
            "",
            "## Commercial Context",
            f"- Package: {proposal['solution_profile']['package']['name']}",
            f"- Buyer: {proposal['solution_profile']['executive_buyer']}",
            f"- Setup fee: {proposal['commercial_structure']['setup_fee']}",
            f"- Monthly recurring service: {proposal['commercial_structure']['monthly_service']}",
        ]
    )
    summary_path = approvals_dir / "approval_summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"Formal approval pack generated in {approvals_dir}")


if __name__ == "__main__":
    main()
