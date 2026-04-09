from __future__ import annotations

from pathlib import Path


def test_required_controls_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "LICENSE",
        root / "NOTICE",
        root / "SECURITY.md",
        root / ".github" / "CODEOWNERS",
        root / "docs" / "compliance-checklist.md",
        root / "docs" / "privacy-and-lgpd-policy.md",
        root / "docs" / "data-retention-matrix.md",
        root / "docs" / "client-data-onboarding-template.md",
        root / "docs" / "governance-raci.md",
        root / "docs" / "tenant-secrets.md",
        root / "docs" / "sso.md",
        root / "docs" / "approval-workflow.md",
        root / "docs" / "external-publication.md",
        root / "docs" / "adr" / "0002-privacy-and-client-data-governance.md",
    ]
    missing = [path for path in required if not path.exists()]
    assert not missing, f"Missing required controls: {missing}"
