"""
Session Duration Filter Utility.

This script processes a CSV file to identify and extract user sessions that
meet or exceed a specified duration threshold.
"""

import pandas as pd
import argparse
import sys


def filter_by_duration(file_path, min_duration, export=None):
    """
    Filters a CSV file for sessions that lasted a minimum amount of time.

    Args:
        file_path (str): The path to the source CSV file.
        min_duration (int or float): The minimum threshold for session duration.
        export (str, optional): The filename to save results to (.csv or .txt).
            Defaults to None.

    Returns:
        None: Prints the filtered DataFrame to the console or saves to a file.

    Raises:
        SystemExit: If the input file cannot be read or is missing required columns.
    """
    # Validate that duration isn't a nonsensical negative number
    if min_duration < 0:
        print("Error: Minimum duration cannot be negative.")
        sys.exit(1)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Check if the required column exists
    if "session_duration" not in df.columns:
        print("Error: CSV must contain a 'session_duration' column.")
        sys.exit(1)

    # Convert session_duration to numeric, coerce errors to NaN
    df["session_duration"] = pd.to_numeric(df["session_duration"], errors="coerce")

    # Drop rows where session_duration could not be converted to a number
    result = df[df["session_duration"] >= min_duration]

    if result.empty:
        print(f"No sessions found with duration >= {min_duration}.")
    else:
        print(result.to_string(index=False))
        if export:
            try:
                sep = "," if export.endswith(".csv") else "\t"
                result.to_csv(export, index=False, sep=sep)
                print(f"Results exported to {export}")
            except Exception as e:
                print(f"Error exporting file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter sessions by minimum duration")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("duration", type=int, help="Minimum session duration")
    parser.add_argument("--export", help="Optional file to export results (csv or txt)")
    args = parser.parse_args()

    filter_by_duration(args.file, args.duration, args.export)
