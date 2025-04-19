# preprocess_module.py

import re
import pandas as pd
import numpy as np
from datetime import datetime

# --- DATE FORMAT NORMALIZATION ---
def normalize_date(value):
    if pd.isnull(value):
        return None
    try:
        # Attempt parsing various common formats
        parsed_date = pd.to_datetime(''.join(filter(str.isdigit, str(value))), errors='coerce', dayfirst=True)
        if pd.isnull(parsed_date):
            return str(value).strip()
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        return str(value).strip()

# --- NUMERIC NORMALIZATION ---
def normalize_numeric(value):
    if pd.isnull(value):
        return None
    try:
        # Remove commas, spaces, etc.
        val = str(value).replace(",", "").replace(" ", "").strip()
        if re.match(r"^[-+]?\d*\.?\d+$", val):
            return str(float(val))
        return val
    except Exception:
        return str(value).strip()

# --- WHITESPACE NORMALIZATION ---
def normalize_whitespace(value):
    if pd.isnull(value):
        return None
    return re.sub(r"\s+", " ", str(value)).strip()

# --- FULL VALUE NORMALIZATION ---
def normalize_value(value):
    if pd.isnull(value):
        return None
    val = str(value)
    val = normalize_whitespace(val)
    val = normalize_numeric(val)
    val = normalize_date(val)
    return str(val).lower().strip()  # Case-insensitive matching

# --- COLUMN NAME NORMALIZATION ---
def normalize_column_names(columns):
    return [normalize_whitespace(col).lower() for col in columns]

# --- PREPROCESS ENTIRE DATAFRAME ---
def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = normalize_column_names(df.columns)
    for col in df.columns:
        df[col] = df[col].apply(normalize_value)
    return df

# --- ALIGN COLUMNS ---
def align_columns(df_before: pd.DataFrame, df_after: pd.DataFrame):
    """
    Keeps only common columns and aligns their order for comparison.
    """
    common_cols = [col for col in df_before.columns if col in df_after.columns]
    df_before_aligned = df_before[common_cols]
    df_after_aligned = df_after[common_cols]
    return df_before_aligned, df_after_aligned

# --- SORT ROWS FOR BETTER COMPARISON (Optional Matching Aid) ---
def sort_rows(df: pd.DataFrame):
    return df.sort_values(by=df.columns.tolist()).reset_index(drop=True)

# --- NULL/EMPTY NORMALIZATION ---
def is_effectively_null(val):
    if pd.isnull(val):
        return True
    return str(val).strip().lower() in ["", "none", "null", "nan"]
