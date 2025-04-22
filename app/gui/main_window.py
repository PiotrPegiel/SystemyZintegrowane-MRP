import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.bom import BOM, Material
from src.ghp import GHP
from src.mrp import MRP
from gui.bom_gui import BOMGUI
from gui.ghp_gui import GHPGUI
from gui.mrp_gui import MRPGUI


class MainWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # Initialize BOM, GHP, and MRP
        self.LEFT_FRAME = ttk.Frame(self)
        self.LEFT_FRAME.pack(side=LEFT)
        self.RIGHT_FRAME = ttk.Frame(self)
        self.RIGHT_FRAME.pack(side=RIGHT)
        self.MRP_frame = ttk.Frame(self.RIGHT_FRAME)
        self.MRP_frame.pack(fill=BOTH, expand=YES,side=BOTTOM)
        self.bom = BOM()
        self.ghp_system = GHP(self.bom)
        self.time_periods = 10  # Default value, user can change this later

        # Create BOM GUI
        self.bom_gui = BOMGUI(self.LEFT_FRAME, self.bom, self.on_material_added)

        # Create input for "Number of Time Periods"
        self.create_time_period_input()

        # Create GHP GUI
        self.ghp_gui = GHPGUI(self.RIGHT_FRAME, self.ghp_system, self.time_periods_var, self.display_message)

        # Create "Calculate GHP" button
        self.create_calculate_ghp_button()
        
        # Create "Load Hardcoded Data" button
        self.create_load_hardcoded_data_button()

    def create_time_period_input(self):
        """Create input field for the number of time periods."""
        action_frame = ttk.Frame(master=self.LEFT_FRAME)
        action_frame.pack(fill=X, pady=10)

        time_periods_label = ttk.Label(action_frame, text="Number of Time Periods")
        time_periods_label.pack(side=LEFT, padx=5)

        self.time_periods_var = ttk.IntVar(value=10)  # Default value
        time_periods_entry = ttk.Entry(action_frame, textvariable=self.time_periods_var, width=5)
        time_periods_entry.pack(side=LEFT, padx=5)

    def create_calculate_ghp_button(self):
        """Create the 'Calculate GHP' button."""
        self.calculate_ghp_button = ttk.Button(
            master=self.LEFT_FRAME,
            text="Calculate GHP",
            bootstyle=PRIMARY,
            command=self.calculate_ghp,
        )
        self.calculate_ghp_button.pack(side=TOP, pady=10)
        self.calculate_ghp_button.pack_forget()  # Initially hidden

    def create_load_hardcoded_data_button(self):
        """Create the 'Load Hardcoded Data' button."""
        load_button = ttk.Button(
            master=self.LEFT_FRAME,
            text="Load hardcoded data",
            bootstyle=SUCCESS,
            command=self.load_hardcoded_data,
        )
        load_button.pack(side=TOP, pady=10)

    def load_hardcoded_data(self):
        """Load hardcoded data into the BOM, GHP, and MRP."""
        try:
            # Clear existing BOM
            self.bom = BOM()

            # Create hardcoded BOM
            papier_toaletowy = Material(name="papier toaletowy", stock=200, production_time=1)
            rolka = Material(name="rolka", parent="papier toaletowy", quantity_needed=1, stock=22, production_time=2, production_capacity=100)
            makulatura = Material(name="makulatura", parent="rolka", quantity_needed=5, stock=200, production_time=1, production_capacity=150)
            papier = Material(name="papier", parent="papier toaletowy", quantity_needed=3, stock=50, production_time=1, production_capacity=120)
            masa_papiernicza = Material(name="masa papiernicza", parent="papier", quantity_needed=2, stock=80, production_time=3, production_capacity=400)

            papier_toaletowy.add_child(rolka)
            papier_toaletowy.add_child(papier)
            rolka.add_child(makulatura)
            papier.add_child(masa_papiernicza)

            self.bom.add_material(papier_toaletowy)
            self.bom.add_material(rolka)
            self.bom.add_material(makulatura)
            self.bom.add_material(papier)
            self.bom.add_material(masa_papiernicza)

            # Notify BOM GUI
            self.bom_gui.bom = self.bom
            self.bom_gui.update_product_list()

            self.calculate_ghp_button.pack(side=TOP, pady=10)
            self.ghp_system = GHP(self.bom)
            self.ghp_gui = GHPGUI(self.RIGHT_FRAME, self.ghp_system, self.time_periods_var, self.display_message)
            self.bom_gui.create_additional_form()
            self.bom_gui.create_additional_form()
            



        except Exception as e:
            self.display_message(f"Error: {str(e)}")

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

            try:
                self.calculate_mrp_button.destroy()  # Destroy the old button if it exists
            except AttributeError:
                pass
            

            self.calculate_mrp_button = ttk.Button(
            master=self.RIGHT_FRAME,
            text="Calculate MRP",
            bootstyle=PRIMARY,
            command=self.calculate_mrp    # Placeholder for MRP calculation
            )
            self.calculate_mrp_button.pack(side=TOP, pady=10)
            
            

            
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

    def calculate_mrp(self):
        """Calculate and display MRP results."""
        try:
            # Get the number of time periods from the input field
            time_periods = self.time_periods_var.get()
            if time_periods <= 0:
                raise ValueError("Number of time periods must be a positive integer.")

            # Convert GHP data to numeric values
            demand = [int(value) if str(value).strip().isdigit() else 0 for value in self.ghp_gui.sheet.data[0]]
            production = [int(value) if str(value).strip().isdigit() else 0 for value in self.ghp_gui.sheet.data[1]]
            table_size = len(demand)  # Determine table size from demand

            # Recalculate GHP with sanitized data
            ghp_system = GHP(self.bom)
            ghp_system.calculate_ghp(demand, production, table_size)

            # Initialize planned deliveries with zeros
            planned_deliveries = {
                material.name: [0] * table_size for material in self.bom.materials
            }

            # Create and calculate MRP system
            mrp_system = MRP(self.bom, ghp_system, table_size, planned_deliveries)
            mrp_system.calculate_mrp()

            # Initialize MRP GUI
            for widget in self.MRP_frame.winfo_children():
                widget.destroy()

            mrp_gui = MRPGUI(self.MRP_frame, mrp_system, time_periods)

            # Display MRP tables
            mrp_gui.display_mrp_tables()
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

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