class Player:
    """
    Represents a player in the Woven Monopoly game.
    Tracks the player's position, money, and owned properties.
    """

    def __init__(self, name):
        """
        Initialise a player with starting game values.

        Parameters
        ----------
        name : str
            Name of the player.
        """
        self.name = name
        self.money = 16
        self.position = 0
        self.properties = []

    def move(self, steps, board_size):
        """
        Move the player forward on the board.

        Parameters
        ----------
        steps : int
            Number of spaces to move (dice roll).
        board_size : int
            Total number of spaces on the board.

        Returns
        -------
        bool
            True if the player passed GO during this move.
        """
        old_position = self.position

        # Board wraps around using modulo
        self.position = (self.position + steps) % board_size

        # Player passes GO if movement exceeds board size
        passed_go = (old_position + steps) >= board_size

        return passed_go

    def buy_property(self, prop):
        """
        Purchase a property and assign ownership.

        Parameters
        ----------
        prop : Property
            Property object to purchase.
        """
        self.money -= prop.price
        self.properties.append(prop)
        prop.owner = self

    def pay_rent(self, amount, owner):
        """
        Pay rent to another player.

        Parameters
        ----------
        amount : int
            Rent amount.
        owner : Player
            Owner of the property receiving rent.
        """
        self.money -= amount
        owner.money += amount

    def is_bankrupt(self):
        """
        Check whether the player is bankrupt.

        Returns
        -------
        bool
        """
        return self.money < 0