class Material:
    def __init__(self, name, parent, quantity_needed, stock, production_time, production_capacity, available):
        """
        Initializes a Material object.
        :param name: The name of the material.
        :param parent: The parent material (None for top-level items).
        :param quantity_needed: Quantity needed for production of parent item.
        :param stock: Initial stock available.
        :param production_time: Time required to produce the material.
        :param production_capacity: Maximum production capacity per period.
        :param available: Available quantity.
        """
        self.name = name
        self.parent = parent
        self.quantity_needed = quantity_needed
        self.stock = stock
        self.production_time = production_time
        self.production_capacity = production_capacity
        self.available = available
        self.children = []

    def add_child(self, material):
        """ Add a child material to this material (used for BOM). """
        self.children.append(material)

class MRP:
    def __init__(self, bom):
        """
        Initializes the MRP system with the given Bill of Materials (BOM).
        :param bom: The Bill of Materials object.
        """
        self.bom = bom
        self.materials = bom.materials
        self.planned_orders = {}

    def calculate_mrp(self, ghp_demand, time_periods):
        """
        Calculate the MRP for the given number of time periods, considering GHP demand.
        :param ghp_demand: A list representing demand for the level 0 product for each time period.
        :param time_periods: The number of periods for which to calculate MRP.
        """
        # For each material at level 0 (starting point)
        for material in self.materials:
            if material.parent is None:  # Only process level 0 products for GHP
                self.calculate_material_mrp(material, ghp_demand, time_periods)

    def calculate_material_mrp(self, material, ghp_demand, time_periods):
        """
        Calculate MRP for a specific material.
        :param material: Material object to calculate.
        :param ghp_demand: The GHP demand for the level 0 product.
        :param time_periods: The number of periods to consider.
        """
        # Initialize MRP for this material
        demand = [0] * time_periods
        planned_delivery = [0] * time_periods
        available = [material.available] * time_periods
        net_requirement = [0] * time_periods
        planned_order = [0] * time_periods
        planned_receipt = [0] * time_periods

        # For level 0 product (GHP)
        if material.parent is None:
            for t in range(time_periods):
                # Demand for level 0 from GHP
                demand[t] = ghp_demand[t]
                # Update stock based on GHP production
                available[t] = material.stock + demand[t] - planned_delivery[t]

        # For level 1 and beyond (MRP)
        else:
            # Calculate the demand based on parent demand (or child level demand)
            for t in range(time_periods):
                if material.parent:  # If it's not level 0
                    # Demand based on parent level (multiplied by quantity needed in BOM)
                    parent_demand = demand[t] if material.parent is not None else 0
                    demand[t] = parent_demand * material.quantity_needed

            # Now calculate MRP for each time period
            for t in range(time_periods):
                # Calculate the net requirement
                net_requirement[t] = max(demand[t] - available[t], 0)

                # If net requirement is positive, create a planned order
                if net_requirement[t] > 0:
                    # Create planned order in the period adjusted by lead time
                    release_time = t + material.production_time
                    if release_time < time_periods:
                        planned_order[release_time] += net_requirement[t]

                    # Add the planned receipt in future periods
                    for future_t in range(t + material.production_time, time_periods):
                        planned_receipt[future_t] += net_requirement[t]

                # Update available stock for future periods
                if t < time_periods - 1:
                    available[t + 1] = available[t] + planned_receipt[t] - demand[t + 1] - planned_delivery[t + 1]

        # Store results in planned_orders dictionary for material
        self.planned_orders[material.name] = {
            "demand": demand,
            "planned_delivery": planned_delivery,
            "available": available,
            "net_requirement": net_requirement,
            "planned_order": planned_order,
            "planned_receipt": planned_receipt
        }

    def display_mrp(self):
        """
        Displays the MRP results for all materials.
        """
        for material_name, data in self.planned_orders.items():
            print(f"MRP for {material_name}:")
            print(f"  Demand: {data['demand']}")
            print(f"  Planned Delivery: {data['planned_delivery']}")
            print(f"  Available: {data['available']}")
            print(f"  Net Requirement: {data['net_requirement']}")
            print(f"  Planned Order: {data['planned_order']}")
            print(f"  Planned Receipt: {data['planned_receipt']}")
            print()

# Example of usage:
if __name__ == "__main__":
    # Creating a sample BOM
    table = Material(name="Table", parent=None, quantity_needed=1, stock=2, production_time=1, production_capacity=40, available=2)
    countertop = Material(name="Countertop", parent="Table", quantity_needed=1, stock=22, production_time=3, production_capacity=40, available=22)
    wooden_plate = Material(name="Wooden Plate", parent="Countertop", quantity_needed=1, stock=10, production_time=1, production_capacity=50, available=10)
    legs = Material(name="Legs", parent="Table", quantity_needed=4, stock=40, production_time=2, production_capacity=120, available=40)

    # Add child materials to BOM
    table.add_child(countertop)
    table.add_child(legs)
    countertop.add_child(wooden_plate)

    # Create BOM and add materials
    bom = BOM()
    bom.add_material(table)
    bom.add_material(countertop)
    bom.add_material(wooden_plate)
    bom.add_material(legs)

    # Create MRP system and calculate
    mrp_system = MRP(bom)
    ghp_demand = [0, 0, 0, 0, 20, 0, 40, 0, 0, 0]  # Example GHP demand for the table
    mrp_system.calculate_mrp(ghp_demand, time_periods=10)

    # Display MRP results
    mrp_system.display_mrp()
