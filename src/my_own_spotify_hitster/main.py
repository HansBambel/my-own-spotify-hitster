from components.game_state import MoshGame
from nicegui import ui

from my_own_spotify_hitster.components.game_board import draw_gameboard, sizing_str

# game = MoshGame()

# with ui.row().classes("w-full items-center"):
#     result = ui.label().classes("mr-auto")
#     with ui.button(icon="menu"):
#         with ui.menu() as menu:
#             ui.menu_item("2 Players", lambda: ui.number().bind_value(game, "number_players"))
#             ui.menu_item("Play", lambda: result.set_text("Selected item 2"))
#             ui.separator()
#             ui.menu_item("Close", menu.close)


with ui.tabs() as tabs:
    ui.tab("Config", icon="settings")
    ui.tab("Game", icon="radio")
with ui.tab_panels(tabs).classes(sizing_str) as panels:
    game: MoshGame = MoshGame()
    with ui.tab_panel("Config"):
        # TODO for each player set a name
        players_number = ui.number(placeholder="2", min=1)
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
    panels.set_value("Game")


panels.set_value("Config")

ui.run(title="MOSH")
