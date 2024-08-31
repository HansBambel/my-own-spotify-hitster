import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

from my_own_spotify_hitster.config import settings


@st.cache_resource
def get_spotify_client():
    """Get client from Spotify API to read library and modify playback."""
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            redirect_uri=settings.REDIRECT_URI,
            scope=["user-read-playback-state", "user-modify-playback-state", "user-library-read"],
        )
    )
    return sp


sp = get_spotify_client()


def init_game():
    """Initialize the game."""
    if "player_count" not in st.session_state:
        st.session_state.player_count = 2
        reset_player_scores()
    if "current_player" not in st.session_state:
        st.session_state.current_player = 0
    if "current_round" not in st.session_state:
        st.session_state.current_round = 0


def reset_player_scores():
    """Reset the player scores."""
    st.session_state.player_scores = {i: 0 for i in range(st.session_state.player_count)}


def update_score_view():
    """Update the score view."""
    columns = st.columns(st.session_state.player_count)
    for i, column in enumerate(columns):
        column.write(f"Player {i + 1}")
        column.write(f"Score: {st.session_state.player_scores[i]}")


st.title("My Own Spotify Hitster")
init_game()

# TODO maybe use a fragment here?
with st.form("music_source"):
    source = st.radio("Select music source", ["My Daily mix", "Some Playlist"])
    st.form_submit_button("Submit")

if source == "Some Playlist":
    st.text_input("Playlist link", key="playlist_link")


st.number_input("Number of players", min_value=1, value=2, step=1, on_change=reset_player_scores, key="player_count")
# Create a score for each player containing the number of correct guesses
update_score_view()

st.header(f"Current Player: {st.session_state.current_player+1}")


@st.fragment()
def play_pause_music():
    """Play/pause currently playing music."""
    if "playing" not in st.session_state:
        st.session_state.playing = True
    clicked = st.button("Play/Pause")
    if clicked:
        if st.session_state.playing:
            sp.pause_playback()
        else:
            sp.start_playback()
        st.session_state.playing = False


play_pause_music()


# if __name__ == '__main__':
# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
# sp = get_spotify_read_auth()
# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])
