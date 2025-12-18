"""
User Activity Search Utility.

This script allows users to query a CSV database for records associated with
a specific username. The search is case-insensitive.
"""

import pandas as pd
import argparse
import sys


def search_by_username(file_path, username, export=None):
    """
    Searches a CSV file for records matching a specific username.

    Args:
        file_path (str): The path to the source CSV file.
        username (str): The username to filter for (case-insensitive).
        export (str, optional): Save the results to (.csv or .txt).
            Defaults to None.

    Returns:
        None

    Raises:
        SystemExit:
            If the file is unreadable or the 'username' column is missing.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Validate column presence
    if "username" not in df.columns:
        print("Error: The CSV file is missing the required 'username' column.")
        sys.exit(1)

    mask = df["username"].fillna("").str.lower() == username.lower()
    result = df[mask]

    if result.empty:
        print(f"No records found for username '{username}'.")
    else:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search user activity by username")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("username", help="Username to search")
    parser.add_argument("--export", help="Optional file to export results (csv or txt)")
    args = parser.parse_args()

    search_by_username(args.file, args.username, args.export)
