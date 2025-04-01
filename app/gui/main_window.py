import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tksheet import Sheet
from src.bom import BOM
from src.ghp import GHP
from src.mrp import MRP
from gui.bom_gui import BOMGUI


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

        # Create buttons for GHP and MRP
        self.create_action_buttons()

        # Create result display area
        self.result_frame = ttk.Frame(self)
        self.result_frame.pack(fill=BOTH, expand=YES, pady=10)

    def create_action_buttons(self):
        """Create buttons for GHP and MRP actions."""
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=X, pady=10)

        demand_label = ttk.Label(action_frame, text="Demand (e.g., [0, 0, 20, 0, 40])")
        demand_label.pack(side=LEFT, padx=5)

        self.demand = ttk.StringVar(value="")
        demand_entry = ttk.Entry(action_frame, textvariable=self.demand)
        demand_entry.pack(side=LEFT, padx=5, fill=X, expand=YES)

        calculate_ghp_button = ttk.Button(
            master=action_frame,
            text="Calculate GHP",
            bootstyle=PRIMARY,
            command=self.calculate_ghp,
        )
        calculate_ghp_button.pack(side=LEFT, padx=5)

        calculate_mrp_button = ttk.Button(
            master=action_frame,
            text="Get MRP",
            bootstyle=INFO,
            command=self.calculate_mrp,
        )
        calculate_mrp_button.pack(side=LEFT, padx=5)

    def on_material_added(self, material):
        """Callback when a material is added."""
        print(f"Material added: {material.name}")

    def calculate_ghp(self):
        """Calculate and display GHP results."""
        try:
            demand = eval(self.demand.get())
            if not isinstance(demand, list) or not all(isinstance(i, int) for i in demand):
                raise ValueError("Demand must be a list of integers.")

            self.time_periods = len(demand)
            production = [0] * self.time_periods  # Example production, can be modified
            availability = self.ghp_system.calculate_ghp(demand, production, self.time_periods)

            self.display_ghp_table(demand, production, availability)
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

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

        sheet = Sheet(self.result_frame, data=data, headers=headers, row_index=indexes)
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

    def display_message(self, message):
        """Display a message in the result frame."""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        label = ttk.Label(self.result_frame, text=message, bootstyle=DANGER)
        label.pack(fill=X, pady=10)


if __name__ == "__main__":
    app = ttk.Window("GHP and MRP Application", "litera", resizable=(False, False))
    MainWindow(app)
    app.mainloop()