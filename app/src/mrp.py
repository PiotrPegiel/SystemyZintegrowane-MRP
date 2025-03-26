from bom import BOM, Material
from ghp import GHP

class MRP:
    def __init__(self, bom):
        """
        Initializes the MRP system with the given Bill of Materials (BOM).
        :param bom: The Bill of Materials object.
        """
        self.bom = bom
        self.materials = bom.materials
        self.planned_orders = {}

    def calculate_mrp(self, ghp_demand, planned_deliveries, time_periods):
        """
        Calculate the MRP for all materials.
        :param ghp_demand: A list representing demand for the level 0 product for each time period.
        :param planned_deliveries: A dictionary where keys are material names and values are their planned deliveries.
        :param time_periods: The number of periods for which to calculate MRP.
        """
        # Start with the level 0 material
        level_0_material = self.bom.level_0_material
        if not level_0_material:
            raise ValueError("No level 0 material found in BOM.")

        # Recursively calculate MRP for all materials
        self._calculate_mrp_recursive(level_0_material, ghp_demand, planned_deliveries, time_periods)

    def _calculate_mrp_recursive(self, material, ghp_demand, planned_deliveries, time_periods):
        """
        Recursively calculate MRP for a material and its children.
        :param material: The current material to process.
        :param ghp_demand: A list representing demand for the level 0 product for each time period.
        :param planned_deliveries: A dictionary where keys are material names and values are their planned deliveries.
        :param time_periods: The number of periods for which to calculate MRP.
        """
        # Pass the planned delivery for the current material
        planned_delivery = planned_deliveries.get(material.name, [0] * time_periods)

        # If this is a level 0 material, skip further calculations
        if material.parent is None:
            return

        # Calculate MRP for the current material
        self.calculate_material_mrp(material, ghp_demand, planned_delivery, time_periods)

        # Recursively calculate MRP for all child materials
        for child in material.children:
            self._calculate_mrp_recursive(child, ghp_demand, planned_deliveries, time_periods)

    def calculate_material_mrp(self, material, ghp_demand, planned_delivery, time_periods):
        """
        Calculate MRP for a specific material.
        :param material: Material object to calculate.
        :param ghp_demand: The GHP demand for the level 0 product.
        :param planned_delivery: The planned delivery for this material.
        :param time_periods: The number of periods to consider.
        """
        # Initialize MRP for this material
        demand = [0] * time_periods
        available = [material.stock] + [0] * (time_periods - 1)
        net_requirement = [0] * time_periods
        planned_order = [0] * time_periods
        planned_receipt = [0] * time_periods

        # Get parent demand (for level 1 and beyond)
        if material.parent is None:
            return
        parent_demand = self.planned_orders[material.parent]["planned_order"]

        for t in range(time_periods):
            # Calculate demand based on parent planned orders
            demand[t] = parent_demand[t] * material.quantity_needed

            # Calculate net requirement and availability
            if t == 0:
                available[t] = material.stock - demand[t] - planned_delivery[t]
            else:
                available[t] = available[t - 1] + planned_receipt[t - 1] - demand[t] - planned_delivery[t]

            if available[t] < 0:
                # Create net requirement to cover the shortage
                net_requirement[t] = abs(available[t])

                # Determine the release time for the planned order
                release_time = t - material.production_time
                if release_time >= 0:
                    planned_order[release_time] += net_requirement[t]
                    planned_receipt[t] += net_requirement[t]

                # Update availability after planned receipt
                available[t] += net_requirement[t]

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
        Displays the MRP results for all materials except for level 0 materials.
        """
        for material_name, data in self.planned_orders.items():
            # Skip level 0 materials
            if self.bom.get_material_by_name(material_name).parent is None:
                continue

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
    

    # Create MRP system and calculate
    mrp_system = MRP(bom)
    #planned_delivery = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    planned_deliveries = {
        "Countertop": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Wooden Plate": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Legs": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    mrp_system.calculate_mrp(ghp_production, planned_deliveries, table_size)
    
    # Display MRP results
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