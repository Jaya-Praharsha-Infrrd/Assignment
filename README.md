# Assignment


---

### Installation
1. Clone the repository.
2. Ensure you have Python 3.11 installed.
3. Install dependencies:
   ```bash
   pip install pandas
    ```

## User Activity Analyzer
The UserActivityAnalyzer class is the core engine for data insights.
It provides these following functions:


1. total_users() - Number of unique users in the dataset.
2. total_sessions_per_user()- Count of sessions per username.
3. average_session_duration_per_user() - Mean session time per user.
4. most_common_activity_type() - The most frequent activity in the log.
5. longest_session_recorded() - The maximum duration found.


## Scripts


### 1. Session Date Filter
Filters login records based on a specific date range. It validates date inputs and ensures the start date precedes the end date.

```bash
python -m src.filter_by_daterange.py <file_path> <start_date> <end_date> [--export <output_file>]
```

```bash
python -m src.filter_by_daterange.py data/input.csv 2023-01-01 2023-01-31 --export jan_results.csv
```


### 2. Session Duration Filter
Extracts sessions that meet or exceed a minimum duration threshold.

```bash
python -m  src.filter_by_duration.py <file_path> <min_duration> [--export <output_file>]
```

```bash
python -m src.filter_by_duration.py data/input.csv 60 --export long_sessions.csv
```

### 3. Username Search
Performs a case-insensitive search for all records associated with a specific user.

```bash
python -m src.search_by_username.py <file_path> <username> [--export <output_file>]
```
