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

# Taken from here: https://github.com/zauberzeug/nicegui/discussions/932#discussioncomment-10990750
# ui.add_body_html(r'''
#     <script type="module">
#     import 'https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js';
#     document.addEventListener('DOMContentLoaded', () => {
#         Sortable.create(document.querySelector('.sortable'), {
#             animation: 150,
#             ghostClass: 'opacity-50',
#             onEnd: (evt) => emitEvent("item_drop", {id: evt.item.id, new_index: evt.newIndex }),
#         });
#     });
#     </script>
# ''')
# ui.on('item_drop', lambda e: ui.context.client.elements[int(e.args['id'][1:])].move(target_index=e.args['new_index']))

ui.run(title="MOSH")
