import json
from src.property import Property


class Board:
    def __init__(self, file_path):
        with open(file_path) as f:
            data = json.load(f)

        self.spaces = []
        for item in data:
            if item["type"] == "property":
                self.spaces.append(
                    Property(item["name"], item["price"], item["colour"])
                )
            else:
                self.spaces.append(item)  # GO

    def size(self):
        return len(self.spaces)