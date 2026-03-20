class Player:
    def __init__(self, name):
        self.name = name
        self.money = 16
        self.position = 0
        self.properties = []

    def move(self, steps, board_size):
        old_position = self.position
        self.position = (self.position + steps) % board_size
        passed_go = (old_position + steps) >= board_size
        return passed_go

    def buy_property(self, property):
        self.money -= property.price
        self.properties.append(property)
        property.owner = self

    def pay_rent(self, amount, owner):
        self.money -= amount
        owner.money += amount

    def is_bankrupt(self):
        return self.money < 0