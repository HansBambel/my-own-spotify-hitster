import spotipy
import streamlit as st
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth

from config import settings

for k, v in st.session_state.items():
    st.session_state[k] = v


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


def update_score_view():
    """Update the score view."""
    columns = st.columns(st.session_state.player_count)
    for i, column in enumerate(columns):
        column.write(f"Player {i + 1}")
        column.write(f"Score: {st.session_state.player_scores[i]}")


##### Streamlit starts #####
sp = get_spotify_client()

st.header(f"Music source: {st.session_state.source}")
# Create a score for each player containing the number of correct guesses
update_score_view()

st.header(f"Current Player: {st.session_state.current_player+1}")


# print(sp.currently_playing())
@st.fragment()
def play_pause_music():
    """Play/pause currently playing music."""
    if "playing" not in st.session_state:
        st.session_state.playing = True
    clicked = st.button("Play/Pause")
    if clicked:
        try:
            if st.session_state.playing:
                sp.pause_playback()
                st.session_state.playing = False
            else:
                sp.start_playback()
                st.session_state.playing = True
        except SpotifyException:
            st.warning("Failed to get the correct device. Play a song in Spotify and try again")


play_pause_music()
