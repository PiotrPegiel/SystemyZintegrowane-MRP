class GHP:
    def __init__(self, bom):
        """
        Initializes the GHP system with the given Bill of Materials (BOM).
        :param bom: The Bill of Materials object.
        """
        self.bom = bom
        self.materials = bom.materials
        self.production_schedule = {}

    def calculate_ghp(self, demand, time_periods):
        """
        Calculate the GHP for the given number of time periods.
        :param demand: A list representing the demand for the level 0 product (e.g., "Table").
        :param time_periods: The number of periods for which to calculate GHP.
        """
        # For each material in BOM
        for material in self.materials:
            self.calculate_material_ghp(material, demand, time_periods)

    def calculate_material_ghp(self, material, demand, time_periods):
        """
        Calculate the GHP for a specific material.
        :param material: Material object to calculate.
        :param demand: Demand for the level 0 product (which drives demand for level 1, 2, etc.).
        :param time_periods: Number of periods for which GHP is calculated.
        """
        # Initialize the GHP for this material
        available = [material.available] * time_periods
        production = [0] * time_periods
        available_stock = [material.available] * time_periods

        if material.parent is None:  # Only for level 0 products (i.e., Table)
            for t in range(time_periods):
                production[t] = demand[t]  # Production is equal to the demand for level 0
                available_stock[t] = available_stock[t-1] if t > 0 else material.available + production[t]

        # Store the results in the production schedule dictionary
        self.production_schedule[material.name] = {
            "demand": demand,
            "production": production,
            "available_stock": available_stock
        }

    def display_ghp(self):
        """
        Display the GHP results for all materials.
        """
        for material_name, data in self.production_schedule.items():
            print(f"GHP for {material_name}:")
            print(f"  Demand: {data['demand']}")
            print(f"  Production: {data['production']}")
            print(f"  Available Stock: {data['available_stock']}")
            print()


# Example of usage:
if __name__ == "__main__":
    # Create GHP system and calculate
    ghp_system = GHP(bom)
    demand = [0, 0, 0, 0, 20, 0, 40, 0, 0, 0]  # Example demand for the Table
    ghp_system.calculate_ghp(demand, time_periods=10)

    # Display GHP results
    ghp_system.display_ghp()
