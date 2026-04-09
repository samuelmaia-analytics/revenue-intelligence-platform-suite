import json
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from dashboard_theme import apply_dashboard_theme, render_footer, render_hero, render_intro_banner, render_section_label  # noqa: E402
from dashboard_ui import (  # noqa: E402
    build_bar_chart,
    build_line_chart,
    format_currency,
    format_percent,
    render_command_bar,
    render_global_context,
    render_insight_grid,
    render_kpi_note,
    render_metrics_grid,
    render_sidebar_nav,
    render_signal_band,
    render_story_block,
    render_table,
)


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "platform_connectors").exists():
            return candidate
    return Path(__file__).resolve().parents[3]


ROOT = _find_repo_root(Path(__file__).resolve())
try:
    from common import enforce_streamlit_sso
    from platform_connectors import (
        DuckDBTelemetryConnector,
        SQLiteTelemetryConnector,
        seed_demo_telemetry,
        seed_demo_telemetry_duckdb,
    )
    from platform_observability import ActionAdoptionLogger
except ModuleNotFoundError:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(ROOT / "packages") not in sys.path:
        sys.path.insert(0, str(ROOT / "packages"))
    from common import enforce_streamlit_sso
    from platform_connectors import (
        DuckDBTelemetryConnector,
        SQLiteTelemetryConnector,
        seed_demo_telemetry,
        seed_demo_telemetry_duckdb,
    )
    from platform_observability import ActionAdoptionLogger

st.set_page_config(page_title="Executive KPI Board", layout="wide")
identity = enforce_streamlit_sso(st)

with st.sidebar:
    render_sidebar_nav(
        st,
        current_page="kpi_board",
        mode_label="Operating review",
        mode_body="Executive weekly board for revenue trend, risk sizing, action approval and governance confidence.",
        flow_label="Decision sequence",
        flow_body="Current state, what changed, decisions this week, action register, then trust layer.",
    )

SALES_PATH = ROOT / "modules" / "analise-vendas-python" / "dados_processados" / "vendas_simples.csv"
CUSTOMER_PATH = (
    ROOT / "modules" / "revenue-intelligence" / "data" / "raw" / "E-commerce Customer Behavior - Sheet1.csv"
)
METRICS_PATH = ROOT / "modules" / "revenue-intelligence" / "data" / "processed" / "metrics_report.json"
SHOWCASE_SUMMARY_PATH = ROOT / "reports" / "showcase" / "summary.json"
SHOWCASE_INSIGHTS_PATH = ROOT / "reports" / "showcase" / "executive_insights.json"
SHOWCASE_SCORECARD_PATH = ROOT / "reports" / "showcase" / "data_quality_scorecard.json"
SHOWCASE_PROFILE_PATH = ROOT / "reports" / "showcase" / "solution_profile.json"
SEMANTIC_METRICS_PATH = ROOT / "config" / "semantic_metrics.json"
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
def load_json_artifact(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fp:
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
    executive_insights = load_json_artifact(SHOWCASE_INSIGHTS_PATH)
    quality_scorecard = load_json_artifact(SHOWCASE_SCORECARD_PATH)
    solution_profile = load_json_artifact(SHOWCASE_PROFILE_PATH)
    semantic_catalog = load_json_artifact(SEMANTIC_METRICS_PATH)
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

apply_dashboard_theme(st)
render_intro_banner(
    st,
    title="Executive KPI Board",
    subtitle="Board-facing control room for revenue trend, retention exposure, action prioritization, and governance confidence.",
    notice=(
        "This Streamlit application is publicly viewable for demonstration purposes. "
        "The platform, generated assets, and source repository remain proprietary to Samuel Maia."
    ),
    eyebrow="UI refresh 2026-04-09",
)
render_global_context(
    st,
    suite_label="Executive Board",
    page_title="Revenue and Retention Control Room",
    summary="A board-facing operating surface for revenue trend, retention exposure, action prioritization, and governance confidence.",
    right_hint=solution_profile.get("package", {}).get("name", "Revenue Command Center"),
)
render_hero(
    st,
    title="Executive KPI Board",
    kicker="Operational Control Room",
    subtitle="Real integrated data from platform modules, organized as an executive operating system for revenue, retention, and governance.",
    chips=[
        solution_profile.get("package", {}).get("name", "Revenue Command Center"),
        solution_profile.get("industry", "Industry adaptation"),
        f"Telemetry: {TELEMETRY_BACKEND}",
    ],
)
if identity.get("authenticated"):
    st.markdown(
        (
            '<div class="rip-inline-pill">'
            f"SSO session: {identity.get('display_name')} | groups={', '.join(identity.get('groups', [])) or 'n/a'}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

st.sidebar.markdown("### Scenario Controls")
segment = st.sidebar.selectbox(
    "Customer segment in focus", ["All"] + sorted(risk_df["Membership Type"].dropna().unique().tolist())
)
uplift = st.sidebar.slider("Recovery uplift assumption (%)", min_value=0, max_value=30, value=8, step=1)
budget = st.sidebar.slider("Intervention budget (USD)", min_value=10_000, max_value=500_000, value=120_000, step=10_000)

render_command_bar(
    st,
    [
        {
            "label": "Scenario",
            "title": "Segment in review",
            "value": segment,
            "note": "Active cohort for exposure and action prioritization.",
            "primary": True,
        },
        {
            "label": "Decision Lever",
            "title": "Uplift assumption",
            "value": f"{uplift}%",
            "note": "Recovery assumption applied to the current watchlist.",
        },
        {
            "label": "Budget",
            "title": "Intervention budget",
            "value": format_currency(budget),
            "note": "Executive budget currently allocated to the save motion.",
        },
        {
            "label": "Telemetry",
            "title": "Backend mode",
            "value": TELEMETRY_BACKEND.upper(),
            "note": "Operational telemetry source used by the board.",
        },
    ],
)

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

render_metrics_grid(
    st,
    [
        {
            "label": "Revenue",
            "value": format_currency(current_revenue),
            "delta": showcase_summary.get("latest_month", "Latest month"),
            "caption": "Latest closed month revenue baseline for the executive cadence.",
            "context": "Current state",
            "featured": True,
            "context_tone": "positive",
        },
        {
            "label": "NRR",
            "value": format_percent(current_nrr),
            "delta": f"Gross churn {format_percent(gross_churn)}",
            "caption": "Retention momentum pulled from telemetry or deterministic fallback.",
            "context": "Trend",
            "tone": "governance",
            "context_tone": "warning",
        },
        {
            "label": "Revenue At Risk",
            "value": format_currency(value_at_risk),
            "delta": f"Exposure in {segment}",
            "caption": "Accounts currently exposed to churn or leakage pressure.",
            "context": "Risk",
            "tone": "risk",
            "context_tone": "risk",
        },
        {
            "label": "Expected Recovery",
            "value": format_currency(expected_recovery),
            "delta": f"ROI {format_percent(roi)}",
            "caption": "Estimated recovery under the selected intervention scenario.",
            "context": "Opportunity",
            "tone": "opportunity",
            "context_tone": "positive",
        },
    ],
)

previous_revenue = float(monthly_revenue["SALES"].iloc[-2]) if len(monthly_revenue) >= 2 else current_revenue
revenue_change = current_revenue - previous_revenue
nrr_target_gap = current_nrr - 0.92
top_watchlist = risk_view.sort_values("Revenue at Risk (USD)", ascending=False).head(3)
top_account_value = float(top_watchlist["Revenue at Risk (USD)"].sum()) if not top_watchlist.empty else 0.0
decision_focus = "Approve save motion" if roi > 0 else "Reframe intervention plan"

if solution_profile:
    render_signal_band(
        st,
        [
            {
                "title": "Industry Adaptation",
                "value": solution_profile.get("industry", "n/a"),
                "body": f"Client profile: {solution_profile.get('client_name', 'n/a')}",
            },
            {
                "title": "Executive Buyer",
                "value": solution_profile.get("executive_buyer", "n/a"),
                "body": f"Telemetry backend: {solution_profile.get('telemetry_backend', 'n/a')}",
            },
            {
                "title": "Action Model",
                "value": "Scenario-driven",
                "body": "The board couples risk sizing with guided action and operating follow-through.",
            },
        ],
    )

render_section_label(st, "Operating Review")
review_left, review_mid, review_right = st.columns(3)
with review_left:
    render_kpi_note(
        st,
        title="What changed",
        body=f"Revenue moved {format_currency(revenue_change)} versus the prior month while NRR is running at {format_percent(current_nrr)}.",
        tone="info" if revenue_change >= 0 else "risk",
    )
with review_mid:
    render_kpi_note(
        st,
        title="Decision required",
        body=f"{decision_focus} because modeled exposure is {format_currency(value_at_risk)} and scenario ROI is {format_percent(roi)}.",
        tone="positive" if roi > 0 else "risk",
    )
with review_right:
    render_kpi_note(
        st,
        title="Leadership watchlist",
        body=f"The top watchlist concentrates {format_currency(top_account_value)} in exposure across the first three accounts.",
        tone="warning",
    )

render_section_label(st, "Executive Context")
insights = executive_insights.get("insights", []) if executive_insights else []
render_insight_grid(
    st,
    [
        {
            "eyebrow": "Current State",
            "title": "Revenue and retention are visible in one operating frame.",
            "body": f"Latest month revenue is {format_currency(current_revenue)} while NRR is running at {format_percent(current_nrr)}.",
            "action": "Use these figures as the baseline for weekly leadership review.",
        },
        {
            "eyebrow": "Risk Signal",
            "title": insights[0]["headline"] if insights else "There is a concentrated recovery pocket in the highest-risk accounts.",
            "body": insights[0]["detail"] if insights else f"The selected scope contains {format_currency(value_at_risk)} in modeled exposure.",
            "action": insights[0]["recommended_action"] if insights else "Focus leadership attention on the first recovery cohort.",
        },
        {
            "eyebrow": "Action Lens",
            "title": "This board is sequenced for weekly decisions, not passive monitoring.",
            "body": f"With a {uplift}% uplift assumption and {format_currency(budget)} budget, the scenario yields {format_currency(expected_recovery)} in potential recovery.",
            "action": "Review the watchlist, approve the top actions, and track adoption weekly.",
        },
    ],
)

render_section_label(st, "Risk, Opportunity, Action")

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

risk_summary_left, risk_summary_right = st.columns([1.18, 1])
with risk_summary_left:
    render_signal_band(
        st,
        [
            {
                "title": "Revenue Risk",
                "value": format_currency(value_at_risk),
                "body": "Current modeled exposure across the selected customer scope.",
            },
            {
                "title": "Recovery Headroom",
                "value": format_currency(expected_recovery),
                "body": f"Potential recovery under the active {uplift}% uplift scenario.",
            },
            {
                "title": "Decision ROI",
                "value": format_percent(roi),
                "body": "Financial framing for intervention approval.",
            },
        ],
    )
with risk_summary_right:
    render_story_block(
        st,
        title="Action Recommendation",
        body="The board is intentionally sequenced from current state to exposure, then to approved actions with owners and delivery follow-through.",
        badge="Decision-ready",
    )
    render_story_block(
        st,
        title="Leadership Focus",
        body="Use this page to align executives on what changed, where the recovery headroom sits, and which actions deserve immediate approval this week.",
        badge="Operating cadence",
    )

render_section_label(st, "Target Alignment")
target_left, target_right = st.columns([1.18, 1])
with target_left:
    render_table(
        st,
        display_kpis,
        formatters={"Target": "{:,.1f}", "Actual": "{:,.1f}", "Gap": "{:,.1f}"},
    )
with target_right:
    render_story_block(
        st,
        title="Actual vs Target",
        body="Target framing stays next to the leading KPIs so the board reads like an executive review product instead of a descriptive dashboard.",
        badge="Performance frame",
    )
    render_story_block(
        st,
        title="Review Question",
        body="Which KPI is off-plan enough to justify intervention now, and which action produces the cleanest recovery path with available budget?",
        badge="Decision prompt",
    )

trend_tab, risk_tab, action_tab, governance_tab = st.tabs(
    ["Trend & Targets", "Risk & Opportunity", "Prioritized Actions", "Governance & Trust"]
)

with trend_tab:
    render_story_block(
        st,
        title="Trend Reading",
        body="The trend layer is intentionally spaced as a clean two-step read: revenue first, then retention quality. This keeps the board closer to an executive operating review than a compressed BI canvas.",
        badge="State -> trend",
    )
    render_section_label(st, "Revenue Trend")
    st.altair_chart(
        build_line_chart(
            monthly_revenue,
            x="month:N",
            y="SALES:Q",
            color="#1d4ed8",
            y_title="Revenue",
            tooltip=["month:N", "SALES:Q"],
        ),
        use_container_width=True,
    )
    render_kpi_note(
        st,
        title="Revenue read",
        body="Use this chart to anchor the review in current momentum before moving into retention quality and action pressure.",
        tone="info",
    )
    render_section_label(st, "NRR Telemetry Trend")
    if telemetry_df.empty:
        fallback_nrr = (
            monthly_revenue["SALES"] / monthly_revenue["SALES"].shift(1)
        ).fillna(1.0).clip(lower=0.6, upper=1.2)
        fallback_df = pd.DataFrame(
            {"month": monthly_revenue["month"], "NRR": (fallback_nrr * 100).round(2)}
        )
        st.altair_chart(
            build_line_chart(
                fallback_df,
                x="month:N",
                y="NRR:Q",
                color="#0f766e",
                y_title="NRR (%)",
                tooltip=["month:N", "NRR:Q"],
            ),
            use_container_width=True,
        )
        st.info("Telemetry DB not found in host; showing computed fallback NRR trend.")
    else:
        nrr_chart_df = telemetry_df.copy()
        nrr_chart_df["NRR"] = (nrr_chart_df["nrr"] * 100).round(2)
        st.altair_chart(
            build_line_chart(
                nrr_chart_df,
                x="month:N",
                y="NRR:Q",
                color="#0f766e",
                y_title="NRR (%)",
                tooltip=["month:N", "NRR:Q"],
            ),
            use_container_width=True,
        )
    render_kpi_note(
        st,
        title="Retention read",
        body="NRR stays isolated here so leadership can judge whether top-line movement is being sustained with enough retention quality.",
        tone="positive" if current_nrr >= nrr_target else "warning",
    )
    if showcase_summary:
        st.info(
            "Showcase artifacts loaded from reports/showcase/summary.json "
            f"(latest month: {showcase_summary.get('latest_month', 'n/a')})."
        )

risk_view["Expected Recovery (USD)"] = (risk_view["Revenue at Risk (USD)"] * (uplift / 100)).round(2)
risk_view["Recommended Action"] = risk_view["Risk Score"].apply(
    lambda x: "Executive Save Offer"
    if x >= 0.8
    else ("CSM Priority Call" if x >= 0.6 else "Nurture Campaign")
)

top_cols = [
    "Priority",
    "Customer ID",
    "Membership Type",
    "City",
    "Risk Score",
    "Revenue at Risk (USD)",
    "Expected Recovery (USD)",
    "Recommended Action",
]
top_priorities = risk_view.sort_values("Expected Recovery (USD)", ascending=False).head(12).copy()
top_priorities["Priority"] = [f"P{1 if idx < 3 else 2 if idx < 7 else 3}" for idx in range(len(top_priorities))]
top_priorities = top_priorities[top_cols]

with risk_tab:
    render_signal_band(
        st,
        [
            {
                "title": "Exposure Snapshot",
                "value": format_currency(value_at_risk),
                "body": "Modeled risk across the selected cohort, combining recency, satisfaction, and spend exposure.",
            },
            {
                "title": "Recovery Potential",
                "value": format_currency(expected_recovery),
                "body": f"Expected recovery at {uplift}% uplift under the current scenario assumption.",
            },
            {
                "title": "Budget Efficiency",
                "value": format_percent(roi),
                "body": "Scenario ROI helps leadership decide whether to approve intervention intensity.",
            },
        ],
    )
    risk_left, risk_right = st.columns([1.35, 1])
    with risk_left:
        render_section_label(st, "Retention Exposure Snapshot")
        render_table(
            st,
            top_priorities,
            formatters={
                "Risk Score": "{:.2f}",
                "Revenue at Risk (USD)": "${:,.0f}",
                "Expected Recovery (USD)": "${:,.0f}",
            },
        )
    with risk_right:
        render_story_block(
            st,
            title="Opportunity Highlights",
            body="The watchlist ranks accounts by expected recovery, so leadership can move directly from exposure sizing to action approval.",
            badge="Risk -> opportunity",
        )
        watchlist = top_priorities.head(5)[
            ["Customer ID", "Revenue at Risk (USD)", "Expected Recovery (USD)", "Recommended Action"]
        ]
        render_table(
            st,
            watchlist,
            formatters={
                "Revenue at Risk (USD)": "${:,.0f}",
                "Expected Recovery (USD)": "${:,.0f}",
            },
        )
    if executive_insights.get("recommended_actions"):
        render_section_label(st, "Prioritized Action Candidates")
        actions_df = pd.DataFrame(executive_insights["recommended_actions"])
        render_table(st, actions_df)

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

action_chart = build_bar_chart(
    action_counts,
    x="Accounts:Q",
    y="Action:N",
    color="#14532d",
    tooltip=["Action:N", "Accounts:Q"],
    y_title="Recommended Action",
)

register = top_priorities.head(8).copy()
owners = ["CSM Team A", "CSM Team B", "CSM Team A", "Retention Ops", "Retention Ops", "CSM Team B", "Growth Squad", "Growth Squad"]
etas = ["3d", "5d", "7d", "5d", "10d", "7d", "14d", "14d"]
statuses = ["Approved", "In Progress", "In Progress", "Planned", "Planned", "In Progress", "Planned", "Planned"]
register["Owner"] = owners[: len(register)]
register["ETA"] = etas[: len(register)]
register["Status"] = statuses[: len(register)]
register["Priority"] = [f"P{min(index + 1, 3)}" for index in range(len(register))]
register = register[
    [
        "Priority",
        "Customer ID",
        "Recommended Action",
        "Expected Recovery (USD)",
        "Risk Score",
        "Owner",
        "ETA",
        "Status",
    ]
]
with action_tab:
    render_section_label(st, "Leadership Actions This Week")
    decision_left, decision_right = st.columns([1, 1])
    with decision_left:
        render_kpi_note(
            st,
            title="Decision required this week",
            body=f"Approve the top save motion if leadership accepts {format_currency(budget)} of budget for {format_currency(expected_recovery)} in modeled recovery.",
            tone="positive" if roi > 0 else "risk",
        )
    with decision_right:
        render_kpi_note(
            st,
            title="Target pressure",
            body=f"NRR gap to target is {format_percent(nrr_target_gap)} and should frame how aggressive the action register needs to be this week.",
            tone="warning" if nrr_target_gap < 0 else "positive",
        )
    action_left, action_right = st.columns([1, 1.15])
    with action_left:
        st.altair_chart(action_chart, use_container_width=True)
        render_table(st, action_counts[["Action", "Accounts"]])
    with action_right:
        render_story_block(
            st,
            title="Prioritized Actions",
            body="The board converts risk scores into a compact action register with owner, ETA, and expected recovery so leadership can manage follow-through instead of just reviewing charts.",
            badge="Action layer",
        )
        render_table(
            st,
            register,
            formatters={"Expected Recovery (USD)": "${:,.0f}", "Risk Score": "{:.2f}"},
        )

    render_section_label(st, "Scenario Analysis")
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
    render_table(
        st,
        scenario_df,
        formatters={
            "Budget (USD)": "${:,.0f}",
            "Expected Recovery (USD)": "${:,.0f}",
            "ROI": "{:.2f}",
        },
    )
    st.download_button(
        "Download Scenario Analysis (CSV)",
        data=scenario_df.to_csv(index=False).encode("utf-8"),
        file_name="scenario_analysis.csv",
        mime="text/csv",
    )

    render_section_label(st, "Action Adoption Monitoring")
    adoption_logger = ActionAdoptionLogger(SHOWCASE_OUTPUT_DIR)
    event_rows = register.copy()
    event_rows["action_id"] = event_rows["Customer ID"].astype(str) + "::" + event_rows["Recommended Action"]
    event_options = event_rows["action_id"].tolist()
    monitor_left, monitor_right = st.columns([1, 1.2])
    with monitor_left:
        selected_action_id = st.selectbox("Action ID", options=event_options)
        selected_outcome = st.selectbox("Outcome", options=["accepted", "in_progress", "rejected"])
        if st.button("Log Action Outcome", use_container_width=True):
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
    with monitor_right:
        render_story_block(
            st,
            title="Execution Discipline",
            body="Adoption logging keeps the board connected to what the organization actually acted on, allowing realized-outcomes review rather than purely hypothetical prioritization.",
            badge="Operating cadence",
        )

with governance_tab:
    render_section_label(st, "Health and Governance")
    a, b, c = st.columns(3)
    with a:
        render_story_block(
            st,
            title="Pipeline Health",
            body=(
                f"Scorecard status is {quality_scorecard.get('status', 'not_generated').title()} with "
                f"{len(sales_df):,} sales rows and {len(customer_df):,} customer rows in scope."
            ),
            badge="Source readiness",
        )
    with b:
        churn_auc = model_metrics.get("churn", {}).get("temporal_test_roc_auc", 0.0)
        next_auc = model_metrics.get("next_purchase_30d", {}).get("temporal_test_roc_auc", 0.0)
        render_story_block(
            st,
            title="Model Health",
            body=f"Temporal AUC is {churn_auc:.3f} for churn and {next_auc:.3f} for next purchase, keeping predictive quality explicit in the board.",
            badge="Validation",
        )
    with c:
        last_sales_date = sales_df["ORDERDATE"].max().date() if not sales_df.empty else "N/A"
        customer_file_mtime = CUSTOMER_PATH.stat().st_mtime
        render_story_block(
            st,
            title="Data Freshness",
            body=(
                f"Latest sales date is {last_sales_date} and the customer source file was updated on "
                f"{pd.to_datetime(customer_file_mtime, unit='s').date()}."
            ),
            badge="Freshness",
        )

    if quality_scorecard:
        render_section_label(st, "Data Quality Scorecard")
        render_metrics_grid(
            st,
            [
                {
                    "label": "Overall Score",
                    "value": f"{quality_scorecard.get('overall_score', 0):.1f}",
                    "delta": quality_scorecard.get("status", "not_generated").title(),
                    "caption": "Composite trust signal for executive use.",
                    "context": "Quality",
                    "tone": "governance",
                    "context_tone": "warning",
                },
                {
                    "label": "Critical Accounts",
                    "value": str(quality_scorecard.get("dimensions", {}).get("critical_accounts", 0)),
                    "delta": "High-priority",
                    "caption": "Accounts requiring immediate commercial attention.",
                    "context": "Exposure",
                    "tone": "risk",
                    "context_tone": "risk",
                },
                {
                    "label": "Freshness Gap",
                    "value": str(quality_scorecard.get("dimensions", {}).get("freshness_days", "n/a")),
                    "delta": "days",
                    "caption": "Gap between expected freshness and current artifact age.",
                    "context": "Ops",
                    "tone": "governance",
                    "context_tone": "warning",
                },
                {
                    "label": "Churn AUC",
                    "value": f"{quality_scorecard.get('dimensions', {}).get('churn_auc_temporal_test', 0.0):.3f}",
                    "delta": "Temporal test",
                    "caption": "Model quality exposed directly in the governance layer.",
                    "context": "Model",
                    "tone": "opportunity",
                    "context_tone": "positive",
                },
            ],
        )
        checks_df = pd.DataFrame(quality_scorecard.get("checks", []))
        if not checks_df.empty:
            render_table(st, checks_df)

    if semantic_catalog.get("metrics"):
        render_section_label(st, "Semantic Metric Layer")
        semantic_df = pd.DataFrame(semantic_catalog["metrics"])[
            ["display_name", "domain", "grain", "formula", "executive_use"]
        ]
        render_table(st, semantic_df)

    if showcase_summary:
        render_section_label(st, "Realized Outcomes Tracking")
        adoption_metrics = load_json_artifact(SHOWCASE_OUTPUT_DIR / "action_adoption_metrics.json")
        render_metrics_grid(
            st,
            [
                {
                    "label": "Adoption Rate",
                    "value": format_percent(adoption_metrics.get("adoption_rate", 0.0)),
                    "delta": "Action follow-through",
                    "caption": "Share of logged actions that moved into accepted state.",
                    "context": "Execution",
                },
                {
                    "label": "Accepted Actions",
                    "value": str(adoption_metrics.get("accepted_events", 0)),
                    "delta": "Activated",
                    "caption": "Count of actions already approved or accepted.",
                    "context": "Count",
                },
                {
                    "label": "Accepted Recovery",
                    "value": format_currency(adoption_metrics.get("accepted_expected_recovery_usd", 0.0)),
                    "delta": "Booked opportunity",
                    "caption": "Expected recovery tied to accepted actions.",
                    "context": "Value",
                },
                {
                    "label": "In Progress Recovery",
                    "value": format_currency(adoption_metrics.get("in_progress_expected_recovery_usd", 0.0)),
                    "delta": "Pipeline value",
                    "caption": "Expected recovery tied to actions still underway.",
                    "context": "Progress",
                },
            ],
        )

render_footer(
    st,
    "Copyright (c) 2026 Samuel Maia. Proprietary platform. "
    "Author: [LinkedIn](https://linkedin.com/in/samuelmaia-analytics) | "
    "[GitHub](https://github.com/samuelmaia-analytics)",
)
