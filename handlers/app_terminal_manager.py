# terminal_manager.py
import tkinter as tk

def update_terminal_output(terminal_widget, message,tag=None):
    """
    Function to update the terminal (scrolled text) widget with messages.
    """
    terminal_widget.config(state=tk.NORMAL)
    terminal_widget.insert(tk.END, message + "\n")
    terminal_widget.see(tk.END)  # Auto scroll to the end
    terminal_widget.config(state=tk.DISABLED)

def clear_terminal(terminal_widget):
    """
    Clears the terminal output.
    """
    terminal_widget.config(state=tk.NORMAL)
    terminal_widget.delete(1.0, tk.END)
    terminal_widget.config(state=tk.DISABLED)

def log_missing_row(terminal_widget, row_data, row_number):
    """
    Log a missing row from the 'AFTER' file.
    """
    message = f"[Missing Row] Row {row_number} in BEFORE not found in AFTER:\n{row_data}"
    update_terminal_output(terminal_widget, message)

def log_comparison_result(terminal_widget, match_count, mismatch_count):
    """
    Log the results of the comparison (matched/mismatched row counts).
    """
    update_terminal_output(terminal_widget, f"✅ Total Matched Rows: {match_count}")
    update_terminal_output(terminal_widget, f"❌ Total Mismatched Rows: {mismatch_count}")

def log_starting_comparison(terminal_widget):
    """
    Log the starting message of comparison process.
    """
    update_terminal_output(terminal_widget, "Starting comparison...")

