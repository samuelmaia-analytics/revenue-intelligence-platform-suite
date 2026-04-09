from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from common import build_approval_workflow, load_approval_overrides  # noqa: E402
from scripts.build_client_microsite import main as build_client_microsite  # noqa: E402
from scripts.build_client_proposal_pack import main as build_client_proposal_pack  # noqa: E402
from scripts.build_executive_review_pack import build_pack as build_executive_review_pack  # noqa: E402
from scripts.build_release_evidence_pack import main as build_release_evidence_pack  # noqa: E402
from scripts.build_synthetic_benchmark import main as build_synthetic_benchmark  # noqa: E402


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
    room_slug = _slugify(deal_name)
    deal_room_dir = DIST_DIR / "deal-rooms" / room_slug
    deal_room_dir.mkdir(parents=True, exist_ok=True)

    build_synthetic_benchmark()
    build_client_proposal_pack()
    build_executive_review_pack()
    build_client_microsite()
    build_release_evidence_pack()

    proposal = _load_json(DIST_DIR / "client-proposal-pack" / "client_proposal.json")
    review = _load_json(DIST_DIR / "executive-review-pack" / "executive_review_pack.json")
    solution_profile = proposal["solution_profile"]

    copies = {
        "client_proposal.html": DIST_DIR / "client-proposal-pack" / "client_proposal.html",
        "client_proposal.md": DIST_DIR / "client-proposal-pack" / "client_proposal.md",
        "client_proposal.json": DIST_DIR / "client-proposal-pack" / "client_proposal.json",
        "executive_review_pack.html": DIST_DIR / "executive-review-pack" / "executive_review_pack.html",
        "executive_review_pack.md": DIST_DIR / "executive-review-pack" / "executive_review_pack.md",
        "executive_review_pack.json": DIST_DIR / "executive-review-pack" / "executive_review_pack.json",
        "microsite.html": DIST_DIR / "client-microsite" / "index.html",
        "industry_benchmark.csv": DIST_DIR / "benchmarks" / "industry_benchmark.csv",
        f"release-evidence-pack-{release_tag}.tar.gz": DIST_DIR / f"release-evidence-pack-{release_tag}.tar.gz",
    }

    artifacts = []
    for name, src in copies.items():
        dest = deal_room_dir / name
        shutil.copy2(src, dest)
        artifacts.append({"name": name, "source": str(src.relative_to(ROOT))})

    summary_md = deal_room_dir / "README.md"
    summary_md.write_text(
        "\n".join(
            [
                f"# Deal Room: {proposal_client_name}",
                "",
                f"Deal name: {deal_name}",
                f"Industry: {solution_profile.get('industry', 'n/a')}",
                f"Package: {solution_profile.get('package', {}).get('name', 'n/a')}",
                "",
                "## Included Assets",
                "- client proposal pack",
                "- executive review pack",
                "- client microsite",
                "- benchmark snapshot",
                "- release evidence pack",
                "",
                "## Why This Deal Room Exists",
                "Use this directory as a sales engineering handoff for discovery, proposal review, and executive follow-up.",
                "",
                f"Current value at risk: ${proposal.get('summary', {}).get('total_value_at_risk_usd', 0.0):,.0f}",
                f"Current quality score: {proposal.get('scorecard', {}).get('overall_score', 0.0):.1f}",
                f"Recommended package: {solution_profile.get('package', {}).get('delivery_model', 'n/a')}",
                "",
                "## Approval Status",
                "Formal sign-off workflow generated in `approvals/approval_workflow.json`.",
                "",
                "## Top Executive Signal",
                review.get("insights", {}).get("insights", [{}])[0].get("headline", "n/a"),
            ]
        ),
        encoding="utf-8",
    )

    approvals_dir = deal_room_dir / "approvals"
    approvals_dir.mkdir(parents=True, exist_ok=True)
    approval_workflow = build_approval_workflow(
        deal_name=deal_name,
        proposal_client_name=proposal_client_name,
        artifact_version=release_tag,
        release_tag=release_tag,
        approval_overrides=load_approval_overrides(),
    )
    (approvals_dir / "approval_workflow.json").write_text(
        json.dumps(approval_workflow, indent=2),
        encoding="utf-8",
    )

    manifest = {
        "deal_name": deal_name,
        "proposal_client_name": proposal_client_name,
        "room_slug": room_slug,
        "industry": solution_profile.get("industry", "n/a"),
        "package": solution_profile.get("package", {}).get("name", "n/a"),
        "approval_status": {
            "approved_stage_count": approval_workflow["approved_stage_count"],
            "stage_count": approval_workflow["stage_count"],
            "ready_for_client_delivery": approval_workflow["ready_for_client_delivery"],
        },
        "artifacts": artifacts,
    }
    (deal_room_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    archive_path = DIST_DIR / f"deal-room-{room_slug}.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(deal_room_dir, arcname=deal_room_dir.name)

    print(f"Deal room generated in {deal_room_dir}")
    print(f"Deal room archive generated at {archive_path}")


if __name__ == "__main__":
    main()
