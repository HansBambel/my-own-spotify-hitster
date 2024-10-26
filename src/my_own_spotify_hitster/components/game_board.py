import logging

from nicegui import ui

import my_own_spotify_hitster.components.draganddrop as dnd
from my_own_spotify_hitster.components.draganddrop import SortableColumn, SortableRow
from my_own_spotify_hitster.components.game_state import MoshGame
from my_own_spotify_hitster.config import ROOT_DIR, settings
from my_own_spotify_hitster.spotify_functions import NoActiveDeviceFoundError, SpotifySong, play_pause

sizing_str = "self-center items-center justify-center w-1/2"

logger = logging.getLogger(__name__)


def notify(item, location: str) -> None:
    """Notify the player about the card movement."""
    ui.notify(f"Dropped {item.title} on {location}")


@ui.refreshable
def draw_current_card(song: SpotifySong | None) -> None:
    """Draw the current card of the game."""
    if song is None:
        return

    logger.debug(f"Redrawing card: {song}")

    with SortableColumn(group="test"):
        ui.label("New song").classes("text-bold text-lg ml-1 self-center")
        dnd.Card(song)


def prepare_for_new_song(game: MoshGame, switch) -> None:
    """Get a new song, draw a new card and disable the reveal switch."""
    logger.debug("Prepare for new song")
    logger.debug(f"Old song: {game.current_song}")
    game.get_new_song()
    logger.debug(f"New song: {game.current_song}")
    draw_current_card.refresh(game.current_song)
    switch.set_value(False)
    try:
        play_pause(resume=False)
    except NoActiveDeviceFoundError as e:
        ui.notify(e)


def reveal_conceal_song(game: MoshGame, switch: ui.switch) -> None:
    """Reveal or conceal the song depending on the switch."""
    if game.current_song is None:
        return
    game.current_song.reveal = switch.value
    draw_current_card.refresh(game.current_song)


def draw_gameboard(game: MoshGame) -> None:
    """Draw the game board."""
    ui.label("Play Hitster with your own spotify").classes("text-4xl self-center")

    if settings.DEBUG:
        ui.label(f"Songs left:{len(game.upcoming_recommended_songs)}").bind_text_from(
            game, "upcoming_recommended_songs", backward=lambda x: f"Songs left in recommender: {len(x)}"
        ).classes("text-m self-center")

    with ui.splitter(horizontal=True).classes(sizing_str) as splitter:
        with splitter.before:
            with ui.grid(columns=3).classes(sizing_str):
                with ui.column():
                    new_song_button = ui.button(text="New song")

                    reveal_switch = ui.switch(
                        text="Reveal", on_change=lambda enabled: reveal_conceal_song(game, enabled)
                    )
                    new_song_button.on("click", lambda: prepare_for_new_song(game, reveal_switch))
                draw_current_card(game.current_song)

                with ui.column():
                    # Toggle for play/pause
                    with ui.button(on_click=lambda: (play_pause(game.current_song))):
                        ui.label("Play/Pause")
                        ui.image(ROOT_DIR / "my_own_spotify_hitster" / "play_pause.svg")

        with splitter.after:
            # The board game
            ui.separator()
            for i in range(game.number_players):
                with ui.column().classes("self-center items-center"):
                    ui.label(f"Player {i + 1}").classes("text-bold text-xl ml-1 self-center")
                    SortableRow(group="test")
                # dnd.Row(f"Player {i + 1}", wrap=False, align_items="center", on_drop=notify).classes(sizing_str)
                # ui.separator()
