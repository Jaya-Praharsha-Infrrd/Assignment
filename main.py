import pandas as pd

from src.analyzer import UserActivityAnalyzer

df = pd.read_csv("/home/jayapraharsha/Projects/Assignment/data/input.csv")

analyzer = UserActivityAnalyzer(df)
print(analyzer.average_session_duration_per_user(), "\n")
print(analyzer.average_session_duration_per_user(), "\n")
print(analyzer.total_users(), "\n")
print(analyzer.total_sessions_per_user(), "\n")
print(analyzer.most_common_activity_type(), "\n")
