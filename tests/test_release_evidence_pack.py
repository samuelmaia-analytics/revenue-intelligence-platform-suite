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


def test_build_executive_review_pack_and_release_evidence() -> None:
    root = Path(__file__).resolve().parents[1]
    review_pack = _load_module(root, "scripts/build_executive_review_pack.py", "build_executive_review_pack")
    release_pack = _load_module(root, "scripts/build_release_evidence_pack.py", "build_release_evidence_pack")

    review_outputs = review_pack.build_pack()
    assert review_outputs["markdown"].exists()
    assert review_outputs["html"].exists()
    assert review_outputs["json"].exists()

    release_pack.main()
    archive = root / "dist" / "release-evidence-pack-local.tar.gz"
    assert archive.exists()
