import json
from src.board import Board
from src.game import Game


def run_simulation(roll_file):
    """
    Runs a single game simulation using the provided dice roll file.
    Loads the board, executes the game, and prints formatted results.
    """

    # Initialize board from JSON configuration
    board = Board("data/board.json")

    # Load predefined dice rolls (deterministic gameplay)
    with open(roll_file) as f:
        rolls = json.load(f)

    # Create and run the game simulation
    game = Game(board, rolls)
    game.play()

    # Print results in a clean, aligned format
    print(f"\n=== Results for {roll_file.split('/')[-1]} ===")
    for r in game.results():
        print(f"{r['name']:10} | Money: ${r['money']:3} | Position: {r['position']}")

    # Display winner with highest remaining money
    winner = game.winner()
    print(f"🏆 Winner: {winner.name} with ${winner.money}")


if __name__ == "__main__":
    """
    Entry point of the application.
    Runs simulations for both provided dice roll files.
    """
    run_simulation("data/rolls_1.json")
    run_simulation("data/rolls_2.json")