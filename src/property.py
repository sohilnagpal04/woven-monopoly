class Property:
    def __init__(self, name, price, colour):
        self.name = name
        self.price = price
        self.colour = colour
        self.owner = None

    def is_owned(self):
        return self.owner is not None