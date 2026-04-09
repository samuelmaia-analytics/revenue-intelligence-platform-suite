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
    render_command_grid,
    render_global_context,
    render_insight_grid,
    render_metrics_grid,
    render_module_cards,
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
    st.markdown("### Workspace")
    st.page_link("app.py", label="Platform Home")
    st.page_link("pages/1_Executive_KPI_Board.py", label="Executive KPI Board")
    st.page_link("pages/2_Modules_Access.py", label="Modules Access")
    st.markdown("### Use")
    st.caption("Premium analytics control tower for recurring revenue, retention and governance.")
    st.markdown("### Read Flow")
    st.caption("Context, core KPIs, trust layer, package footprint and executive assets.")

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

render_command_grid(
    st,
    [
        {
            "label": "Context",
            "title": "Executive landing zone",
            "body": "Use this page as the high-level product surface before drilling into KPI execution and module footprint.",
        },
        {
            "label": "Priority",
            "title": "Start with revenue risk",
            "body": "Current-state metrics and governance indicators are positioned first so decision quality is obvious before actioning.",
        },
        {
            "label": "Flow",
            "title": "Navigate by decision layer",
            "body": "Home frames the platform, KPI Board operationalizes it, and Modules Access shows reusable product breadth.",
        },
    ],
)
render_command_bar(
    st,
    [
        {
            "label": "Platform State",
            "title": "Executive suite status",
            "value": solution_profile.get("deployment_env", "showcase").title(),
            "note": "Single surface for revenue, retention, governance and delivery assets.",
            "primary": True,
        },
        {
            "label": "Profiles",
            "title": "Client adaptations",
            "value": str(len(client_profiles)),
            "note": "Reusable profiles already mapped into the suite.",
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
    render_signal_band(
        st,
        [
            {
                "title": "Tenant Readiness",
                "value": f"{tenant_secret_status.get('configured_secret_count', 0)}/{tenant_secret_status.get('required_secret_count', 0)} configured",
                "body": "Multi-tenant secrets status is visible at the landing layer to reinforce deployment readiness.",
            },
            {
                "title": "Freshness Gap",
                "value": f"{quality_scorecard.get('dimensions', {}).get('freshness_days', 'n/a')} days",
                "body": "Freshness is kept visible so executive consumers can judge whether outputs are current enough for action.",
            },
            {
                "title": "Model Quality",
                "value": f"AUC {quality_scorecard.get('dimensions', {}).get('churn_auc_temporal_test', 0.0):.3f}",
                "body": "Temporal validation remains attached to the product experience, not hidden inside technical docs.",
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
            "title": "The platform is structured as an executive control layer.",
            "body": "Home, KPI board, modules, proposal assets, evidence packs, and telemetry live as one integrated product surface.",
            "action": "Use the KPI board for the operational narrative and the modules page for solution footprint.",
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

render_section_label(st, "Navigation")
nav_left, nav_right = st.columns([1.05, 1])
with nav_left:
    render_story_block(
        st,
        title="Start with the KPI Board",
        body="Use the flagship board for the full decision flow: current state, trend, exposure, recommended actions, governance, and realized outcomes.",
        badge="Primary experience",
    )
    n1, n2 = st.columns(2)
    with n1:
        if st.button("Open Executive KPI Board", use_container_width=True):
            st.switch_page("pages/1_Executive_KPI_Board.py")
    with n2:
        if st.button("Open Modules Portal", use_container_width=True):
            st.switch_page("pages/2_Modules_Access.py")
with nav_right:
    render_story_block(
        st,
        title="Use this as a client-facing demo suite",
        body="The experience is designed to support interviews, executive demos, pre-sales, and reusable packaging for analytics services.",
        badge="Commercially presentable",
    )
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

render_section_label(st, "Platform Value")
value_left, value_right = st.columns([1.2, 1])
with value_left:
    render_story_block(
        st,
        title="Why this feels like a product, not a portfolio dashboard",
        body="Telemetry-backed KPIs, recommended actions, governance scorecards, semantic metrics, deal-room assets, and multi-client adaptation are surfaced as one platform narrative.",
        badge="Productized analytics",
    )
with value_right:
    render_signal_band(
        st,
        [
            {
                "title": "Decision Cycle",
                "value": "Weekly",
                "body": "Optimized for recurring executive review instead of ad hoc exploration.",
            },
            {
                "title": "Primary Buyers",
                "value": "Revenue + CS + COO",
                "body": "Built for commercial leadership and executive operating cadences.",
            },
            {
                "title": "Delivery Model",
                "value": "Board + Actions",
                "body": "The suite couples KPI review with action registers and evidence artifacts.",
            },
        ],
    )

render_section_label(st, "Solution Packages")
package_cards = [
    [
        {
            "name": "Revenue Command Center",
            "category": "Flagship Package",
            "status": "Primary",
            "role": "Protect recurring revenue with prioritized action playbooks, exposure framing, and executive weekly operating reviews.",
            "value": "Buyer: CRO / RevOps",
            "asset_type": "Board + action register",
        },
        {
            "name": "Retention Intelligence",
            "category": "Retention Package",
            "status": "Live",
            "role": "Surface churn exposure, account risk, and save-motion opportunities for Customer Success and retention leadership.",
            "value": "Buyer: CS leadership",
            "asset_type": "Risk + recovery layer",
        },
        {
            "name": "Executive KPI Governance",
            "category": "Governance Package",
            "status": "Live",
            "role": "Standardize definitions, freshness, trust signals, and accountability around executive metrics.",
            "value": "Buyer: CEO / COO / CFO",
            "asset_type": "Metric contracts + scorecards",
        },
        {
            "name": "Commercial Performance Analytics",
            "category": "Commercial Package",
            "status": "Live",
            "role": "Improve seller, channel, and segment performance visibility with a clearer operating view for commercial teams.",
            "value": "Buyer: Sales / Commercial Ops",
            "asset_type": "Performance analytics",
        },
    ]
]
render_module_cards(st, package_cards[0])

render_section_label(st, "Executive Deliverables")
render_story_block(
    st,
    title="Board-ready artifacts are part of the platform surface",
    body="The suite produces review packs, proposal packs, evidence packs, deal rooms, and industry demo assets that reinforce its value as a client solution.",
    badge="Commercial asset layer",
)
deliverables = pd.DataFrame(
    [
        {"Deliverable": "Executive Review Pack", "Format": "Markdown / JSON / HTML", "Use": "Board and steering review"},
        {"Deliverable": "Client Proposal Pack", "Format": "Markdown / JSON / HTML", "Use": "Commercial proposal and pitch asset"},
        {"Deliverable": "Release Evidence Pack", "Format": "tar.gz", "Use": "Quarterly proof and release artifact"},
        {"Deliverable": "Industry Demo Packs", "Format": "Per-profile folders", "Use": "Client-specific commercial demos"},
    ]
)
render_table(st, deliverables)

render_footer(
    st,
    "Copyright (c) 2026 Samuel Maia. Proprietary platform. "
    "Author: [LinkedIn](https://linkedin.com/in/samuelmaia-analytics) | "
    "[GitHub](https://github.com/samuelmaia-analytics)",
)
