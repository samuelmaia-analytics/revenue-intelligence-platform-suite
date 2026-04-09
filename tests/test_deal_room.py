from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(root: Path, relative_script: str, module_name: str):
    script_path = root / relative_script
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_deal_room() -> None:
    root = Path(__file__).resolve().parents[1]
    deal_module = _load_module(root, "scripts/build_deal_room.py", "build_deal_room")
    deal_module.main()
    assert (root / "dist" / "deal-rooms" / "flagship-client" / "manifest.json").exists()
    assert (
        root / "dist" / "deal-rooms" / "flagship-client" / "approvals" / "approval_workflow.json"
    ).exists()
    assert (root / "dist" / "deal-room-flagship-client.tar.gz").exists()
