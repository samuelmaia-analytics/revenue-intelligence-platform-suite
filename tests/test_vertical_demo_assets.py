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


def test_build_industry_demo_packs_and_benchmark() -> None:
    root = Path(__file__).resolve().parents[1]
    benchmark_module = _load_module(root, "scripts/build_synthetic_benchmark.py", "build_synthetic_benchmark")
    packs_module = _load_module(root, "scripts/build_industry_demo_packs.py", "build_industry_demo_packs")

    benchmark_module.main()
    packs_module.main()

    assert (root / "dist" / "benchmarks" / "industry_benchmark.csv").exists()
    assert (root / "dist" / "industry-demo-packs" / "manifest.json").exists()
    assert (
        root / "dist" / "industry-demo-packs" / "saas_b2b" / "executive_review_pack.html"
    ).exists()
    assert (root / "dist" / "industry-demo-packs" / "saas_b2b" / "client_proposal.html").exists()
    assert (root / "dist" / "industry-demo-packs" / "saas_b2b" / "microsite_index.html").exists()
