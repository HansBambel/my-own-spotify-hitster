import logging
import random
import re
from dataclasses import dataclass
from functools import lru_cache

import spotipy
from spotipy import Spotify, SpotifyOAuth

from config import settings

logger = logging.getLogger(__name__)


class NoActiveDeviceFoundError(Exception):
    """Special Error case when no device is found."""

    pass


@dataclass
class SpotifySong:
    """Class containing info about a Song form Spotify."""

    title: str = "?"
    artist: str = "?"
    release_year: int = 0
    album: str | None = None
    uri: str | None = None
    reveal: bool = False

    def __eq__(self, other):
        """Equality check only takes title and artist into consideration."""
        return (self.title == other.title) and (self.artist == other.artist)


@lru_cache(maxsize=1)
def get_spotify_client() -> Spotify:
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


def force_play(song: SpotifySong) -> None:
    """Play the song."""
    sp = get_spotify_client()
    sp.start_playback(uris=[song.uri])


def play_pause(song: SpotifySong | None = None, resume: bool = True) -> None:
    """Play or pause the currently playing song."""
    sp = get_spotify_client()
    playback = sp.current_playback()
    if playback is None:
        raise NoActiveDeviceFoundError("Found no active device. Play a song from the device you want to play MOSH.")
    if playback["is_playing"]:
        sp.pause_playback()
    elif resume:
        if song and song.uri:
            force_play(song)
        else:
            logger.warning(f"Error trying to play song: {song}")
            sp.start_playback()


def get_songs_from_saved_playlist(amount=5) -> list[dict]:
    """Get the current users saved playlist and get `amount` songs from it. Returns list of spotify songs."""
    sp = get_spotify_client()

    logger.debug("Getting songs from saved tracks.")
    liked_playlist = sp.current_user_saved_tracks()
    number_of_songs = liked_playlist["total"]
    # Get random songs from that list
    song_ids = random.sample(range(number_of_songs), k=amount)
    songs = [sp.current_user_saved_tracks(limit=1, offset=offset)["items"][0] for offset in song_ids]
    return songs


def get_songs_from_custom_playlist(playlist_url: str, amount=5) -> list[dict]:
    """Get `amount` songs from the given playlist. Returns list of spotify songs."""
    sp = get_spotify_client()

    logger.debug(f"Getting songs from custom playlist: {playlist_url}")
    playlist = sp.playlist(playlist_url)
    logger.debug(f"Playlist name: {playlist['name']}")
    number_of_songs = playlist["tracks"]["total"]
    song_ids = random.sample(range(number_of_songs), k=amount)
    songs = [sp.playlist_items(playlist_url, limit=1, offset=offset)["items"][0] for offset in song_ids]
    return songs


def get_recommendations(based_on: list[dict], min_popularity: int = 69) -> list[dict]:
    """Get (popular) recommendations based on the given list (in spotify track data model)."""
    sp = get_spotify_client()
    songs = [song["track"]["id"] for song in based_on]
    recommendations = sp.recommendations(seed_tracks=songs, limit=10, min_popularity=min_popularity)
    return recommendations["tracks"]


def from_recommendation_to_spotify_song(recommendation: dict) -> SpotifySong:
    """Convert from spotify data model to own Spotify Song model."""
    release_year = re.findall(r"\d{4}", recommendation["album"]["release_date"])
    if not release_year:
        raise RuntimeError(f"Could not find release year in album: {recommendation['album']}")
    return SpotifySong(
        title=recommendation["name"],
        album=recommendation["album"]["name"],
        artist=recommendation["artists"][0]["name"],
        release_year=release_year[0],
        uri=recommendation["uri"],
    )


if __name__ == "__main__":
    # songs = get_songs_from_saved_playlist()
    # recommendations = get_recommendations(songs)

    get_songs_from_custom_playlist("https://open.spotify.com/playlist/2XyhXRIemHuTDwk79oHvoU?si=f06ce5903bce4f27")

    # song = {
    #     "album": {"name": "<AlbumName>", "release_date": "2024-07-23"},
    #     "artists": [{"name": "<NAME>"}],
    #     "name": "<SongName>",
    #     "uri": "<some-uri>",
    # }
    # print(from_recommendation_to_spotify_song(song))
