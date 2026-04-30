from pathlib import Path

import pandas as pd
import pytest

from src.quality.validation import DataQualityError, validate_silver_tables
from src.transform.silver import build_silver_layer


def test_validate_silver_tables_rejects_duplicate_orders() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": [1],
            "signup_date": ["2025-01-01"],
            "channel": ["Organic"],
            "segment": ["SMB"],
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": ["O1", "O1"],
            "customer_id": [1, 1],
            "order_date": ["2025-01-10", "2025-01-11"],
            "order_value": [100.0, 120.0],
        }
    )
    marketing = pd.DataFrame({"channel": ["Organic"], "marketing_spend": [1000.0]})

    with pytest.raises(DataQualityError):
        validate_silver_tables(customers, orders, marketing)


def test_build_silver_layer_emits_quality_report(tmp_path: Path) -> None:
    bronze_dir = tmp_path / "bronze"
    silver_dir = tmp_path / "silver"
    bronze_dir.mkdir(parents=True, exist_ok=True)
    report_path = tmp_path / "processed" / "data_quality_report.json"

    pd.DataFrame(
        {
            "customer_id": [1, 1, 2],
            "signup_date": ["2025-01-01", "2025-01-01", "2025-01-02"],
            "channel": ["Organic", "Organic", "Paid Search"],
            "segment": ["SMB", "SMB", "Mid-Market"],
        }
    ).to_csv(bronze_dir / "bronze_customers.csv", index=False)
    pd.DataFrame(
        {
            "order_id": ["O1", "O2"],
            "customer_id": [1, 2],
            "order_date": ["2025-01-10", "2025-01-11"],
            "order_value": [120.0, 200.0],
        }
    ).to_csv(bronze_dir / "bronze_orders.csv", index=False)
    pd.DataFrame({"channel": ["Organic", "Paid Search"], "marketing_spend": [1000, 2000]}).to_csv(
        bronze_dir / "bronze_marketing_spend.csv", index=False
    )

    build_silver_layer(
        bronze_dir / "bronze_customers.csv",
        bronze_dir / "bronze_orders.csv",
        bronze_dir / "bronze_marketing_spend.csv",
        silver_dir,
        quality_report_path=report_path,
    )

    assert report_path.exists()
