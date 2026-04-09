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


def test_build_gtm_exports() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(root, "scripts/build_gtm_exports.py", "build_gtm_exports")
    module.main()
    exports_dir = root / "dist" / "deal-rooms" / "flagship-client" / "sales-enablement" / "exports"
    assert (exports_dir / "hubspot_deal_payload.json").exists()
    assert (exports_dir / "salesforce_opportunity_payload.json").exists()
    assert (exports_dir / "notion_page_payload.json").exists()
    assert (exports_dir / "microsite_publish_manifest.json").exists()
