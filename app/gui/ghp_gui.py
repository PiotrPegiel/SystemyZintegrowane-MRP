import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tksheet import Sheet


class GHPGUI(ttk.Frame):
    def __init__(self, master, ghp_system, time_periods_var, display_message):
        super().__init__(master, padding=(10, 10))
        self.pack(fill=BOTH, expand=YES)

        self.ghp_system = ghp_system
        self.time_periods_var = time_periods_var
        self.display_message = display_message
        self.result_frame = ttk.Frame(self)
        self.result_frame.pack(fill=BOTH, expand=YES, pady=10)

    def display_ghp_table(self, demand, production, availability, time_periods):
        """Display GHP results in a table and dynamically update availability."""
        # Clear any existing widgets in the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Define table headers and data
        headers = [str(i + 1) for i in range(time_periods)]
        indexes = ["Demand", "Production", "Availability"]
        data = [demand, production, availability]

        # Create the Sheet widget and store it as an instance variable
        self.sheet = Sheet(self.result_frame, data=data, headers=headers, row_index=indexes, 
                           default_column_width=70, default_row_index_width=170, 
                           row_index_align="e", align=CENTER, height=280, width=500)
        self.sheet.enable_bindings()

        # Event listener for cell edits
        def on_cell_edit(event):
            try:
                # Get the modified cell's row and column
                row = event["row"]
                col = event["column"]

                # Update the corresponding demand or production value
                if row == 0:  # Demand row
                    demand[col] = int(self.sheet.get_cell_data(row, col))
                elif row == 1:  # Production row
                    production[col] = int(self.sheet.get_cell_data(row, col))

                # Recalculate availability
                new_availability = self.ghp_system.calculate_ghp(demand, production, time_periods)

                # Update the availability row in the table
                for i in range(time_periods):
                    self.sheet.set_cell_data(2, i, new_availability[i])  # Row 2 is the availability row
            except ValueError:
                self.display_message("Error: Please enter a valid integer.")
            except Exception as e:
                self.display_message(f"Error: {str(e)}")

        # Bind the "edit_cell" event to the on_cell_edit function
        self.sheet.extra_bindings("edit_cell", on_cell_edit)

        # Pack the Sheet widget into the result frame
        self.sheet.pack(fill=BOTH, expand=YES)