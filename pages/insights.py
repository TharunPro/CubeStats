import streamlit as st
import matplotlib.pyplot as plt
from utils.loader import load_solves
from utils.stats import format_time, format_hour, time_of_day_performance
from utils.ui import analytics_card

st.set_page_config(page_title="CubeStats", page_icon="⚡", layout= "wide")


if "file" not in st.session_state:
    st.warning("Upload a csTimer file first.")
    st.stop()

st.title("Insights")
st.caption("A deeper look at solve distribution and time-of-day performance.")

df = load_solves(st.session_state["file"])

# Time of Day Performance
hourly_stats, best_hour_row = time_of_day_performance(df)

if best_hour_row is not None:
    best_hour = int(best_hour_row["hour"])
    summary_hour = format_hour(best_hour)
    summary_details = [
        f"Average solve: {format_time(float(best_hour_row['average_solve']))}",
        f"Median solve: {format_time(float(best_hour_row['median_solve']))}",
        f"Best solve: {format_time(float(best_hour_row['best_solve']))}",
        f"Consistency: {format_time(float(best_hour_row['consistency']))}",
        f"Solve count: {int(best_hour_row['solve_count'])}",
    ]
else:
    best_hour = None
    summary_hour = "No hour with 5+ solves"
    summary_details = [
        "Add more solves in a single hour to compare time-of-day performance.",
    ]

analytics_card("Best Time of Day", summary_hour, summary_details, "#3B8BD4")
st.divider()

# Total time spent solving
total_time = df["seconds"].sum()
st.metric("Total time spent solving", f"{format_time(total_time)}s")
st.divider()

# Average solve time
avg = df["seconds"].mean()
st.metric("Session Average", f"{format_time(avg)}s")
st.divider()

# Most active day
most_active = df.groupby(df["date"].dt.date).size().idxmax()
st.metric("Most active day", str(most_active))
st.divider()

# Most solves in a day
best_day_count = df.groupby(df["date"].dt.date).size().max()
st.metric("Most solves in a day", str(best_day_count))
st.divider()

# Consistency Score
std = df["seconds"].std()
mean = df["seconds"].mean()
score = max(0, 100 - (std / mean) * 100)

st.metric("Consistency Score", f"{score:.0f}/100")

if score >= 80:
    st.badge("Very Consistent!", color="green")
elif score >= 60:
    st.badge("Consistent", color="yellow")
else:
    st.badge("Keep Practicing!", color="red")
st.divider()
