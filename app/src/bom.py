class Material:
    def __init__(self, name, parent=None, quantity_needed=0, stock=0, production_time=0, production_capacity=0, available=0):
        """
        Initializes a Material object.
        :param name: The name of the material.
        :param parent: The parent material (None for top-level items).
        :param quantity_needed: Quantity needed for production of parent item.
        :param stock: Initial stock available.
        :param production_time: Time required to produce the material.
        :param production_capacity: Maximum production capacity per period.
        """
        self.name = name
        self.parent = parent
        self.quantity_needed = quantity_needed
        self.stock = stock
        self.production_time = production_time
        self.production_capacity = production_capacity
        self.children = []

    def add_child(self, material):
        """ Add a child material to this material (used for BOM). """
        self.children.append(material)


class BOM:
    def __init__(self):
        """ Initialize BOM with a materials list. """
        self.materials = []
        self.level_0_material = None # Track the single level 0 material

    def add_material(self, material):
        """ Add a material to BOM. """
        if material.parent is None:  # Check if it's a level 0 material
            if self.level_0_material is not None:
                raise ValueError("Only one level 0 material is allowed in the BOM.")
            self.level_0_material = material
        self.materials.append(material)

    def display_bom(self):
        """ Display the BOM structure (materials and their children) in a tree format. """
        if self.level_0_material is None:
            print("No materials in the BOM.")
            return

        def display_material(material, level=0):
            """ Recursively display material and its children with indentation. """
            indent = "  " * level + ("-> " if level > 0 else "")
            if level == 0:
                # Display level 0 material (parent) with basic information
                print(f"{indent}{material.name} (Production Time: {material.production_time}, Stock: {material.stock})")
            else:
                # Display child materials with additional information
                print(f"{indent}{material.name} (Needed: {material.quantity_needed}, Production Time: {material.production_time}, Production Capacity: {material.production_capacity}, Stock: {material.stock})")
            for child in material.children:
                display_material(child, level + 1)

        # Start displaying from the level 0 material
        display_material(self.level_0_material)


# Example Usage:
if __name__ == "__main__":
    # Creating a sample BOM for the table
    table = Material(name="Table", stock=2, production_time=1)
    countertop = Material(name="Countertop", parent="Table", quantity_needed=1, stock=22, production_time=3, production_capacity=40)
    wooden_plate = Material(name="Wooden Plate", parent="Countertop", quantity_needed=1, stock=10, production_time=1, production_capacity=50)
    legs = Material(name="Legs", parent="Table", quantity_needed=4, stock=40, production_time=2, production_capacity=120)

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
