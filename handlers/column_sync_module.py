import tkinter as tk
from tkinter import messagebox

def check_filename_match(before_filename, after_filename):
    """
    Check if BEFORE and AFTER filenames match.
    If not, show a popup and return False.
    """
    if before_filename != after_filename:
        messagebox.showerror("Filename Mismatch", f"The file name '{after_filename}' doesn't match with the expected BEFORE file '{before_filename}'.\nPlease upload the correct AFTER file.")
        return False
    return True


def check_and_sync_columns(before_df, after_df, treeview=None):
    """
    Checks if all columns in after_df match those in before_df.
    If mismatched, ask user to auto-correct or manually fix them.

    Parameters:
        before_df: DataFrame from BEFORE file
        after_df: DataFrame from AFTER file
        treeview: Optional TreeView reference for UI interaction (highlight + navigation)
    Returns:
        Updated after_df with renamed columns (if any renaming done)
    """
    before_cols = list(before_df.columns)
    after_cols = list(after_df.columns)

    col_mapping = {} 

    if before_cols == after_cols:
        return after_df, col_mapping  # No mismatch

    for idx, (before_col, after_col) in enumerate(zip(before_cols, after_cols)):
        if before_col != after_col:
            msg = (
                f"Column mismatch detected:\n\n"
                f"BEFORE column: '{before_col}'\n"
                f"AFTER column: '{after_col}'\n\n"
                "Do you want to auto-rename the AFTER column to match?"
            )
            answer = messagebox.askyesno("Column Name Mismatch", msg)

            if answer:
                after_df.rename(columns={after_col: before_col}, inplace=True)
                col_mapping[after_col] = before_col  # Save the mapping
                if treeview:
                    _rename_column_in_treeview(treeview, old=after_col, new=before_col)
            else:
                if treeview:
                    _highlight_column_in_treeview(treeview, after_col)
                    _scroll_to_column(treeview, after_col)

    return after_df, col_mapping


def _highlight_column_in_treeview(treeview, column_name):
    """
    Apply red highlight to a column header in TreeView to indicate mismatch.
    """
    # You must have logic to tag column headers in your TreeView setup
    # This assumes column header tag styling is handled in your UI setup
    treeview.heading(column_name, text=column_name, anchor='w')
    treeview.tag_configure(column_name, background='red')


def _scroll_to_column(treeview, column_name):
    """
    Scroll or focus to the specified column in TreeView.
    This behavior depends on how you're rendering columns—can be adjusted.
    """
    # Implementation here is symbolic. Actual scroll/focus depends on TreeView structure.
    try:
        col_index = list(treeview["columns"]).index(column_name)
        treeview.xview_moveto(col_index / len(treeview["columns"]))
    except Exception as e:
        print(f"Unable to scroll to column '{column_name}': {e}")


def _rename_column_in_treeview(treeview, old, new):
    """
    Update TreeView display header when column is renamed.
    """
    try:
        treeview.heading(old, text=new)
    except Exception as e:
        print(f"Error renaming column in TreeView: {e}")

