# handlers/workflow_manager.py

from handlers.file_handler import read_file
from handlers.preprocess_module import preprocess_dataframe
from handlers.compare_engine import compare_dataframes
from handlers.report_module import generate_html_report, generate_csv_report
from handlers.proof_module import generate_proof_image
from handlers.logger import log_starting_comparison, log_comparison_result
from handlers.app_terminal_manager import update_terminal_output


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

        try:
            html_report_path = generate_html_report(self.comparison_result)
            csv_report_path = generate_csv_report(self.comparison_result)
            update_terminal_output(self.terminal_text_widget, f"Reports generated: {html_report_path}, {csv_report_path}")
        except Exception as e:
            update_terminal_output(self.terminal_text_widget, f"Error generating reports: {str(e)}", "error")
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
