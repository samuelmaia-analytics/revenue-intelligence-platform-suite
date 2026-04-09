from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validation_module(root: Path):
    script_path = root / "scripts" / "validate_showcase_artifacts.py"
    spec = importlib.util.spec_from_file_location("validate_showcase_artifacts", script_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load validation module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_showcase_validation_script_passes_for_current_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    validator = _load_validation_module(root)
    validator.main()
