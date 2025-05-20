
from datetime import datetime, timedelta

# Categories with daily limits (in minutes)
REFERENCE_TIMES = {
    "education": 300,
    "games": 60,
    "entertainment": 100,
    "SNS": 60
}

# Weekly limits: 7 times the daily limits
WEEKLY_LIMITS = {
    category: REFERENCE_TIMES[category] * 7
    for category in REFERENCE_TIMES
}

# All categories (some with no limit)
ALL_CATEGORIES = ["education", "games", "entertainment", "SNS"]

# Dictionary to store user input data by date
usage_history = {}

# Function to enter usage time per category
def enter_usage():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    if date not in usage_history:
        usage_history[date] = {}

    print(f"\nEntering usage for {date}:")
    for category in ALL_CATEGORIES:
        try:
            minutes = int(input(f"  {category.capitalize()} usage (min): "))
            usage_history[date][category] = minutes
        except ValueError:
            print("  ❌ Invalid input. Please enter a number.")
            usage_history[date][category] = 0

# Function to check if user exceeded daily time limits
def check_warnings(date):
    print(f"\n🔍 Checking usage for {date}:")
    for category in ALL_CATEGORIES:
        used = usage_history[date].get(category, 0)
        if category in REFERENCE_TIMES:
            limit = REFERENCE_TIMES[category]
            if used > limit:
                print(f"⚠️ {category}: {used} min (limit: {limit}) — Overuse!")
            else:
                print(f"✅ {category}: {used} min (limit: {limit})")
        else:
            print(f"ℹ️ {category}: {used} min (no time limit)")

# Function to show all daily entries
def summary():
    print("\n📊 Daily Usage Summary:")
    for date in sorted(usage_history.keys()):
        print(f"  {date}:")
        for category, minutes in usage_history[date].items():
            print(f"    {category}: {minutes} min")

# Function to show weekly summary and check against limits
def weekly_summary():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday

    weekly_total = {cat: 0 for cat in ALL_CATEGORIES}

    for date_str in usage_history:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if start_of_week <= date_obj <= today:
            for category in ALL_CATEGORIES:
                weekly_total[category] += usage_history[date_str].get(category, 0)

    print("\n📅 Weekly Usage Summary (This Week):")
    for category in ALL_CATEGORIES:
        used = weekly_total[category]
        if category in WEEKLY_LIMITS:
            limit = WEEKLY_LIMITS[category]
            if used > limit:
                print(f"⚠️ {category}: {used} min (limit: {limit}) — Overuse!")
            else:
                print(f"✅ {category}: {used} min (limit: {limit})")
        else:
            print(f"ℹ️ {category}: {used} min (no weekly limit)")

# Function to display 7-day calendar sheet
def calendar_sheet():
    print("\n📆 Weekly Calendar Sheet (Last 7 Days)\n")
    today = datetime.now()
    last_7_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    # Header
    header = f"{'Date':<12} | " + " | ".join(f"{cat[:4]:>4}" for cat in ALL_CATEGORIES)
    print(header)
    print("-" * len(header))

    # Each row: a day of data
    for date in last_7_days:
        row = f"{date:<12} | "
        for category in ALL_CATEGORIES:
            value = usage_history.get(date, {}).get(category, 0)
            row += f"{value:>4} | "
        print(row)

# Main function for menu system
def main():
    while True:
        print("\n--- 📱 Mobile Time Manager ---")
        print("1. 📆 Show weekly calendar sheet")
        print("2. 📝 Enter daily usage")
        print("3. ⚠️ Check today's warnings")
        print("4. 📊 Show daily summary")
        print("5. 📅 Show weekly summary")
        print("6. ❌ Exit") 
        choice = input("Select an option: ")

        if choice == "1":
            calendar_sheet()
        elif choice == "2":
            enter_usage()
        elif choice == "3":
            today = datetime.now().strftime("%Y-%m-%d")
            if today in usage_history:
                check_warnings(today)
            else:
                print("❗ No usage entered for today.")
        elif choice == "4":
            summary()
        elif choice == "5":
            weekly_summary()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    main()