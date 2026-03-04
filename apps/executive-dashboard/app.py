import streamlit as st

st.set_page_config(
    page_title="Revenue-Intelligence-Platform-Suite",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Revenue-Intelligence-Platform-Suite")
st.caption("Unified portal for Revenue + Retention decision systems.")

st.markdown(
    """
### What You Can Access Here
- Executive KPI board with real integrated module data
- Direct links to all module repositories inside the monorepo
- Direct links to available public demos
"""
)

st.info(
    "Use the sidebar pages or the buttons below to open `Executive KPI Board` and `Modules Access`."
)

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
        "https://analys-vendas-python.streamlit.app/",
        use_container_width=True,
    )

st.markdown("---")
st.subheader("Purpose")
st.write(
    "This flagship app is the access layer that unifies all modules into one platform "
    "experience, with business decision support as the core outcome."
)
