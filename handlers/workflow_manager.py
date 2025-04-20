# handlers/workflow_manager.py

from handlers.file_handler import read_file
from handlers.preprocess_module import preprocess_dataframe
from handlers.compare_engine import compare_dataframes
from handlers.report_module import generate_html_report, generate_csv_report
from handlers.proof_module import generate_proof_image
from handlers.logger import log_starting_comparison, log_comparison_result
from handlers.app_terminal_manager import update_terminal_output
import os
import webbrowser
from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd
from utils.config import REPORT_PATH, SCREENSHOT_PATH

class WorkflowManager:
    def __init__(self, terminal_text_widget):
        self.terminal_text_widget = terminal_text_widget
        self.before_file = None
        self.after_file = None
        self.comparison_result = None

    def load_files(self, before_file_path, after_file_path):
        """Load the 'before' and 'after' files."""
        update_terminal_output(self.terminal_text_widget, f"Loading files: {before_file_path} and {after_file_path}...")

        try:
            self.before_file = read_file(before_file_path)
            self.after_file = read_file(after_file_path)

            # ✅ Store original file paths separately
            self.before_file_path = before_file_path
            self.after_file_path = after_file_path

            update_terminal_output(self.terminal_text_widget, f"Files loaded successfully!")
        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"Error loading files: {str(e)}", "error")
            return False
        return True


    def preprocess_files(self):
        """Preprocess the files to normalize data."""
        update_terminal_output(self.terminal_text_widget, "Preprocessing files...")

        try:
            self.before_file = preprocess_dataframe(self.before_file)
            self.after_file = preprocess_dataframe(self.after_file)
            update_terminal_output(self.terminal_text_widget, "Files preprocessed successfully!")
        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"Error preprocessing files: {str(e)}", "error")
            return False
        return True

    def start_comparison(self):
        log_starting_comparison(self.before_file, self.after_file)
        update_terminal_output(self.terminal_text_widget, "Starting file comparison...")

        try:
            match_df, mismatch_df = compare_dataframes(self.before_file, self.after_file)
            self.comparison_result = {
                "match": pd.DataFrame(match_df),      # force convert if not already
                "mismatch": pd.DataFrame(mismatch_df)
            }
            update_terminal_output(self.terminal_text_widget, "Comparison completed successfully!")
        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"Error during comparison: {str(e)}", "error")
            return False
        return True

    def generate_reports(self, before_file_path, after_file_path):
        """Generate HTML and CSV reports based on the comparison results."""
        update_terminal_output(self.terminal_text_widget, "Generating reports...")

        result = messagebox.askyesno("Generate Report", "Comparison completed.\nDo you want to save the report?")

        if not result:
            update_terminal_output(self.terminal_text_widget, "User chose not to save the report.")
            return True

        try:
            file_basename = os.path.splitext(os.path.basename(after_file_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            suggested_name = f"{file_basename}_{timestamp}"

            html_path = filedialog.asksaveasfilename(
                initialfile=f"{suggested_name}.html",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html")],
                title="Save HTML Report As"
            )
            if not html_path:
                update_terminal_output(self.terminal_text_widget, "Report generation cancelled by user.")
                return False

            csv_path = filedialog.asksaveasfilename(
                initialfile=f"{suggested_name}.csv",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV Report As"
            )
            if not csv_path:
                update_terminal_output(self.terminal_text_widget, "CSV export cancelled by user.")
                return False

            # Generate the proof paths
            proof_paths = {}
            proof_image_path = generate_proof_image(self.before_file, self.after_file, suggested_name)
            proof_paths[suggested_name] = proof_image_path


            generate_html_report(self.comparison_result["mismatch"], html_path)
            generate_csv_report(self.comparison_result["mismatch"], csv_path)

            update_terminal_output(self.terminal_text_widget, f"✅ Reports generated successfully:\n📄 HTML: {html_path}\n📄 CSV: {csv_path}")

            webbrowser.open(f"file://{html_path}")

        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"❌ Error generating reports: {str(e)}", "error")
            return False

        return True


    def generate_proof(self):
        """Generate proof images for mismatches."""
        update_terminal_output(self.terminal_text_widget, "Generating proof images for mismatches...")

        try:
            _, mismatch_df = self.comparison_result
            proof_image_path = generate_proof_image(self.before_file, self.after_file, "proof_image")
            update_terminal_output(self.terminal_text_widget, f"Proof image generated: {proof_image_path}")
        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"Error generating proof images: {str(e)}", "error")
            return False
        return True


    def run_workflow(self, before_file_path, after_file_path):
        """Complete workflow from loading to generating reports and proof."""
        if not self.load_files(before_file_path, after_file_path):
            return False
        if not self.preprocess_files():
            return False
        if not self.start_comparison():
            return False
        if not self.generate_reports(before_file_path, after_file_path):
            return False
        if not self.generate_proof():
            return False

        log_comparison_result(self.comparison_result)
        update_terminal_output(self.terminal_text_widget, "Workflow completed successfully!")
        return True

    def save_report(self, report_data):
        """Save comparison results as a report in the configured path."""
        report_file = os.path.join(REPORT_PATH, 'comparison_report.html')
        with open(report_file, 'w') as file:
            file.write(report_data)

    def save_screenshot(self, screenshot_data):
        """Save screenshot for proof of mismatch."""
        screenshot_file = os.path.join(SCREENSHOT_PATH, 'mismatch_screenshot.png')
        with open(screenshot_file, 'wb') as file:
            file.write(screenshot_data)