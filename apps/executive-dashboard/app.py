import sys
from pathlib import Path

import pandas as pd
import streamlit as st


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

st.set_page_config(
    page_title="Revenue-Intelligence-Platform-Suite",
    layout="wide",
    initial_sidebar_state="expanded",
)

identity = enforce_streamlit_sso(st)

st.title("Revenue-Intelligence-Platform-Suite")
st.caption("Executive-grade analytics platform for recurring revenue, retention, and commercial governance.")
st.warning(
    "Copyright Samuel Maia. This platform, its executive assets, and generated materials are proprietary. "
    "Public app access does not grant rights to reuse, copy, or redistribute the codebase or commercial assets."
)

SHOWCASE_DIR = ROOT / "reports" / "showcase"


@st.cache_data(show_spinner=False)
def load_showcase_artifact(file_name: str) -> dict:
    artifact_path = SHOWCASE_DIR / file_name
    if not artifact_path.exists():
        return {}
    return pd.read_json(artifact_path, typ="series").to_dict()


solution_profile = load_showcase_artifact("solution_profile.json")
quality_scorecard = load_showcase_artifact("data_quality_scorecard.json")
tenant_secret_status = load_showcase_artifact("tenant_secret_status.json")
client_profiles = list_client_profiles()
brand = solution_profile.get("brand", {})
narrative = solution_profile.get("narrative", {})

if brand:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(180deg, {brand.get("hero_gradient_start", "#eef6ff")} 0%, {brand.get("hero_gradient_end", "#ffffff")} 100%);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if narrative:
    st.markdown(f"**{narrative.get('headline', '')}**")
    st.write(narrative.get("value_proposition", ""))

st.markdown(
    """
### What You Can Access Here
- Executive KPI board with real integrated module data and recommended actions
- Multi-client solution framing for SaaS, healthtech, retail, and recurring-revenue operators
- Direct links to flagship demos and packaged analytics modules
"""
)

st.info(
    "Use this app as the executive landing zone: it combines commercial narrative, operating scorecards, and direct access to the flagship KPI board."
)

hero_left, hero_mid, hero_right = st.columns(3)
hero_left.metric(
    "Primary Package",
    solution_profile.get("package", {}).get("name", "Revenue Command Center"),
)
hero_mid.metric(
    "Deployment Model",
    solution_profile.get("deployment_env", "showcase").title(),
)
hero_right.metric(
    "Data Quality Score",
    f"{quality_scorecard.get('overall_score', 0):.1f}",
    delta=quality_scorecard.get("status", "not_generated").title(),
)

if tenant_secret_status:
    st.caption(
        "Tenant secrets readiness: "
        f"{tenant_secret_status.get('configured_secret_count', 0)}/"
        f"{tenant_secret_status.get('required_secret_count', 0)} configured | "
        f"ready={tenant_secret_status.get('ready', False)}"
    )

if identity.get("authenticated"):
    st.caption(f"SSO session: {identity.get('display_name')} | groups={', '.join(identity.get('groups', [])) or 'n/a'}")

st.markdown("---")
st.subheader("Client Adaptation Profiles")
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
st.dataframe(profiles_df, width="stretch", hide_index=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Primary Navigation")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Open Executive KPI Board", use_container_width=True):
            st.switch_page("pages/1_Executive_KPI_Board.py")
    with c2:
        if st.button("Open Modules Access", use_container_width=True):
            st.switch_page("pages/2_Modules_Access.py")
    st.caption("If the sidebar is collapsed, click the top-left `>` icon to expand it.")

with col2:
    st.subheader("Public Demos")
    st.link_button(
        "Revenue Intelligence Demo",
        "https://revenue-intelligence-platform.streamlit.app/",
        use_container_width=True,
    )
    st.link_button(
        "Data Senior Analytics Demo",
        "https://data-analytics-sr.streamlit.app",
        use_container_width=True,
    )
    st.link_button(
        "Sales Analytics Demo",
        "https://sales-analytics-dashboardd.streamlit.app/",
        use_container_width=True,
    )

st.markdown("---")
left, right = st.columns([1.4, 1])
with left:
    st.subheader("Why This Platform Sells")
    st.write(
        "The repository is positioned as a reusable client solution, not only a portfolio demo. "
        "It combines telemetry-backed executive KPIs, action prioritization, governance artifacts, "
        "and solution packaging that can be adapted by industry."
    )
    st.markdown(
        """
        **Who This Is For**
        - CRO, VP Revenue, Revenue Operations
        - Chief Customer Officer, VP Customer Success
        - COO, CFO, Strategy, and Executive PMO
        """
    )
with right:
    st.subheader("Commercial Outcomes")
    st.write("- Faster weekly executive decision cycles")
    st.write("- Better prioritization of revenue recovery actions")
    st.write("- Stronger governance for KPI trust and recurring service delivery")

st.markdown("---")
st.subheader("Solution Packages")
packages = pd.DataFrame(
    [
        {
            "Package": "Revenue Command Center",
            "Primary Buyer": "CRO / RevOps",
            "Outcome": "Protect recurring revenue with prioritized action playbooks",
        },
        {
            "Package": "Retention Intelligence",
            "Primary Buyer": "Customer Success Leadership",
            "Outcome": "Surface churn exposure and save-motion opportunities",
        },
        {
            "Package": "Executive KPI Governance",
            "Primary Buyer": "CEO / COO / CFO",
            "Outcome": "Standardize definitions, freshness, and decision accountability",
        },
        {
            "Package": "Commercial Performance Analytics",
            "Primary Buyer": "Sales / Commercial Ops",
            "Outcome": "Improve channel, seller, and segment performance visibility",
        },
    ]
)
st.dataframe(packages, width="stretch", hide_index=True)

st.markdown("---")
st.subheader("Executive Deliverables")
st.write(
    "The platform now produces a board-ready review pack in markdown, JSON, and HTML, plus a release evidence pack for steering committees and client reviews."
)
deliverables = pd.DataFrame(
    [
        {"Deliverable": "Executive Review Pack", "Format": "Markdown / JSON / HTML", "Use": "Board and steering review"},
        {"Deliverable": "Client Proposal Pack", "Format": "Markdown / JSON / HTML", "Use": "Commercial proposal and pitch asset"},
        {"Deliverable": "Release Evidence Pack", "Format": "tar.gz", "Use": "Quarterly proof and release artifact"},
        {"Deliverable": "Industry Demo Packs", "Format": "Per-profile folders", "Use": "Client-specific commercial demos"},
    ]
)
st.dataframe(deliverables, width="stretch", hide_index=True)

st.markdown("---")
st.caption(
    "Copyright (c) 2026 Samuel Maia. Proprietary platform. "
    "Author: [LinkedIn](https://linkedin.com/in/samuelmaia-analytics) | "
    "[GitHub](https://github.com/samuelmaia-analytics)"
)
