from __future__ import annotations

from pathlib import Path


def test_protected_stack_assets_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "docker-compose.yml",
        root / "deploy" / "nginx" / "executive-proxy.conf",
        root / "docs" / "docker-compose.md",
        root / "docs" / "sso.md",
    ]
    missing = [path for path in required if not path.exists()]
    assert not missing, f"Missing protected stack assets: {missing}"
