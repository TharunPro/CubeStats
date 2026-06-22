import streamlit as st

st.set_page_config(page_title="CubeStats", page_icon="⚡", layout= "wide")
st.title("CubeStats")
st.caption("Get insights into your cubing performance with your csTimer data. Upload your solves and explore your stats, progression, and insights.")

uploaded = st.file_uploader("Upload csTimer CSV", type=["csv"])
if uploaded:
    st.session_state["file"] = uploaded.read()
    st.success("File loaded successfully! - navigate to a page using the sidebar.")


pages = {
    "My Cubing Stats": [
        st.Page("pages/overview.py", title="Overview", default=True),
        st.Page("pages/progression.py", title="Progression"),
        st.Page("pages/insights.py", title="Insights"),
    ]
}
    
pg = st.navigation(pages)
pg.run()

