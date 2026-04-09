import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from dashboard_theme import apply_dashboard_theme, render_footer, render_hero, render_intro_banner, render_section_label  # noqa: E402
from dashboard_ui import render_command_bar, render_command_grid, render_global_context, render_module_cards, render_sidebar_nav, render_story_block  # noqa: E402


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "platform_connectors").exists():
            return candidate
    return Path(__file__).resolve().parents[3]


st.set_page_config(page_title="Modules Access", layout="wide")

try:
    import common  # noqa: F401
except ModuleNotFoundError:
    ROOT = _find_repo_root(Path(__file__).resolve())
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(ROOT / "packages") not in sys.path:
        sys.path.insert(0, str(ROOT / "packages"))

from common import enforce_streamlit_sso  # noqa: E402

identity = enforce_streamlit_sso(st)

with st.sidebar:
    render_sidebar_nav(
        st,
        current_page="modules",
        mode_label="Product catalog",
        mode_body="Module catalog, public demos, repositories and trust assets in one executive portal.",
        flow_label="Read top-down",
        flow_body="Portfolio scope, module footprint, proof assets and direct links.",
    )

ROOT = _find_repo_root(Path(__file__).resolve())
apply_dashboard_theme(st)
render_intro_banner(
    st,
    title="Modules Access",
    subtitle="Portal for integrated repositories, public demos, and the technical assets that support the flagship executive platform.",
    notice="Use this page to navigate the suite footprint during demos, interviews, and client conversations.",
    eyebrow="UI refresh 2026-04-09",
)
render_global_context(
    st,
    suite_label="Module Catalog",
    page_title="Integrated Analytics Suite",
    summary="Browse the specialized analytics modules that feed the flagship executive platform and demonstrate the breadth of the productized service model.",
    right_hint="Internal platform portal",
)

render_hero(
    st,
    title="Modules Access",
    kicker="Integrated Repository Map",
    subtitle="Single place to access integrated repositories, public demos, and the technical assets that support the flagship executive platform.",
    chips=["Flagship suite", "Public demos", "Source repositories"],
)
render_command_grid(
    st,
    [
        {
            "label": "Portfolio",
            "title": "Reusable analytics assets",
            "body": "Each module strengthens the platform story as a productized analytics suite, not a collection of isolated demos.",
        },
        {
            "label": "Use",
            "title": "Demo and diligence hub",
            "body": "Open code, live demos and trust assets from the same screen during interviews, pre-sales and executive walkthroughs.",
        },
        {
            "label": "Signal",
            "title": "Commercial breadth",
            "body": "The catalog reinforces that the suite can expand across revenue, churn, commerce and senior analytics delivery motions.",
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

modules = [
    {
        "name": "Revenue Intelligence",
        "path": "modules/revenue-intelligence",
        "role": "Revenue analytics, scoring, recommendations, executive assets",
        "demo": "https://revenue-intelligence-platform.streamlit.app/",
        "repo": "https://github.com/samuelmaia-analytics/Revenue-Intelligence-Platform-End-to-End-Analytics-ML-System",
    },
    {
        "name": "Churn Prediction",
        "path": "modules/churn-prediction",
        "role": "Churn modeling, orchestration patterns, ML tracking",
        "demo": "https://telecom-churn-prediction-samuelmaiapro.streamlit.app/",
        "repo": "https://github.com/samuelmaia-analytics/churn-prediction",
    },
    {
        "name": "Amazon Sales Analysis",
        "path": "modules/amazon-sales-analysis",
        "role": "Sales leakage and KPI analytics with contracts and CI patterns",
        "demo": "https://amazon-sales-analysis-samuemaiapro.streamlit.app/",
        "repo": "https://github.com/samuelmaia-analytics/amazon-sales-analysis",
    },
    {
        "name": "Analise Vendas Python",
        "path": "modules/analise-vendas-python",
        "role": "Operational sales analytics and processed star-style datasets",
        "demo": "https://sales-analytics-dashboardd.streamlit.app/",
        "repo": "https://github.com/samuelmaia-analytics/analise-vendas-python",
    },
    {
        "name": "Data Senior Analytics",
        "path": "modules/data-senior-analytics",
        "role": "Business-focused analytics pipeline and dashboard outputs",
        "demo": "https://data-analytics-sr.streamlit.app",
        "repo": "https://github.com/samuelmaia-analytics/data-senior-analytics",
    },
]

module_cards = [
    {
        "name": module["name"],
        "category": "Integrated module",
        "status": "Available" if (ROOT / module["path"]).exists() else "External only",
        "status_tone": "positive" if (ROOT / module["path"]).exists() else "warning",
        "role": module["role"],
        "value": f"Path: {module['path']}",
        "asset_type": "Source repo + public demo",
    }
    for module in modules
]

render_command_bar(
    st,
    [
        {
            "label": "Coverage",
            "title": "Integrated modules",
            "value": str(len(modules)),
            "note": "Portfolio assets surfaced from one executive portal.",
            "primary": True,
        },
        {
            "label": "Availability",
            "title": "Local modules",
            "value": str(sum(1 for module in modules if (ROOT / module["path"]).exists())),
            "note": "Modules already present inside this monorepo.",
        },
        {
            "label": "Proof",
            "title": "Public demos",
            "value": str(sum(1 for module in modules if module["demo"])),
            "note": "Live links usable in interviews and client walkthroughs.",
        },
        {
            "label": "Commercial Use",
            "title": "Primary lens",
            "value": "Product suite",
            "note": "Framed as reusable analytics offerings, not isolated projects.",
        },
    ],
)

render_section_label(st, "Suite Overview")
overview_left, overview_right = st.columns([1.25, 1])
with overview_left:
    render_story_block(
        st,
        title="Why the module portal matters",
        body="This page frames the monorepo as a suite of reusable analytics products rather than isolated experiments. Each module represents an adaptation path, delivery asset, or specialization that can feed the commercial platform motion.",
        badge="Platform narrative",
    )
with overview_right:
    render_story_block(
        st,
        title="How to use this page",
        body="Use the cards below to navigate the suite footprint during demos, interviews, and client conversations. Jump into the source repo for depth or the public app when you want a live proof point.",
        badge="Demo-ready",
    )

render_section_label(st, "Module Catalog")
render_module_cards(st, module_cards)

catalog_tab, proof_tab = st.tabs(["Module Actions", "Proof & Governance"])

with catalog_tab:
    for module in modules:
        module_exists = (ROOT / module["path"]).exists()
        render_section_label(st, module["name"])
        detail_left, detail_mid, detail_right = st.columns([1.2, 0.9, 0.9])
        with detail_left:
            render_story_block(
                st,
                title=module["name"],
                body=module["role"],
                badge="In monorepo" if module_exists else "External asset",
            )
        with detail_mid:
            st.link_button(f"Open Repository: {module['name']}", module["repo"], use_container_width=True)
        with detail_right:
            if module["demo"]:
                st.link_button(f"Open Demo: {module['name']}", module["demo"], use_container_width=True)
            else:
                st.caption("Public demo not available.")

with proof_tab:
    render_section_label(st, "Flagship Governance and Proof")
    proof_left, proof_right = st.columns([1.2, 1])
    with proof_left:
        render_story_block(
            st,
            title="Governance and trust assets",
            body="The suite is reinforced by proof docs, KPI scorecards, governance artifacts, and security controls that help it present as a client-ready analytics product.",
            badge="Trust layer",
        )
    with proof_right:
        st.markdown("- Use case: `docs/showcase-use-case.md`")
        st.markdown("- Proof: `docs/proof.md`")
        st.markdown("- KPI scorecard: `docs/kpi-scorecard.md`")
        st.markdown("- Security: `SECURITY.md`")

render_footer(
    st,
    "Author: [LinkedIn](https://linkedin.com/in/samuelmaia-analytics) | "
    "[GitHub](https://github.com/samuelmaia-analytics)",
)
