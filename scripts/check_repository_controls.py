from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required_files = [
        ROOT / "LICENSE",
        ROOT / "NOTICE",
        ROOT / "SECURITY.md",
        ROOT / ".github" / "CODEOWNERS",
        ROOT / "docs" / "compliance-checklist.md",
        ROOT / "docs" / "privacy-and-lgpd-policy.md",
        ROOT / "docs" / "data-retention-matrix.md",
        ROOT / "docs" / "client-data-onboarding-template.md",
        ROOT / "docs" / "governance-raci.md",
        ROOT / "docs" / "tenant-secrets.md",
        ROOT / "docs" / "sso.md",
        ROOT / "docs" / "approval-workflow.md",
        ROOT / "docs" / "external-publication.md",
        ROOT / "docs" / "adr" / "0002-privacy-and-client-data-governance.md",
        ROOT / "config" / "secrets" / "README.md",
        ROOT / "config" / "secrets" / "templates" / "global.template.json",
    ]

    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required repository controls: {missing}")

    print("Repository compliance and governance controls are present.")


if __name__ == "__main__":
    sys.exit(main())
