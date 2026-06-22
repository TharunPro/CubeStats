import streamlit as st
from utils.loader import load_solves
from utils.stats import personal_best, best_ao, format_time
from utils.ui import metric_card

st.set_page_config(page_title="CubeStats", page_icon="⚡", layout= "wide")

if "file" not in st.session_state:
    st.warning("Upload a csTimer file first.")
    st.stop()

st.title("Overview")

df = load_solves(st.session_state["file"])

col1, col2 = st.columns(2)

with col1:
    metric_card("Total solves", len(df), "#3B8BD4")
    st.write("")
    metric_card("Personal best", format_time(personal_best(df)),  "#E8593C")

    pb = personal_best(df)
with col2:
    metric_card("Best Ao5", format_time(best_ao(df, 5)),  "#2ECC71")
    st.write("")
    metric_card("Best Ao12", format_time(best_ao(df, 12)), "#F39C12")

