import tkinter as tk
from tkinter import filedialog, messagebox,simpledialog

class FileMenu:
    def __init__(self, root, menu_bar):
        self.root = root
        self.menu_bar = menu_bar
        self.create_file_menu()

    def create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        # Add File menu to menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # New
        file_menu.add_command(label="New Session", command=self.new_session)
        
        # Open
        file_menu.add_command(label="Open File", command=self.open_file)
        
        # Save As
        file_menu.add_command(label="Save As", command=self.save_as)
        
        # Exit
        file_menu.add_command(label="Exit", command=self.exit_app)

    def new_session(self):
        print("New session initiated")
        # You can reset the app or clear the panels

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Open File", filetypes=[("All Files", "*.*")])
        if file_path:
            print(f"File selected: {file_path}")
            # You can now load the file in the UI

    def save_as(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            print(f"File will be saved as: {save_path}")
            # Implement saving the current comparison to file

    def exit_app(self):
        confirm_exit = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm_exit:
            self.root.quit()

class EditMenu:
    def __init__(self, root, menu_bar):
        self.root = root
        self.menu_bar = menu_bar
        self.create_edit_menu()

    def create_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Search option
        edit_menu.add_command(label="Search", command=self.search)

    def search(self):
        search_term = simpledialog.askstring("Search", "Enter the term to search:")
        print(f"Search term: {search_term}")
        # Implement search logic for comparing files

class ViewMenu:
    def __init__(self, root, menu_bar):
        self.root = root
        self.menu_bar = menu_bar
        self.create_view_menu()

    def create_view_menu(self):
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Show Matching/Unmatching Rows
        view_menu.add_command(label="Show Matching Rows", command=self.show_matching_rows)
        view_menu.add_command(label="Show Unmatching Rows", command=self.show_unmatching_rows)

    def show_matching_rows(self):
        print("Show matching rows only")
        # Logic to show matching rows

    def show_unmatching_rows(self):
        print("Show unmatching rows only")
        # Logic to show unmatching rows

class HelpMenu:
    def __init__(self, root, menu_bar):
        self.root = root
        self.menu_bar = menu_bar
        self.create_help_menu()

    def create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Help documentation option
        help_menu.add_command(label="Documentation", command=self.show_help)

    def show_help(self):
        messagebox.showinfo("Help", "SmartComparePro\nVersion 1.0\nFor more details, refer to the documentation.")
