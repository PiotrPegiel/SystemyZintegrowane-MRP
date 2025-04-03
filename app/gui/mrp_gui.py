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

        # Store references to Sheet widgets for each material
        self.sheets = {}

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

            # Create the Sheet widget and store it in the sheets dictionary
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

            # Store the sheet reference for this material
            self.sheets[material_name] = sheet

            # Bind the "edit_cell" event to the on_cell_edit function
            self.bind_sheet_events(sheet, material_name)

    def bind_sheet_events(self, sheet, material_name):
        """
        Bind the edit_cell event for a specific sheet and material.
        """
        def on_cell_edit(event):
            try:
                # Get the modified cell's row and column
                row = event["row"]
                col = event["column"]

                # Update the planned delivery for the material
                if row == 1:  # Planned Delivery row
                    new_value = int(sheet.get_cell_data(row, col))
                    self.mrp_system.planned_delivery[material_name][col] = new_value

                    # Recalculate MRP tables
                    self.mrp_system.calculate_mrp()

                    # Refresh the data in all sheets
                    self.refresh_mrp_data()
            except ValueError:
                print("Error: Please enter a valid integer.")
            except Exception as e:
                print(f"Error: {str(e)}")

        # Bind the "edit_cell" event to the on_cell_edit function
        sheet.extra_bindings("edit_cell", on_cell_edit)

    def refresh_mrp_data(self):
        """
        Refresh the data in all MRP tables without recreating the widgets.
        """
        for material_name, sheet in self.sheets.items():
            table = self.mrp_system.mrp_tables[material_name]

            # Update the data in the existing Sheet widget
            sheet.set_sheet_data([
                table.demand,
                table.planned_delivery,
                table.available,
                table.net_requirement,
                table.planned_order,
                table.planned_receipt,
            ])