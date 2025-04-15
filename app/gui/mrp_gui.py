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
                [value if value != 0 else "" for value in table.demand],  # Hide zeros in demand
                [value if value != 0 else "" for value in table.planned_delivery],  # Hide zeros in planned delivery
                table.available,  # Keep zeros in availability
                [value if value != 0 else "" for value in table.net_requirement],  # Hide zeros in net requirement
                [value if value != 0 else "" for value in table.planned_order],  # Hide zeros in planned order
                [value if value != 0 else "" for value in table.planned_receipt],  # Hide zeros in planned receipt
            ]

            # Create the Sheet widget and store it in the sheets dictionary
            sheet = Sheet(
                frame,
                data=data,
                headers=headers,
                row_index=indexes,
                default_column_width=35,
                default_row_index_width=150,
                row_index_align="e",
                align=CENTER,
                height=230,
                width=550,
            )
            sheet.enable_bindings()
            sheet.pack(fill=BOTH, expand=YES)

            # Store the sheet reference for this material
            self.sheets[material_name] = sheet

            # Bind the "edit_cell" event to the on_cell_edit function
            self.bind_sheet_events(sheet, material_name)

    def bind_sheet_events(self, sheet, material_name):
        """Bind events to the Sheet widget for editing."""
        def on_cell_edit(event):
            try:
                # Get the modified cell's row and column
                row = event["row"]
                col = event["column"]

                # Get the cell data and convert it to an integer (default to 0 if empty)
                cell_data = sheet.get_cell_data(row, col)
                value = int(cell_data) if cell_data.strip() else 0

                # Update the corresponding MRP table data
                table = self.mrp_system.mrp_tables[material_name]
                if row == 0:  # Demand row
                    table.demand[col] = value
                elif row == 1:  # Planned Delivery row
                    table.planned_delivery[col] = value

                # Recalculate MRP
                self.mrp_system.calculate_mrp()

                # Refresh the table data
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


            sheet_data = [
                [value if value != 0 else "" for value in table.demand],  # Hide zeros in demand
                [value if value != 0 else "" for value in table.planned_delivery],  # Hide zeros in planned delivery
                table.available,  # Keep zeros in availability
                [value if value != 0 else "" for value in table.net_requirement],  # Hide zeros in net requirement
                [value if value != 0 else "" for value in table.planned_order],  # Hide zeros in planned order
                [value if value != 0 else "" for value in table.planned_receipt],  # Hide zeros in planned receipt
            ]
 

            sheet.set_sheet_data(
                data = sheet_data
            )