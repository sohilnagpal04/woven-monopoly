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

#Test 2 : Players start correctly at position 0 with $16 and 4 players
def test_initial_player_state():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)

    for player in game.players:
        assert player.money == 16
        assert player.position == 0