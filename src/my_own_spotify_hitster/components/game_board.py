from nicegui import ui

import my_own_spotify_hitster.components.draganddrop as dnd
from my_own_spotify_hitster.components.draganddrop import SortableRow
from my_own_spotify_hitster.components.game_state import MoshGame, SpotifySong

sizing_str = "justify-content: flex-start; w-full"


def notify(item, location: str) -> None:
    """Notify the player about the card movement."""
    ui.notify(f"Dropped {item.title} on {location}")


@ui.refreshable
def draw_current_card(song: SpotifySong | None) -> None:
    """Draw the current card of the game."""
    if song is None:
        return

    with SortableRow(group="test"):
        ui.label("New song").classes("text-bold ml-1")
        dnd.Card(song)


def prepare_for_new_song(game: MoshGame, switch) -> None:
    """Get a new song, draw a new card and disable the reveal switch."""
    game.get_new_song()
    draw_current_card.refresh()
    switch.set_value(False)


def draw_gameboard(game: MoshGame) -> None:
    """Draw the game board."""
    ui.label("Play Hitster with your own spotify")

    with ui.splitter(horizontal=True).classes(sizing_str) as splitter:
        with splitter.before:
            with ui.grid(columns=3).classes(sizing_str):
                with ui.column():
                    new_song_button = ui.button(text="New song")

                    # TODO: this might have side-effects
                    reveal_switch = ui.switch(text="Reveal", on_change=draw_current_card.refresh).bind_value_to(
                        game.current_song, "reveal"
                    )
                    new_song_button.on("click", lambda: prepare_for_new_song(game, reveal_switch))
                draw_current_card(game.current_song)

                # TODO implement functionality
                with ui.column():
                    ui.button(icon="play_circle")
                    ui.button(icon="pause_circle")
                # Toggle for play/pause
                # with ui.button():
                #     ui.label("Play/Pause")
                #     ui.icon(ROOT_DIR / "my_own_spotify_hitster" / "play_pause.svg")

        with splitter.after:
            # The board game
            ui.separator()
            for i in range(game.number_players):
                with ui.row():
                    ui.label(f"Player {i + 1}").classes("text-bold ml-1")
                    SortableRow(group="test")
                # dnd.Row(f"Player {i + 1}", wrap=False, align_items="center", on_drop=notify).classes(sizing_str)
                # ui.separator()
