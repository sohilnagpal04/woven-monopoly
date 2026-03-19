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

