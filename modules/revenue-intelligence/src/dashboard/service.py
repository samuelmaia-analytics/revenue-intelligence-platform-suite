from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.analytics.semantic_layer import calculate_growth_rate


@dataclass(frozen=True)
class DashboardData:
    recommendations: pd.DataFrame
    cohort: pd.DataFrame
    unit_economics: pd.DataFrame
    report: dict
    outcomes: dict
    top_actions: pd.DataFrame
    monthly_revenue: pd.DataFrame


def build_dashboard_payload(processed_dir: Path) -> DashboardData:
    recommendations = pd.read_csv(processed_dir / "recommendations.csv")
    cohort = pd.read_csv(processed_dir / "cohort_retention.csv")
    unit_economics = pd.read_csv(processed_dir / "unit_economics.csv")
    top_actions = pd.read_csv(processed_dir / "top_10_actions.csv")
    with (processed_dir / "executive_report.json").open("r", encoding="utf-8") as file:
        report = json.load(file)
    with (processed_dir / "business_outcomes.json").open("r", encoding="utf-8") as file:
        outcomes = json.load(file)

    monthly_revenue = pd.DataFrame()
    scored_path = processed_dir / "scored_customers.csv"
    fact_orders_path = processed_dir / "fact_orders.csv"
    if fact_orders_path.exists():
        fact_orders = pd.read_csv(fact_orders_path, parse_dates=["order_date"])
        monthly_revenue = (
            fact_orders.assign(month=fact_orders["order_date"].dt.to_period("M").astype(str))
            .groupby("month", as_index=False)
            .agg(revenue=("order_amount", "sum"))
        )
        if scored_path.exists():
            scored = pd.read_csv(scored_path)
            arpu = float(scored["arpu"].mean()) if not scored.empty else 0.0
            monthly_revenue["arpu"] = arpu
    elif scored_path.exists():
        scored = pd.read_csv(scored_path, parse_dates=["as_of_date"])
        monthly_revenue = (
            scored.assign(month=scored["as_of_date"].dt.to_period("M").astype(str))
            .groupby("month", as_index=False)
            .agg(revenue=("monetary", "sum"), arpu=("arpu", "mean"))
        )

    return DashboardData(
        recommendations=recommendations,
        cohort=cohort,
        unit_economics=unit_economics,
        report=report,
        outcomes=outcomes,
        top_actions=top_actions,
        monthly_revenue=monthly_revenue,
    )


def filter_recommendations(
    recommendations: pd.DataFrame,
    *,
    segment: str | None = None,
    channel: str | None = None,
    action: str | None = None,
) -> pd.DataFrame:
    df = recommendations.copy()
    if segment and segment != "All":
        df = df[df["segment"] == segment]
    if channel and channel != "All":
        df = df[df["channel"] == channel]
    if action and action != "All":
        df = df[df["recommended_action"] == action]
    return df


def compute_executive_story(df: pd.DataFrame) -> dict[str, object]:
    enriched = df.copy()
    enriched["potential_impact"] = 0.0
    retention_mask = enriched["recommended_action"] == "Retention Campaign"
    upsell_mask = enriched["recommended_action"] == "Upsell Offer"
    spend_mask = enriched["recommended_action"] == "Reduce Acquisition Spend"
    nurture_mask = ~(retention_mask | upsell_mask | spend_mask)

    enriched.loc[retention_mask, "potential_impact"] = (
        enriched.loc[retention_mask, "ltv"]
        * enriched.loc[retention_mask, "churn_probability"]
        * 0.35
    )
    enriched.loc[upsell_mask, "potential_impact"] = (
        enriched.loc[upsell_mask, "ltv"]
        * enriched.loc[upsell_mask, "next_purchase_probability"]
        * 0.15
    )
    enriched.loc[spend_mask, "potential_impact"] = enriched.loc[spend_mask, "cac"] * 0.5
    enriched.loc[nurture_mask, "potential_impact"] = (
        enriched.loc[nurture_mask, "ltv"]
        * enriched.loc[nurture_mask, "next_purchase_probability"]
        * 0.03
    )

    top_customer = enriched.sort_values("potential_impact", ascending=False).iloc[0]
    top_segment = (
        enriched.groupby("segment", as_index=False)["churn_probability"]
        .mean()
        .sort_values("churn_probability", ascending=False)
        .iloc[0]
    )
    top_action = (
        enriched["recommended_action"]
        .value_counts(normalize=True)
        .rename("proportion")
        .mul(100)
        .reset_index()
        .iloc[0]
    )
    return {
        "df": enriched,
        "top_customer": top_customer,
        "top_segment": top_segment,
        "top_action": top_action,
        "portfolio_growth_rate": calculate_growth_rate(enriched.groupby("channel")["ltv"].sum()),
    }
