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
        """Start the comparison process."""
        log_starting_comparison(self.before_file, self.after_file)
        update_terminal_output(self.terminal_text_widget, "Starting file comparison...")

        try:
            self.comparison_result = compare_dataframes(self.before_file, self.after_file)
            update_terminal_output(self.terminal_text_widget, "Comparison completed successfully!")
        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"Error during comparison: {str(e)}", "error")
            return False
        return True

    def generate_reports(self):
        """Generate HTML and CSV reports based on the comparison results."""
        update_terminal_output(self.terminal_text_widget, "Generating reports...")

        """Ask user if they want to save report, then generate HTML and CSV reports."""
        result = messagebox.askyesno("Generate Report", "Comparison completed.\nDo you want to save the report?")

        if not result:
            update_terminal_output(self.terminal_text_widget, "User chose not to save the report.")
            return True  # Not an error, just a choice


        try:
            # Get AFTER file name without extension
            file_basename = os.path.splitext(os.path.basename(self.after_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            suggested_name = f"{file_basename}_{timestamp}"

            # Ask where to save HTML report
            html_path = filedialog.asksaveasfilename(
                initialfile=f"{suggested_name}.html",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html")],
                title="Save HTML Report As"
            )
            if not html_path:
                update_terminal_output(self.terminal_text_widget, "Report generation cancelled by user.")
                return False

            # Ask where to save CSV report
            csv_path = filedialog.asksaveasfilename(
                initialfile=f"{suggested_name}.csv",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV Report As"
            )
            if not csv_path:
                update_terminal_output(self.terminal_text_widget, "CSV export cancelled by user.")
                return False

            # Generate both reports

            generate_html_report(self.comparison_result, html_path)
            generate_csv_report(self.comparison_result, csv_path)

            update_terminal_output(self.terminal_text_widget, f"✅ Reports generated successfully:\n📄 HTML: {html_path}\n📄 CSV: {csv_path}")

            # Preview HTML report
            webbrowser.open(f"file://{html_path}")


        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"❌ Error generating reports: {str(e)}", "error")
            return False

        return True

    def generate_proof(self):
        """Generate proof images for mismatches."""
        update_terminal_output(self.terminal_text_widget, "Generating proof images for mismatches...")

        try:
            proof_image_path = generate_proof_image(self.before_file, self.after_file, self.comparison_result)
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
        if not self.generate_reports():
            return False
        if not self.generate_proof():
            return False

        log_comparison_result(self.comparison_result)
        update_terminal_output(self.terminal_text_widget, "Workflow completed successfully!")
        return True
