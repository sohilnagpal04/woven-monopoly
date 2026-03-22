import json
from src.property import Property


class Board:
    """
    Represents the Monopoly board.

    The board configuration is loaded from a JSON file. Each space
    can either be a property (converted into a Property object) or
    a special space such as GO.
    """

    def __init__(self, file_path):
        """
        Load the board spaces from the given JSON file.

        Parameters
        ----------
        file_path : str
            Path to the board.json file containing board spaces.
        """

        with open(file_path) as f:
            board_data = json.load(f)

        self.spaces = []

        # Convert JSON entries into board spaces
        for item in board_data:
            if item["type"] == "property":
                # Create a Property object for property spaces
                property_obj = Property(
                    item["name"],
                    item["price"],
                    item["colour"]
                )
                self.spaces.append(property_obj)
            else:
                # Special spaces such as GO remain as dictionaries
                self.spaces.append(item)

    def size(self):
        """
        Return the number of spaces on the board.

        This is used to implement board wrap-around when players move
        beyond the last space.
        """
        return len(self.spaces)