from __future__ import annotations

import importlib.util
import os
from pathlib import Path


def _load_module(root: Path, relative_script: str, module_name: str):
    script_path = root / relative_script
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prepare_github_pages_publication_requires_ready_approval() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(
        root,
        "scripts/prepare_github_pages_publication.py",
        "prepare_github_pages_publication_unapproved",
    )
    original = os.environ.get("ALLOW_UNAPPROVED_PUBLICATION")
    os.environ.pop("ALLOW_UNAPPROVED_PUBLICATION", None)
    try:
        try:
            module.main()
        except SystemExit as exc:
            assert "ready_for_external_publication=false" in str(exc)
        else:
            raise AssertionError("Expected publication to be blocked when approvals are pending.")
    finally:
        if original is None:
            os.environ.pop("ALLOW_UNAPPROVED_PUBLICATION", None)
        else:
            os.environ["ALLOW_UNAPPROVED_PUBLICATION"] = original


def test_prepare_github_pages_publication_generates_site_when_allowed() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(
        root,
        "scripts/prepare_github_pages_publication.py",
        "prepare_github_pages_publication_allowed",
    )
    original = os.environ.get("ALLOW_UNAPPROVED_PUBLICATION")
    os.environ["ALLOW_UNAPPROVED_PUBLICATION"] = "1"
    try:
        module.main()
        assert (root / "dist" / "github-pages" / "flagship-client" / "index.html").exists()
    finally:
        if original is None:
            os.environ.pop("ALLOW_UNAPPROVED_PUBLICATION", None)
        else:
            os.environ["ALLOW_UNAPPROVED_PUBLICATION"] = original
