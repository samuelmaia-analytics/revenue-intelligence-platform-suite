from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pandas as pd

from common.contracts import validate_contract


def _load_showcase_module(root: Path):
    script_path = root / "scripts" / "run_showcase_demo.py"
    spec = importlib.util.spec_from_file_location("run_showcase_demo", script_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load showcase module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_showcase_build_risk_score_applies_expected_thresholds() -> None:
    root = Path(__file__).resolve().parents[1]
    showcase = _load_showcase_module(root)

    frame = pd.DataFrame(
        [
            {
                "Days Since Last Purchase": 120,
                "Total Spend": 1000.0,
                "Satisfaction Level": "Unsatisfied",
            },
            {
                "Days Since Last Purchase": 75,
                "Total Spend": 400.0,
                "Satisfaction Level": "Neutral",
            },
            {
                "Days Since Last Purchase": 5,
                "Total Spend": 100.0,
                "Satisfaction Level": "Satisfied",
            },
        ]
    )

    risk = showcase.build_risk_score(frame)

    assert risk["Risk Score"].between(0, 1).all()
    assert risk["Recommended Action"].tolist() == [
        "Executive Save Offer",
        "CSM Priority Call",
        "Nurture Campaign",
    ]
    assert risk["Revenue at Risk (USD)"].iloc[0] > risk["Revenue at Risk (USD)"].iloc[-1]


def test_showcase_main_generates_contract_valid_summary(tmp_path: Path, monkeypatch) -> None:
    root = Path(__file__).resolve().parents[1]
    showcase = _load_showcase_module(root)

    sales_path = tmp_path / "sales.csv"
    customer_path = tmp_path / "customers.csv"
    metrics_path = tmp_path / "metrics_report.json"
    output_dir = tmp_path / "showcase"

    pd.DataFrame(
        [
            {"ORDERDATE": "2026-01-10", "SALES": 1000.0},
            {"ORDERDATE": "2026-02-10", "SALES": 1100.0},
            {"ORDERDATE": "2026-02-25", "SALES": 400.0},
        ]
    ).to_csv(sales_path, index=False)
    pd.DataFrame(
        [
            {
                "Customer ID": "C-001",
                "Days Since Last Purchase": 90,
                "Total Spend": 1200.0,
                "Satisfaction Level": "Unsatisfied",
            },
            {
                "Customer ID": "C-002",
                "Days Since Last Purchase": 40,
                "Total Spend": 800.0,
                "Satisfaction Level": "Neutral",
            },
            {
                "Customer ID": "C-003",
                "Days Since Last Purchase": 5,
                "Total Spend": 150.0,
                "Satisfaction Level": "Satisfied",
            },
        ]
    ).to_csv(customer_path, index=False)
    metrics_path.write_text(
        json.dumps(
            {
                "churn": {"temporal_test_roc_auc": 0.81},
                "next_purchase_30d": {"temporal_test_roc_auc": 0.77},
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(showcase, "SALES_PATH", sales_path)
    monkeypatch.setattr(showcase, "CUSTOMER_PATH", customer_path)
    monkeypatch.setattr(showcase, "MODEL_METRICS_PATH", metrics_path)
    monkeypatch.setattr(showcase, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(showcase, "TELEMETRY_DB_PATH", output_dir / "enterprise_telemetry.sqlite")
    monkeypatch.setattr(showcase, "TELEMETRY_DUCKDB_PATH", output_dir / "enterprise_telemetry.duckdb")
    monkeypatch.setattr(showcase, "TELEMETRY_BACKEND", "sqlite")

    showcase.main()

    summary_path = output_dir / "summary.json"
    top_actions_path = output_dir / "top_actions.csv"
    telemetry_path = output_dir / "enterprise_telemetry.sqlite"
    solution_profile_path = output_dir / "solution_profile.json"
    data_quality_scorecard_path = output_dir / "data_quality_scorecard.json"
    executive_insights_path = output_dir / "executive_insights.json"

    assert summary_path.exists()
    assert top_actions_path.exists()
    assert telemetry_path.exists()
    assert solution_profile_path.exists()
    assert data_quality_scorecard_path.exists()
    assert executive_insights_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    solution_profile = json.loads(solution_profile_path.read_text(encoding="utf-8"))
    quality_scorecard = json.loads(data_quality_scorecard_path.read_text(encoding="utf-8"))
    executive_insights = json.loads(executive_insights_path.read_text(encoding="utf-8"))
    assert not validate_contract(summary, "showcase_summary.schema.json")
    assert summary["latest_month"] == "2026-02"
    assert summary["latest_revenue_usd"] == 1500.0
    assert summary["top_50_value_at_risk_usd"] <= summary["total_value_at_risk_usd"]
    assert solution_profile["multi_tenant_ready"] is True
    assert quality_scorecard["status"] in {"healthy", "watch", "critical"}
    assert executive_insights["generation_mode"] == "deterministic_fallback"
