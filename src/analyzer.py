"""
User Activity Analysis Module.

This module provides the UserActivityAnalyzer class, which processes user session
data to extract key performance indicators (KPIs) such as usage frequency,
session length, and common behaviors.
"""

import pandas as pd
from src.logging.logger import LoggerSingleton


class UserActivityAnalyzer:
    """
    A class used to perform statistical analysis on user activity DataFrames.

    Attributes:
        df (pd.DataFrame): The cleaned and normalized activity dataset.
        logger (logging.Logger): Logger instance for tracking calculation steps.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the analyzer with a copy of the provided DataFrame.

        Args:
            df (pd.DataFrame): The raw input data containing columns like
                'user_id', 'username', 'session_duration', and 'activity_type'.
        """
        self.logger = LoggerSingleton.get_logger(self.__class__.__name__)
        self.df = df.copy()
        self._prepare_dataframe()

    def _prepare_dataframe(self) -> None:
        """
        Clean and normalize dataframe for analytics.

        Converts 'login_date' to datetime objects and 'session_duration'
        to numeric types, coercing errors to NaN.
        """
        if "login_date" in self.df.columns:
            self.df["login_date"] = pd.to_datetime(
                self.df["login_date"], errors="coerce"
            )

        if "session_duration" in self.df.columns:
            self.df["session_duration"] = pd.to_numeric(
                self.df["session_duration"], errors="coerce"
            )

    def total_users(self) -> int:
        """
        Calculates the count of unique user IDs in the dataset.

        Returns:
            int: The number of unique users. Returns 0 if column is missing.
        """
        try:
            total = self.df["user_id"].nunique()
            self.logger.info(f"Total unique users: {total}")
            return total
        except KeyError:
            self.logger.error("Column 'user_id' not found in DataFrame")
            return 0

    def total_sessions_per_user(self) -> pd.Series:
        """
        Counts the total number of activity records associated with each username.

        Returns:
            pd.Series: A series indexed by username with session counts.
        """
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
        """
        Calculates the mean session duration for each user.

        Rows with non-numeric or missing durations are excluded from calculation.

        Returns:
            pd.Series: A series indexed by username with average session lengths.
        """
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
        """
        Identifies the most frequently occurring activity in the dataset.

        Returns:
            str | None: The most common activity type string, or None if data is empty.
        """
        try:
            common_activity = self.df["activity_type"].mode().iloc[0]
            self.logger.info(f"Most common activity type: {common_activity}")
            return common_activity
        except (KeyError, IndexError):
            self.logger.error("Column 'activity_type' missing or empty")
            return None

    def longest_session_recorded(self) -> float | None:
        """
        Finds the maximum value in the session duration column.

        Returns:
            float | None: The highest duration value, or None if column is missing.
        """
        try:
            longest = self.df["session_duration"].max()
            self.logger.info(f"Longest session recorded: {longest}")
            return longest
        except KeyError:
            self.logger.error("Column 'session_duration' not found")
            return None
