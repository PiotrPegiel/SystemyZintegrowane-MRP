import customtkinter as ctk
from src.bom import Material, BOM
from src.ghp import GHP


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GHP and BOM Application")
        self.geometry("900x700")

        # Initialize BOM and GHP
        self.bom = BOM()
        self.ghp_system = GHP(self.bom)

        # Initialize dynamic material list and GUI elements
        self.materials = []
        self.time_periods = 10  # Default value, user can change this later

        # Labels and inputs for creating BOM
        self.material_frame = ctk.CTkFrame(self)
        self.material_frame.pack(pady=20)

        self.material_name_label = ctk.CTkLabel(self.material_frame, text="Material Name")
        self.material_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.material_name_entry = ctk.CTkEntry(self.material_frame)
        self.material_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.quantity_needed_label = ctk.CTkLabel(self.material_frame, text="Quantity Needed")
        self.quantity_needed_label.grid(row=1, column=0, padx=10, pady=10)

        self.quantity_needed_entry = ctk.CTkEntry(self.material_frame)
        self.quantity_needed_entry.grid(row=1, column=1, padx=10, pady=10)

        self.stock_label = ctk.CTkLabel(self.material_frame, text="Stock")
        self.stock_label.grid(row=2, column=0, padx=10, pady=10)

        self.stock_entry = ctk.CTkEntry(self.material_frame)
        self.stock_entry.grid(row=2, column=1, padx=10, pady=10)

        self.production_time_label = ctk.CTkLabel(self.material_frame, text="Production Time")
        self.production_time_label.grid(row=3, column=0, padx=10, pady=10)

        self.production_time_entry = ctk.CTkEntry(self.material_frame)
        self.production_time_entry.grid(row=3, column=1, padx=10, pady=10)

        self.production_capacity_label = ctk.CTkLabel(self.material_frame, text="Production Capacity")
        self.production_capacity_label.grid(row=4, column=0, padx=10, pady=10)

        self.production_capacity_entry = ctk.CTkEntry(self.material_frame)
        self.production_capacity_entry.grid(row=4, column=1, padx=10, pady=10)

        self.add_material_button = ctk.CTkButton(self.material_frame, text="Add Material", command=self.add_material)
        self.add_material_button.grid(row=5, columnspan=2, pady=10)

        # self.material_listbox = ctk.CTkListbox(self, height=10)
        # self.material_listbox.pack(pady=20)

        # Demand input
        self.demand_label = ctk.CTkLabel(self, text="Demand for Level 0 Product (e.g., [0, 0, 0, 0, 20, 0, 40, 0, 0, 0])")
        self.demand_label.pack(pady=10)

        self.demand_entry = ctk.CTkEntry(self, placeholder_text="Enter demand for Table")
        self.demand_entry.pack(pady=10)

        self.time_periods_label = ctk.CTkLabel(self, text="Time Periods (number of columns for GHP/MRP)")
        self.time_periods_label.pack(pady=10)

        self.time_periods_entry = ctk.CTkEntry(self, placeholder_text="Enter number of periods")
        self.time_periods_entry.pack(pady=10)

        # Calculate and display results
        self.calculate_button = ctk.CTkButton(self, text="Calculate GHP", command=self.calculate_ghp)
        self.calculate_button.pack(pady=20)

        self.result_text = ctk.CTkTextbox(self, width=700, height=300)
        self.result_text.pack(pady=10)

    def add_material(self):
        # Get input values from user
        name = self.material_name_entry.get()
        quantity_needed = int(self.quantity_needed_entry.get())
        stock = int(self.stock_entry.get())
        production_time = int(self.production_time_entry.get())
        production_capacity = int(self.production_capacity_entry.get())

        # Create material and add it to the BOM
        material = Material(name=name, parent=None, quantity_needed=quantity_needed, stock=stock, production_time=production_time, production_capacity=production_capacity, available=stock)
        self.bom.add_material(material)
        self.materials.append(material)

        # Add material to listbox
        self.material_listbox.insert(ctk.END, name)

        # Clear the input fields
        self.material_name_entry.delete(0, ctk.END)
        self.quantity_needed_entry.delete(0, ctk.END)
        self.stock_entry.delete(0, ctk.END)
        self.production_time_entry.delete(0, ctk.END)
        self.production_capacity_entry.delete(0, ctk.END)

    def calculate_ghp(self):
        # Get demand from user input
        try:
            demand_input = self.demand_entry.get()
            demand = eval(demand_input)  # Convert input to list (assuming input is in correct format)
            if isinstance(demand, list) and all(isinstance(i, int) for i in demand):
                self.time_periods = len(demand)

                # Get the number of time periods
                time_periods_input = self.time_periods_entry.get()
                if time_periods_input:
                    self.time_periods = int(time_periods_input)

                # Calculate GHP
                self.ghp_system.calculate_ghp(demand, time_periods=self.time_periods)
                result = self.ghp_system.display_ghp()

                # Display results in Textbox
                self.result_text.delete(1.0, ctk.END)  # Clear previous results
                for material_name, data in result.items():
                    self.result_text.insert(ctk.END, f"GHP for {material_name}:\n")
                    self.result_text.insert(ctk.END, f"  Demand: {data['demand']}\n")
                    self.result_text.insert(ctk.END, f"  Production: {data['production']}\n")
                    self.result_text.insert(ctk.END, f"  Available Stock: {data['available_stock']}\n\n")
            else:
                self.result_text.delete(1.0, ctk.END)
                self.result_text.insert(ctk.END, "Invalid input format. Please enter a valid list of integers.")
        except Exception as e:
            self.result_text.delete(1.0, ctk.END)
            self.result_text.insert(ctk.END, f"Error: {str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
