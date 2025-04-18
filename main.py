import tkinter as tk
from ui.ui_module import SmartCompareUI

def main():
    root = tk.Tk()
    app = SmartCompareUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
