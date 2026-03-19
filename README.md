# woven-monopoly
Deterministic Monopoly game simulation (Woven coding test)

## 🏗️ System Design

```mermaid
classDiagram

class Game {
  - players
  - board
  - dice_rolls
  + play()
  + calculate_rent()
  + results()
  + winner()
}

class Player {
  - name
  - money
  - position
  - properties
  + move()
  + buy_property()
  + pay_rent()
  + is_bankrupt()
}

class Property {
  - name
  - price
  - colour
  - owner
  + is_owned()
}

class Board {
  - spaces
  + load()
  + size()
}

Game --> Player
Game --> Board
Board --> Property
Player --> Property


## 📁 Project Structure

```bash
woven-monopoly/
│
├── src/                # Core application logic
│   ├── player.py       # Player state and behaviour
│   ├── property.py     # Property model and ownership
│   ├── board.py        # Board loading and representation
│   └── game.py         # Game engine and rules
│
├── data/               # Input data files
│   ├── board.json
│   ├── rolls_1.json
│   └── rolls_2.json
│
├── tests/              # Unit tests
│   ├── test_player.py
│   └── test_game.py
│
├── main.py             # Entry point to run simulations
├── requirements.txt    # Dependencies
└── README.md           # Project documentation