from __future__ import annotations

import importlib.util
from pathlib import Path

from common import build_approval_workflow


def _load_module(root: Path, relative_script: str, module_name: str):
    script_path = root / relative_script
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_approval_workflow_defaults_to_pending() -> None:
    workflow = build_approval_workflow(
        deal_name="Flagship Client",
        proposal_client_name="Flagship Client",
        artifact_version="local",
        release_tag="local",
    )
    assert workflow["stage_count"] == 4
    assert workflow["approved_stage_count"] == 0
    assert workflow["ready_for_client_delivery"] is False


def test_build_formal_approval_pack_creates_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(root, "scripts/build_formal_approval_pack.py", "build_formal_approval_pack")
    module.main()
    approvals_dir = root / "dist" / "deal-rooms" / "flagship-client" / "approvals"
    assert (approvals_dir / "approval_workflow.json").exists()
    assert (approvals_dir / "approval_log.csv").exists()
    assert (approvals_dir / "approval_summary.md").exists()
