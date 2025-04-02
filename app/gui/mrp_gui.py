import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tksheet import Sheet   


class MRPGUI(ttk.Frame):
    def __init__(self, master, mrp_system, time_periods_var):
        """
        Initialize the MRP GUI.
        :param master: Parent widget.
        :param mrp_system: The MRP system object.
        :param time_periods_var: Variable for the number of time periods.
        """
        super().__init__(master, padding=(10, 10))
        self.pack(fill=BOTH, expand=YES)

        self.mrp_system = mrp_system
        self.time_periods_var = time_periods_var
        self.mrp_frame = ttk.Frame(self)
        self.mrp_frame.pack(fill=BOTH, expand=YES, pady=10)

    def display_mrp_tables(self):
        """
        Display MRP tables for all materials in the BOM.
        """
        # Clear any existing widgets in the result frame
        for widget in self.mrp_frame.winfo_children():
            widget.destroy()

        self.mrp_system.calculate_mrp()
        mrp_tables = self.mrp_system.mrp_tables
       

        # Create a tabbed interface for each material's MRP table
        notebook = ttk.Notebook(self.mrp_frame)
        notebook.pack(fill=BOTH, expand=YES)

        for material_name, table in mrp_tables.items():
            # Create a frame for each material
            frame = ttk.Frame(notebook, padding=(10, 10))
            notebook.add(frame, text=material_name)

            # Define table headers and data
            headers = [str(i + 1) for i in range(self.time_periods_var)]
            indexes = [
                "Demand",
                "Planned Delivery",
                "Available",
                "Net Requirement",
                "Planned Order",
                "Planned Receipt",
            ]
            data = [
                table.demand,
                table.planned_delivery,
                table.available,
                table.net_requirement,
                table.planned_order,
                table.planned_receipt,
            ]

            # Create the Sheet widget
            sheet = Sheet(
                frame,
                data=data,
                headers=headers,
                row_index=indexes,
                default_column_width=70,
                default_row_index_width=170,
                row_index_align="e",
                align=CENTER,
                height=280,
                width=500,
            )
            sheet.enable_bindings()
            sheet.pack(fill=BOTH, expand=YES)