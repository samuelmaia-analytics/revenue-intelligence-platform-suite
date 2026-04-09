import sys
import json
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "platform_connectors").exists():
            return candidate
    return Path(__file__).resolve().parents[2]


ROOT = _find_repo_root(Path(__file__).resolve())
try:
    import common  # noqa: F401
    import platform_connectors  # noqa: F401
except ModuleNotFoundError:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(ROOT / "packages") not in sys.path:
        sys.path.insert(0, str(ROOT / "packages"))

from common import enforce_streamlit_sso, list_client_profiles  # noqa: E402
from dashboard_theme import apply_dashboard_theme, render_footer, render_hero, render_intro_banner, render_section_label  # noqa: E402
from dashboard_ui import (  # noqa: E402
    render_command_bar,
    format_percent,
    render_global_context,
    render_insight_grid,
    render_kpi_note,
    render_metrics_grid,
    render_sidebar_nav,
    render_signal_band,
    render_story_block,
    render_table,
)

st.set_page_config(
    page_title="Revenue-Intelligence-Platform-Suite",
    layout="wide",
    initial_sidebar_state="expanded",
)

identity = enforce_streamlit_sso(st)

with st.sidebar:
    render_sidebar_nav(
        st,
        current_page="home",
        mode_label="Executive landing",
        mode_body="Premium control tower for recurring revenue, retention, and KPI governance.",
        flow_label="Read top-down",
        flow_body="Positioning, four core KPIs, trust signals, then the two primary navigation paths.",
    )

SHOWCASE_DIR = ROOT / "reports" / "showcase"


@st.cache_data(show_spinner=False)
def load_showcase_artifact(file_name: str) -> dict:
    artifact_path = SHOWCASE_DIR / file_name
    if not artifact_path.exists():
        return {}
    return pd.read_json(artifact_path, typ="series").to_dict()


@st.cache_data(show_spinner=False)
def load_json_artifact(file_name: str) -> dict:
    artifact_path = SHOWCASE_DIR / file_name
    if not artifact_path.exists():
        return {}
    with artifact_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


solution_profile = load_showcase_artifact("solution_profile.json")
quality_scorecard = load_showcase_artifact("data_quality_scorecard.json")
tenant_secret_status = load_showcase_artifact("tenant_secret_status.json")
executive_insights = load_json_artifact("executive_insights.json")
showcase_summary = load_showcase_artifact("summary.json")
client_profiles = list_client_profiles()
narrative = solution_profile.get("narrative", {})
apply_dashboard_theme(st)
render_intro_banner(
    st,
    title="Revenue-Intelligence-Platform-Suite",
    subtitle="Executive-grade analytics platform for recurring revenue, retention, and commercial governance.",
    notice=(
        "Copyright Samuel Maia. This platform, its executive assets, and generated materials are proprietary. "
        "Public app access does not grant rights to reuse, copy, or redistribute the codebase or commercial assets."
    ),
    eyebrow="UI refresh 2026-04-09",
)

render_global_context(
    st,
    suite_label="Platform Suite",
    page_title="Executive Analytics Workspace",
    summary="A white-label analytics suite for revenue performance, retention exposure, KPI governance, and board-level decision support.",
    right_hint=solution_profile.get("deployment_env", "showcase").title(),
)

render_hero(
    st,
    title="Revenue Intelligence Platform Suite",
    kicker="Executive Analytics Platform",
    subtitle=(
        narrative.get("value_proposition")
        or "Use this app as the executive landing zone for KPI governance, revenue risk exposure, and board-ready action planning."
    ),
    chips=[
        solution_profile.get("package", {}).get("name", "Revenue Command Center"),
        solution_profile.get("industry", "Multi-client adaptation"),
        solution_profile.get("deployment_env", "showcase").title(),
    ],
)

render_command_bar(
    st,
    [
        {
            "label": "Platform",
            "title": "Executive suite status",
            "value": solution_profile.get("deployment_env", "showcase").title(),
            "note": "Single control layer for revenue, retention, governance and delivery assets.",
            "primary": True,
        },
        {
            "label": "Profiles",
            "title": "Adaptation profiles",
            "value": str(len(client_profiles)),
            "note": "Reusable client lenses already mapped into the suite.",
        },
        {
            "label": "Trust",
            "title": "Quality score",
            "value": f"{quality_scorecard.get('overall_score', 0):.1f}",
            "note": quality_scorecard.get("status", "not_generated").title(),
        },
        {
            "label": "Decision Layer",
            "title": "Value at risk",
            "value": f"${showcase_summary.get('total_value_at_risk_usd', 0):,.0f}",
            "note": "Commercial exposure framed for leadership review.",
        },
    ],
)

if narrative.get("headline"):
    st.markdown(
        f'<div class="rip-inline-pill">{narrative["headline"]}</div>',
        unsafe_allow_html=True,
    )

render_metrics_grid(
    st,
    [
        {
            "label": "Primary Package",
            "value": solution_profile.get("package", {}).get("name", "Revenue Command Center"),
            "delta": solution_profile.get("executive_buyer", "Executive buyer"),
            "caption": "Commercial packaging for recurring revenue and executive actioning.",
            "context": "Go-to-market",
            "context_tone": "positive",
            "featured": True,
        },
        {
            "label": "Latest Revenue",
            "value": f"${showcase_summary.get('latest_revenue_usd', 0):,.0f}",
            "delta": format_percent(showcase_summary.get("nrr_latest", 0.0)),
            "caption": "Latest closed month loaded from showcase telemetry artifacts.",
            "context": "Revenue",
            "tone": "opportunity",
            "context_tone": "positive",
        },
        {
            "label": "Value At Risk",
            "value": f"${showcase_summary.get('total_value_at_risk_usd', 0):,.0f}",
            "delta": f"Top 50: ${showcase_summary.get('top_50_value_at_risk_usd', 0):,.0f}",
            "caption": "Revenue exposure that can be converted into prioritized action plans.",
            "context": "Risk",
            "tone": "risk",
            "context_tone": "risk",
        },
        {
            "label": "Data Confidence",
            "value": f"{quality_scorecard.get('overall_score', 0):.1f}",
            "delta": quality_scorecard.get("status", "not_generated").title(),
            "caption": "Operational scorecard covering freshness, guardrails, and model health.",
            "context": "Governance",
            "tone": "governance",
            "context_tone": "warning",
        },
    ],
)

if tenant_secret_status:
    render_section_label(st, "Trust Layer")
    render_signal_band(
        st,
        [
            {
                "title": "Tenant Readiness",
                "value": f"{tenant_secret_status.get('configured_secret_count', 0)}/{tenant_secret_status.get('required_secret_count', 0)} configured",
                "body": "Secrets readiness stays visible at landing level because deployment hygiene affects decision confidence.",
            },
            {
                "title": "Freshness Gap",
                "value": f"{quality_scorecard.get('dimensions', {}).get('freshness_days', 'n/a')} days",
                "body": "Freshness remains adjacent to KPIs so executives know whether the surface is current enough for action.",
            },
            {
                "title": "Model Quality",
                "value": f"AUC {quality_scorecard.get('dimensions', {}).get('churn_auc_temporal_test', 0.0):.3f}",
                "body": "Predictive quality is kept in the product surface instead of being buried in technical documentation.",
            },
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

render_section_label(st, "Executive Summary")
summary_insights = executive_insights.get("insights", []) if executive_insights else []
render_insight_grid(
    st,
    [
        {
            "eyebrow": "Current State",
            "title": "This page now works as an executive preface, not as the full operating review.",
            "body": "The landing layer is intentionally compressed so leadership gets product context, baseline KPIs, trust signals, and clear next steps in one read.",
            "action": "Use the KPI board for weekly review and the modules page for product breadth.",
        },
        {
            "eyebrow": "Business Signal",
            "title": summary_insights[0]["headline"] if summary_insights else "Recovery pockets are visible at account level.",
            "body": summary_insights[0]["detail"] if summary_insights else "Revenue-at-risk concentration is already shaped for action prioritization.",
            "action": summary_insights[0]["recommended_action"] if summary_insights else "Launch a weekly action review with revenue and CS leadership.",
        },
        {
            "eyebrow": "Trust Layer",
            "title": "Governance is part of the product experience.",
            "body": "Semantic metrics, scorecards, tenant readiness, release evidence, and approval flow are positioned as visible product features.",
            "action": "Keep confidence signals adjacent to decisions, not buried in separate technical documentation.",
        },
    ],
)

render_section_label(st, "Primary Paths")
path_left, path_right = st.columns(2)
with path_left:
    render_story_block(
        st,
        title="KPI Board",
        body="Open the operating review for trend, exposure, weekly decisions, prioritized actions, and governance confidence.",
        badge="Primary path",
    )
    if st.button("Open Executive KPI Board", use_container_width=True):
        st.switch_page("pages/1_Executive_KPI_Board.py")
with path_right:
    render_story_block(
        st,
        title="Modules Portal",
        body="Open the product catalog when the conversation needs breadth, repositories, public demos, and asset coverage.",
        badge="Secondary path",
    )
    if st.button("Open Modules Portal", use_container_width=True):
        st.switch_page("pages/2_Modules_Access.py")

render_section_label(st, "Client Adaptation Profiles")
profiles_df = pd.DataFrame(
    [
        {
            "Profile": profile.get("profile_id", ""),
            "Client": profile.get("client_name", ""),
            "Industry": profile.get("industry", ""),
            "Primary Buyer": profile.get("executive_buyer", ""),
        }
        for profile in client_profiles
    ]
)
render_table(st, profiles_df)

render_section_label(st, "Decision Notes")
note_left, note_mid, note_right = st.columns(3)
with note_left:
    render_kpi_note(
        st,
        title="Risk posture",
        body=f"Current modeled exposure is ${showcase_summary.get('total_value_at_risk_usd', 0):,.0f}, so revenue risk stays as the first read on this surface.",
        tone="risk",
    )
with note_mid:
    render_kpi_note(
        st,
        title="Opportunity",
        body=f"The top-50 account cohort concentrates ${showcase_summary.get('top_50_value_at_risk_usd', 0):,.0f} in recovery potential for the next save motion.",
        tone="positive",
    )
with note_right:
    render_kpi_note(
        st,
        title="Trust signal",
        body=f"Quality score is {quality_scorecard.get('overall_score', 0):.1f}, keeping freshness, guardrails and model validity visible to executives.",
        tone="info",
    )

render_section_label(st, "Proof of Value")
value_left, value_right = st.columns([1.15, 1])
with value_left:
    render_story_block(
        st,
        title="Why this reads like a product",
        body="Telemetry-backed KPIs, decision framing, governance scorecards, semantic metrics and client adaptation are presented as one executive system rather than isolated assets.",
        badge="Product signal",
    )
with value_right:
    render_story_block(
        st,
        title="Executive deliverables",
        body="Review packs, proposal packs, release evidence and industry-specific demos are positioned as part of the platform surface, not as separate afterthoughts.",
        badge="Commercial proof",
    )

deliverable_left, deliverable_right = st.columns([1.15, 1])
with deliverable_left:
    deliverables = pd.DataFrame(
        [
            {"Deliverable": "Executive Review Pack", "Format": "Markdown / JSON / HTML", "Use": "Board and steering review"},
            {"Deliverable": "Client Proposal Pack", "Format": "Markdown / JSON / HTML", "Use": "Commercial proposal and pitch asset"},
            {"Deliverable": "Release Evidence Pack", "Format": "tar.gz", "Use": "Quarterly proof and release artifact"},
            {"Deliverable": "Industry Demo Packs", "Format": "Per-profile folders", "Use": "Client-specific commercial demos"},
        ]
    )
    render_table(st, deliverables)
with deliverable_right:
    st.link_button(
        "Open Revenue Intelligence Demo",
        "https://revenue-intelligence-platform.streamlit.app/",
        use_container_width=True,
    )
    st.link_button(
        "Open Data Senior Analytics Demo",
        "https://data-analytics-sr.streamlit.app",
        use_container_width=True,
    )

render_footer(
    st,
    "Copyright (c) 2026 Samuel Maia. Proprietary platform. "
    "Author: [LinkedIn](https://linkedin.com/in/samuelmaia-analytics) | "
    "[GitHub](https://github.com/samuelmaia-analytics)",
)
