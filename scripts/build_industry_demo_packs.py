from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist" / "industry-demo-packs"


PROFILES = [
    ("saas_b2b", "revenue_command_center"),
    ("healthtech_growth", "retention_intelligence"),
    ("retail_omnichannel", "commercial_performance_analytics"),
]


def _run_showcase(profile: str, package: str) -> None:
    env = os.environ.copy()
    env["CLIENT_PROFILE"] = profile
    env["SOLUTION_PACKAGE"] = package
    env["DEPLOYMENT_ENV"] = "showcase"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_showcase_demo.py")],
        check=True,
        cwd=ROOT,
        env=env,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_executive_review_pack.py")],
        check=True,
        cwd=ROOT,
        env=env,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_client_proposal_pack.py")],
        check=True,
        cwd=ROOT,
        env=env,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_client_microsite.py")],
        check=True,
        cwd=ROOT,
        env=env,
    )


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, str]] = []
    for profile, package in PROFILES:
        _run_showcase(profile, package)
        target_dir = DIST_DIR / profile
        target_dir.mkdir(parents=True, exist_ok=True)

        copies = {
            "summary.json": ROOT / "reports" / "showcase" / "summary.json",
            "solution_profile.json": ROOT / "reports" / "showcase" / "solution_profile.json",
            "data_quality_scorecard.json": ROOT / "reports" / "showcase" / "data_quality_scorecard.json",
            "executive_insights.json": ROOT / "reports" / "showcase" / "executive_insights.json",
            "executive_review_pack.json": ROOT / "dist" / "executive-review-pack" / "executive_review_pack.json",
            "executive_review_pack.md": ROOT / "dist" / "executive-review-pack" / "executive_review_pack.md",
            "executive_review_pack.html": ROOT / "dist" / "executive-review-pack" / "executive_review_pack.html",
            "client_proposal.json": ROOT / "dist" / "client-proposal-pack" / "client_proposal.json",
            "client_proposal.md": ROOT / "dist" / "client-proposal-pack" / "client_proposal.md",
            "client_proposal.html": ROOT / "dist" / "client-proposal-pack" / "client_proposal.html",
            "microsite_index.html": ROOT / "dist" / "client-microsite" / "index.html",
        }
        for name, src in copies.items():
            dest = target_dir / name
            dest.write_bytes(src.read_bytes())
        manifest.append({"profile": profile, "package": package, "output_dir": str(target_dir.relative_to(ROOT))})

    (DIST_DIR / "manifest.json").write_text(json.dumps({"demo_packs": manifest}, indent=2), encoding="utf-8")
    print(f"Industry demo packs generated in {DIST_DIR}")


if __name__ == "__main__":
    main()
