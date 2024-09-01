import streamlit as st

for k, v in st.session_state.items():
    st.session_state[k] = v


def init_game():
    """Initialize the game."""
    if "player_count" not in st.session_state:
        st.session_state.player_count = 2
        reset_player_scores()
    if "current_player" not in st.session_state:
        st.session_state.current_player = 0
    if "current_round" not in st.session_state:
        st.session_state.current_round = 0

    if "source" not in st.session_state:
        st.session_state.source = "My dummy value" if source == "My Daily mix" else source

    reset_player_scores()


def reset_player_scores():
    """Reset the player scores."""
    st.session_state.player_scores = {i: 0 for i in range(st.session_state.player_count)}


source = st.radio("Select music source", ["My Daily mix", "Some Playlist"])

st.text_input("Playlist link", key="playlist_link", disabled=True if source == "My Daily mix" else False)


st.number_input("Number of players", min_value=1, value=2, step=1, key="player_count", on_change=reset_player_scores)

init_game()
if st.button("Play"):
    st.switch_page("pages/play_page.py")
