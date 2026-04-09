from __future__ import annotations

import json
import os
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from scripts.build_executive_review_pack import build_pack  # noqa: E402
from scripts.build_client_proposal_pack import main as build_client_proposal_pack  # noqa: E402
from scripts.build_client_microsite import main as build_client_microsite  # noqa: E402


SHOWCASE_DIR = ROOT / "reports" / "showcase"
DIST_DIR = ROOT / "dist"


def main() -> None:
    tag = os.getenv("RELEASE_TAG", "local")
    evidence_dir = DIST_DIR / f"release-evidence-{tag}"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    build_pack()
    build_client_proposal_pack()
    build_client_microsite()

    files_to_copy = [
        SHOWCASE_DIR / "summary.json",
        SHOWCASE_DIR / "solution_profile.json",
        SHOWCASE_DIR / "data_quality_scorecard.json",
        SHOWCASE_DIR / "executive_insights.json",
        SHOWCASE_DIR / "action_adoption_metrics.json",
        SHOWCASE_DIR / "monitoring_summary.json",
        DIST_DIR / "executive-review-pack" / "executive_review_pack.md",
        DIST_DIR / "executive-review-pack" / "executive_review_pack.html",
        DIST_DIR / "executive-review-pack" / "executive_review_pack.json",
        DIST_DIR / "client-proposal-pack" / "client_proposal.md",
        DIST_DIR / "client-proposal-pack" / "client_proposal.html",
        DIST_DIR / "client-proposal-pack" / "client_proposal.json",
        DIST_DIR / "client-microsite" / "index.html",
        DIST_DIR / "executive-review-pack" / "board_summary.csv",
        DIST_DIR / "executive-review-pack" / "top_actions.csv",
    ]

    manifest = []
    for src in files_to_copy:
        dest = evidence_dir / src.name
        shutil.copy2(src, dest)
        manifest.append({"file": src.name, "source": str(src.relative_to(ROOT))})

    manifest_path = evidence_dir / "manifest.json"
    manifest_path.write_text(json.dumps({"tag": tag, "artifacts": manifest}, indent=2), encoding="utf-8")

    archive_path = DIST_DIR / f"release-evidence-pack-{tag}.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(evidence_dir, arcname=evidence_dir.name)

    print(f"Release evidence pack generated: {archive_path}")


if __name__ == "__main__":
    main()
