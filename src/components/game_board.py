import logging

from nicegui import ui

import components.draganddrop as dnd
from components.draganddrop import SortableColumn, SortableRow
from components.game_state import MoshGame
from config import ROOT_DIR, settings
from spotify_functions import NoActiveDeviceFoundError, SpotifySong, force_play, play_pause

logger = logging.getLogger(__name__)


current_card_holder: SortableColumn | None = None
current_card: dnd.Card | None = None


def notify(item, location: str) -> None:
    """Notify the player about the card movement."""
    ui.notify(f"Dropped {item.title} on {location}")


@ui.refreshable
def draw_current_card(song: SpotifySong | None) -> None:
    """Draw the current card of the game."""
    if song is None:
        return

    logger.debug(f"Redrawing card: {song}")

    global current_card
    if current_card:
        current_card.update()


def prepare_for_new_song(game: MoshGame, switch) -> None:
    """Get a new song, draw a new card and disable the reveal switch."""
    if switch.value is False:
        ui.notify("Need to reveal card to continue")
        return
    logger.debug("Prepare for new song")
    logger.debug(f"Old song: {game.current_song}")
    if len(game.upcoming_recommended_songs) == 0:
        ui.notify("Getting new songs, please wait", position="top")
    game.get_new_song()
    logger.debug(f"New song: {game.current_song}")

    if current_card_holder:
        with current_card_holder:
            ui.label("New song").classes("text-bold text-lg ml-1 self-center")
            global current_card
            current_card = dnd.Card(game.current_song)
    # draw_current_card.refresh(game.current_song)
    switch.set_value(False)
    try:
        # play_pause(resume=False)
        force_play(song=game.current_song)
    except NoActiveDeviceFoundError as e:
        ui.notify(e)


def reveal_conceal_song(game: MoshGame, switch: ui.switch) -> None:
    """Reveal or conceal the song depending on the switch."""
    if game.current_song is None:
        return
    game.current_song.reveal = switch.value
    logger.debug(f"Switched reveal to {switch.value}")
    draw_current_card.refresh(game.current_song)


@ui.refreshable
def draw_gameboard(game: MoshGame) -> None:
    """Draw the game board."""
    ui.label("Play Hitster with your own spotify").classes("text-4xl self-center")

    if settings.DEBUG:
        ui.label(f"Songs left:{len(game.upcoming_recommended_songs)}").bind_text_from(
            game, "upcoming_recommended_songs", backward=lambda x: f"Songs left in recommender: {len(x)}"
        ).classes("text-m self-center")

    with ui.column().classes("w-full items-center"):
        with ui.splitter(horizontal=True).classes("w-3/4 flex-1") as splitter:
            with splitter.before:
                # The new song etc
                with ui.grid(columns=3).classes("w-full self-center justify-items-center"):
                    with ui.column():
                        new_song_button = ui.button(text="New song")

                        reveal_switch = ui.switch(
                            text="Reveal", on_change=lambda enabled: reveal_conceal_song(game, enabled)
                        )
                        new_song_button.on("click", lambda: prepare_for_new_song(game, reveal_switch))
                    global current_card_holder
                    current_card_holder = SortableColumn(group="test")
                    with current_card_holder:
                        logger.debug("Drawing card holder")
                        ui.label("New song").classes("text-bold text-lg ml-1 self-center")
                        if game.current_song:
                            logger.debug("Drawing first card")
                            dnd.Card(game.current_song)
                    # draw_current_card(game.current_song)

                    with ui.column().classes("mb-6"):
                        # Toggle for play/pause
                        with ui.button(on_click=lambda: (play_pause(game.current_song))):
                            ui.label("Play/Pause")
                            ui.image(ROOT_DIR / "play_pause.svg")

            with splitter.after:
                # The board game
                ui.separator()
                logger.debug(f"Number of players: {game.number_players}")
                for i in range(game.number_players):
                    with ui.skeleton(bordered=True, animation="none").classes("self-center items-center"):
                        with ui.column().classes("self-center items-center"):
                            ui.label(game.player_names.get(f"Player {i + 1}", f"Player {i + 1}")).classes(
                                "text-bold text-xl ml-1 self-center"
                            )
                            with ui.skeleton(bordered=True, animation="none"):
                                with SortableRow(group="test"):
                                    if game.current_song:
                                        game.current_song.reveal = True
                                        dnd.Card(game.current_song)
                                        game.get_new_song()

        # TODO put this on the right side
        with ui.element().classes("w-1/4"):
            ui.label("Wrong guesses").classes("text-bold text-xl justify-self-center")
            with ui.skeleton(bordered=True, animation="none").classes("object-right"):
                SortableRow(group="test")
