import streamlit as st
from datetime import datetime, timedelta
import json
import os

# Constants
REFERENCE_TIMES = {
    "games": 60,
    "entertainment": 90,
    "YouTube": 60,
    "SNS": 90
}
WEEKLY_LIMITS = {k: v * 7 for k, v in REFERENCE_TIMES.items()}
ALL_CATEGORIES = ["education", "games", "entertainment", "YouTube", "SNS", "message"]
DATA_FILE = "usage_data.json"

# Load and save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

usage_history = load_data()

# Sidebar - Navigation
st.sidebar.title("📱 Mobile Time Manager")
page = st.sidebar.radio("Go to", [
    "📆 Weekly Calendar Sheet",
    "📝 Enter Daily Usage",
    "⚠️ Check Daily Warnings",
    "📊 Daily Summary",
    "📅 Weekly Summary",
    "⏳ Remaining Time Today"
])

# 1. Weekly Calendar Sheet
if page == "📆 Weekly Calendar Sheet":
    st.header("📆 Weekly Calendar Sheet (Last 7 Days)")
    today = datetime.now()
    last_7_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    table = []
    for date in last_7_days:
        row = {"Date": date}
        for category in ALL_CATEGORIES:
            row[category] = usage_history.get(date, {}).get(category, 0)
        table.append(row)

    st.dataframe(table, use_container_width=True)

# 2. Enter Usage
elif page == "📝 Enter Daily Usage":
    st.header("📝 Enter Daily Usage")

    date = st.date_input("Select a date", datetime.now()).strftime("%Y-%m-%d")
    if date not in usage_history:
        usage_history[date] = {}

    for category in ALL_CATEGORIES:
        usage = st.number_input(f"{category.capitalize()} (minutes)", min_value=0, step=1, key=category)
        usage_history[date][category] = usage

    if st.button("✅ Save Usage"):
        save_data(usage_history)
        st.success(f"Saved usage for {date}!")

# 3. Check Warnings
elif page == "⚠️ Check Daily Warnings":
    st.header("⚠️ Daily Usage Check")
    date = st.date_input("Select a date to check", datetime.now()).strftime("%Y-%m-%d")

    if date not in usage_history:
        st.warning("No data for selected date.")
    else:
        for category in ALL_CATEGORIES:
            used = usage_history[date].get(category, 0)
            if category in REFERENCE_TIMES:
                limit = REFERENCE_TIMES[category]
                if used > limit:
                    st.error(f"⚠️ {category}: {used} min (limit: {limit}) — Overuse!")
                else:
                    st.success(f"✅ {category}: {used} min (limit: {limit})")
            else:
                st.info(f"ℹ️ {category}: {used} min (no limit)")

# 4. Daily Summary
elif page == "📊 Daily Summary":
    st.header("📊 Daily Usage Summary")
    for date in sorted(usage_history.keys()):
        with st.expander(f"📅 {date}"):
            for category, minutes in usage_history[date].items():
                st.write(f"- **{category}**: {minutes} min")

# 5. Weekly Summary
elif page == "📅 Weekly Summary":
    st.header("📅 Weekly Summary (This Week)")
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())

    weekly_total = {cat: 0 for cat in ALL_CATEGORIES}
    for date_str, data in usage_history.items():
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if start_of_week <= date_obj <= today:
                for category in ALL_CATEGORIES:
                    weekly_total[category] += data.get(category, 0)
        except:
            continue

    for category in ALL_CATEGORIES:
        used = weekly_total[category]
        if category in WEEKLY_LIMITS:
            limit = WEEKLY_LIMITS[category]
            if used > limit:
                st.error(f"⚠️ {category}: {used} min (limit: {limit}) — Overuse!")
            else:
                st.success(f"✅ {category}: {used} min (limit: {limit})")
        else:
            st.info(f"ℹ️ {category}: {used} min (no weekly limit)")

# 6. Remaining Time
elif page == "⏳ Remaining Time Today":
    st.header("⏳ Remaining Time (Today)")
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_data = usage_history.get(today_str, {})
    
    for category in ALL_CATEGORIES:
        used = today_data.get(category, 0)
        if category in REFERENCE_TIMES:
            remaining = max(0, REFERENCE_TIMES[category] - used)
            st.write(f"🕓 {category}: {remaining} min remaining (used: {used})")
        else:
            st.write(f"ℹ️ {category}: {used} min (no limit)")
