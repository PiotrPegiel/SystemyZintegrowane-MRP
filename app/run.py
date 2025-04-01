import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import ttkbootstrap as ttk
from gui.main_window import MainWindow


def run_application():
    app = ttk.Window("GHP and MRP Application", "litera", resizable=(False, False))
    MainWindow(app)
    app.mainloop()


if __name__ == "__main__":
    run_application()