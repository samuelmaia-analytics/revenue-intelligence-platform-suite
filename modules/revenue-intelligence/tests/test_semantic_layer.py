from pathlib import Path

import pandas as pd
import pytest

from src.analytics.semantic_layer import (
    METRIC_CATALOG,
    calculate_growth_rate,
    calculate_retention_rate,
    cohort_analysis,
)


def test_metric_catalog_contains_core_revenue_kpis() -> None:
    assert {"revenue", "growth_rate", "arpu", "retention_rate", "churn_rate"}.issubset(
        METRIC_CATALOG.keys()
    )


def test_calculate_growth_rate_uses_latest_two_periods() -> None:
    revenue = pd.Series([100.0, 125.0, 150.0])
    assert calculate_growth_rate(revenue) == pytest.approx(0.2)


def test_calculate_retention_rate_returns_average_cohort_retention() -> None:
    cohort_df = pd.DataFrame({"retention_rate": [1.0, 0.5, 0.25]})
    assert calculate_retention_rate(cohort_df) == 0.5833333333333334


def test_cohort_analysis_adds_churn_rate(tmp_path: Path) -> None:
    customers_path = tmp_path / "customers.csv"
    orders_path = tmp_path / "orders.csv"

    pd.DataFrame(
        {
            "customer_id": [1, 2],
            "signup_date": ["2025-01-01", "2025-01-10"],
            "channel": ["Organic", "Paid Search"],
            "segment": ["SMB", "Enterprise"],
        }
    ).to_csv(customers_path, index=False)
    pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3"],
            "customer_id": [1, 1, 2],
            "order_date": ["2025-01-05", "2025-02-05", "2025-01-20"],
            "order_value": [100.0, 120.0, 300.0],
        }
    ).to_csv(orders_path, index=False)

    cohort_df = cohort_analysis(orders_path, customers_path)
    assert {"retention_rate", "churn_rate"}.issubset(cohort_df.columns)
    assert cohort_df["retention_rate"].between(0, 1).all()
