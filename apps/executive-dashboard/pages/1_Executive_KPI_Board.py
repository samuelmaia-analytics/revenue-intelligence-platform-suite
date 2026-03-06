import json
import os
import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "platform_connectors").exists():
            return candidate
    return Path(__file__).resolve().parents[3]


ROOT = _find_repo_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from platform_connectors import (  # noqa: E402
    DuckDBTelemetryConnector,
    SQLiteTelemetryConnector,
    seed_demo_telemetry,
    seed_demo_telemetry_duckdb,
)
from platform_observability import ActionAdoptionLogger  # noqa: E402

st.set_page_config(page_title="Executive KPI Board", layout="wide")

if st.button("Voltar para Revenue-Intelligence-Platform-Suite"):
    st.switch_page("app.py")

with st.sidebar:
    if st.button("Home: Revenue-Intelligence-Platform-Suite"):
        st.switch_page("app.py")

SALES_PATH = ROOT / "modules" / "analise-vendas-python" / "dados_processados" / "vendas_simples.csv"
CUSTOMER_PATH = (
    ROOT / "modules" / "revenue-intelligence" / "data" / "raw" / "E-commerce Customer Behavior - Sheet1.csv"
)
METRICS_PATH = ROOT / "modules" / "revenue-intelligence" / "data" / "processed" / "metrics_report.json"
SHOWCASE_SUMMARY_PATH = ROOT / "reports" / "showcase" / "summary.json"
TELEMETRY_DB_PATH = ROOT / "reports" / "showcase" / "enterprise_telemetry.sqlite"
TELEMETRY_DUCKDB_PATH = ROOT / "reports" / "showcase" / "enterprise_telemetry.duckdb"
SHOWCASE_OUTPUT_DIR = ROOT / "reports" / "showcase"
TELEMETRY_BACKEND = os.getenv("TELEMETRY_BACKEND", "sqlite").strip().lower()


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    sales_df = pd.read_csv(SALES_PATH)
    customer_df = pd.read_csv(CUSTOMER_PATH)
    with METRICS_PATH.open("r", encoding="utf-8") as fp:
        model_metrics = json.load(fp)
    return sales_df, customer_df, model_metrics


@st.cache_data(show_spinner=False)
def load_showcase_summary() -> dict:
    if not SHOWCASE_SUMMARY_PATH.exists():
        return {}
    with SHOWCASE_SUMMARY_PATH.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@st.cache_data(show_spinner=False)
def load_enterprise_telemetry() -> pd.DataFrame:
    connector = (
        DuckDBTelemetryConnector(TELEMETRY_DUCKDB_PATH)
        if TELEMETRY_BACKEND == "duckdb"
        else SQLiteTelemetryConnector(TELEMETRY_DB_PATH)
    )
    return connector.fetch_monthly_revenue_telemetry()


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
    return risk


try:
    sales_df, customer_df, model_metrics = load_data()
    showcase_summary = load_showcase_summary()
    telemetry_df = load_enterprise_telemetry()
except Exception as exc:
    st.error("Could not load real module data. Check repository paths and file integrity.")
    st.exception(exc)
    st.stop()

sales_df["ORDERDATE"] = pd.to_datetime(sales_df["ORDERDATE"], errors="coerce")
sales_df["SALES"] = pd.to_numeric(sales_df["SALES"], errors="coerce").fillna(0)
sales_df = sales_df.dropna(subset=["ORDERDATE"]).copy()
sales_df["month"] = sales_df["ORDERDATE"].dt.to_period("M").astype(str)
monthly_revenue = sales_df.groupby("month", as_index=False)["SALES"].sum().sort_values("month")

risk_df = build_risk_score(customer_df)

if telemetry_df.empty:
    try:
        if TELEMETRY_BACKEND == "duckdb":
            seed_demo_telemetry_duckdb(TELEMETRY_DUCKDB_PATH, monthly_revenue)
        else:
            seed_demo_telemetry(TELEMETRY_DB_PATH, monthly_revenue)
        load_enterprise_telemetry.clear()
        telemetry_df = load_enterprise_telemetry()
    except Exception:
        # Keep running with computed fallback if filesystem is not writable in hosting.
        pass

st.title("Executive KPI Board")
st.caption("Real integrated data from platform modules.")

st.sidebar.header("Scenario Controls")
segment = st.sidebar.selectbox(
    "Membership Type", ["All"] + sorted(risk_df["Membership Type"].dropna().unique().tolist())
)
uplift = st.sidebar.slider("Retention uplift scenario (%)", min_value=0, max_value=30, value=8, step=1)
budget = st.sidebar.slider("Campaign budget (USD)", min_value=10_000, max_value=500_000, value=120_000, step=10_000)

if segment != "All":
    risk_view = risk_df[risk_df["Membership Type"] == segment].copy()
else:
    risk_view = risk_df.copy()

current_revenue = float(monthly_revenue["SALES"].iloc[-1]) if not monthly_revenue.empty else 0.0
if telemetry_df.empty:
    if len(monthly_revenue) >= 2:
        nrr_series = (monthly_revenue["SALES"] / monthly_revenue["SALES"].shift(1)).fillna(1.0).clip(
            lower=0.6, upper=1.2
        )
        current_nrr = float(nrr_series.iloc[-1])
    else:
        current_nrr = 1.0
    gross_churn = max(0.0, 1 - current_nrr)
else:
    current_nrr = float(telemetry_df["nrr"].iloc[-1])
    gross_churn = float(telemetry_df["gross_churn"].iloc[-1])
value_at_risk = float(risk_view["Revenue at Risk (USD)"].sum())
expected_recovery = value_at_risk * (uplift / 100)
roi = ((expected_recovery - budget) / budget) if budget else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Revenue (Latest Month)", f"${current_revenue:,.0f}")
col2.metric("NRR (Telemetry)", f"{current_nrr*100:.1f}%")
col3.metric("Gross Revenue Churn (Telemetry)", f"{gross_churn*100:.1f}%")
col4.metric("Value at Risk", f"${value_at_risk:,.0f}")
col5.metric("Expected Recovery", f"${expected_recovery:,.0f}", delta=f"ROI {roi*100:.0f}%")

st.markdown("---")
st.subheader("KPI Target vs Actual")

revenue_target = current_revenue * 1.08
nrr_target = 0.92
churn_target = 0.08
recovery_target = value_at_risk * 0.12

kpi_table = pd.DataFrame(
    [
        {
            "KPI": "Revenue (Latest Month)",
            "Target": revenue_target,
            "Actual": current_revenue,
            "Gap": current_revenue - revenue_target,
            "Owner": "Revenue Lead",
            "Deadline": "Q2",
        },
        {
            "KPI": "NRR",
            "Target": nrr_target,
            "Actual": current_nrr,
            "Gap": current_nrr - nrr_target,
            "Owner": "Retention Lead",
            "Deadline": "Q2",
        },
        {
            "KPI": "Gross Churn",
            "Target": churn_target,
            "Actual": gross_churn,
            "Gap": churn_target - gross_churn,
            "Owner": "Retention Ops",
            "Deadline": "Q2",
        },
        {
            "KPI": "Expected Recovery",
            "Target": recovery_target,
            "Actual": expected_recovery,
            "Gap": expected_recovery - recovery_target,
            "Owner": "Growth Lead",
            "Deadline": "Q2",
        },
    ]
)

display_kpis = kpi_table.copy()
pct_mask = display_kpis["KPI"].str.contains("NRR|Churn")
display_kpis.loc[pct_mask, "Target"] = (display_kpis.loc[pct_mask, "Target"] * 100).round(1)
display_kpis.loc[pct_mask, "Actual"] = (display_kpis.loc[pct_mask, "Actual"] * 100).round(1)
display_kpis.loc[pct_mask, "Gap"] = (display_kpis.loc[pct_mask, "Gap"] * 100).round(1)
display_kpis.loc[~pct_mask, ["Target", "Actual", "Gap"]] = (
    display_kpis.loc[~pct_mask, ["Target", "Actual", "Gap"]].round(0)
)
st.dataframe(display_kpis, width="stretch", hide_index=True)

st.markdown("---")
left, right = st.columns([2, 1])
with left:
    st.subheader("Revenue Trend (Real Data)")
    st.line_chart(monthly_revenue.set_index("month")["SALES"])
with right:
    st.subheader("NRR Telemetry Trend (MoM)")
    if telemetry_df.empty:
        fallback_nrr = (monthly_revenue["SALES"] / monthly_revenue["SALES"].shift(1)).fillna(1.0).clip(
            lower=0.6, upper=1.2
        )
        st.line_chart((fallback_nrr * 100).round(2))
        st.info("Telemetry DB not found in host; showing computed fallback NRR trend.")
    else:
        nrr_series = telemetry_df.set_index("month")["nrr"] * 100
        st.line_chart(nrr_series.round(2))

if showcase_summary:
    st.info(
        "Showcase artifacts loaded from reports/showcase/summary.json "
        f"(latest month: {showcase_summary.get('latest_month', 'n/a')})."
    )

st.markdown("---")
st.subheader("Top Retention Priorities (Real Customer Data)")

risk_view["Expected Recovery (USD)"] = (risk_view["Revenue at Risk (USD)"] * (uplift / 100)).round(2)
risk_view["Recommended Action"] = risk_view["Risk Score"].apply(
    lambda x: "Executive Save Offer"
    if x >= 0.8
    else ("CSM Priority Call" if x >= 0.6 else "Nurture Campaign")
)

top_cols = [
    "Customer ID",
    "Membership Type",
    "City",
    "Risk Score",
    "Revenue at Risk (USD)",
    "Expected Recovery (USD)",
    "Recommended Action",
]
top_priorities = risk_view.sort_values("Expected Recovery (USD)", ascending=False)[top_cols].head(12)
st.dataframe(top_priorities, width="stretch")

st.subheader("Leadership Actions This Week")
action_counts = (
    top_priorities["Recommended Action"].value_counts().rename_axis("Action").reset_index(name="Accounts")
)
# Keep all action categories visible even when count is zero.
all_actions = pd.DataFrame(
    {"Action": ["Executive Save Offer", "CSM Priority Call", "Nurture Campaign"]}
)
action_counts = (
    all_actions.merge(action_counts, on="Action", how="left")
    .fillna({"Accounts": 0})
    .astype({"Accounts": "int64"})
)
action_counts = action_counts.sort_values(["Accounts", "Action"], ascending=[False, True]).reset_index(
    drop=True
)

action_chart = (
    alt.Chart(action_counts)
    .mark_bar(cornerRadiusEnd=4)
    .encode(
        x=alt.X("Accounts:Q", title="Accounts"),
        y=alt.Y("Action:N", sort="-x", title="Recommended Action"),
        color=alt.Color(
            "Action:N",
            legend=None,
            scale=alt.Scale(
                domain=["Executive Save Offer", "CSM Priority Call", "Nurture Campaign"],
                range=["#1f77b4", "#2ca02c", "#ff7f0e"],
            ),
        ),
        tooltip=["Action:N", "Accounts:Q"],
    )
    .properties(height=220)
)
st.altair_chart(action_chart, width="stretch")
st.dataframe(action_counts[["Action", "Accounts"]], width="stretch", hide_index=True)

st.subheader("Action Register")
register = top_priorities.head(8).copy()
owners = ["CSM Team A", "CSM Team B", "CSM Team A", "Retention Ops", "Retention Ops", "CSM Team B", "Growth Squad", "Growth Squad"]
etas = ["3d", "5d", "7d", "5d", "10d", "7d", "14d", "14d"]
statuses = ["Approved", "In Progress", "In Progress", "Planned", "Planned", "In Progress", "Planned", "Planned"]
register["Owner"] = owners[: len(register)]
register["ETA"] = etas[: len(register)]
register["Status"] = statuses[: len(register)]
register = register[
    [
        "Customer ID",
        "Recommended Action",
        "Expected Recovery (USD)",
        "Risk Score",
        "Owner",
        "ETA",
        "Status",
    ]
]
st.dataframe(register, width="stretch", hide_index=True)

st.markdown("---")
st.subheader("Action Adoption Monitoring")
adoption_logger = ActionAdoptionLogger(SHOWCASE_OUTPUT_DIR)
event_rows = register.copy()
event_rows["action_id"] = event_rows["Customer ID"].astype(str) + "::" + event_rows["Recommended Action"]
event_options = event_rows["action_id"].tolist()
selected_action_id = st.selectbox("Action ID", options=event_options)
selected_outcome = st.selectbox("Outcome", options=["accepted", "in_progress", "rejected"])
if st.button("Log Action Outcome", use_container_width=False):
    selected_row = event_rows[event_rows["action_id"] == selected_action_id].iloc[0]
    adoption_logger.log(
        action_id=selected_action_id,
        outcome=selected_outcome,
        metadata={
            "expected_recovery_usd": float(selected_row["Expected Recovery (USD)"]),
            "owner": selected_row["Owner"],
            "eta": selected_row["ETA"],
            "status": selected_row["Status"],
        },
    )
    st.success("Action outcome logged in reports/showcase/action_adoption_log.csv and .jsonl")

st.markdown("---")
st.subheader("Scenario Analysis")
scenario_df = pd.DataFrame(
    [
        {"Scenario": "Conservative", "Uplift %": 5, "Budget (USD)": budget * 0.8},
        {"Scenario": "Base", "Uplift %": uplift, "Budget (USD)": budget},
        {"Scenario": "Aggressive", "Uplift %": min(30, uplift + 7), "Budget (USD)": budget * 1.3},
    ]
)
scenario_df["Expected Recovery (USD)"] = (
    value_at_risk * (scenario_df["Uplift %"] / 100)
).round(2)
scenario_df["ROI"] = (
    (scenario_df["Expected Recovery (USD)"] - scenario_df["Budget (USD)"]) / scenario_df["Budget (USD)"]
).round(2)
st.dataframe(scenario_df, width="stretch", hide_index=True)
st.download_button(
    "Download Scenario Analysis (CSV)",
    data=scenario_df.to_csv(index=False).encode("utf-8"),
    file_name="scenario_analysis.csv",
    mime="text/csv",
)

st.markdown("---")
a, b, c = st.columns(3)
with a:
    st.subheader("Pipeline Health")
    st.write(f"- Source rows (sales): **{len(sales_df):,}**")
    st.write(f"- Source rows (customers): **{len(customer_df):,}**")
    st.write("- Data contracts: **Loaded from module repos**")

with b:
    st.subheader("Model Health")
    churn_auc = model_metrics.get("churn", {}).get("temporal_test_roc_auc", 0.0)
    next_auc = model_metrics.get("next_purchase_30d", {}).get("temporal_test_roc_auc", 0.0)
    st.write(f"- Churn AUC (temporal test): **{churn_auc:.3f}**")
    st.write(f"- Next purchase AUC (temporal test): **{next_auc:.3f}**")
    st.write("- Source: **modules/revenue-intelligence/data/processed/metrics_report.json**")

with c:
    st.subheader("Data Freshness")
    last_sales_date = sales_df["ORDERDATE"].max().date() if not sales_df.empty else "N/A"
    customer_file_mtime = CUSTOMER_PATH.stat().st_mtime
    st.write(f"- Last sales date in dataset: **{last_sales_date}**")
    st.write(f"- Customer file updated: **{pd.to_datetime(customer_file_mtime, unit='s').date()}**")
    st.write(f"- Dashboard generated at: **{pd.Timestamp.utcnow().strftime('%Y-%m-%d %H:%M UTC')}**")

st.markdown("---")
st.caption(
    "Author: [LinkedIn](https://linkedin.com/in/samuelmaia-analytics) | "
    "[GitHub](https://github.com/samuelmaia-analytics)"
)
