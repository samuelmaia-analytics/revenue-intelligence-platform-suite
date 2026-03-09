import os
from pathlib import Path

from src.warehouse_loader import WarehouseConfig


def test_warehouse_config_defaults_to_none(monkeypatch) -> None:
    monkeypatch.delenv("RIP_WAREHOUSE_PROVIDER", raising=False)
    cfg = WarehouseConfig.from_env()
    assert cfg.provider == "none"
    assert cfg.dataset == "revenue_intelligence"
    assert cfg.schema == "analytics"


def test_warehouse_config_bigquery(monkeypatch) -> None:
    monkeypatch.setenv("RIP_WAREHOUSE_PROVIDER", "bigquery")
    monkeypatch.setenv("RIP_BQ_PROJECT", "demo-project")
    monkeypatch.setenv("RIP_WAREHOUSE_DATASET", "rip")

    cfg = WarehouseConfig.from_env()
    assert cfg.provider == "bigquery"
    assert cfg.bq_project == "demo-project"
    assert cfg.dataset == "rip"


def test_dbt_structure_exists() -> None:
    project_root = Path(__file__).resolve().parents[1]
    dbt_root = project_root / "dbt"

    expected_paths = [
        dbt_root / "dbt_project.yml",
        dbt_root / "profiles.yml.example",
        dbt_root / "models" / "staging" / "stg_customers.sql",
        dbt_root / "models" / "intermediate" / "int_orders_enriched.sql",
        dbt_root / "models" / "marts" / "mart_revenue_kpis.sql",
    ]

    for path in expected_paths:
        assert path.exists(), f"Missing dbt asset: {os.fspath(path)}"
