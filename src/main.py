import logging

from nicegui import ui

from components.game_board import draw_gameboard
from components.game_state import MoshGame

logger = logging.getLogger(__name__)

MY_HITSTER_PLAYLIST_LINK = "https://open.spotify.com/playlist/69El5G3vSe2btfG0kLztbh?si=a01fbfbe8a254a6b"
STETWF_PLAYLIST_LINK = "https://open.spotify.com/playlist/3M1Ib7CzYyy9pOWpmwlfIr?si=f65cd5c9884648b4"


@ui.refreshable
def player_names_input(game: MoshGame):
    """Render input for player naming."""
    logger.debug(f"Player names input - value: {players_number.value}")
    for i in range(int(players_number.value)):
        player_input = ui.input(label=f"Player {i+1}", placeholder=f"Player {i+1}")
        player_input.value = f"Player {i+1}"
        player_input.bind_value_to(game.player_names, f"Player {i+1}")


with ui.element().classes("w-full justify-start items-center"):
    with ui.tabs() as tabs:
        ui.tab("Config", icon="settings")
        ui.tab("Game", icon="radio")
    with ui.tab_panels(tabs) as panels:
        game: MoshGame = MoshGame()
        with ui.tab_panel("Config"):
            with ui.column().classes("w-full items-center"):
                players_number = ui.number(placeholder="2", min=1)
                players_number.bind_value(game, "number_players", forward=int)
                player_names_input(game)
                players_number.on("change", player_names_input.refresh)

                ui.button("New game", on_click=lambda: start_game(game))
                # implement multiple based on approaches
                based_on = ui.radio({False: "Based on liked songs", True: "Playlist"}, value=False).bind_value_to(
                    game, "use_playlists"
                )
                ui.radio(
                    {
                        MY_HITSTER_PLAYLIST_LINK: "My own Hitster",
                        STETWF_PLAYLIST_LINK: "Songs that excite the white folk",
                    }
                ).bind_visibility_from(based_on, "value", value=True).bind_value_to(game, "custom_playlist")
                # ui.input(
                #     label="Playlist-URL",
                #     value="https://open.spotify.com/playlist/3M1Ib7CzYyy9pOWpmwlfIr?si=f65cd5c9884648b4",
                # )

        with ui.tab_panel("Game"):
            if game is not None:
                draw_gameboard(game)
            else:
                ui.label("Start a game first")


def start_game(game: MoshGame):
    """Trigger starting the game and switch tab to the game board."""
    game.start_game()
    draw_gameboard.refresh()
    panels.set_value("Game")


panels.set_value("Config")

ui.run(title="MOSH")
