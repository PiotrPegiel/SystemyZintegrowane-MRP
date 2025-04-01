import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.bom import BOM
from src.ghp import GHP
from src.mrp import MRP
from gui.bom_gui import BOMGUI
from gui.ghp_gui import GHPGUI


class MainWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # Initialize BOM, GHP, and MRP
        self.bom = BOM()
        self.ghp_system = GHP(self.bom)
        self.mrp_system = None  # Will be initialized after GHP calculation
        self.time_periods = 10  # Default value, user can change this later

        # Create BOM GUI
        self.bom_gui = BOMGUI(self, self.bom, self.on_material_added)

        # Create input for "Number of Time Periods"
        self.create_time_period_input()

        # Create GHP GUI
        self.ghp_gui = GHPGUI(self, self.ghp_system, self.time_periods_var, self.display_message)

        # Create "Calculate GHP" button
        self.create_calculate_ghp_button()

    def create_time_period_input(self):
        """Create input field for the number of time periods."""
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=X, pady=10)

        time_periods_label = ttk.Label(action_frame, text="Number of Time Periods")
        time_periods_label.pack(side=LEFT, padx=5)

        self.time_periods_var = ttk.IntVar(value=10)  # Default value
        time_periods_entry = ttk.Entry(action_frame, textvariable=self.time_periods_var, width=5)
        time_periods_entry.pack(side=LEFT, padx=5)

    def create_calculate_ghp_button(self):
        """Create the 'Calculate GHP' button."""
        self.calculate_ghp_button = ttk.Button(
            master=self,
            text="Calculate GHP",
            bootstyle=PRIMARY,
            command=self.calculate_ghp,
        )
        self.calculate_ghp_button.pack(side=TOP, pady=10)
        self.calculate_ghp_button.pack_forget()  # Initially hidden

    def on_material_added(self, material):
        """Callback when a material is added."""
        print(f"Material added: {material.name}")

        # Show the "Calculate GHP" button if a level 0 material is present
        if self.bom.level_0_material is not None:
            self.calculate_ghp_button.pack(side=TOP, pady=10)

    def calculate_ghp(self):
        """Calculate and display GHP results."""
        try:
            # Get the number of time periods from the input field
            time_periods = self.time_periods_var.get()
            if time_periods <= 0:
                raise ValueError("Number of time periods must be a positive integer.")

            # Initialize demand and production arrays
            demand = [0] * time_periods
            production = [0] * time_periods

            # Calculate availability using the GHP system
            availability = self.ghp_system.calculate_ghp(demand, production, time_periods)

            # Display the GHP table
            self.ghp_gui.display_ghp_table(demand, production, availability, time_periods)
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

<<<<<<<<< Temporary merge branch 1
=========
    def calculate_mrp(self):
        """Calculate and display MRP results."""
        try:
            planned_deliveries = {material.name: [0] * self.time_periods for material in self.bom.materials}
            self.mrp_system = MRP(self.bom, self.ghp_system, self.time_periods, planned_deliveries)
            self.mrp_system.calculate_mrp()

            self.display_mrp_tables()
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

    def display_ghp_table(self, demand, production, availability):
        """Display GHP results in a table."""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        headers = [str(i + 1) for i in range(self.time_periods)]
        indexes = ["Demand", "Production", "Availability"]
        data = [demand, production, availability]

        sheet = Sheet(self.result_frame, data=data, headers=headers, 
                      row_index=indexes, default_column_width=70, 
                      default_row_index_width=300, row_index_align="e",
                      align=CENTER)
        sheet.enable_bindings()
        sheet.pack(fill=BOTH, expand=YES)

    def display_mrp_tables(self):
        """Display MRP results in tables."""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        for material_name, table in self.mrp_system.mrp_tables.items():
            frame = ttk.Frame(self.result_frame)
            frame.pack(fill=X, pady=10)

            headers = [str(i + 1) for i in range(self.time_periods)]
            indexes = ["Demand", "Planned Delivery", "Available", "Net Requirement", "Planned Order", "Planned Receipt"]
            data = [
                table.demand,
                table.planned_delivery,
                table.available,
                table.net_requirement,
                table.planned_order,
                table.planned_receipt,
            ]

            label = ttk.Label(frame, text=f"MRP for {material_name}", bootstyle=INFO)
            label.pack(fill=X, pady=5)

            sheet = Sheet(frame, data=data, headers=headers, row_index=indexes)
            sheet.enable_bindings()
            sheet.pack(fill=BOTH, expand=YES)

>>>>>>>>> Temporary merge branch 2
    def display_message(self, message):
        """Display a message in the result frame."""
        for widget in self.ghp_gui.result_frame.winfo_children():
            widget.destroy()

        label = ttk.Label(self.ghp_gui.result_frame, text=message, bootstyle=DANGER)
        label.pack(fill=X, pady=10)


if __name__ == "__main__":
    app = ttk.Window("GHP and MRP Application", "litera", resizable=(False, False))
    MainWindow(app)
    app.mainloop()