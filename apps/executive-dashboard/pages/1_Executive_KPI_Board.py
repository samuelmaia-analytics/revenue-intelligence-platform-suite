from pathlib import Path
import json

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Executive KPI Board", layout="wide")

if st.button("← Back to Home"):
    st.switch_page("app.py")

ROOT = Path(__file__).resolve().parents[3]
SALES_PATH = ROOT / "modules" / "analise-vendas-python" / "dados_processados" / "vendas_simples.csv"
CUSTOMER_PATH = (
    ROOT / "modules" / "revenue-intelligence" / "data" / "raw" / "E-commerce Customer Behavior - Sheet1.csv"
)
METRICS_PATH = ROOT / "modules" / "revenue-intelligence" / "data" / "processed" / "metrics_report.json"
SHOWCASE_SUMMARY_PATH = ROOT / "reports" / "showcase" / "summary.json"


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
except Exception as exc:
    st.error("Could not load real module data. Check repository paths and file integrity.")
    st.exception(exc)
    st.stop()

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

risk_df = build_risk_score(customer_df)

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
current_nrr = float(monthly_revenue["nrr_proxy"].iloc[-1]) if not monthly_revenue.empty else 1.0
gross_churn = max(0.0, 1 - current_nrr)
value_at_risk = float(risk_view["Revenue at Risk (USD)"].sum())
expected_recovery = value_at_risk * (uplift / 100)
roi = ((expected_recovery - budget) / budget) if budget else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Revenue (Latest Month)", f"${current_revenue:,.0f}")
col2.metric("NRR Proxy (MoM)", f"{current_nrr*100:.1f}%")
col3.metric("Gross Revenue Churn Proxy", f"{gross_churn*100:.1f}%")
col4.metric("Value at Risk", f"${value_at_risk:,.0f}")
col5.metric("Expected Recovery", f"${expected_recovery:,.0f}", delta=f"ROI {roi*100:.0f}%")

st.markdown("---")
left, right = st.columns([2, 1])
with left:
    st.subheader("Revenue Trend (Real Data)")
    st.line_chart(monthly_revenue.set_index("month")["SALES"])
with right:
    st.subheader("NRR Proxy Trend (MoM)")
    st.line_chart((monthly_revenue.set_index("month")["nrr_proxy"] * 100).round(2))

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
action_alias = {
    "Executive Save Offer": "Exec Save Offer",
    "CSM Priority Call": "CSM Priority Call",
    "Nurture Campaign": "Nurture Campaign",
}
action_counts["Action Short"] = action_counts["Action"].map(action_alias).fillna(action_counts["Action"])

action_chart = (
    alt.Chart(action_counts)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X("Action Short:N", sort="-y", title="Recommended Action"),
        y=alt.Y("Accounts:Q", title="Accounts"),
        tooltip=["Action:N", "Accounts:Q"],
    )
    .properties(height=260)
)
st.altair_chart(action_chart, width="stretch")
st.dataframe(action_counts[["Action", "Accounts"]], width="stretch", hide_index=True)

action_notes = [
    "Approve targeted retention offers for top 10 accounts by expected recovery.",
    "Assign CSM owners to all accounts with Risk Score >= 0.60.",
    "Run pricing review for customers flagged with high risk and high spend.",
]
for idx, note in enumerate(action_notes, start=1):
    st.write(f"{idx}. {note}")

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
