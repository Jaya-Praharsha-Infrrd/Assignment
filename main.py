import pandas as pd

from src.analyzer import UserActivityAnalyzer

df = pd.read_csv("/home/jayapraharsha/Projects/Assignment/data/input.csv")

analyzer = UserActivityAnalyzer(df)
print(analyzer.average_session_duration_per_user())
print(analyzer.most_common_activity_type())
print(analyzer.average_session_duration_per_user())
print(analyzer.total_users())
print(analyzer.total_sessions_per_user())
