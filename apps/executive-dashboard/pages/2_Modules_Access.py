from pathlib import Path

import streamlit as st


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "platform_connectors").exists():
            return candidate
    return Path(__file__).resolve().parents[3]


st.set_page_config(page_title="Modules Access", layout="wide")

if st.button("Voltar para Revenue-Intelligence-Platform-Suite"):
    st.switch_page("app.py")

with st.sidebar:
    if st.button("Home: Revenue-Intelligence-Platform-Suite"):
        st.switch_page("app.py")

ROOT = _find_repo_root(Path(__file__).resolve())

st.title("Modules Access")
st.caption("Single place to access all integrated repositories and demos.")

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
        "demo": "https://analys-vendas-python.streamlit.app/",
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

for module in modules:
    module_exists = (ROOT / module["path"]).exists()
    st.subheader(module["name"])
    st.write(module["role"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"- Monorepo path: `{module['path']}`")
    with col2:
        st.write("- Source repo")
        st.link_button("Open Repository", module["repo"], use_container_width=True)
    with col3:
        st.write("- Public demo")
        if module["demo"]:
            st.link_button("Open App", module["demo"], use_container_width=True)
        else:
            st.caption("Public demo not available.")
    if not module_exists:
        st.caption("Module path not found in current deployment.")
    st.markdown("---")

st.subheader("Flagship Governance and Proof")
st.markdown("- Use case: `docs/showcase-use-case.md`")
st.markdown("- Proof: `docs/proof.md`")
st.markdown("- KPI scorecard: `docs/kpi-scorecard.md`")
st.markdown("- Security: `SECURITY.md`")
