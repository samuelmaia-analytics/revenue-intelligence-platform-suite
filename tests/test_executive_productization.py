from __future__ import annotations

from pathlib import Path

import pandas as pd

from common import (
    build_data_quality_scorecard,
    build_recommended_actions,
    build_solution_profile,
    generate_executive_insight_report,
    get_solution_packages,
)


def test_solution_packages_cover_commercial_offers() -> None:
    packages = get_solution_packages()
    package_ids = {package["package_id"] for package in packages}
    assert {
        "revenue_command_center",
        "retention_intelligence",
        "executive_kpi_governance",
        "commercial_performance_analytics",
    }.issubset(package_ids)


def test_solution_profile_marks_multi_tenant_readiness() -> None:
    profile = build_solution_profile(client_name="HealthCo", industry="Healthtech")
    assert profile["client_name"] == "HealthCo"
    assert profile["industry"] == "Healthtech"
    assert profile["multi_tenant_ready"] is True
    assert "client" in profile["config_layers"]


def test_quality_scorecard_and_insight_generation(tmp_path: Path) -> None:
    customer_path = tmp_path / "customers.csv"
    sales_path = tmp_path / "sales.csv"
    customer_path.write_text("id\n1\n", encoding="utf-8")
    sales_path.write_text("id\n1\n", encoding="utf-8")

    monthly_revenue = pd.DataFrame(
        [{"month": "2026-01", "SALES": 1000.0}, {"month": "2026-02", "SALES": 900.0}]
    )
    risk_df = pd.DataFrame(
        [
            {
                "Customer ID": "C-1",
                "Risk Score": 0.92,
                "Revenue at Risk (USD)": 2000.0,
                "Recommended Action": "Executive Save Offer",
            }
        ]
    )
    summary = {
        "latest_month": "2026-02",
        "nrr_latest": 0.85,
        "gross_churn_latest": 0.15,
        "total_value_at_risk_usd": 2000.0,
        "top_50_value_at_risk_usd": 2000.0,
    }
    model_metrics = {
        "churn": {"temporal_test_roc_auc": 0.71},
        "next_purchase_30d": {"temporal_test_roc_auc": 0.69},
    }

    scorecard = build_data_quality_scorecard(
        summary=summary,
        monthly_revenue=monthly_revenue,
        risk_df=risk_df,
        model_metrics=model_metrics,
        customer_file_path=customer_path,
        sales_file_path=sales_path,
    )
    actions = build_recommended_actions(risk_df, uplift_pct=10)
    report = generate_executive_insight_report(summary, scorecard, actions)

    assert scorecard["overall_score"] <= 85
    assert actions[0]["priority"] == "P1"
    assert report["generation_mode"] == "deterministic_fallback"
    assert any(insight["type"] == "risk" for insight in report["insights"])
