import json
from src.board import Board
from src.game import Game


def load_rolls(file):
    with open(file) as f:
        return json.load(f)


# Test 1: Game runs without crashing
def test_game_runs_without_crashing():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    assert len(game.players) == 4


# Test 2: Players start correctly at position 0 with $16 and total 4 players
def test_initial_player_state():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)

    assert len(game.players) == 4
    for player in game.players:
        assert player.money == 16
        assert player.position == 0


# Test 3: Money changes after game (buying + rent logic)
def test_money_changes_after_game():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    assert any(player.money != 16 for player in game.players)


# Test 4: Winner is a valid player
def test_winner_is_valid_player():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    winner = game.winner()

    assert winner in game.players


# Test 5: Bankruptcy occurs (game ends when a player goes bankrupt)
def test_bankruptcy_occurs():
    board = Board("data/board.json")
    rolls = load_rolls("data/rolls_1.json")

    game = Game(board, rolls)
    game.play()

    bankrupt_players = [p for p in game.players if p.money < 0]

    assert len(bankrupt_players) >= 1


# Test 6: Board wraps around correctly
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