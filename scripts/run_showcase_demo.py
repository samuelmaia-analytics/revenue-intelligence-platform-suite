from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

try:
    from common import (
        build_data_quality_scorecard,
        build_recommended_actions,
        build_tenant_secret_status,
        build_solution_profile,
        generate_executive_insight_report,
        load_solution_configuration,
    )
    from common.contracts import validate_contract
    from platform_connectors import (
        DuckDBTelemetryConnector,
        SQLiteTelemetryConnector,
        seed_demo_telemetry,
        seed_demo_telemetry_duckdb,
    )
    from platform_observability import write_monitoring_outputs
except ModuleNotFoundError:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(ROOT / "packages") not in sys.path:
        sys.path.insert(0, str(ROOT / "packages"))
    from common import (
        build_data_quality_scorecard,
        build_recommended_actions,
        build_tenant_secret_status,
        build_solution_profile,
        generate_executive_insight_report,
        load_solution_configuration,
    )
    from common.contracts import validate_contract
    from platform_connectors import (
        DuckDBTelemetryConnector,
        SQLiteTelemetryConnector,
        seed_demo_telemetry,
        seed_demo_telemetry_duckdb,
    )
    from platform_observability import write_monitoring_outputs

SALES_PATH = ROOT / "modules" / "analise-vendas-python" / "dados_processados" / "vendas_simples.csv"
CUSTOMER_PATH = (
    ROOT / "modules" / "revenue-intelligence" / "data" / "raw" / "E-commerce Customer Behavior - Sheet1.csv"
)
MODEL_METRICS_PATH = ROOT / "modules" / "revenue-intelligence" / "data" / "processed" / "metrics_report.json"
OUTPUT_DIR = ROOT / "reports" / "showcase"
TELEMETRY_DB_PATH = OUTPUT_DIR / "enterprise_telemetry.sqlite"
TELEMETRY_DUCKDB_PATH = OUTPUT_DIR / "enterprise_telemetry.duckdb"
TELEMETRY_BACKEND = os.getenv("TELEMETRY_BACKEND", "sqlite").strip().lower()
CLIENT_PROFILE = os.getenv("CLIENT_PROFILE", "saas_b2b").strip().lower()
DEPLOYMENT_ENV = os.getenv("DEPLOYMENT_ENV", "showcase").strip().lower()
SOLUTION_PACKAGE = os.getenv("SOLUTION_PACKAGE", "revenue_command_center").strip().lower()


def build_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    risk = df.copy()
    risk["Days Since Last Purchase"] = pd.to_numeric(
        risk["Days Since Last Purchase"], errors="coerce"
    ).fillna(0)
    risk["Total Spend"] = pd.to_numeric(risk["Total Spend"], errors="coerce").fillna(0)
    risk["Satisfaction Level"] = risk["Satisfaction Level"].fillna("Neutral")

    sat_weight = risk["Satisfaction Level"].map(
        {"Unsatisfied": 1.0, "Neutral": 0.7, "Satisfied": 0.35}
    ).fillna(0.5)
    recency_weight = (
        risk["Days Since Last Purchase"] / max(risk["Days Since Last Purchase"].max(), 1)
    ).fillna(0)
    spend_weight = (risk["Total Spend"] / max(risk["Total Spend"].max(), 1)).fillna(0)

    risk["Risk Score"] = (0.5 * recency_weight + 0.35 * sat_weight + 0.15 * spend_weight).clip(0, 1)
    risk["Revenue at Risk (USD)"] = (risk["Total Spend"] * risk["Risk Score"]).round(2)
    risk["Recommended Action"] = risk["Risk Score"].apply(
        lambda x: "Executive Save Offer"
        if x >= 0.8
        else ("CSM Priority Call" if x >= 0.6 else "Nurture Campaign")
    )
    return risk


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    solution_config = load_solution_configuration(
        client_profile=CLIENT_PROFILE,
        deployment_env=DEPLOYMENT_ENV,
        solution_package=SOLUTION_PACKAGE,
    )

    sales_df = pd.read_csv(SALES_PATH)
    sales_df["ORDERDATE"] = pd.to_datetime(sales_df["ORDERDATE"], errors="coerce")
    sales_df["SALES"] = pd.to_numeric(sales_df["SALES"], errors="coerce").fillna(0)
    sales_df = sales_df.dropna(subset=["ORDERDATE"]).copy()
    sales_df["month"] = sales_df["ORDERDATE"].dt.to_period("M").astype(str)
    monthly_revenue = sales_df.groupby("month", as_index=False)["SALES"].sum().sort_values("month")

    if len(monthly_revenue) >= 2:
        monthly_revenue["nrr_proxy"] = (
            monthly_revenue["SALES"] / monthly_revenue["SALES"].shift(1)
        ).fillna(1.0).clip(lower=0.6, upper=1.2)
    else:
        monthly_revenue["nrr_proxy"] = 1.0

    customer_df = pd.read_csv(CUSTOMER_PATH)
    risk_df = build_risk_score(customer_df)
    top_actions = risk_df.sort_values("Revenue at Risk (USD)", ascending=False).head(50).copy()

    if TELEMETRY_BACKEND == "duckdb":
        seed_demo_telemetry_duckdb(TELEMETRY_DUCKDB_PATH, monthly_revenue)
        telemetry = DuckDBTelemetryConnector(TELEMETRY_DUCKDB_PATH)
        telemetry_artifact = TELEMETRY_DUCKDB_PATH
    else:
        seed_demo_telemetry(TELEMETRY_DB_PATH, monthly_revenue)
        telemetry = SQLiteTelemetryConnector(TELEMETRY_DB_PATH)
        telemetry_artifact = TELEMETRY_DB_PATH
    latest_kpis = telemetry.fetch_latest_kpis()

    with MODEL_METRICS_PATH.open("r", encoding="utf-8") as fp:
        model_metrics = json.load(fp)

    summary = {
        "latest_month": latest_kpis["latest_month"] or "",
        "latest_revenue_usd": float(latest_kpis["latest_revenue_usd"]),
        "nrr_latest": float(latest_kpis["nrr_latest"]),
        "gross_churn_latest": float(latest_kpis["gross_churn_latest"]),
        "total_value_at_risk_usd": float(risk_df["Revenue at Risk (USD)"].sum()),
        "top_50_value_at_risk_usd": float(top_actions["Revenue at Risk (USD)"].sum()),
        "churn_auc_temporal_test": float(
            model_metrics.get("churn", {}).get("temporal_test_roc_auc", 0.0)
        ),
        "next_purchase_auc_temporal_test": float(
            model_metrics.get("next_purchase_30d", {}).get("temporal_test_roc_auc", 0.0)
        ),
        "telemetry_source": latest_kpis["source_system"],
    }

    monthly_revenue.to_csv(OUTPUT_DIR / "monthly_revenue.csv", index=False)
    top_actions.to_csv(OUTPUT_DIR / "top_actions.csv", index=False)
    monitoring = write_monitoring_outputs(OUTPUT_DIR, monthly_revenue)
    solution_profile = build_solution_profile(
        client_name=solution_config.get("client_name", "Flagship Demo Client"),
        industry=solution_config.get("industry", "SaaS"),
        deployment_env=DEPLOYMENT_ENV,
        package_id=SOLUTION_PACKAGE,
        telemetry_backend=TELEMETRY_BACKEND,
        configuration=solution_config,
        profile_id=CLIENT_PROFILE,
    )
    quality_scorecard = build_data_quality_scorecard(
        summary=summary,
        monthly_revenue=monthly_revenue,
        risk_df=risk_df,
        model_metrics=model_metrics,
        customer_file_path=CUSTOMER_PATH,
        sales_file_path=SALES_PATH,
    )
    recommended_actions = build_recommended_actions(top_actions)
    executive_insights = generate_executive_insight_report(
        summary=summary,
        scorecard=quality_scorecard,
        recommended_actions=recommended_actions,
        package_id=SOLUTION_PACKAGE,
        thresholds=solution_config.get("thresholds"),
    )
    tenant_secret_status = build_tenant_secret_status(
        client_profile=CLIENT_PROFILE,
        deployment_env=DEPLOYMENT_ENV,
    )

    errors = validate_contract(summary, "showcase_summary.schema.json")
    if errors:
        raise ValueError(f"Contract validation failed for showcase summary: {errors}")

    with (OUTPUT_DIR / "summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)
    with (OUTPUT_DIR / "solution_profile.json").open("w", encoding="utf-8") as fp:
        json.dump(solution_profile, fp, indent=2)
    with (OUTPUT_DIR / "data_quality_scorecard.json").open("w", encoding="utf-8") as fp:
        json.dump(quality_scorecard, fp, indent=2)
    with (OUTPUT_DIR / "executive_insights.json").open("w", encoding="utf-8") as fp:
        json.dump(executive_insights, fp, indent=2)
    with (OUTPUT_DIR / "tenant_secret_status.json").open("w", encoding="utf-8") as fp:
        json.dump(tenant_secret_status, fp, indent=2)

    print("Showcase demo artifacts generated:")
    print(f"- {OUTPUT_DIR / 'monthly_revenue.csv'}")
    print(f"- {OUTPUT_DIR / 'top_actions.csv'}")
    print(f"- {OUTPUT_DIR / 'summary.json'}")
    print(f"- {OUTPUT_DIR / 'solution_profile.json'}")
    print(f"- {OUTPUT_DIR / 'data_quality_scorecard.json'}")
    print(f"- {OUTPUT_DIR / 'executive_insights.json'}")
    print(f"- {OUTPUT_DIR / 'tenant_secret_status.json'}")
    print(f"- {telemetry_artifact}")
    print(f"- {OUTPUT_DIR / 'drift_report.json'}")
    print(f"- {OUTPUT_DIR / 'action_adoption_metrics.json'}")
    print(
        "Monitoring status: "
        f"drift_detected={monitoring['drift']['drift_detected']}, "
        f"adoption_events={monitoring['action_adoption']['total_events']}"
    )


if __name__ == "__main__":
    main()
