from itertools import chain, repeat
from unittest.mock import MagicMock, patch

import pytest

from spotify_functions import (
    SpotifySong,
    from_recommendation_to_spotify_song,
    get_recommendations,
    get_songs_from_custom_playlist,
    get_songs_from_saved_playlist,
)


@patch("spotify_functions.spotipy.Spotify", autospec=True)
def test_get_songs_from_saved_playlist_makes_calls_to_api(my_mock: MagicMock):
    """Test that songs from the saved playlist are taken."""
    mock_spotipy = my_mock()
    mock_spotipy.current_user_saved_tracks.side_effect = chain([{"total": 42}], repeat({"items": [1337]}))
    songs = get_songs_from_saved_playlist()
    assert len(songs) == 5
    assert songs == [1337] * 5
    assert mock_spotipy.current_user_saved_tracks.call_count == 6


@patch("spotify_functions.spotipy.Spotify", autospec=True)
def test_get_songs_from_custom_playlist_makes_calls_to_api(my_mock: MagicMock):
    """Test that songs from the custom playlist are taken."""
    mock_spotipy = my_mock()
    mock_spotipy.playlist.return_value = {"name": "My playlist", "tracks": {"total": 42}}
    mock_spotipy.playlist_items.side_effect = repeat({"items": [1337]})
    songs = get_songs_from_custom_playlist(playlist_url="www.some-url.com")
    assert len(songs) == 5
    assert songs == [1337] * 5
    assert mock_spotipy.playlist_items.call_count == 5
    mock_spotipy.playlist.assert_called_with("www.some-url.com")


@patch("spotify_functions.spotipy.Spotify", autospec=True)
def test_get_recommendations_returns_tracks(my_mock: MagicMock):
    """Test that recommendations are returned."""
    mock_spotipy = my_mock()
    mock_spotipy.recommendations.return_value = {"tracks": ["Song1", "Song2"]}
    base = [
        {
            "track": {"id": 42},
        },
        {
            "track": {"id": 1337},
        },
    ]
    songs = get_recommendations(based_on=base)
    assert songs == ["Song1", "Song2"]
    assert mock_spotipy.recommendations.call_count == 1
    mock_spotipy.recommendations.assert_called_with(seed_tracks=[42, 1337], limit=10, min_popularity=69)


@pytest.mark.parametrize("year", ["2024-11-22", "2024-01", "2024"])
def test_from_recommendation_to_spotify_song(year: str):
    """Test conversion from spotify-internal representation to SpotifySong."""
    spotify_dict = {
        "name": "Song title",
        "artists": [
            {
                "name": "cool artist",
            }
        ],
        "album": {
            "name": "My album",
            "release_date": year,
        },
        "uri": "spotify:artist:cool-artist:1",
    }
    converted = from_recommendation_to_spotify_song(spotify_dict)
    assert converted == SpotifySong(
        title="Song title",
        artist="cool artist",
        album="My album",
        uri="spotify:artist:cool-artist:1",
        release_year=2024,
    )


@pytest.mark.parametrize("year", [None, "missing"])
def test_from_recommendation_to_spotify_song_error_when_no_release_year(year):
    """Test that an error is thrown when the release year is missing."""
    with pytest.raises(RuntimeError, match="Could not find release year in album:"):
        from_recommendation_to_spotify_song({"album": {"name": "My album", "release_date": year}})
