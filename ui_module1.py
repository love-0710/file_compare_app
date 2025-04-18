import tkinter as tk
from tkinter import ttk, filedialog
from ui.file_menu import FileMenu, EditMenu, ViewMenu, HelpMenu
from handlers.file_handler import browse_file
from handlers.file_handler import get_file_list_from_folder
from handlers.file_handler import read_file
from tkinter import scrolledtext
from handlers.app_terminal_manager import update_terminal_output, clear_terminal, log_missing_row, log_comparison_result, log_starting_comparison
from handlers.compare_engine import compare_dataframes
import pandas as pd

class SmartCompareUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartComparePro")
        self.root.geometry("1400x800")

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add file menu to the menu bar
        self.file_menu = FileMenu(self.root, self.menu_bar)
        self.edit_menu = EditMenu(self.root, self.menu_bar)
        self.view_menu = ViewMenu(self.root, self.menu_bar)
        self.help_menu = HelpMenu(self.root, self.menu_bar)

        self.setup_top_controls()
        self.setup_panels()

        # Initialize terminal output (scrolled text widget)
        self.terminal_label = tk.Label(self.root, text="Terminal Output", font=("Arial", 10, "bold"))
        self.terminal_label.pack(pady=(10, 0))

        self.terminal_output = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state='disabled')
        self.terminal_output.pack(fill=tk.BOTH, padx=10, pady=5)

        # Add Clear Terminal Button
        self.clear_btn = tk.Button(self.root, text="Clear Terminal", command=self.clear_terminal)
        self.clear_btn.pack(pady=5)


    def sync_scroll(self, event, before_panel, after_panel):
        """
        Synchronize the scroll of two panels (before and after) when one is scrolled.
        
        Args:
            event: The scroll event from one of the panels (before or after).
            before_panel: The panel for the 'before' file.
            after_panel: The panel for the 'after' file.
        """
        if event.widget == before_panel:
            after_panel.yview_scroll(event.delta, "units")
            after_panel.xview_scroll(event.delta, "units")
        elif event.widget == after_panel:
            before_panel.yview_scroll(event.delta, "units")
            before_panel.xview_scroll(event.delta, "units")



    def setup_top_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.folder_btn = tk.Button(control_frame, text="Browse Folder", command=self.browse_folder)
        self.folder_btn.pack(side=tk.LEFT, padx=5)

        self.before_file_btn = tk.Button(control_frame, text="Load BEFORE File", command=self.load_before_file)
        self.before_file_btn.pack(side=tk.LEFT, padx=5)

        self.after_file_btn = tk.Button(control_frame, text="Load AFTER File", command=self.load_after_file)
        self.after_file_btn.pack(side=tk.LEFT, padx=5)


        self.start_btn = tk.Button(control_frame, text="Start", bg="green", fg="white")
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(control_frame, text="Stop", bg="red", fg="white")
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.report_btn = tk.Button(control_frame, text="Generate Report", bg="blue", fg="white")
        self.report_btn.pack(side=tk.LEFT, padx=5)

        # Tag filter
        self.tag_filter = ttk.Combobox(control_frame, values=["*", "=", "≠"], width=5)
        self.tag_filter.current(0)
        self.tag_filter.pack(side=tk.LEFT, padx=5)


    def setup_panels(self):
        panel_frame = tk.Frame(self.root)
        panel_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        self.before_scroll_y = tk.Scrollbar(panel_frame, orient=tk.VERTICAL)
        self.after_scroll_y = tk.Scrollbar(panel_frame, orient=tk.VERTICAL)

        self.before_scroll_x = tk.Scrollbar(panel_frame, orient=tk.HORIZONTAL)
        self.after_scroll_x = tk.Scrollbar(panel_frame, orient=tk.HORIZONTAL)

        # BEFORE Treeview
        self.before_panel = ttk.Treeview(panel_frame, show="headings", yscrollcommand=self.sync_vertical_scroll, xscrollcommand=self.sync_horizontal_scroll, height=30)
        
        # AFTER Treeview
        self.after_panel = ttk.Treeview(panel_frame, show="headings", yscrollcommand=self.sync_vertical_scroll, xscrollcommand=self.sync_horizontal_scroll, height=30)

        panel_frame.grid_columnconfigure(0, weight=1, uniform="panel")
        panel_frame.grid_columnconfigure(1, weight=1, uniform="panel")


        # Scrollbars control both panels
        self.before_scroll_y.config(command=self.sync_vertical_scroll)
        self.after_scroll_y.config(command=self.sync_vertical_scroll)
        self.before_scroll_x.config(command=self.sync_horizontal_scroll)
        self.after_scroll_x.config(command=self.sync_horizontal_scroll)

        # Layout using grid to ensure both panels have equal space (50% each)
        self.before_panel.grid(row=0, column=0, sticky="nsew")
        self.after_panel.grid(row=0, column=1, sticky="nsew")

        self.before_scroll_y.grid(row=0, column=2, sticky="ns")
        self.after_scroll_y.grid(row=0, column=3, sticky="ns")

        self.before_scroll_x.grid(row=1, column=0, sticky="ew")
        self.after_scroll_x.grid(row=1, column=1, sticky="ew")

        # Labels (Optional)
        tk.Label(panel_frame, text="Before", font=("Arial", 12, "bold")).grid(row=2, column=0)
        tk.Label(panel_frame, text="After", font=("Arial", 12, "bold")).grid(row=2, column=1)

        # Bind the scroll events
        self.before_panel.bind("<Configure>", lambda event: self.sync_scroll(event, self.before_panel, self.after_panel))
        self.after_panel.bind("<Configure>", lambda event: self.sync_scroll(event, self.before_panel, self.after_panel))

    def sync_vertical_scroll(self, *args):
        # Sync vertical scrolling (both before and after)
        self.before_panel.yview(*args)
        self.after_panel.yview(*args)
        self.before_scroll_y.set(*args)
        self.after_scroll_y.set(*args)

    def sync_horizontal_scroll(self, *args):
        # Sync horizontal scrolling (both before and after)
        self.before_panel.xview(*args)
        self.after_panel.xview(*args)
        self.before_scroll_x.set(*args)
        self.after_scroll_x.set(*args)



    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        print(f"Selected Folder: {folder_path}")
        if folder_path:
            file_list = get_file_list_from_folder(folder_path)
            print(f"Files in Folder: {file_list}")


    def browse_file(self):
        file_path = browse_file()
        print(f"Selected File: {file_path}")
        if file_path:
            # Load the file data
            data = read_file(file_path)
            print(f"Loaded Data: {data.head()}")  # Example: Print the first few rows of the loaded data
            self.display_file_data(data)

    def display_file_data(self, data):
        # Display the loaded file data (this can be formatted as a table or raw text in the UI)
        self.before_panel.delete(1.0, tk.END)
        self.before_panel.insert(tk.END, data.to_string())
        
    def load_before_file(self):
        file_path = browse_file()
        if file_path:
            df = read_file(file_path)
            if df is not None:
                self.display_data_in_treeview(self.before_panel, df)

    def load_after_file(self):
        file_path = browse_file()
        if file_path:
            df = read_file(file_path)
            if df is not None:
                self.display_data_in_treeview(self.after_panel, df)


    def display_data_in_treeview(self, tree, dataframe):
        tree.delete(*tree.get_children())  # Clear old data
        tree["columns"] = list(dataframe.columns)
        tree["show"] = "headings"

        for col in dataframe.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)

        for _, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))



    def clear_terminal(self):
        clear_terminal(self.terminal_output)

    def update_terminal(self, message):
        update_terminal_output(self.terminal_output, message)

    def start_comparison(self):
        log_starting_comparison(self.terminal_output)

        # Extract data from Treeviews (before and after panels)
        df_before = self.treeview_to_dataframe(self.before_panel)
        df_after = self.treeview_to_dataframe(self.after_panel)

        # Call comparison logic with the DataFrames
        comparison_results, missing_rows = compare_dataframes(df_before, df_after, terminal_widget=self.terminal_output)

        # Optionally log comparison result summary
        log_comparison_result(self.terminal_output, len(comparison_results), len(missing_rows))

        # Log missing rows in terminal
        for missing_row in missing_rows:
            log_missing_row(self.terminal_output, missing_row)

    def treeview_to_dataframe(self, treeview):
        """Converts the data in the Treeview widget to a pandas DataFrame."""
        columns = treeview["columns"]
        data = []

        # Iterate through all the rows in the Treeview widget and extract the values
        for item in treeview.get_children():
            row = treeview.item(item)["values"]
            data.append(row)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=columns)
        return df


    def log_missing_row(self, row_data, row_number):
        log_missing_row(self.terminal_output, row_data, row_number)

    def log_comparison_results(self, match_count, mismatch_count):
        log_comparison_result(self.terminal_output, match_count, mismatch_count)



