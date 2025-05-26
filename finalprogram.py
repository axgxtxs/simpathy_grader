import streamlit as st
from datetime import datetime, timedelta

# --- Configuration ---
REFERENCE_TIMES = {
    "games": 60,
    "entertainment": 90,
    "YouTube": 60,
    "SNS": 90
}
WEEKLY_LIMITS = {cat: val * 7 for cat, val in REFERENCE_TIMES.items()}
ALL_CATEGORIES = ["education", "games", "entertainment", "YouTube", "SNS", "message"]

# --- Session State Setup ---
if "usage_history" not in st.session_state:
    st.session_state.usage_history = {}

# --- Helpers ---

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def get_week_range():
    today = datetime.now()
    start = today - timedelta(days=today.weekday())  # Monday
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def get_last_7_days():
    today = datetime.now()
    return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

def enter_usage(date, category_inputs):
    if date not in st.session_state.usage_history:
        st.session_state.usage_history[date] = {}
    for cat in ALL_CATEGORIES:
        st.session_state.usage_history[date][cat] = category_inputs.get(cat, 0)

def get_weekly_totals():
    week_dates = get_week_range()
    totals = {cat: 0 for cat in ALL_CATEGORIES}
    for date in week_dates:
        daily_data = st.session_state.usage_history.get(date, {})
        for cat in ALL_CATEGORIES:
            totals[cat] += daily_data.get(cat, 0)
    return totals

# --- UI ---
st.title("📱 Mobile Time Tracker (Private)")

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Enter Usage",
    "📊 Daily Summary",
    "📅 Weekly Calendar",
    "📈 Weekly Summary"
])

# --- Tab 1: Enter Daily Usage ---
with tab1:
    st.subheader("📝 Enter Daily Usage")
    date = st.date_input("Select Date", value=datetime.now()).strftime("%Y-%m-%d")

    category_inputs = {}
    for cat in ALL_CATEGORIES:
        category_inputs[cat] = st.number_input(
            f"{cat.capitalize()} (minutes)",
            min_value=0,
            step=5,
            key=f"{date}-{cat}"
        )

    if st.button("💾 Save"):
        enter_usage(date, category_inputs)
        st.success(f"Saved usage for {date}")

# --- Tab 2: Daily Summary ---
with tab2:
    st.subheader("📊 Daily Summary")

    if not st.session_state.usage_history:
        st.info("No usage data entered yet.")
    else:
        for date in sorted(st.session_state.usage_history.keys()):
            st.markdown(f"### {date}")
            for cat in ALL_CATEGORIES:
                used = st.session_state.usage_history[date].get(cat, 0)
                if cat in REFERENCE_TIMES:
                    limit = REFERENCE_TIMES[cat]
                    if used > limit:
                        st.warning(f"⚠️ {cat}: {used} min (limit: {limit})")
                    else:
                        st.success(f"{cat}: {used} min (limit: {limit})")
                else:
                    st.info(f"{cat}: {used} min (no limit)")

# --- Tab 3: Weekly Calendar ---
with tab3:
    st.subheader("📅 Weekly Calendar (Last 7 Days)")
    dates = get_last_7_days()

    header = ["Date"] + ALL_CATEGORIES
    table = []
    for date in dates:
        row = [date]
        for cat in ALL_CATEGORIES:
            val = st.session_state.usage_history.get(date, {}).get(cat, 0)
            row.append(val)
        table.append(row)

    st.table([header] + table)

# --- Tab 4: Weekly Summary ---
with tab4:
    st.subheader("📈 Weekly Summary (This Week)")
    totals = get_weekly_totals()

    for cat in ALL_CATEGORIES:
        used = totals[cat]
        if cat in WEEKLY_LIMITS:
            limit = WEEKLY_LIMITS[cat]
            if used > limit:
                st.warning(f"⚠️ {cat}: {used} min (limit: {limit}) — Overuse!")
            else:
                st.success(f"{cat}: {used} min (limit: {limit})")
        else:
            st.info(f"{cat}: {used} min (no weekly limit)")
