from __future__ import annotations

import json
from pathlib import Path

from common.contracts import validate_contract


def test_showcase_summary_contract_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "reports" / "showcase" / "summary.json"
    assert summary_path.exists(), "Missing showcase summary artifact."

    with summary_path.open("r", encoding="utf-8") as fp:
        summary = json.load(fp)

    errors = validate_contract(summary, "showcase_summary.schema.json")
    assert not errors, f"Showcase summary contract errors: {errors}"


def test_action_adoption_event_contract_is_valid() -> None:
    event = {
        "action_id": "CUST-100::Executive Save Offer",
        "timestamp": "2026-03-05T00:00:00Z",
        "outcome": "accepted",
        "metadata": {"owner": "CSM Team A"},
    }
    errors = validate_contract(event, "action_adoption_event.schema.json")
    assert not errors, f"Action adoption contract errors: {errors}"


def test_versioned_contracts_are_compatible_with_current_payloads() -> None:
    summary = {
        "latest_month": "2026-03",
        "latest_revenue_usd": 1000.0,
        "nrr_latest": 0.93,
        "gross_churn_latest": 0.07,
        "total_value_at_risk_usd": 150.0,
        "top_50_value_at_risk_usd": 150.0,
        "churn_auc_temporal_test": 0.81,
        "next_purchase_auc_temporal_test": 0.78,
        "telemetry_source": "sqlite",
    }
    report = {
        "report_version": "1.0.0",
        "generation_mode": "deterministic_fallback",
        "llm_enabled": False,
        "package": {"package_id": "revenue_command_center"},
        "thresholds": {"nrr_floor": 0.9},
        "prompt_policy": {"prompt_template_version": "deterministic-v1"},
        "recommended_actions": [],
        "insights": [],
        "generated_at": "2026-03-05T00:00:00Z",
    }

    assert not validate_contract(summary, "showcase_summary.v1.schema.json")
    action_event = {
        "action_id": "CUST-100::Executive Save Offer",
        "timestamp": "2026-03-05T00:00:00Z",
        "outcome": "accepted",
        "metadata": {"owner": "CSM Team A"},
    }

    assert not validate_contract(action_event, "action_adoption_event.v1.schema.json")
    assert not validate_contract(report, "executive_insight_report.v1.schema.json")
