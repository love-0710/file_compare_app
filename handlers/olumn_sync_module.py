import difflib

def suggest_column_matches(before_columns, after_columns, threshold=0.6):
    """
    Suggest likely matching columns between BEFORE and AFTER files using similarity ratio.
    """
    suggestions = {}
    for before_col in before_columns:
        match = difflib.get_close_matches(before_col, after_columns, n=1, cutoff=threshold)
        if match:
            suggestions[before_col] = match[0]
    return suggestions


def apply_column_sync(before_df, after_df, mapping):
    """
    Rename AFTER dataframe columns based on provided mapping.
    mapping = {'BeforeCol': 'AfterCol'}
    """
    reverse_mapping = {v: k for k, v in mapping.items()}
    after_df_renamed = after_df.rename(columns=reverse_mapping)
    
    # Keep only the columns that exist in both after_df_renamed and before_df
    common_cols = [col for col in before_df.columns if col in after_df_renamed.columns]
    return before_df[common_cols].copy(), after_df_renamed[common_cols].copy()
