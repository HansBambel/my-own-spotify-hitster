from __future__ import annotations

from collections.abc import Callable

from nicegui import ui

from my_own_spotify_hitster.components.game_state import SpotifySong

dragged: Card | None = None


class DragAndDropBase(ui.element):
    """Parent class for drag and drop elements."""

    def __init__(self, name: str, on_drop: Callable[[SpotifySong, str], None] | None = None, *args, **kwargs) -> None:
        """Initialize the element."""
        super().__init__(*args, **kwargs)
        with self.classes("bg-blue-grey-2 w-60 p-4 rounded shadow-2"):
            ui.label(name).classes("text-bold ml-1")
        self.name = name
        self.on("dragover.prevent", self.highlight)
        self.on("dragleave", self.unhighlight)
        self.on("drop", self.move_card)
        self.on_drop = on_drop

    def highlight(self) -> None:
        """Set style for highlighting."""
        self.classes(remove="bg-blue-grey-2", add="bg-blue-grey-3")

    def unhighlight(self) -> None:
        """Set style for un-highlighting."""
        self.classes(remove="bg-blue-grey-3", add="bg-blue-grey-2")

    def move_card(self) -> None:
        """Remove the card from the origin column and put it in the target column."""
        global dragged  # pylint: disable=global-statement
        if dragged is None:
            return
        self.unhighlight()
        if dragged.parent_slot is not None:
            dragged.parent_slot.parent.remove(dragged)
        with self:
            Card(dragged.item)
        if self.on_drop:
            self.on_drop(dragged.item, self.name)
        dragged = None


class Column(DragAndDropBase, ui.column):
    """Drag and drop column."""

    def __init__(self, name: str, on_drop: Callable[[SpotifySong, str], None] | None = None, *args, **kwargs) -> None:
        """Initialize a Column-wise drag-and-drop element."""
        super().__init__(name, on_drop, *args, **kwargs)


class Row(DragAndDropBase, ui.row):
    """Drag and drop row."""

    def __init__(self, name: str, on_drop: Callable[[SpotifySong, str], None] | None = None, *args, **kwargs) -> None:
        """Initialize a Row-wise drag-and-drop element."""
        super().__init__(name, on_drop, *args, **kwargs)


class Card(ui.card):
    """A draggable card."""

    def __init__(self, item: SpotifySong) -> None:
        """Initialize the card with the info of the SpotifySong it represents."""
        super().__init__()
        self.item = item
        with self.props("draggable").classes("w-full cursor-pointer bg-grey-1"):
            if item.reveal:
                ui.label(f"Title:\n{item.title}")
                ui.label(f"Artist:\n{item.artist}")
                ui.label(f"Release year:\n{item.release_year}")
            else:
                ui.label("?")
        self.on("dragstart", self.handle_dragstart)

    def handle_dragstart(self) -> None:
        """Set the current dragged card to this one."""
        global dragged  # pylint: disable=global-statement
        dragged = self
