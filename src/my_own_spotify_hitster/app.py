import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

from my_own_spotify_hitster.config import settings


@st.cache_resource
def get_spotify_read_auth():
    """Get client from Spotify API to read library."""
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            redirect_uri=settings.REDIRECT_URI,
            scope="user-library-read",
        )
    )
    return sp


@st.cache_resource
def get_spotify_modify_playback():
    """Get client from Spotify API to modify playback."""
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            redirect_uri=settings.REDIRECT_URI,
            scope="user-modify-playback-state",
        )
    )
    return sp


st.title("My Own Spotify Hitster")

st.radio("Select music source", ["My Daily mix", "Some Playlist"])
st.button("Start playing")


sp_read = get_spotify_read_auth()

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
