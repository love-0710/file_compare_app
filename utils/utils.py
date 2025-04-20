import os
import re
from datetime import datetime
import difflib


def normalize_date(date_str):
    """Normalize date in formats dd/mm/yyyy or mm/dd/yyyy to yyyy-mm-dd."""
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            return date_str  # Return as is if not a valid date


def normalize_number(num_str):
    """Normalize numbers by removing commas and converting to float."""
    try:
        return float(num_str.replace(',', ''))
    except ValueError:
        return num_str  # Return as is if not a valid number


def fuzzy_match(str1, str2, threshold=0.9):
    """Compare two strings using difflib and return True if match exceeds threshold."""
    ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
    return ratio >= threshold


def remove_extra_whitespace(text):
    """Remove leading, trailing, and excessive spaces within text."""
    return re.sub(r'\s+', ' ', text.strip())


def sort_rows_by_column(data, column_index):
    """Sort data by a specific column index."""
    return sorted(data, key=lambda x: x[column_index])


def is_valid_file_path(file_path):
    """Check if a given file path exists."""
    return os.path.exists(file_path)


def check_threshold(value, threshold):
    """Checks if a value exceeds a threshold."""
    return value >= threshold
