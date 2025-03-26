import customtkinter as ctk
from gui.main_window import App  # Import the App class from the main_window.py


def run_application():
    # Initialize the app and run the main loop
    app = App()
    app.mainloop()


if __name__ == "__main__":
    run_application()
