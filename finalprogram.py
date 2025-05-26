import streamlit as st
from datetime import datetime, timedelta

# --- Setup ---

REFERENCE_TIMES = {
    "games": 60,
    "entertainment": 90,
    "YouTube": 60,
    "SNS": 90
}

WEEKLY_LIMITS = {cat: REFERENCE_TIMES[cat] * 7 for cat in REFERENCE_TIMES}
ALL_CATEGORIES = ["education", "games", "entertainment", "YouTube", "SNS", "message"]

if "usage_history" not in st.session_state:
    st.session_state.usage_history = {}

# --- Helper Functions ---

def enter_usage(date, input_data):
    history = st.session_state.usage_history
    if date not in history:
        history[date] = {}
    for cat in ALL_CATEGORIES:
        history[date][cat] = input_data.get(cat, 0)

def get_week_dates():
    today = datetime.now()
    start = today - timedelta(days=today.weekday())  # Monday
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def get_last_7_days():
    today = datetime.now()
    return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

# --- UI ---

st.title("📱 Mobile Time Manager")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Weekly Calendar", "📝 Enter Usage", "📊 Daily Summary", "📈 Weekly Summary"])

# --- Tab 1: Weekly Calendar ---
with tab1:
    st.header("📆 Weekly Calendar Sheet (Last 7 Days)")
    last_7_days = get_last_7_days()

    table = []
    for date in last_7_days:
        row = [date]
        for cat in ALL_CATEGORIES:
            value = st.session_state.usage_history.get(date, {}).get(cat, 0)
            row.append(value)
        table.append(row)

    st.table(
        [["Date"] + ALL_CATEGORIES] + table
    )

# --- Tab 2: Enter Usage ---
with tab2:
    st.header("📝 Enter Daily Usage")

    date = st.date_input("Select a date", value=datetime.now()).strftime("%Y-%m-%d")

    input_minutes = {}
    for cat in ALL_CATEGORIES:
        input_minutes[cat] = st.number_input(f"{cat.capitalize()} (min)", min_value=0, value=0, step=5)

    if st.button("💾 Save Usage"):
        enter_usage(date, input_minutes)
        st.success(f"Saved usage for {date}.")

# --- Tab 3: Daily Summary ---
with tab3:
    st.header("📊 Daily Summary")

    if not st.session_state.usage_history:
        st.info("No usage data entered yet.")
    else:
        for date in sorted(st.session_state.usage_history.keys()):
            st.subheader(f"📅 {date}")
            for cat, min_used in st.session_state.usage_history[date].items():
                if cat in REFERENCE_TIMES:
                    limit = REFERENCE_TIMES[cat]
                    if min_used > limit:
                        st.warning(f"⚠️ {cat}: {min_used} min (limit: {limit}) — Overuse!")
                    else:
                        st.success(f"{cat}: {min_used} min (limit: {limit})")
                else:
                    st.info(f"{cat}: {min_used} min (no limit)")

# --- Tab 4: Weekly Summary ---
with tab4:
    st.header("📈 Weekly Summary (This Week)")

    week_dates = get_week_dates()
    totals = {cat: 0 for cat in ALL_CATEGORIES}

    for date in week_dates:
        daily_data = st.session_state.usage_history.get(date, {})
        for cat in ALL_CATEGORIES:
            totals[cat] += daily_data.get(cat, 0)

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
