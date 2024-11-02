from components.game_state import MoshGame
from nicegui import ui

from my_own_spotify_hitster.components.game_board import draw_gameboard

with ui.element().classes("w-full justify-start items-center"):
    with ui.tabs() as tabs:
        ui.tab("Config", icon="settings")
        ui.tab("Game", icon="radio")
    with ui.tab_panels(tabs) as panels:
        game: MoshGame = MoshGame()
        with ui.tab_panel("Config"):
            # TODO for each player set a name
            players_number = ui.number(placeholder="2", min=1)
            players_number.bind_value(game, "number_players", forward=int)
            ui.button("New game", on_click=lambda: start_game(game))
            # TODO implement multiple based on approaches
            based_on = ui.switch("Based on liked songs")
            based_on.set_value(True)
            based_on.disable()
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
