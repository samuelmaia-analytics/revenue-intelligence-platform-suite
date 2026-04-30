import sys
from datetime import datetime
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from main import run_pipeline  # noqa: E402
from src.config import PipelineConfig  # noqa: E402
from src.dashboard.service import (  # noqa: E402
    build_dashboard_payload,
    compute_executive_story,
    filter_recommendations,
)

CFG = PipelineConfig.from_env(PROJECT_ROOT)

LABELS = {
    "page_title": "Revenue Intelligence Executive Board",
    "subtitle": "End-to-end revenue analytics with semantic KPIs, retention risk, and channel efficiency.",
    "refresh": "Refresh pipeline outputs",
    "filters": "Portfolio filters",
    "segment": "Segment",
    "channel": "Channel",
    "action": "Action",
    "overview": "Overview",
    "trend": "Trend",
    "segmentation": "Segmentation",
    "insights": "Insights",
    "all": "All",
}


def ensure_outputs(processed_dir: Path) -> None:
    required = [
        "recommendations.csv",
        "cohort_retention.csv",
        "unit_economics.csv",
        "executive_report.json",
        "business_outcomes.json",
        "top_10_actions.csv",
    ]
    if not all((processed_dir / file_name).exists() for file_name in required):
        run_pipeline(CFG)


def format_currency(value: float) -> str:
    return f"{CFG.app.currency_symbol}{value:,.0f}"


def style_chart(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#f6f3ee",
        plot_bgcolor="#fffdf8",
        font={"family": "Georgia, Times New Roman, serif", "color": "#1f2933"},
        margin={"l": 30, "r": 20, "t": 48, "b": 30},
    )
    return fig


st.set_page_config(page_title=LABELS["page_title"], layout="wide")
st.markdown(
    """
    <style>
        .stApp { background: linear-gradient(180deg, #f4efe7 0%, #fbfaf7 55%, #f1f5f2 100%); color: #1f2933; }
        [data-testid="stSidebar"] { background: rgba(255, 253, 248, 0.95); border-right: 1px solid #ddd6c8; }
        .hero { background: linear-gradient(135deg, #1f3b4d 0%, #284f63 60%, #6a8b6f 100%); color: #f8f4ec; padding: 24px 28px; border-radius: 20px; box-shadow: 0 18px 45px rgba(31, 59, 77, 0.18); margin-bottom: 18px; }
        .hero h1 { font-family: Georgia, Times New Roman, serif; letter-spacing: 0.02em; margin: 0; }
        .hero p { margin: 6px 0 0; color: #f1e8db; max-width: 820px; }
        .metric-shell { background: rgba(255,255,255,0.88); border: 1px solid #ddd6c8; border-radius: 18px; padding: 14px 16px; box-shadow: 0 8px 22px rgba(31, 41, 51, 0.06); }
        .metric-shell .label { text-transform: uppercase; letter-spacing: 0.08em; color: #7b6f62; font-size: 0.75rem; }
        .metric-shell .value { font-family: Georgia, Times New Roman, serif; font-size: 2rem; color: #1f2933; margin-top: 6px; }
        .metric-shell .sub { color: #52606d; font-size: 0.85rem; margin-top: 4px; }
        .story-card { background: rgba(255, 253, 248, 0.92); border-left: 5px solid #b27d4f; border-radius: 14px; padding: 16px 18px; box-shadow: 0 10px 28px rgba(31, 41, 51, 0.05); }
        .story-card strong { color: #1f3b4d; }
    </style>
    """,
    unsafe_allow_html=True,
)

processed_dir = PROJECT_ROOT / "data" / "processed"
ensure_outputs(processed_dir)
payload = build_dashboard_payload(processed_dir)

with st.sidebar:
    st.header(LABELS["filters"])
    if st.button(LABELS["refresh"], use_container_width=True):
        run_pipeline(CFG)
        st.rerun()

    segment = st.selectbox(
        LABELS["segment"],
        [LABELS["all"]] + sorted(payload.recommendations["segment"].dropna().unique().tolist()),
    )
    channel = st.selectbox(
        LABELS["channel"],
        [LABELS["all"]] + sorted(payload.recommendations["channel"].dropna().unique().tolist()),
    )
    action = st.selectbox(
        LABELS["action"],
        [LABELS["all"]]
        + sorted(payload.recommendations["recommended_action"].dropna().unique().tolist()),
    )

filtered = filter_recommendations(
    payload.recommendations,
    segment=segment,
    channel=channel,
    action=action,
)
if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

story = compute_executive_story(filtered)
df = story["df"]

st.markdown(
    f"""
    <div class="hero">
        <h1>{LABELS["page_title"]}</h1>
        <p>{LABELS["subtitle"]}</p>
        <p>Updated at {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4 = st.columns(4)
k1.markdown(
    f"<div class='metric-shell'><div class='label'>Revenue</div><div class='value'>{format_currency(df['ltv'].sum())}</div><div class='sub'>Portfolio lifetime value in scope</div></div>",
    unsafe_allow_html=True,
)
k2.markdown(
    f"<div class='metric-shell'><div class='label'>Growth Rate</div><div class='value'>{story['portfolio_growth_rate']:.1%}</div><div class='sub'>Latest period-over-period signal</div></div>",
    unsafe_allow_html=True,
)
k3.markdown(
    f"<div class='metric-shell'><div class='label'>ARPU</div><div class='value'>{format_currency(df['ltv'].mean())}</div><div class='sub'>Average LTV proxy per customer</div></div>",
    unsafe_allow_html=True,
)
k4.markdown(
    f"<div class='metric-shell'><div class='label'>Churn</div><div class='value'>{df['churn_probability'].mean():.1%}</div><div class='sub'>Average predicted churn risk</div></div>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="story-card">
        <strong>Executive narrative.</strong> {story["top_segment"]["segment"]} is the highest-risk segment at
        {story["top_segment"]["churn_probability"]:.1%}. Customer {int(story["top_customer"]["customer_id"])}
        has the largest modeled upside with {format_currency(float(story["top_customer"]["potential_impact"]))}
        of potential impact. The current action mix is led by {story["top_action"]["recommended_action"]}
        at {story["top_action"]["proportion"]:.1f}% of the filtered portfolio.
    </div>
    """,
    unsafe_allow_html=True,
)

tab_overview, tab_trend, tab_segmentation, tab_insights = st.tabs(
    [LABELS["overview"], LABELS["trend"], LABELS["segmentation"], LABELS["insights"]]
)

with tab_overview:
    left, right = st.columns(2)
    with left:
        action_mix = df["recommended_action"].value_counts().reset_index()
        action_mix.columns = ["recommended_action", "customers"]
        fig_action = px.bar(
            action_mix,
            x="recommended_action",
            y="customers",
            color="recommended_action",
            title="Recommended action mix",
            color_discrete_sequence=["#1f3b4d", "#b27d4f", "#6a8b6f", "#8b5e3c"],
        )
        fig_action.update_layout(showlegend=False)
        st.plotly_chart(style_chart(fig_action), use_container_width=True, theme=None)
    with right:
        fig_eff = px.bar(
            payload.unit_economics.sort_values("ltv_cac_ratio", ascending=False),
            x="channel",
            y="ltv_cac_ratio",
            color="channel",
            title="Channel efficiency",
            color_discrete_sequence=["#284f63", "#6a8b6f", "#b27d4f", "#8c6d46", "#3f4c5a"],
        )
        fig_eff.update_layout(showlegend=False)
        st.plotly_chart(style_chart(fig_eff), use_container_width=True, theme=None)

with tab_trend:
    trend_df = payload.monthly_revenue.copy()
    if trend_df.empty:
        st.info("Monthly trend is unavailable because the scored dataset does not contain multiple periods.")
    else:
        trend_left, trend_right = st.columns(2)
        with trend_left:
            fig_revenue = px.line(
                trend_df,
                x="month",
                y="revenue",
                markers=True,
                title="Revenue trend",
            )
            st.plotly_chart(style_chart(fig_revenue), use_container_width=True, theme=None)
        with trend_right:
            fig_arpu = px.area(
                trend_df,
                x="month",
                y="arpu",
                title="ARPU trend",
                color_discrete_sequence=["#b27d4f"],
            )
            st.plotly_chart(style_chart(fig_arpu), use_container_width=True, theme=None)

    cohort_heatmap = payload.cohort.copy()
    cohort_heatmap["retention_pct"] = cohort_heatmap["retention_rate"] * 100
    heat = cohort_heatmap.pivot(index="cohort_month", columns="cohort_index", values="retention_pct")
    fig_cohort = px.imshow(
        heat.sort_index(),
        aspect="auto",
        text_auto=".0f",
        title="Retention by cohort",
        color_continuous_scale=[[0, "#f2e9dc"], [0.5, "#a7c4a0"], [1, "#1f3b4d"]],
    )
    st.plotly_chart(style_chart(fig_cohort), use_container_width=True, theme=None)

with tab_segmentation:
    seg_left, seg_right = st.columns(2)
    with seg_left:
        churn_segment = (
            df.groupby("segment", as_index=False)["churn_probability"]
            .mean()
            .sort_values("churn_probability", ascending=False)
        )
        fig_segment = px.bar(
            churn_segment,
            x="segment",
            y="churn_probability",
            color="segment",
            title="Churn by segment",
        )
        fig_segment.update_layout(showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(style_chart(fig_segment), use_container_width=True, theme=None)
    with seg_right:
        next_purchase = (
            df.groupby("channel", as_index=False)["next_purchase_probability"]
            .mean()
            .sort_values("next_purchase_probability", ascending=False)
        )
        fig_channel = px.bar(
            next_purchase,
            x="channel",
            y="next_purchase_probability",
            color="channel",
            title="Next purchase probability by channel",
        )
        fig_channel.update_layout(showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(style_chart(fig_channel), use_container_width=True, theme=None)

    scatter = px.scatter(
        df,
        x="churn_probability",
        y="ltv_cac_ratio",
        size="ltv",
        color="segment",
        hover_data=["customer_id", "recommended_action"],
        title="Portfolio segmentation map",
        color_discrete_sequence=["#1f3b4d", "#6a8b6f", "#b27d4f"],
    )
    st.plotly_chart(style_chart(scatter), use_container_width=True, theme=None)

with tab_insights:
    insight_left, insight_right = st.columns([1.1, 0.9])
    with insight_left:
        fig_top = px.bar(
            payload.top_actions.sort_values("net_impact", ascending=True),
            x="net_impact",
            y="customer_id",
            color="action",
            orientation="h",
            title="Top actions by simulated net impact",
            color_discrete_sequence=["#1f3b4d", "#b27d4f", "#6a8b6f", "#8b5e3c"],
        )
        st.plotly_chart(style_chart(fig_top), use_container_width=True, theme=None)
    with insight_right:
        outcomes = payload.outcomes["simulation_summary_top10"]
        st.metric("Scenario revenue 90d", format_currency(float(outcomes["scenario_revenue_90d"])))
        st.metric("Revenue delta 90d", format_currency(float(outcomes["delta_revenue_90d"])))
        st.metric("Simulated ROI", f"{float(outcomes['roi_simulated']):.2f}x")

    st.dataframe(
        payload.top_actions.sort_values("strategic_priority_score", ascending=False),
        use_container_width=True,
        hide_index=True,
        height=420,
    )
