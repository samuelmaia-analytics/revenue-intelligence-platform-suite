from __future__ import annotations

from pathlib import Path


def test_google_workspace_stack_assets_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "docker-compose.yml",
        root / "deploy" / "oauth2-proxy" / "google-workspace.env.example",
        root / "deploy" / "oauth2-proxy" / "README.md",
        root / "docs" / "docker-compose.md",
        root / "docs" / "sso.md",
    ]
    missing = [path for path in required if not path.exists()]
    assert not missing, f"Missing Google Workspace stack assets: {missing}"
