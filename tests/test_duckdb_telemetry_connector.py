from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from platform_connectors import DuckDBTelemetryConnector, seed_demo_telemetry_duckdb

pytest.importorskip("duckdb")


def test_duckdb_connector_reads_seeded_telemetry(tmp_path: Path) -> None:
    db_path = tmp_path / "enterprise_telemetry.duckdb"
    monthly = pd.DataFrame(
        [
            {"month": "2026-01", "SALES": 100000.0},
            {"month": "2026-02", "SALES": 108000.0},
        ]
    )
    seed_demo_telemetry_duckdb(db_path, monthly)

    connector = DuckDBTelemetryConnector(db_path)
    telemetry = connector.fetch_monthly_revenue_telemetry()
    latest = connector.fetch_latest_kpis()

    assert len(telemetry) == 2
    assert {"month", "revenue_usd", "nrr", "gross_churn"}.issubset(telemetry.columns)
    assert latest["latest_month"] == "2026-02"
    assert latest["latest_revenue_usd"] == 108000.0
