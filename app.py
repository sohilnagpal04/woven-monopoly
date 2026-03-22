import json
import streamlit as st
import streamlit.components.v1 as components

from src.board import Board
from src.game import Game

st.set_page_config(page_title="Woven Monopoly", layout="wide")

# -------------------------------------------------------
# GLOBAL UI STYLE
# -------------------------------------------------------

st.markdown("""
<style>

/* GOOGLE FONTS */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&family=Inter:wght@400;500&display=swap');

/* PAGE */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* REMOVE EXTRA SPACE */
.block-container {
    padding-top: 0.5rem;
}

/* HEADINGS */
h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
}

/* PLAYER CARD */
.player-card{
    background:#161B22;
    padding:14px;
    border-radius:10px;
    border:1px solid #30363D;
    box-shadow:0 3px 8px rgba(0,0,0,0.35);
}

/* TURN INFO */
.turn-box{
    background:#1c2a3a;
    padding:12px;
    border-radius:8px;
    border-left:4px solid #FF4B4B;
}

/* TILE HOVER */
.tile:hover{
    transform:scale(1.03);
    transition:all 0.2s ease;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOAD ROLLS
# -------------------------------------------------------

def load_rolls(file_path):
    with open(file_path) as f:
        return json.load(f)


# -------------------------------------------------------
# HELPERS
# -------------------------------------------------------

def get_space_name(space):
    if isinstance(space, dict):
        return space["name"]
    return space.name


def get_space_colour(space):

    if isinstance(space, dict):
        return "#eeeeee"

    colours = {
        "Brown": "#8B4513",
        "Red": "#e74c3c",
        "Green": "#27ae60",
        "Blue": "#3498db",
    }

    return colours.get(space.colour, "#dddddd")


PLAYER_COLOURS = {
    "Peter": "#3498db",
    "Billy": "#2ecc71",
    "Charlotte": "#9b59b6",
    "Sweedal": "#e74c3c"
}

# -------------------------------------------------------
# BOARD UI
# -------------------------------------------------------

def build_board_html(board, players):

    board_html = """
    <div style="
        display:flex;
        gap:10px;
        overflow-x:auto;
        padding:6px;
        font-family:'Inter', sans-serif;
    ">
    """

    colour_background = {
        "Brown": "#f5e6d3",
        "Red": "#fdecea",
        "Green": "#eafaf1",
        "Blue": "#eaf2fb"
    }

    for i, space in enumerate(board.spaces):

        name = get_space_name(space)

        # GO TILE
        if name == "GO":

            tokens = ""

            for p in players:
                if p.position == 0:

                    token_colour = PLAYER_COLOURS.get(p.name, "black")

                    tokens += f"""
                    <div style="
                        width:18px;
                        height:18px;
                        border-radius:50%;
                        background:{token_colour};
                        color:white;
                        display:inline-flex;
                        align-items:center;
                        justify-content:center;
                        font-size:10px;
                        margin-right:3px;
                    ">
                    {p.name[0]}
                    </div>
                    """

            board_html += f"""
            <div style="
                min-width:130px;
                height:100px;
                border:3px solid black;
                border-radius:10px;
                background:linear-gradient(135deg,#f1c40f,#f39c12);
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                font-size:24px;
                font-weight:bold;
            ">

            GO

            <div style="margin-top:6px">
            {tokens}
            </div>

            </div>
            """
            continue

        colour = get_space_colour(space)

        bg = "#ffffff"

        if not isinstance(space, dict):
            bg = colour_background.get(space.colour, "#ffffff")

        owner = ""
        if not isinstance(space, dict) and space.owner:
            owner = f"{space.owner.name}"

        price = ""
        if not isinstance(space, dict):
            price = f"${space.price}"

        tokens = ""

        for p in players:
            if p.position == i:

                token_colour = PLAYER_COLOURS.get(p.name, "black")

                tokens += f"""
                <div style="
                    width:18px;
                    height:18px;
                    border-radius:50%;
                    background:{token_colour};
                    color:white;
                    display:inline-flex;
                    align-items:center;
                    justify-content:center;
                    font-size:10px;
                    margin-right:3px;
                ">
                {p.name[0]}
                </div>
                """

        board_html += f"""
        <div class="tile" style="
            min-width:130px;
            height:100px;
            border:2px solid #333;
            border-radius:10px;
            background:{bg};
            display:flex;
            flex-direction:column;
            justify-content:space-between;
            box-shadow:0px 2px 6px rgba(0,0,0,0.2);
        ">

        <div style="height:8px;background:{colour};border-radius:8px 8px 0 0"></div>

        <div style="padding:6px;font-size:12px;">

        <b style="font-size:13px">{name}</b><br>
        {price}<br>
        <span style="color:grey">{owner}</span>

        </div>

        <div style="padding:4px">
        {tokens}
        </div>

        </div>
        """

    board_html += "</div>"

    return board_html


# -------------------------------------------------------
# GAME INIT
# -------------------------------------------------------

def initialise_game(roll_file):

    board = Board("data/board.json")
    rolls = load_rolls(roll_file)

    st.session_state.board = board
    st.session_state.rolls = rolls
    st.session_state.roll_file = roll_file
    st.session_state.game = Game(board, rolls)

    st.session_state.turn = 0
    st.session_state.roll_index = 0
    st.session_state.game_over = False
    st.session_state.last_action = "Game ready."
    st.session_state.winner_name = None
    st.session_state.history = []


# -------------------------------------------------------
# PLAY TURN
# -------------------------------------------------------

def play_next_turn():

    if st.session_state.game_over:
        return

    game = st.session_state.game
    board = st.session_state.board
    rolls = st.session_state.rolls

    if st.session_state.roll_index >= len(rolls):

        st.session_state.game_over = True
        winner = game.winner()
        st.session_state.winner_name = winner.name
        return

    player = game.players[st.session_state.turn % len(game.players)]
    roll = rolls[st.session_state.roll_index]

    actions = []

    actions.append(f"{player.name} rolled 🎲 {roll}.")

    passed_go = player.move(roll, board.size())

    if passed_go:
        player.money += 1
        actions.append(f"{player.name} passed GO and received $1.")

    space = board.spaces[player.position]
    space_name = get_space_name(space)

    actions.append(f"{player.name} landed on {space_name}.")

    if not isinstance(space, dict):

        if not space.is_owned():

            player.buy_property(space)
            actions.append(f"{player.name} bought {space.name} for ${space.price}.")

        elif space.owner != player:

            rent = game.calculate_rent(space)
            player.pay_rent(rent, space.owner)

            actions.append(
                f"{player.name} paid ${rent} rent to {space.owner.name}."
            )

    if player.is_bankrupt():

        st.session_state.game_over = True
        winner = game.winner()

        actions.append(f"{player.name} is bankrupt.")
        actions.append(f"Winner: {winner.name}")

        st.session_state.winner_name = winner.name

    text = " ".join(actions)

    st.session_state.last_action = text
    st.session_state.history.append(text)

    st.session_state.turn += 1
    st.session_state.roll_index += 1


# -------------------------------------------------------
# TITLE
# -------------------------------------------------------

st.markdown(
"""
<div style="
display:flex;
justify-content:center;
width:100%;
">

<h1 style="
font-size:52px;
font-weight:900;
color:#FF4B4B;
letter-spacing:4px;
margin-top:30px;
margin-bottom:10px;
text-shadow:0px 2px 10px rgba(255,75,75,0.35);
">
MONOPOLY
</h1>

</div>
""",
unsafe_allow_html=True
)

# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

left, right = st.columns([1,2])

with left:

    st.markdown("### Game Setup")

    game_option = st.selectbox(
        "Select Game",
        ["Game 1", "Game 2"]
    )

    roll_file = "data/rolls_1.json" if game_option == "Game 1" else "data/rolls_2.json"

    if "game" not in st.session_state:
        initialise_game(roll_file)

    if st.session_state.get("roll_file") != roll_file:
        initialise_game(roll_file)

    if st.button("Start Game", use_container_width=True):
        initialise_game(roll_file)

    if st.button("Roll Dice", use_container_width=True):
        play_next_turn()

with right:

    st.markdown("### Turn Information")

    game = st.session_state.game

    if not st.session_state.game_over:

        current_player = game.players[st.session_state.turn % len(game.players)]

        st.markdown(f"**Current Turn:** {current_player.name}")

    st.markdown(
        f"Rolls Used: {st.session_state.roll_index} / {len(st.session_state.rolls)}"
    )

    st.markdown(
        f"""
        <div class="turn-box">
        {st.session_state.last_action}
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# PLAYERS
# -------------------------------------------------------

st.markdown("### Players")

cols = st.columns(4)

current_turn = st.session_state.turn % len(game.players) if not st.session_state.game_over else -1

for i, player in enumerate(game.players):

    properties = len(player.properties)

    dot = ""

    if i == current_turn:
        dot = '<span style="color:#2ecc71;font-size:16px;">● </span>'

    cols[i].markdown(
        f"""
        <div class="player-card">

        <b>{dot}{player.name}</b><br>

        💰 ${player.money} &nbsp;&nbsp;
        📍 {player.position} &nbsp;&nbsp;
        🏠 {properties}

        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# BOARD
# -------------------------------------------------------

st.markdown("### Board")

components.html(
    build_board_html(st.session_state.board, game.players),
    height=170,
    scrolling=False
)

# -------------------------------------------------------
# GAME LOG
# -------------------------------------------------------

with st.expander("Game Log"):

    for h in reversed(st.session_state.history[-8:]):
        st.write(h)

# -------------------------------------------------------
# GAME OVER
# -------------------------------------------------------

if st.session_state.game_over:

    st.balloons()

    st.markdown("## 🎉 Game Over")

    st.markdown(f"### Winner: **{st.session_state.winner_name}**")

    for player in game.players:

        final_space = get_space_name(
            st.session_state.board.spaces[player.position]
        )

        st.write(
            f"{player.name} | Money: ${player.money} | Position: {player.position} ({final_space})"
        )