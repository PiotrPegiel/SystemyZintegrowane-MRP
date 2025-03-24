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


class BOM:
    def __init__(self):
        """ Initialize BOM with a materials list. """
        self.materials = []

    def add_material(self, material):
        """ Add a material to BOM. """
        self.materials.append(material)

    def display_bom(self):
        """ Display the BOM structure (materials and their children). """
        for material in self.materials:
            print(f"{material.name} (Production Time: {material.production_time}, Available: {material.available})")
            for child in material.children:
                print(f"  -> {child.name} (Needed: {child.quantity_needed}, Available: {child.available})")


# Example Usage:
if __name__ == "__main__":
    # Creating a sample BOM for the table
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

    # Display BOM structure
    bom.display_bom()
