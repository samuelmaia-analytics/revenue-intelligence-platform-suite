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


def test_build_external_publication_bundle() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(root, "scripts/build_external_publication_bundle.py", "build_external_publication_bundle")
    module.main()
    publication_dir = root / "dist" / "deal-rooms" / "flagship-client" / "publication"
    assert (publication_dir / "publication_manifest.json").exists()
    assert (publication_dir / "site" / "index.html").exists()
