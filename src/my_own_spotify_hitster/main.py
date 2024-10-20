from components.game_state import MoshGame
from nicegui import ui

from my_own_spotify_hitster.components.game_board import draw_gameboard

game = MoshGame()

with ui.row().classes("w-full items-center"):
    result = ui.label().classes("mr-auto")
    with ui.button(icon="menu"):
        with ui.menu() as menu:
            ui.menu_item("2 Players", lambda: ui.number().bind_value(game, "number_players"))
            ui.menu_item("Play", lambda: result.set_text("Selected item 2"))
            ui.separator()
            ui.menu_item("Close", menu.close)


draw_gameboard(game)


ui.run()
