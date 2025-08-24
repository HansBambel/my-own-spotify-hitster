from nicegui import ui

from src.components.draganddrop import SortableRow as DndRow

with ui.row():
    for i in range(10):
        DndRow(f"Player {i + 1}")
        ui.separator()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
