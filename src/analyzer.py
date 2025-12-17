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
            return self.df["user_id"].nunique()
        except KeyError:
            self.logger.error("Column 'user_id' not found")
            return 0

    def total_sessions_per_user(self) -> pd.Series:
        try:
            return self.df.groupby("username").size()
        except KeyError:
            self.logger.error("Column 'username' not found")
            return pd.Series(dtype=int)

    def average_session_duration_per_user(self) -> pd.Series:
        try:
            return (
                self.df.dropna(subset=["session_duration"])
                .groupby("username")["session_duration"]
                .mean()
            )
        except KeyError as e:
            self.logger.error(f"Missing expected columns in DataFrame: {e}")
            return pd.Series(dtype=float)

    def most_common_activity_type(self) -> str | None:
        try:
            return self.df["activity_type"].mode().iloc[0]
        except (KeyError, IndexError):
            self.logger.error("Column 'activity_type' missing or empty")
            return None

    def longest_session_recorded(self) -> float | None:
        try:
            return self.df["session_duration"].max()
        except KeyError:
            self.logger.error("Column 'session_duration' not found")
            return None
