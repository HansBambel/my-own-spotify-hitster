from functools import lru_cache

import spotipy
from spotipy import SpotifyOAuth

from my_own_spotify_hitster.config import settings


@lru_cache(maxsize=1)
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


def play_pause():
    """Play or pause the currently playing song."""
    sp = get_spotify_client()
    playback = sp.current_playback()
    if playback["is_playing"]:
        sp.pause_playback()
    else:
        sp.start_playback()
