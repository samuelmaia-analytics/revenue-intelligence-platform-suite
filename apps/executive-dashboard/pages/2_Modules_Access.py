from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Modules Access", layout="wide")

if st.button("← Back to Home"):
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
    },
    {
        "name": "Churn Prediction",
        "path": "modules/churn-prediction",
        "role": "Churn modeling, orchestration patterns, ML tracking",
        "demo": "",
    },
    {
        "name": "Amazon Sales Analysis",
        "path": "modules/amazon-sales-analysis",
        "role": "Sales leakage and KPI analytics with contracts and CI patterns",
        "demo": "",
    },
    {
        "name": "Analise Vendas Python",
        "path": "modules/analise-vendas-python",
        "role": "Operational sales analytics and processed star-style datasets",
        "demo": "https://analys-vendas-python.streamlit.app/",
    },
    {
        "name": "Data Senior Analytics",
        "path": "modules/data-senior-analytics",
        "role": "Business-focused analytics pipeline and dashboard outputs",
        "demo": "https://data-analytics-sr.streamlit.app",
    },
]

for module in modules:
    module_abs = ROOT / module["path"]
    st.subheader(module["name"])
    st.write(module["role"])
    st.code(str(module_abs), language="text")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- Local path: `{module['path']}`")
    with col2:
        if module["demo"]:
            st.markdown(f"- Public demo: {module['demo']}")
        else:
            st.markdown("- Public demo: not published")
    st.markdown("---")

st.subheader("Flagship Governance and Proof")
st.markdown("- Use case: `docs/showcase-use-case.md`")
st.markdown("- Proof: `docs/proof.md`")
st.markdown("- KPI scorecard: `docs/kpi-scorecard.md`")
st.markdown("- Security: `SECURITY.md`")
