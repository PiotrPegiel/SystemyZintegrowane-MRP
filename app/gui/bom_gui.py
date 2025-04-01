import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.bom import Material
from .collapsing_frame import CollapsingFrame


class BOMGUI(ttk.Frame):
    def __init__(self, master, bom, on_material_added):
        super().__init__(master, padding=(10, 10))
        self.pack(fill=BOTH, expand=YES)

        self.bom = bom
        self.on_material_added = on_material_added

        # Form variables
        self.material_name = ttk.StringVar(value="")
        self.stock = ttk.IntVar(value=0)
        self.production_time = ttk.IntVar(value=0)
        self.parent = ttk.StringVar(value="")
        self.quantity_needed = ttk.IntVar(value=0)
        self.production_capacity = ttk.IntVar(value=0)

        # Create form for BOM input
        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(fill=X, pady=10)
        self.create_initial_form()

        # Create collapsible frame for product list
        self.product_list_frame = CollapsingFrame(self)
        self.product_list_frame.pack(fill=BOTH, expand=YES, pady=10)

    def create_initial_form(self):
        """Create the initial form for level 0 material input."""
        self.clear_form()
        self.create_form_entry("Material Name", self.material_name, self.form_frame)
        self.create_form_entry("Stock", self.stock, self.form_frame)
        self.create_form_entry("Production Time", self.production_time, self.form_frame)

        self.add_button = ttk.Button(
            master=self.form_frame,
            text="Add Material",
            bootstyle=SUCCESS,
            command=self.add_material,
        )
        self.add_button.pack(side=RIGHT, padx=5, pady=5)

    def create_additional_form(self):
        """Create additional form fields for child materials."""
        self.clear_form()
        self.create_form_entry("Material Name", self.material_name, self.form_frame)
        self.create_form_entry("Parent", self.parent, self.form_frame, is_combobox=True)
        self.create_form_entry("Stock", self.stock, self.form_frame)
        self.create_form_entry("Quantity Needed", self.quantity_needed, self.form_frame)
        self.create_form_entry("Production Time", self.production_time, self.form_frame)
        self.create_form_entry("Production Capacity", self.production_capacity, self.form_frame)

        self.add_button = ttk.Button(
            master=self.form_frame,
            text="Add Material",
            bootstyle=SUCCESS,
            command=self.add_material,
        )
        self.add_button.pack(side=RIGHT, padx=5, pady=5)

    def create_form_entry(self, label, variable, master, is_combobox=False):
        """Create a single form entry."""
        container = ttk.Frame(master=master)
        container.pack(fill=X, pady=5)

        lbl = ttk.Label(master=container, text=label, width=20)
        lbl.pack(side=LEFT, padx=5)

        if is_combobox:
            ent = ttk.Combobox(master=container, textvariable=variable, state="readonly")
            ent["values"] = [material.name for material in self.bom.materials]
        else:
            ent = ttk.Entry(master=container, textvariable=variable)

        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def clear_form(self):
        """Clear all widgets in the form frame."""
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def add_material(self):
        """Add a material to the BOM."""
        try:
            name = self.material_name.get()
            stock = self.stock.get()
            production_time = self.production_time.get()

            # Check if this is the first material (level 0 material)
            if self.bom.level_0_material is None:
                if not name:
                    self.display_message("Error: Material name cannot be empty.")
                    return

                material = Material(
                    name=name,
                    stock=stock,
                    production_time=production_time,
                )
                self.bom.add_material(material)

                # Notify the main window
                self.on_material_added(material)

                # Clear input fields
                self.material_name.set("")
                self.stock.set(0)
                self.production_time.set(0)

                # Show additional form fields for child materials
                self.create_additional_form()
            else:
                # Add child material
                parent_name = self.parent.get()
                quantity_needed = self.quantity_needed.get()
                production_capacity = self.production_capacity.get()

                # Retrieve the parent material object
                parent_material = self.bom.get_material_by_name(parent_name)
                if not parent_material:
                    self.display_message(f"Error: Parent material '{parent_name}' not found.")
                    return

                material = Material(
                    name=name,
                    parent=parent_material.name,
                    quantity_needed=quantity_needed,
                    stock=stock,
                    production_time=production_time,
                    production_capacity=production_capacity,
                )
                self.bom.add_material(material)
                parent_material.add_child(material)

                # Notify the main window
                self.on_material_added(material)

                # Clear input fields
                self.material_name.set("")
                self.stock.set(0)
                self.production_time.set(0)
                self.parent.set("")
                self.quantity_needed.set(0)
                self.production_capacity.set(0)

                # Refresh parent combobox values
                self.create_additional_form()

            # Update the product list
            self.update_product_list()
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

    def update_product_list(self):
        """Update the collapsible frame with the latest materials."""
        # Clear existing entries
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()

        # Add each material to the collapsible frame
        for material in self.bom.materials:
            frame = ttk.Frame(self.product_list_frame)
            label = ttk.Label(
                frame,
                text=f"{material.name} (Stock: {material.stock}, Production Time: {material.production_time})",
            )
            label.pack(fill=X, padx=5, pady=5)
            self.product_list_frame.add(frame, title=material.name, bootstyle=SECONDARY)

    def display_message(self, message):
        """Display a message in the collapsible frame."""
        label = ttk.Label(self.product_list_frame, text=message, bootstyle=DANGER)
        label.pack(fill=X, pady=10)