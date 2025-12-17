import pandas as pd
from src.logging.logger import LoggerSingleton


class UserActivityAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.logger = LoggerSingleton.get_logger(self.__class__.__name__)
        self.df = df.copy()
        self._prepare_dataframe()

    def _prepare_dataframe(self) -> None:
        """Clean and normalize dataframe for analytics."""
        if "login_date" in self.df.columns:
            self.df["login_date"] = pd.to_datetime(
                self.df["login_date"], errors="coerce"
            )

        if "session_duration" in self.df.columns:
            self.df["session_duration"] = pd.to_numeric(
                self.df["session_duration"], errors="coerce"
            )

    def total_users(self) -> int:
        try:
            total = self.df["user_id"].nunique()
            self.logger.info(f"Total unique users: {total}")
            return total
        except KeyError:
            self.logger.error("Column 'user_id' not found in DataFrame")
            return 0

    def total_sessions_per_user(self) -> pd.Series:
        try:
            sessions = self.df.groupby("username").size()
            self.logger.info(
                f"Calculated total sessions per user ({len(sessions)} users)"
            )
            return sessions
        except KeyError:
            self.logger.error("Column 'username' not found in DataFrame")
            return pd.Series(dtype=int)

    def average_session_duration_per_user(self) -> pd.Series:
        try:
            avg_duration = (
                self.df.dropna(subset=["session_duration"])
                .groupby("username")["session_duration"]
                .mean()
            )
            self.logger.info("Calculated average session duration per user")
            return avg_duration
        except KeyError as e:
            self.logger.error(f"Missing expected column(s) in DataFrame: {e}")
            return pd.Series(dtype=float)

    def most_common_activity_type(self) -> str | None:
        try:
            common_activity = self.df["activity_type"].mode().iloc[0]
            self.logger.info(f"Most common activity type: {common_activity}")
            return common_activity
        except (KeyError, IndexError):
            self.logger.error("Column 'activity_type' missing or empty")
            return None

    def longest_session_recorded(self) -> float | None:
        try:
            longest = self.df["session_duration"].max()
            self.logger.info(f"Longest session recorded: {longest}")
            return longest
        except KeyError:
            self.logger.error("Column 'session_duration' not found")
            return None
