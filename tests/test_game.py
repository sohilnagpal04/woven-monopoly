import json
from src.board import Board
from src.game import Game

#Test 1 : Game Runs without crashing
def load_rolls(file):
    with open(file) as f:
        return json.load(f)


def test_game_runs_without_crashing():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    assert len(game.players) == 4