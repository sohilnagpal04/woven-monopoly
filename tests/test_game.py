import json
from src.board import Board
from src.game import Game
from src.player import Player


"""
Basic test suite for the Woven Monopoly simulation.

These tests validate core game behaviour including:
- game execution
- initial player state
- property purchase and rent effects
- bankruptcy condition
- board wrap-around logic
- GO passing behaviour
"""


def load_rolls(file):
    """
    Load dice rolls from a JSON file.
    """
    with open(file) as f:
        return json.load(f)


# Test 1: Game runs without crashing
def test_game_runs_without_crashing():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    assert len(game.players) == 4


# Test 2: Players start correctly
def test_initial_player_state():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)

    assert len(game.players) == 4

    for player in game.players:
        assert player.money == 16
        assert player.position == 0


# Test 3: Money changes during gameplay
def test_money_changes_after_game():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    # At least one player's money should change due to purchases or rent
    assert any(player.money != 16 for player in game.players)


# Test 4: Winner is one of the players
def test_winner_is_valid_player():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    winner = game.winner()

    assert winner in game.players


# Test 5: Bankruptcy condition triggers game end
def test_bankruptcy_occurs():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    bankrupt_players = [p for p in game.players if p.money < 0]

    assert len(bankrupt_players) >= 1


# Test 6: Board wrap-around works correctly
def test_board_wraps_correctly():
    board = Board("data/board.json")

    player = Game(board, []).players[0]
    board_size = board.size()

    player.move(board_size + 2, board_size)

    assert player.position == 2


# Test 7: Different roll files produce different winners
def test_different_rolls_produce_different_winners():
    board1 = Board("data/board.json")
    board2 = Board("data/board.json")

    rolls1 = load_rolls("data/rolls_1.json")
    rolls2 = load_rolls("data/rolls_2.json")

    game1 = Game(board1, rolls1)
    game2 = Game(board2, rolls2)

    game1.play()
    game2.play()

    assert game1.winner().name != game2.winner().name


# Test 8: Player correctly passes GO
def test_player_pass_go():
    player = Player("Test")

    passed = player.move(10, 9)

    assert passed is True
    assert player.position == 1


# Test 9: Player does not pass GO within bounds
def test_player_does_not_pass_go():
    player = Player("Test")

    passed = player.move(3, 9)

    assert passed is False
    assert player.position == 3