from bom import BOM, Material
from ghp import GHP

class MRPTable:
    def __init__(self, material_name, table_size):
        """
        Initializes an MRP table for a specific material.
        :param material_name: The name of the material.
        :param table_size: The number of time periods.
        """
        self.material_name = material_name
        self.demand = [0] * table_size
        self.planned_delivery = [0] * table_size
        self.available = [0] * table_size
        self.net_requirement = [0] * table_size
        self.planned_order = [0] * table_size
        self.planned_receipt = [0] * table_size

class MRP:
    def __init__(self, bom, ghp, table_size, planned_delivery):
        """
        Initializes the MRP system with the given BOM, GHP, and table size.
        :param bom: The Bill of Materials object.
        :param ghp: The GHP object.
        :param table_size: The number of time periods.
        """
        self.bom = bom
        self.ghp = ghp
        self.table_size = table_size
        self.planned_delivery = planned_delivery
        self.mrp_tables = {}

    def order_bom_by_level(self):
        """
        Orders the materials in the BOM by level (increasing).
        """
        ordered_materials = []
        level = 0
        while True:
            materials_at_level = self.bom.get_materials_by_level(level)
            if not materials_at_level:
                break
            ordered_materials.extend(materials_at_level)
            level += 1
        return ordered_materials

    def calculate_mrp(self):
        """
        Calculates the MRP tables for all materials in the BOM.
        """
        # Order materials by level
        ordered_materials = self.order_bom_by_level()

        # Process each material in order
        for material in ordered_materials:
            if material.parent is None:
                # Skip level 0 material (no MRP table needed)
                continue

            # Create an MRP table for the material
            mrp_table = MRPTable(material.name, self.table_size)

            # Use planned delivery if available
            mrp_table.planned_delivery = self.planned_delivery.get(material.name, [0] * self.table_size)

            # Calculate demand
            if self.bom.level_0_material and material.parent == self.bom.level_0_material.name:
                # Level 1 materials: demand comes from GHP production with left offset
                ghp_production = self.ghp.get_tables()["production"]
                offset = self.bom.level_0_material.production_time
                mrp_table.demand = [
                    (ghp_production[i + offset] if i + offset < self.table_size else 0) * material.quantity_needed
                    for i in range(self.table_size)
                ]
            else:
                # Level >= 2 materials: demand comes from parent's planned order
                parent_table = self.mrp_tables[material.parent]
                mrp_table.demand = [
                    parent_table.planned_order[i] * material.quantity_needed
                    for i in range(self.table_size)
                ]

            # Calculate net requirement, planned order, planned receipt, and availability
            for t in range(self.table_size):
                if t == 0:
                    available = material.stock + mrp_table.planned_delivery[t] + mrp_table.planned_receipt[t] - mrp_table.demand[t]
                else:
                    available = (
                        mrp_table.available[t - 1]
                        + mrp_table.planned_delivery[t]
                        + mrp_table.planned_receipt[t]  # Add planned receipt only at this index
                        - mrp_table.demand[t]
                    )

                if available < 0:
                    mrp_table.net_requirement[t] = abs(available)
                    # Find latest planned order with value != 0
                    latest_planned_order_index = 0
                    for i in range(t, -1, -1):
                        if mrp_table.planned_order[i] != 0:
                            latest_planned_order_index = i
                            break
                    if latest_planned_order_index < t and latest_planned_order_index + material.production_time <= t:
                        # Create a new planned order
                        release_time = max(0, t - material.production_time)
                        mrp_table.planned_order[release_time] += material.production_capacity
                        receipt_time = release_time + material.production_time  # Receipt does not always happen at current index
                        if receipt_time < self.table_size:
                            mrp_table.planned_receipt[receipt_time] += material.production_capacity

                if t == 0:
                    available = material.stock + mrp_table.planned_delivery[t] + mrp_table.planned_receipt[t] - mrp_table.demand[t]
                else:
                    available = (
                        mrp_table.available[t - 1]
                        + mrp_table.planned_delivery[t]
                        + mrp_table.planned_receipt[t]  # Add planned receipt only at this index
                        - mrp_table.demand[t]
                    )

                mrp_table.available[t] = available

            # Store the MRP table
            self.mrp_tables[material.name] = mrp_table

    def display_mrp(self):
        """
        Displays the MRP tables for all materials except for level 0 materials.
        """
        for material_name, table in self.mrp_tables.items():
            print(f"MRP for {material_name}:")
            print(f"  Demand: {table.demand}")
            print(f"  Planned Delivery: {table.planned_delivery}")
            print(f"  Available: {table.available}")
            print(f"  Net Requirement: {table.net_requirement}")
            print(f"  Planned Order: {table.planned_order}")
            print(f"  Planned Receipt: {table.planned_receipt}")
            print()

# Example of usage:
if __name__ == "__main__":
    # Creating a sample BOM for the table
    table = Material(name="Table", stock=2, production_time=1)
    countertop = Material(name="Countertop", parent="Table", quantity_needed=1, stock=22, production_time=3, production_capacity=40)
    wooden_plate = Material(name="Wooden Plate", parent="Countertop", quantity_needed=1, stock=10, production_time=1, production_capacity=50)
    legs = Material(name="Legs", parent="Table", quantity_needed=4, stock=40, production_time=2, production_capacity=120)
    table.add_child(countertop)
    table.add_child(legs)
    countertop.add_child(wooden_plate)
    bom = BOM()
    bom.add_material(table)
    bom.add_material(countertop)
    bom.add_material(wooden_plate)
    bom.add_material(legs)

    # Create GHP
    ghp_system = GHP(bom)
    demand = [0, 0, 0, 0, 20, 0, 40, 0, 0, 0] # Example demand for the Table
    production = [0, 0, 0, 0, 28, 0, 30, 0, 0, 0] # Example production for the Table
    table_size = len(demand)  # Determine table size from demand
    ghp_system.calculate_ghp(demand, production, table_size)
    ghp_production = ghp_system.get_tables()['production']
    
    # Planned_delivery
    planned_deliveries = {
        "Countertop": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Wooden Plate": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Legs": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    # Create MRP system and calculate
    mrp_system = MRP(bom, ghp_system, table_size, planned_deliveries)
    mrp_system.calculate_mrp()
    
    # Display MRP results
    mrp_system.display_mrp()

    # Second variant
    planned_deliveries = {
        "Countertop": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Wooden Plate": [30, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Legs": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    mrp_system = MRP(bom, ghp_system, table_size, planned_deliveries)
    mrp_system.calculate_mrp()
    mrp_system.display_mrp()

    # Expected output:
    # countertop:
    # demand: [0, 0, 0, 28, 0, 30, 0, 0, 0, 0]
    # planned delivery: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # available: [22, 22, 22, 34, 34, 4, 4, 4, 4, 4]
    # net requirement: [0, 0, 0, 6, 0, 0, 0, 0, 0, 0]
    # planned order: [40, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned receipt: [0, 0, 0, 40, 0, 0, 0, 0, 0, 0]

    # wooden plate:
    # demand: [40, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned delivery: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # available: [-30, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    # net requirement: [30, 30, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned order: [50, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned receipt: [0, 50, 0, 0, 0, 0, 0, 0, 0, 0]

    # Legs:
    # demand: [0, 0, 0, 112, 0, 120, 0, 0, 0, 0]
    # planned delivery: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # available: [40, 40, 40, 48, 48, 48, 48, 48, 48, 48]
    # net requirement: [0, 0, 0, 72, 0, 72, 0, 0, 0, 0]
    # planned order: [0, 120, 0, 120, 0, 0, 0, 0, 0, 0]
    # planned receipt: [0, 0, 0, 120, 0, 120, 0, 0, 0, 0]

    # In another scenario, user could choose to order from outside and the wooden plate would look like this:
    # wooden plate:
    # demand: [40, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned delivery: [30, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # available: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # net requirement: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned order: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # planned receipt: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]