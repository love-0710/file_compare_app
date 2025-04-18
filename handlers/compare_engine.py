import pandas as pd
from difflib import SequenceMatcher
from handlers.preprocess_module import preprocess_dataframe
from handlers.app_terminal_manager import update_terminal_output

def is_similar(val1, val2, threshold=0.9):
    try:
        val1, val2 = str(val1), str(val2)
        ratio = SequenceMatcher(None, val1.strip(), val2.strip()).ratio()
        return ratio >= threshold
    except:
        return False


def align_dataframes(df1, df2):
    # Sort by all common columns
    common_cols = list(set(df1.columns) & set(df2.columns))
    df1_sorted = df1.sort_values(by=common_cols).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=common_cols).reset_index(drop=True)
    return df1_sorted, df2_sorted


def compare_dataframes(before_df, after_df):
    before_df = preprocess_dataframe(before_df)
    after_df = preprocess_dataframe(after_df)

    shared_columns = [col for col in before_df.columns if col in after_df.columns]
    before_df = before_df[shared_columns].copy()
    after_df = after_df[shared_columns].copy()

    before_df_sorted = before_df.sort_values(by=shared_columns).reset_index(drop=True)
    after_df_sorted = after_df.sort_values(by=shared_columns).reset_index(drop=True)

    max_rows = max(len(before_df_sorted), len(after_df_sorted))
    comparison_results = []
    missing_rows = []

    for i in range(max_rows):
        if i >= len(before_df_sorted):
            break  # No more rows to compare in before
        if i >= len(after_df_sorted):
            missing_rows.append(before_df_sorted.iloc[i].to_dict())
            continue

        row_result = {}
        for col in shared_columns:
            val_before = before_df_sorted.at[i, col]
            val_after = after_df_sorted.at[i, col]
            if pd.isna(val_before) and pd.isna(val_after):
                row_result[col] = '<span style="background-color:#d6ffdd">NaN = NaN</span>'
            elif str(val_before) == str(val_after):
                row_result[col] = f'<span style="background-color:#d6ffdd">{val_before}</span>'
            else:
                row_result[col] = f'<span style="background-color:#ffd6d6">{val_before} != {val_after}</span>'

        comparison_results.append(row_result)

    return comparison_results, missing_rows


def show_missing_rows_in_terminal(terminal_widget, missing_rows):
    """
    Function to log missing rows to the terminal output.
    """
    if not missing_rows:
        update_terminal_output(terminal_widget, "\n✅ No missing rows found in AFTER file compared to BEFORE.")
        return

    update_terminal_output(terminal_widget, "\n⚠️  MISSING ROWS in AFTER file compared to BEFORE:")
    for idx, row in enumerate(missing_rows, 1):
        row_str = ", ".join([f"{col}: {val}" for col, val in row.items()])
        update_terminal_output(terminal_widget, f"{idx}. {row_str}")
