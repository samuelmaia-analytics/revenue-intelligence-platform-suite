from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Modules Access", layout="wide")

if st.button("Voltar para Revenue-Intelligence-Platform-Suite"):
    st.switch_page("app.py")

with st.sidebar:
    if st.button("Home: Revenue-Intelligence-Platform-Suite"):
        st.switch_page("app.py")

ROOT = Path(__file__).resolve().parents[3]

st.title("Modules Access")
st.caption("Single place to access all integrated repositories and demos.")

modules = [
    {
        "name": "Revenue Intelligence",
        "path": "modules/revenue-intelligence",
        "role": "Revenue analytics, scoring, recommendations, executive assets",
        "demo": "https://revenue-intelligence-platform.streamlit.app/",
        "repo": "https://github.com/samuelmaia-data-analyst/Revenue-Intelligence-Platform-End-to-End-Analytics-ML-System",
    },
    {
        "name": "Churn Prediction",
        "path": "modules/churn-prediction",
        "role": "Churn modeling, orchestration patterns, ML tracking",
        "demo": "",
        "repo": "https://github.com/samuelmaia-data-analyst/churn-prediction",
    },
    {
        "name": "Amazon Sales Analysis",
        "path": "modules/amazon-sales-analysis",
        "role": "Sales leakage and KPI analytics with contracts and CI patterns",
        "demo": "",
        "repo": "https://github.com/samuelmaia-data-analyst/amazon-sales-analysis",
    },
    {
        "name": "Analise Vendas Python",
        "path": "modules/analise-vendas-python",
        "role": "Operational sales analytics and processed star-style datasets",
        "demo": "https://analys-vendas-python.streamlit.app/",
        "repo": "https://github.com/samuelmaia-data-analyst/analise-vendas-python",
    },
    {
        "name": "Data Senior Analytics",
        "path": "modules/data-senior-analytics",
        "role": "Business-focused analytics pipeline and dashboard outputs",
        "demo": "https://data-analytics-sr.streamlit.app",
        "repo": "https://github.com/samuelmaia-data-analyst/data-senior-analytics",
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
        st.markdown(f"- Source repo: [open repository]({module['repo']})")
    with col3:
        if module["demo"]:
            st.markdown(f"- Public demo: [open app]({module['demo']})")
    if not module_exists:
        st.caption("Module path not found in current deployment.")
    st.markdown("---")

st.subheader("Flagship Governance and Proof")
st.markdown("- Use case: `docs/showcase-use-case.md`")
st.markdown("- Proof: `docs/proof.md`")
st.markdown("- KPI scorecard: `docs/kpi-scorecard.md`")
st.markdown("- Security: `SECURITY.md`")
