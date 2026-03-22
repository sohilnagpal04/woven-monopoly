class Property:
    """
    Represents a purchasable property on the Monopoly board.
    """

    def __init__(self, name, price, colour):
        """
        Initialise a property with its basic attributes.

        Parameters
        ----------
        name : str
            Name of the property.
        price : int
            Cost required to purchase the property.
        colour : str
            Colour group of the property (used for rent doubling rule).
        """
        self.name = name
        self.price = price
        self.colour = colour
        self.owner = None  # Owner is assigned when a player buys the property

    def is_owned(self):
        """
        Return True if the property already has an owner.
        """
        return self.owner is not None