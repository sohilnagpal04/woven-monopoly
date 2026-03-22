from src.player import Player


class Game:
    """
    Represents the Woven Monopoly game.

    Handles player turns, dice rolls, property purchasing,
    rent payments, and determining the winner.
    """

    def __init__(self, board, dice_rolls):
        """
        Initialise the game.

        Parameters
        ----------
        board : Board
            The game board containing all spaces.
        dice_rolls : list[int]
            Predefined dice rolls used to simulate the game.
        """
        self.board = board
        self.players = [
            Player("Peter"),
            Player("Billy"),
            Player("Charlotte"),
            Player("Sweedal"),
        ]
        self.dice_rolls = dice_rolls

    def calculate_rent(self, prop):
        """
        Calculate the rent for a property.

        Rent is doubled if the owner owns all properties
        of the same colour group.
        """
        owner = prop.owner

        # Properties of the same colour owned by the player
        same_colour_owned = [
            p for p in owner.properties if p.colour == prop.colour
        ]

        # Total properties of that colour on the board
        total_same_colour = [
            s for s in self.board.spaces
            if hasattr(s, "colour") and s.colour == prop.colour
        ]

        # Rent doubles if full colour set is owned
        if len(same_colour_owned) == len(total_same_colour):
            return prop.price * 2

        return prop.price

    def play(self):
        """
        Run the game simulation using the predefined dice rolls.
        """
        turn = 0

        for roll in self.dice_rolls:
            player = self.players[turn % len(self.players)]

            # Move the player and check if GO was passed
            passed_go = player.move(roll, self.board.size())
            if passed_go:
                player.money += 1

            space = self.board.spaces[player.position]

            # Skip non-property spaces (e.g., GO)
            if isinstance(space, dict):
                turn += 1
                continue

            # Buy property if unowned
            if not space.is_owned():
                player.buy_property(space)

            # Otherwise pay rent if owned by another player
            elif space.owner != player:
                rent = self.calculate_rent(space)
                player.pay_rent(rent, space.owner)

            # Stop game if player becomes bankrupt
            if player.is_bankrupt():
                break

            turn += 1

    def results(self):
        """
        Return final player states after the game ends.
        """
        return [
            {
                "name": p.name,
                "money": p.money,
                "position": p.position,
            }
            for p in self.players
        ]

    def winner(self):
        """
        Return the player with the most money remaining.
        """
        return max(self.players, key=lambda p: p.money)