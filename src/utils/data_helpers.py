# src/utils/date_helpers.py
from datetime import datetime, timedelta

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")

def get_date_range(start_date: str, end_date: str) -> (datetime, datetime):
    start = parse_date(start_date)
    end = parse_date(end_date)
    return start, end

def validate_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False