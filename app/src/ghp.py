from bom import BOM
from bom import Material

class GHP:
    def __init__(self, bom):
        """
        Initializes the GHP system with the given Bill of Materials (BOM).
        :param bom: The Bill of Materials object.
        """
        self.bom = bom
        self.production_schedule = {}

    def calculate_ghp(self, demand, production, table_size):
        """
        Calculate the GHP for the level 0 material.
        :param demand: A list representing the demand for the level 0 product.
        :param production: A list representing the production for the level 0 product.
        :param table_size: The size of the demand and production tables.
        """
        # Get the level 0 material from BOM
        level_0_material = next((m for m in self.bom.materials if m.parent is None), None)
        if not level_0_material:
            raise ValueError("No level 0 material found in BOM.")

        # Initialize the availability table
        availability = [0] * table_size

        # Calculate availability for each time period
        for t in range(table_size):
            if t == 0:
                availability[t] = level_0_material.stock + production[t] - demand[t]
            else:
                availability[t] = availability[t - 1] + production[t] - demand[t]

        # Store the results in the production schedule dictionary
        self.production_schedule[level_0_material.name] = {
            "demand": demand,
            "production": production,
            "availability": availability
        }

        return availability

    def get_tables(self):
        """
        Retrieve the demand, production, and availability tables for the level 0 material.
        :return: A dictionary containing the tables for the level 0 material.
        """
        if not self.production_schedule:
            raise ValueError("No production schedule available. Please calculate GHP first.")

        # Assuming only one level 0 material exists
        material_name, data = next(iter(self.production_schedule.items()))
        return {
            "material_name": material_name,
            "demand": data["demand"],
            "production": data["production"],
            "availability": data["availability"]
        }

    def display_ghp(self):
        """
        Display the GHP results for the level 0 material.
        """
        for material_name, data in self.production_schedule.items():
            print(f"GHP for {material_name}:")
            print(f"  Demand: {data['demand']}")
            print(f"  Production: {data['production']}")
            print(f"  Availability: {data['availability']}")
            print()

# Example of usage:
if __name__ == "__main__":
    # Create a Bill of Materials (BOM)
    bom = BOM()
    table = Material(name="Table", stock=2, production_time=1)
    bom.add_material(table)

    # Create GHP system and calculate
    ghp_system = GHP(bom)
    demand = [0, 0, 0, 0, 20, 0, 40, 0, 0, 0] # Example demand for the Table
    production = [0, 0, 0, 0, 28, 0, 30, 0, 0, 0] # Example production for the Table
    table_size = len(demand)  # Determine table size from demand

    # Calculate GHP
    availability = ghp_system.calculate_ghp(demand, production, table_size)

    # Display GHP results
    ghp_system.display_ghp()

    # Print the availability table
    print("Availability Table:", availability)