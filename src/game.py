from src.player import Player


class Game:
    def __init__(self, board, dice_rolls):
        self.board = board
        self.players = [
            Player("Peter"),
            Player("Billy"),
            Player("Charlotte"),
            Player("Sweedal"),
        ]
        self.dice_rolls = dice_rolls

    def calculate_rent(self, property):
        owner = property.owner

        same_colour_owned = [
            p for p in owner.properties if p.colour == property.colour
        ]

        total_same_colour = [
            s for s in self.board.spaces
            if isinstance(s, type(property)) and s.colour == property.colour
        ]

        if len(same_colour_owned) == len(total_same_colour):
            return property.price * 2
        return property.price

    def play(self):
        turn = 0

        for roll in self.dice_rolls:
            player = self.players[turn % 4]

            passed_go = player.move(roll, self.board.size())
            if passed_go:
                player.money += 1

            space = self.board.spaces[player.position]

            if isinstance(space, dict):
                turn += 1
                continue

            if not space.is_owned():
                player.buy_property(space)
            elif space.owner != player:
                rent = self.calculate_rent(space)
                player.pay_rent(rent, space.owner)

            if player.is_bankrupt():
                break

            turn += 1

    def results(self):
        return [
            {
                "name": p.name,
                "money": p.money,
                "position": p.position,
            }
            for p in self.players
        ]

    def winner(self):
        return max(self.players, key=lambda p: p.money)