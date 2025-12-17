import pandas as pd
from pathlib import Path
from src.analyzer import UserActivityAnalyzer


BASE_DIR = Path(__file__).resolve().parent

data_path = BASE_DIR / "data" / "input.csv"

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    print(f"Error: Could not find the file at {data_path}")
    exit(1)

analyzer = UserActivityAnalyzer(df)


print(
    "Average Session Duration Per User:\n",
    analyzer.average_session_duration_per_user(),
    "\n",
)
print("Total Users:", analyzer.total_users(), "\n")
print("Total Sessions Per User:\n", analyzer.total_sessions_per_user(), "\n")
print("Most Common Activity Type:", analyzer.most_common_activity_type(), "\n")
print("Longest Session Recorded", analyzer.longest_session_recorded(), "\n")
