from __future__ import annotations

from common import get_semantic_metric, list_semantic_metrics, load_semantic_metric_catalog


def test_semantic_metric_catalog_contains_core_metrics() -> None:
    catalog = load_semantic_metric_catalog()
    assert catalog["catalog_version"] == "1.0.0"
    metric_ids = {metric["metric_id"] for metric in list_semantic_metrics()}
    assert {
        "latest_revenue_usd",
        "nrr_latest",
        "gross_churn_latest",
        "total_value_at_risk_usd",
        "overall_score",
        "adoption_rate",
    }.issubset(metric_ids)


def test_get_semantic_metric_returns_expected_payload() -> None:
    metric = get_semantic_metric("nrr_latest")
    assert metric["domain"] == "retention"
    assert "retention" in metric["executive_use"].lower()
