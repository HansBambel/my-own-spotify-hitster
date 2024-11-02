import logging

from nicegui import binding

from my_own_spotify_hitster.spotify_functions import (
    SpotifySong,
    from_recommendation_to_spotify_song,
    get_recommendations,
    get_songs_from_saved_playlist,
)

logger = logging.getLogger(__name__)

default_song = SpotifySong(
    title="Never gonna give you up",
    artist="Rick Astley",
    release_year=1987,
    album="Whenever you need somebody",
    reveal=False,
)


class MoshGame:
    """Contains the game state of a round of My Own Spotify Hitster."""

    number_players: binding.BindableProperty
    round: int = 1
    past_songs: list[SpotifySong]
    recommendations_based_on: list
    upcoming_recommended_songs: list[SpotifySong]

    def __init__(self, number_players: int = 2) -> None:
        """Initialize MOSH game state."""
        logger.debug(f"Creating MOSH game state with {number_players} players.")
        self.number_players = number_players
        self.past_songs = []
        self.recommendations_based_on = []
        self.upcoming_recommended_songs = []

    def start_game(self) -> None:
        """Fill game state with songs."""
        logger.debug("Start game -> filling songs")
        self.recommendations_based_on = get_songs_from_saved_playlist()
        self._fill_upcoming_songs()
        self.past_songs = [self.upcoming_recommended_songs.pop(0)]

    def _fill_upcoming_songs(self):
        """
        Call the spotify API to get new upcoming songs. Uses new recommendations for the new batch.
        Filters duplicates.
        """
        logger.debug("Filling upcoming songs.")
        self.recommendations_based_on = get_songs_from_saved_playlist()
        upcoming_recommended_songs_raw = get_recommendations(self.recommendations_based_on)
        new_recommendations = [from_recommendation_to_spotify_song(song) for song in upcoming_recommended_songs_raw]
        logger.debug(f"Found {len(new_recommendations)} new recommendations.")
        self.upcoming_recommended_songs = [song for song in new_recommendations if song not in self.past_songs]
        logger.debug(f"Found {len(new_recommendations)-len(self.upcoming_recommended_songs)} duplicates.")
        if len(self.upcoming_recommended_songs) == 0:
            # All songs are duplicates -> call _fill_upcoming songs again
            self._fill_upcoming_songs()

    @property
    def current_song(self) -> SpotifySong | None:
        """Get the latest entry in the past songs."""
        return self.past_songs[-1] if len(self.past_songs) > 0 else None

    def get_new_song(self) -> SpotifySong:
        """Get a new song from the upcoming recommended songs."""
        logger.debug("New song gets called")

        if len(self.upcoming_recommended_songs) == 0:
            self._fill_upcoming_songs()
        new_song = self.upcoming_recommended_songs.pop(0)
        self.past_songs.append(new_song)
        logger.debug(f"Songs left: {len(self.upcoming_recommended_songs)}")
        logger.debug(f"Past songs: {self.past_songs}")
        return new_song
