from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.core.logging import get_logger
from src.quality.validation import (
    DataQualityError,
    DataValidationRule,
    validate_dataset,
    validate_silver_tables,
)

LOGGER = get_logger("revenue_intelligence.transform")


def build_silver_layer(
    bronze_customers_path: Path,
    bronze_orders_path: Path,
    bronze_marketing_path: Path,
    silver_dir: Path,
    *,
    quality_report_path: Path | None = None,
) -> tuple[Path, Path, Path]:
    silver_dir.mkdir(parents=True, exist_ok=True)

    customers = pd.read_csv(bronze_customers_path, parse_dates=["signup_date"], low_memory=False)
    orders = pd.read_csv(bronze_orders_path, parse_dates=["order_date"], low_memory=False)
    marketing = pd.read_csv(bronze_marketing_path, low_memory=False)

    bronze_reports = [
        validate_dataset(
        customers,
        table_name="bronze_customers",
        rule=DataValidationRule(required_columns=("customer_id", "signup_date", "channel", "segment")),
        ),
        validate_dataset(
        orders,
        table_name="bronze_orders",
        rule=DataValidationRule(required_columns=("order_id", "customer_id", "order_date", "order_value")),
        ),
        validate_dataset(
        marketing,
        table_name="bronze_marketing_spend",
        rule=DataValidationRule(required_columns=("channel", "marketing_spend")),
        ),
    ]
    failed_bronze = [report for report in bronze_reports if report.status != "passed"]
    if failed_bronze:
        raise DataQualityError(f"Bronze validation failed: {[report.table_name for report in failed_bronze]}")

    customers = customers.drop(columns=["_source_file", "_ingestion_ts"], errors="ignore")
    orders = orders.drop(columns=["_source_file", "_ingestion_ts"], errors="ignore")
    marketing = marketing.drop(columns=["_source_file", "_ingestion_ts"], errors="ignore")

    customers = customers.drop_duplicates(subset=["customer_id"]).copy()
    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    marketing = marketing.drop_duplicates(subset=["channel"]).copy()

    customers["customer_id"] = pd.to_numeric(customers["customer_id"], errors="coerce").astype("Int64")
    orders["customer_id"] = pd.to_numeric(orders["customer_id"], errors="coerce").astype("Int64")
    orders["order_value"] = pd.to_numeric(orders["order_value"], errors="coerce")
    marketing["marketing_spend"] = pd.to_numeric(marketing["marketing_spend"], errors="coerce")

    customers = customers.dropna(subset=["customer_id", "signup_date", "channel", "segment"]).copy()
    customers["customer_id"] = customers["customer_id"].astype(int)
    orders = orders.dropna(subset=["order_id", "customer_id", "order_date", "order_value"]).copy()
    orders["customer_id"] = orders["customer_id"].astype(int)
    orders = orders[orders["order_value"] > 0].copy()
    orders = orders[orders["customer_id"].isin(customers["customer_id"])].copy()
    marketing = marketing.dropna(subset=["channel", "marketing_spend"]).copy()
    marketing["marketing_spend"] = marketing["marketing_spend"].clip(lower=0)

    validate_silver_tables(customers, orders, marketing, report_path=quality_report_path)

    silver_customers_path = silver_dir / "silver_customers.csv"
    silver_orders_path = silver_dir / "silver_orders.csv"
    silver_marketing_path = silver_dir / "silver_marketing_spend.csv"
    customers.to_csv(silver_customers_path, index=False)
    orders.to_csv(silver_orders_path, index=False)
    marketing.to_csv(silver_marketing_path, index=False)

    LOGGER.info(
        "Silver layer standardized and validated.",
        extra={"stage": "transformation", "rows": len(customers) + len(orders), "status": "success"},
    )
    return silver_customers_path, silver_orders_path, silver_marketing_path
