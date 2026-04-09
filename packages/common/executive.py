from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_THRESHOLDS = {
    "nrr_floor": 0.9,
    "gross_churn_ceiling": 0.1,
    "quality_score_floor": 85.0,
    "freshness_max_days": 30,
    "roi_floor": 0.15,
}


@dataclass(frozen=True)
class SolutionPackage:
    package_id: str
    name: str
    buyer: str
    primary_outcomes: list[str]
    typical_metrics: list[str]
    delivery_model: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


SOLUTION_PACKAGES = {
    "revenue_command_center": SolutionPackage(
        package_id="revenue_command_center",
        name="Revenue Command Center",
        buyer="CRO / VP Revenue / Revenue Operations",
        primary_outcomes=[
            "Protect expansion and recurring revenue",
            "Prioritize accounts and actions by financial impact",
            "Create a weekly executive operating cadence",
        ],
        typical_metrics=["Revenue at Risk", "NRR", "Expansion Pipeline", "Recovery ROI"],
        delivery_model="Executive board + action register + telemetry instrumentation",
    ),
    "retention_intelligence": SolutionPackage(
        package_id="retention_intelligence",
        name="Retention Intelligence",
        buyer="Chief Customer Officer / VP Customer Success",
        primary_outcomes=[
            "Detect churn exposure before revenue is lost",
            "Rank save plays by account and segment",
            "Track save motion adoption and realized recovery",
        ],
        typical_metrics=["Gross Churn", "Retention Exposure", "Save Rate", "Recovery Value"],
        delivery_model="Risk scoring + recommended actions + action outcome monitoring",
    ),
    "executive_kpi_governance": SolutionPackage(
        package_id="executive_kpi_governance",
        name="Executive KPI Governance",
        buyer="CEO / COO / CFO / Strategy",
        primary_outcomes=[
            "Standardize definitions across revenue and customer KPIs",
            "Expose freshness, quality, and accountability gaps",
            "Create governance for executive decision support",
        ],
        typical_metrics=["KPI Target Gap", "Freshness SLA", "Quality Score", "Owner Coverage"],
        delivery_model="Semantic layer + scorecards + operating governance",
    ),
    "commercial_performance_analytics": SolutionPackage(
        package_id="commercial_performance_analytics",
        name="Commercial Performance Analytics",
        buyer="Sales Leadership / Commercial Operations",
        primary_outcomes=[
            "Improve channel and seller efficiency",
            "Expose margin leakage and pipeline inefficiencies",
            "Support forecast reviews with trusted metrics",
        ],
        typical_metrics=["Channel Efficiency", "AOV", "Conversion", "Pipeline Velocity"],
        delivery_model="Commercial diagnostics + drill-down dashboards + opportunity mapping",
    ),
}


def get_solution_packages() -> list[dict[str, Any]]:
    return [package.to_dict() for package in SOLUTION_PACKAGES.values()]


def build_solution_profile(
    client_name: str = "Flagship Demo Client",
    industry: str = "SaaS",
    deployment_env: str = "showcase",
    package_id: str = "revenue_command_center",
    telemetry_backend: str = "sqlite",
    configuration: dict[str, Any] | None = None,
    profile_id: str = "saas_b2b",
) -> dict[str, Any]:
    package = SOLUTION_PACKAGES[package_id]
    config = configuration or {}
    return {
        "solution_profile_version": "1.0.0",
        "profile_id": config.get("profile_id", profile_id),
        "client_name": config.get("client_name", client_name),
        "industry": config.get("industry", industry),
        "deployment_env": deployment_env,
        "package": package.to_dict(),
        "telemetry_backend": telemetry_backend,
        "multi_tenant_ready": True,
        "config_layers": ["global", "environment", "client", "solution_package"],
        "contract_layers": ["source_contract", "metric_contract", "executive_output_contract"],
        "executive_buyer": config.get("executive_buyer", package.buyer),
        "kpi_focus": config.get("kpi_focus", package.typical_metrics),
        "connectors": config.get("connectors", {}),
        "brand": config.get("brand", {}),
        "narrative": config.get("narrative", {}),
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }


def build_data_quality_scorecard(
    summary: dict[str, Any],
    monthly_revenue: pd.DataFrame,
    risk_df: pd.DataFrame,
    model_metrics: dict[str, Any],
    customer_file_path: Path,
    sales_file_path: Path,
) -> dict[str, Any]:
    latest_month = summary.get("latest_month", "")
    data_currency_anchor = None
    if latest_month:
        data_currency_anchor = pd.Period(latest_month, freq="M").end_time

    file_times = [
        pd.Timestamp(customer_file_path.stat().st_mtime, unit="s"),
        pd.Timestamp(sales_file_path.stat().st_mtime, unit="s"),
    ]
    latest_file_update = max(file_times)
    freshness_days = abs((pd.Timestamp.utcnow().tz_localize(None) - latest_file_update.tz_localize(None)).days)
    data_currency_days = (
        abs((pd.Timestamp.utcnow().tz_localize(None) - data_currency_anchor.tz_localize(None)).days)
        if data_currency_anchor is not None
        else None
    )

    churn_auc = float(model_metrics.get("churn", {}).get("temporal_test_roc_auc", 0.0))
    next_purchase_auc = float(model_metrics.get("next_purchase_30d", {}).get("temporal_test_roc_auc", 0.0))
    critical_accounts = int((risk_df["Risk Score"] >= 0.8).sum()) if "Risk Score" in risk_df else 0
    total_accounts = int(len(risk_df))

    score = 100.0
    score -= max(0.0, (DEFAULT_THRESHOLDS["nrr_floor"] - float(summary.get("nrr_latest", 0.0))) * 100)
    score -= max(
        0.0,
        (float(summary.get("gross_churn_latest", 0.0)) - DEFAULT_THRESHOLDS["gross_churn_ceiling"]) * 100,
    )
    score -= max(0.0, (0.75 - churn_auc) * 100)
    score -= max(0.0, (0.70 - next_purchase_auc) * 100)
    if freshness_days is not None and freshness_days > DEFAULT_THRESHOLDS["freshness_max_days"]:
        score -= min(20.0, freshness_days - DEFAULT_THRESHOLDS["freshness_max_days"])
    score = round(max(0.0, min(100.0, score)), 1)

    return {
        "scorecard_version": "1.0.0",
        "overall_score": score,
        "status": "healthy" if score >= 85 else ("watch" if score >= 70 else "critical"),
        "dimensions": {
            "freshness_days": freshness_days,
            "data_currency_days": data_currency_days,
            "source_rows_sales": int(len(monthly_revenue)),
            "source_rows_customers": total_accounts,
            "critical_accounts": critical_accounts,
            "nrr_latest": float(summary.get("nrr_latest", 0.0)),
            "gross_churn_latest": float(summary.get("gross_churn_latest", 0.0)),
            "churn_auc_temporal_test": churn_auc,
            "next_purchase_auc_temporal_test": next_purchase_auc,
        },
        "checks": [
            {
                "check": "nrr_floor",
                "threshold": DEFAULT_THRESHOLDS["nrr_floor"],
                "actual": float(summary.get("nrr_latest", 0.0)),
                "status": "pass"
                if float(summary.get("nrr_latest", 0.0)) >= DEFAULT_THRESHOLDS["nrr_floor"]
                else "fail",
            },
            {
                "check": "gross_churn_ceiling",
                "threshold": DEFAULT_THRESHOLDS["gross_churn_ceiling"],
                "actual": float(summary.get("gross_churn_latest", 0.0)),
                "status": "pass"
                if float(summary.get("gross_churn_latest", 0.0)) <= DEFAULT_THRESHOLDS["gross_churn_ceiling"]
                else "fail",
            },
            {
                "check": "freshness_max_days",
                "threshold": DEFAULT_THRESHOLDS["freshness_max_days"],
                "actual": freshness_days,
                "status": "pass"
                if freshness_days is not None and freshness_days <= DEFAULT_THRESHOLDS["freshness_max_days"]
                else "fail",
            },
        ],
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }


def build_recommended_actions(top_actions: pd.DataFrame, uplift_pct: float = 8.0) -> list[dict[str, Any]]:
    actions = top_actions.head(5).copy()
    actions["Expected Recovery (USD)"] = (
        pd.to_numeric(actions["Revenue at Risk (USD)"], errors="coerce").fillna(0.0) * (uplift_pct / 100)
    ).round(2)
    payload: list[dict[str, Any]] = []
    for _, row in actions.iterrows():
        payload.append(
            {
                "account_id": str(row.get("Customer ID", "")),
                "recommended_action": str(row.get("Recommended Action", "")),
                "revenue_at_risk_usd": float(row.get("Revenue at Risk (USD)", 0.0)),
                "expected_recovery_usd": float(row.get("Expected Recovery (USD)", 0.0)),
                "priority": "P1" if float(row.get("Risk Score", 0.0)) >= 0.8 else "P2",
            }
        )
    return payload


def generate_executive_insight_report(
    summary: dict[str, Any],
    scorecard: dict[str, Any],
    recommended_actions: list[dict[str, Any]],
    package_id: str = "revenue_command_center",
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    rules = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    nrr = float(summary.get("nrr_latest", 0.0))
    churn = float(summary.get("gross_churn_latest", 0.0))
    value_at_risk = float(summary.get("total_value_at_risk_usd", 0.0))
    top_50_risk = float(summary.get("top_50_value_at_risk_usd", 0.0))
    quality_score = float(scorecard.get("overall_score", 0.0))

    insights = []
    if nrr < rules["nrr_floor"]:
        insights.append(
            {
                "type": "risk",
                "headline": "Retention momentum is below executive guardrail.",
                "detail": f"NRR is {nrr:.1%}, below the {rules['nrr_floor']:.0%} floor.",
                "recommended_action": "Review top save motions and rebalance CSM capacity to P1 accounts.",
            }
        )
    if churn > rules["gross_churn_ceiling"]:
        insights.append(
            {
                "type": "risk",
                "headline": "Gross churn is outside target range.",
                "detail": f"Gross churn is {churn:.1%}, above the {rules['gross_churn_ceiling']:.0%} ceiling.",
                "recommended_action": "Escalate root-cause drill-down by segment and trigger retention campaign review.",
            }
        )
    if top_50_risk > 0:
        insights.append(
            {
                "type": "opportunity",
                "headline": "A concentrated recovery pocket exists in the top priority accounts.",
                "detail": f"Top-50 accounts represent ${top_50_risk:,.0f} in revenue at risk.",
                "recommended_action": "Run an executive save sprint on the top accounts and monitor adoption outcomes weekly.",
            }
        )
    if quality_score < rules["quality_score_floor"]:
        insights.append(
            {
                "type": "governance",
                "headline": "Decision support quality needs hardening before scale-out.",
                "detail": f"Quality score is {quality_score:.1f}, below the {rules['quality_score_floor']:.0f} target.",
                "recommended_action": "Tighten freshness SLAs, add regression checks, and promote only validated artifacts.",
            }
        )
    if not insights:
        insights.append(
            {
                "type": "status",
                "headline": "Executive operating baseline is within target.",
                "detail": f"Current value at risk is ${value_at_risk:,.0f} with quality score {quality_score:.1f}.",
                "recommended_action": "Maintain weekly review cadence and expand instrumentation to realized outcomes.",
            }
        )

    return {
        "report_version": "1.0.0",
        "generation_mode": "deterministic_fallback",
        "llm_enabled": False,
        "package": SOLUTION_PACKAGES[package_id].to_dict(),
        "thresholds": rules,
        "prompt_policy": {
            "prompt_template_version": "deterministic-v1",
            "auditability": "Rules, thresholds, and output artifacts are persisted for review.",
            "allowed_use": "Drafting executive insights from validated metrics only.",
        },
        "recommended_actions": recommended_actions,
        "insights": insights,
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }
