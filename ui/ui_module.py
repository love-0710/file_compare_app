
from handlers.logger import log_starting_comparison, log_comparison_result
from handlers.report_module import generate_html_report, generate_csv_report
from handlers.proof_module import generate_proof_image
import tkinter as tk
from tkinter import ttk, filedialog,messagebox
from ui.file_menu import FileMenu, EditMenu, ViewMenu, HelpMenu
from handlers.file_handler import browse_file, get_file_list_from_folder, read_file
from tkinter import scrolledtext
from handlers.app_terminal_manager import update_terminal_output, clear_terminal, log_missing_row, log_comparison_result, log_starting_comparison
from handlers.compare_engine import compare_dataframes
import pandas as pd
from handlers.column_sync_module import check_filename_match, check_and_sync_columns
from handlers.workflow_manager import WorkflowManager
import os


class SmartCompareUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartComparePro")
        self.root.geometry("1400x800")

        self.before_df = None
        self.after_df = None
        self.before_file_path = None
        self.after_file_path = None

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add menus to the menu bar
        self.file_menu = FileMenu(self.root, self.menu_bar)
        self.edit_menu = EditMenu(self.root, self.menu_bar)
        self.view_menu = ViewMenu(self.root, self.menu_bar)
        self.help_menu = HelpMenu(self.root, self.menu_bar)

        self.setup_top_controls()
        self.setup_panels()
        self.setup_terminal()

    def setup_top_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.folder_btn = tk.Button(control_frame, text="Browse Folder", command=self.browse_folder)
        self.folder_btn.pack(side=tk.LEFT, padx=5)

        self.before_file_btn = tk.Button(control_frame, text="Load BEFORE File", command=self.load_before_file)
        self.before_file_btn.pack(side=tk.LEFT, padx=5)

        self.after_file_btn = tk.Button(control_frame, text="Load AFTER File", command=self.load_after_file)
        self.after_file_btn.pack(side=tk.LEFT, padx=5)

        self.start_btn = tk.Button(control_frame, text="Start", bg="green", fg="white", command=self.start_comparison)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(control_frame, text="Stop", bg="red", fg="white")
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.report_btn = tk.Button(control_frame, text="Generate Report", bg="blue", fg="white")
        self.report_btn.pack(side=tk.LEFT, padx=5)

        self.tag_filter = ttk.Combobox(control_frame, values=["*", "=", "≠"], width=5)
        self.tag_filter.current(0)
        self.tag_filter.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Clear Logs", command=lambda: clear_terminal(self.terminal)).pack(side=tk.LEFT)



    def setup_panels(self):
        panel_frame = tk.Frame(self.root)
        panel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create individual frames for each panel
        before_frame = tk.Frame(panel_frame)
        after_frame = tk.Frame(panel_frame)
        before_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        after_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Configure equal column weights
        panel_frame.grid_columnconfigure(0, weight=1, uniform="panels")
        panel_frame.grid_columnconfigure(1, weight=1, uniform="panels")
        panel_frame.grid_rowconfigure(0, weight=1)

        # Create Treeviews
        self.before_panel = ttk.Treeview(before_frame, show="headings")
        self.after_panel = ttk.Treeview(after_frame, show="headings")

        # Vertical scrollbars
        before_vscroll = ttk.Scrollbar(before_frame, orient="vertical", command=self.on_vertical_scroll)
        after_vscroll = ttk.Scrollbar(after_frame, orient="vertical", command=self.on_vertical_scroll)
        
        # Horizontal scrollbar (shared)
        self.hscroll = ttk.Scrollbar(panel_frame, orient="horizontal", command=self.on_horizontal_scroll)
        self.hscroll.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Configure Treeview scrolling
        self.before_panel.configure(
            yscrollcommand=lambda *args: self.on_panel_scroll('before', *args, scrollbar=before_vscroll),
            xscrollcommand=lambda *args: self.on_horizontal_panel_scroll('before', *args)
        )
        self.after_panel.configure(
            yscrollcommand=lambda *args: self.on_panel_scroll('after', *args, scrollbar=after_vscroll),
            xscrollcommand=lambda *args: self.on_horizontal_panel_scroll('after', *args)
        )

        # Grid layout for Treeviews and scrollbars
        self.before_panel.grid(row=0, column=0, sticky="nsew")
        before_vscroll.grid(row=0, column=1, sticky="ns")
        self.after_panel.grid(row=0, column=0, sticky="nsew")
        after_vscroll.grid(row=0, column=1, sticky="ns")

        # Configure frame weights
        before_frame.grid_rowconfigure(0, weight=1)
        before_frame.grid_columnconfigure(0, weight=1)
        after_frame.grid_rowconfigure(0, weight=1)
        after_frame.grid_columnconfigure(0, weight=1)

        # Bind mousewheel events
        self.bind_scroll_events(self.before_panel, self.after_panel)
        self.bind_scroll_events(self.after_panel, self.before_panel)

        # Labels
        tk.Label(panel_frame, text="Before", font=("Arial", 12, "bold")).grid(row=2, column=0)
        tk.Label(panel_frame, text="After", font=("Arial", 12, "bold")).grid(row=2, column=1)

    def setup_terminal(self):
        self.terminal_label = tk.Label(self.root, text="Terminal Output", font=("Arial", 10, "bold"))
        self.terminal_label.pack(pady=(10, 0))

        self.terminal_output = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state='normal')
        self.terminal_output.pack(fill=tk.BOTH, padx=10, pady=5)

        self.clear_btn = tk.Button(self.root, text="Clear Terminal", command=self.clear_terminal)
        self.clear_btn.pack(pady=5)

    def bind_scroll_events(self, source, target):
        source.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, source, target))
        source.bind("<Shift-MouseWheel>", lambda e: self.on_shift_mousewheel(e, source, target))
        source.bind("<Button-4>", lambda e: self.on_linux_scroll(-1, source, target))
        source.bind("<Button-5>", lambda e: self.on_linux_scroll(1, source, target))

    def on_mousewheel(self, event, source, target):
        direction = -1 if event.delta > 0 else 1
        source.yview_scroll(direction, "units")
        target.yview_scroll(direction, "units")
        return "break"

    def on_shift_mousewheel(self, event, source, target):
        direction = -1 if event.delta > 0 else 1
        source.xview_scroll(direction, "units")
        target.xview_scroll(direction, "units")
        return "break"

    def on_linux_scroll(self, direction, source, target):
        source.yview_scroll(direction, "units")
        target.yview_scroll(direction, "units")
        return "break"

    def on_vertical_scroll(self, *args):
        self.before_panel.yview(*args)
        self.after_panel.yview(*args)

    def on_horizontal_scroll(self, *args):
        self.before_panel.xview(*args)
        self.after_panel.xview(*args)

    def on_panel_scroll(self, caller, *args, scrollbar):
        scrollbar.set(*args)
        if caller == 'before':
            self.after_panel.yview_moveto(args[0])
        else:
            self.before_panel.yview_moveto(args[0])

    def on_horizontal_panel_scroll(self, caller, *args):
        self.hscroll.set(*args)
        if caller == 'before':
            self.after_panel.xview_moveto(args[0])
        else:
            self.before_panel.xview_moveto(args[0])

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            file_list = get_file_list_from_folder(folder_path)
            self.update_terminal(f"Found {len(file_list)} files in folder: {folder_path}")

    def load_before_file(self):
        before_file_path = browse_file()
        if before_file_path:
            df = read_file(before_file_path)
            if df is not None:
                self.before_file_path = before_file_path 
                self.before_df = df  
                self.before_panel.delete(*self.before_panel.get_children()) 
                self.display_data_in_treeview(self.before_panel, df)
                self.update_terminal(f"Loaded BEFORE file: {before_file_path}")

    def load_after_file(self):
        after_file_path = browse_file()
        if after_file_path:
            df = read_file(after_file_path)
            if df is not None:
                self.after_file_path = after_file_path
                self.after_df = df  
                self.after_panel.delete(*self.after_panel.get_children()) 
                self.display_data_in_treeview(self.after_panel, df)
                self.update_terminal(f"Loaded AFTER file: {after_file_path}")
                
                self.make_treeview_headers_editable(self.after_panel)

    def trigger_report_generation(self):
        # This method will be used to trigger report generation and pass file paths to the workflow module
        if hasattr(self, 'after_file_path') and hasattr(self, 'before_file_path'):
            self.workflow.generate_reports(self.after_file_path, self.before_file_path)
        else:
            self.update_terminal("Files not loaded properly.")

    def display_data_in_treeview(self, tree, dataframe):
        tree.delete(*tree.get_children())
        tree["columns"] = list(dataframe.columns)
        
        for col in dataframe.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W, stretch=False)
        
        for _, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))
        
        self.auto_adjust_columns(tree, dataframe)

        # Update header visibility
        self.update_header_visibility(tree)

    def auto_adjust_columns(self, tree, dataframe):
        for col in dataframe.columns:
            max_len = max(
                len(str(col)),
                *[len(str(x)) for x in dataframe[col]]
            )
            tree.column(col, width=min(300, max_len * 10))

    def update_header_visibility(self, tree):
    # Ensure header is visible by scrolling horizontally if needed
        tree.xview_moveto(0)

    def clear_terminal(self):
        clear_terminal(self.terminal_output)

    def update_terminal(self, message):
        update_terminal_output(self.terminal_output, message)

    def start_comparison(self):
        log_starting_comparison(self.terminal_output)

        # Retrieve loaded file paths
        before_file_path = self.before_file_path
        after_file_path = self.after_file_path

        # Extract filenames only (without path)
        before_filename = os.path.basename(before_file_path)
        after_filename = os.path.basename(after_file_path)

        # Check if file names match
        if before_filename != after_filename:
            messagebox.showwarning("File Name Mismatch", f"Selected files do not match:\nBEFORE: {before_filename}\nAFTER: {after_filename}\n\nPlease upload matching file pairs.")
            self.update_terminal("❌ File names do not match. Please verify BEFORE and AFTER files.")
            return

        # Convert TreeView content to DataFrames
        df_before = self.treeview_to_dataframe(self.before_panel)
        df_after = self.treeview_to_dataframe(self.after_panel)

        # Proceed with column sync
        updated_after_df, col_mapping = check_and_sync_columns(df_before, df_after)

        if col_mapping:
            self.update_terminal("⚠️ Mismatched columns detected. Syncing...")
            self.display_data_in_treeview(self.after_panel, updated_after_df)
            self.after_df = updated_after_df  # Update reference

        if self.before_df is None or self.after_df is None:
                messagebox.showerror("Error", "Please load both BEFORE and AFTER files")
                return
                
        self.workflow_manager = WorkflowManager(self.terminal_output)
        success = self.workflow_manager.run_workflow(self.before_file_path, self.after_file_path)
            
        if success:
            # Update UI with comparison results
            self.display_comparison_results(self.workflow_manager.comparison_result)


        # Proceed with comparison
        comparison_results, missing_rows = compare_dataframes(df_before, updated_after_df, terminal_widget=self.terminal_output)
        log_comparison_result(self.terminal_output, len(comparison_results), len(missing_rows))

        for missing_row in missing_rows:
            log_missing_row(self.terminal_output, missing_row)

        return updated_after_df, col_mapping


    def treeview_to_dataframe(self, treeview):
        columns = treeview["columns"]
        data = []
        for item in treeview.get_children():
            row = treeview.item(item)["values"]
            data.append(row)
        return pd.DataFrame(data, columns=columns)

    def log_missing_row(self, row_data, row_number):
        log_missing_row(self.terminal_output, row_data, row_number)

    def log_comparison_results(self, match_count, mismatch_count):
        log_comparison_result(self.terminal_output, match_count, mismatch_count)



    def make_treeview_headers_editable(self, tree):
        entry = tk.Entry(tree)
        entry.place_forget()

        def on_double_click(event):
            region = tree.identify("region", event.x, event.y)
            if region != "cell":
                return

            row_id = tree.identify_row(event.y)
            column_id = tree.identify_column(event.x)
            if not row_id or not column_id:
                return

            x, y, width, height = tree.bbox(row_id, column_id)
            column = tree.column(column_id, option="id")
            value = tree.set(row_id, column)

            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.place(x=x, y=y, width=width, height=height)

            def save_edit(event=None):
                new_value = entry.get()
                tree.set(row_id, column, new_value)
                entry.place_forget()

            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", lambda e: entry.place_forget())
            entry.focus()

        tree.bind("<Double-1>", on_double_click)



    def highlight_mismatched_columns(self, treeview, col_mapping):
        for col in col_mapping.values():
            col_id = treeview["columns"].index(col)
            treeview.tag_configure(f"mismatch_{col}", background="salmon")
            for item in treeview.get_children():
                treeview.item(item, tags=(f"mismatch_{col}",))





    