from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .base import TelemetryConnector

try:
    import duckdb
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    duckdb = None


TELEMETRY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS revenue_telemetry (
    month VARCHAR PRIMARY KEY,
    revenue_usd DOUBLE NOT NULL,
    nrr DOUBLE NOT NULL,
    gross_churn DOUBLE NOT NULL,
    source_system VARCHAR NOT NULL,
    ingested_at VARCHAR NOT NULL
);
"""


class DuckDBTelemetryConnector(TelemetryConnector):
    """DuckDB-backed telemetry connector used as enterprise-like mock."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def fetch_monthly_revenue_telemetry(self) -> pd.DataFrame:
        if duckdb is None:
            raise ModuleNotFoundError("duckdb is required for DuckDBTelemetryConnector")
        if not self.db_path.exists():
            return pd.DataFrame(
                columns=[
                    "month",
                    "revenue_usd",
                    "nrr",
                    "gross_churn",
                    "source_system",
                    "ingested_at",
                ]
            )
        with duckdb.connect(str(self.db_path)) as conn:
            return conn.sql(
                """
                SELECT month, revenue_usd, nrr, gross_churn, source_system, ingested_at
                FROM revenue_telemetry
                ORDER BY month
                """
            ).df()

    def fetch_latest_kpis(self) -> dict[str, Any]:
        telemetry = self.fetch_monthly_revenue_telemetry()
        if telemetry.empty:
            return {
                "latest_month": None,
                "latest_revenue_usd": 0.0,
                "nrr_latest": 1.0,
                "gross_churn_latest": 0.0,
                "source_system": "duckdb-enterprise-mock",
            }
        latest = telemetry.iloc[-1]
        return {
            "latest_month": str(latest["month"]),
            "latest_revenue_usd": float(latest["revenue_usd"]),
            "nrr_latest": float(latest["nrr"]),
            "gross_churn_latest": float(latest["gross_churn"]),
            "source_system": str(latest["source_system"]),
        }


def seed_demo_telemetry_duckdb(db_path: Path, monthly_revenue: pd.DataFrame) -> None:
    if duckdb is None:
        raise ModuleNotFoundError("duckdb is required for seed_demo_telemetry_duckdb")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if monthly_revenue.empty:
        rows = pd.DataFrame(
            [
                {
                    "month": "1970-01",
                    "revenue_usd": 0.0,
                    "nrr": 1.0,
                    "gross_churn": 0.0,
                    "source_system": "erp_warehouse_snapshot",
                    "ingested_at": pd.Timestamp.utcnow().isoformat(),
                }
            ]
        )
    else:
        rows = monthly_revenue.rename(columns={"SALES": "revenue_usd"}).copy()
        rows["nrr"] = (rows["revenue_usd"] / rows["revenue_usd"].shift(1)).fillna(1.0).clip(
            lower=0.6, upper=1.2
        )
        rows["gross_churn"] = (1 - rows["nrr"]).clip(lower=0)
        rows["source_system"] = "erp_warehouse_snapshot"
        rows["ingested_at"] = pd.Timestamp.utcnow().isoformat()
        rows = rows[
            ["month", "revenue_usd", "nrr", "gross_churn", "source_system", "ingested_at"]
        ]

    with duckdb.connect(str(db_path)) as conn:
        conn.execute(TELEMETRY_TABLE_SQL)
        conn.execute("DELETE FROM revenue_telemetry")
        conn.register("rows_df", rows)
        conn.execute("INSERT INTO revenue_telemetry SELECT * FROM rows_df")
