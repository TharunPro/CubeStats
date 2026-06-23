import streamlit as st
import matplotlib.pyplot as plt
from utils.loader import load_solves
from utils.stats import personal_best, rolling_average, format_time

st.set_page_config(page_title="CubeStats", page_icon="⚡", layout= "wide")

if "file" not in st.session_state:
    st.warning("Upload a csTimer file first.")
    st.stop()

    
df = load_solves(st.session_state["file"])

st.title("Progression")
# Improvement (first 5 vs last 5)

first_avg = df["seconds"].head(5).mean()
last_avg = df["seconds"].tail(5).mean()
improvement = first_avg - last_avg

st.metric("Improvement (first 5 vs last 5)", format_time(abs(improvement)), 
          delta=f"{improvement:.2f}s faster" if improvement > 0 else f"{abs(improvement):.2f}s slower")

# Average per day

avg_per_day = df.groupby(df["date"].dt.date)["seconds"].mean().mean()

st.metric("Your average per day", format_time(avg_per_day))

# Expected Comp Average

all_ao5 = df["seconds"].rolling(5).mean()

st.metric("Expected Competition Average", format_time(all_ao5.mean()))

# Graph of solves over time with rolling averages

st.caption("Your solve times over time with rolling averages.")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, df["seconds"], alpha=0.3, color="gray", linewidth=0.8, label="Single")
ax.plot(df.index, rolling_average(df, 5),  color="#E8593C", linewidth=1.5, label="Ao5")
ax.plot(df.index, rolling_average(df, 12), color="#3B8BD4", linewidth=1.5, label="Ao12")
ax.axhline(personal_best(df), linestyle="--", color="gold", linewidth=1, label="PB")
ax.set_xlabel("Solve number")
ax.set_ylabel("Time (seconds)")
ax.legend()
st.pyplot(fig)
plt.close(fig)

