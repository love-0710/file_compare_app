import tkinter as tk
from tkinter import ttk

class ScrollSyncApp:
    def __init__(self, root):
        self.root = root
        self.setup_panels()

    def setup_panels(self):
        panel_frame = tk.Frame(self.root)
        panel_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeviews
        self.before_panel = ttk.Treeview(panel_frame, show='headings')
        self.after_panel = ttk.Treeview(panel_frame, show='headings')

        # Shared vertical and horizontal scrollbars
        self.scroll_y = tk.Scrollbar(panel_frame, orient=tk.VERTICAL)
        self.scroll_x = tk.Scrollbar(panel_frame, orient=tk.HORIZONTAL)

        # Configure Treeviews with scroll commands
        self.before_panel.configure(yscrollcommand=lambda *args: self.on_scroll_y(*args, caller='before'),
                                    xscrollcommand=lambda *args: self.on_scroll_x(*args, caller='before'))
        self.after_panel.configure(yscrollcommand=lambda *args: self.on_scroll_y(*args, caller='after'),
                                   xscrollcommand=lambda *args: self.on_scroll_x(*args, caller='after'))

        # Configure scrollbars to control both Treeviews
        self.scroll_y.config(command=self.on_scrollbar_y)
        self.scroll_x.config(command=self.on_scrollbar_x)

        # Grid layout
        self.before_panel.grid(row=0, column=0, sticky="nsew")
        self.after_panel.grid(row=0, column=1, sticky="nsew")
        self.scroll_y.grid(row=0, column=2, sticky="ns")
        self.scroll_x.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Grid config
        panel_frame.grid_rowconfigure(0, weight=1)
        panel_frame.grid_columnconfigure(0, weight=1)
        panel_frame.grid_columnconfigure(1, weight=1)

        # Bind mousewheel to both treeviews
        self.bind_mousewheel_sync(self.before_panel, self.after_panel)
        self.bind_mousewheel_sync(self.after_panel, self.before_panel)

        columns = ['A', 'B', 'C', 'D', 'E']
        self.before_panel['columns'] = columns
        self.after_panel['columns'] = columns

        for col in columns:
            self.before_panel.heading(col, text=col)
            self.after_panel.heading(col, text=col)

        for i in range(50):
            self.before_panel.insert('', 'end', values=[f'b{i}-{j}' for j in range(5)])
            self.after_panel.insert('', 'end', values=[f'a{i}-{j}' for j in range(5)])

    def on_scroll_y(self, *args, caller):
        if caller == 'before':
            self.after_panel.yview_moveto(args[0])
        else:
            self.before_panel.yview_moveto(args[0])
        self.scroll_y.set(*args)

    def on_scroll_x(self, *args, caller):
        if caller == 'before':
            self.after_panel.xview_moveto(args[0])
        else:
            self.before_panel.xview_moveto(args[0])
        self.scroll_x.set(*args)

    def on_scrollbar_y(self, *args):
        self.before_panel.yview(*args)
        self.after_panel.yview(*args)

    def on_scrollbar_x(self, *args):
        self.before_panel.xview(*args)
        self.after_panel.xview(*args)

    def bind_mousewheel_sync(self, source, target):
        def _on_mousewheel(event):
            direction = int(-1 * (event.delta / 120))
            source.yview_scroll(direction, "units")
            target.yview_scroll(direction, "units")
            return "break"
        source.bind("<MouseWheel>", _on_mousewheel)
        source.bind("<Shift-MouseWheel>", lambda e: self.scroll_x_event(e, source, target))

    def scroll_x_event(self, event, source, target):
        direction = int(-1 * (event.delta / 120))
        source.xview_scroll(direction, "units")
        target.xview_scroll(direction, "units")
        return "break"

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    app = ScrollSyncApp(root)
    root.mainloop()
