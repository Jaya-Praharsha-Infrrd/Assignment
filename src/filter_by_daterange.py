"""
Session Log Filter Utility.

This script allows users to filter login session data from a CSV file based on a
specific date range and optionally export the results to a new file.
"""

import pandas as pd
import argparse
import sys


def validate_date(date_str):
    """Checks if the date string is a valid format."""
    try:
        return pd.to_datetime(date_str, errors="raise")
    except (ValueError, TypeError):
        print(f"Error: '{date_str}' is not a valid date. Please use YYYY-MM-DD.")
        sys.exit(1)


def filter_by_date_range(file_path, start_date_str, end_date_str, export=None):
    """
    Filters a CSV file for records within a specified date range with error handling.
    """
    # 1. Validate Date Formats first
    start_dt = validate_date(start_date_str)
    end_dt = validate_date(end_date_str)

    if start_dt > end_dt:
        print("Error: Start date must be before or equal to end date.")
        sys.exit(1)

    # 2. Attempt to read the file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # 3. Check for required column
    if "login_date" not in df.columns:
        print("Error: The CSV file is missing the required 'login_date' column.")
        sys.exit(1)

    # 4. Process and Filter
    try:
        # Convert column to datetime, forcing unparseable dates to NaT (Not a Time)
        df["login_date"] = pd.to_datetime(df["login_date"], errors="coerce")

        # Filter rows where login_date is within range and not NaT
        mask = (df["login_date"] >= start_dt) & (df["login_date"] <= end_dt)
        result = df[mask].copy()

        if result.empty:
            print(f"No sessions found between {start_date_str} and {end_date_str}.")
        else:
            # Format dates back to string for cleaner console printing
            result["login_date"] = result["login_date"].dt.strftime("%Y-%m-%d")
            print(result.to_string(index=False))

            if export:
                if not (export.endswith(".csv") or export.endswith(".txt")):
                    print("Error: Export file must be .csv or .txt")
                    sys.exit(1)

                try:
                    sep = "," if export.endswith(".csv") else "\t"
                    result.to_csv(export, index=False, sep=sep)
                    print(f"Results exported to {export}")
                except Exception as e:
                    print(f"Error exporting file: {e}")

    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter sessions by date range")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("end_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--export", help="Optional file to export results (csv or txt)")
    args = parser.parse_args()

    filter_by_date_range(args.file, args.start_date, args.end_date, args.export)
