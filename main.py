import json
from src.board import Board
from src.game import Game


def run_simulation(roll_file):
    board = Board("data/board.json")

    with open(roll_file) as f:
        rolls = json.load(f)

    game = Game(board, rolls)
    game.play()

    print(f"\nResults for {roll_file}")
    for r in game.results():
        print(f"{r['name']:10} | Money: ${r['money']:3} | Position: {r['position']}")

    print(f"Winner: {game.winner().name}")


if __name__ == "__main__":
    run_simulation("data/rolls_1.json")
    run_simulation("data/rolls_2.json")