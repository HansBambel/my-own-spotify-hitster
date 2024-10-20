import logging
from dataclasses import dataclass
from typing import ClassVar

logger = logging.getLogger(__name__)


@dataclass
class SpotifySong:
    """Class containing info about a Song form Spotify."""

    title: str = "?"
    artist: str = "?"
    release_year: int = 0
    album: str | None = None
    reveal: bool = True


default_song = SpotifySong(
    title="Never gonna give you up",
    artist="Rick Astley",
    release_year=1987,
    album="Whenever you need somebody",
    reveal=False,
)


class MoshGame:
    """Contains the game state of a round of My Own Spotify Hitster."""

    number_players: int
    round: int = 1
    past_songs: ClassVar[list[SpotifySong]] = []

    def __init__(self, number_players: int = 2) -> None:
        """Initialize MOSH game state."""
        self.number_players = number_players
        # TODO remove the default song
        self.past_songs.append(default_song)

    @property
    def current_song(self) -> SpotifySong | None:
        """Get the latest entry in the past songs."""
        return self.past_songs[-1] if len(self.past_songs) > 0 else None

    def get_new_song(self) -> SpotifySong:
        """Call the spotify API to get a new song."""
        logger.info("Get new song from Spotify")
        # TODO: Get currently playing song
        new_song = default_song
        self.past_songs.append(new_song)
        return new_song
