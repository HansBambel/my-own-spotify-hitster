from collections.abc import Callable

from nicegui import ui

from my_own_spotify_hitster.config import ROOT_DIR
from my_own_spotify_hitster.spotify_functions import SpotifySong


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
                ui.label(f"Album:\n{item.album}")
                ui.label(f"Release year:\n{item.release_year}")
            else:
                ui.label("?")


class SortableElement(ui.element, component=ROOT_DIR / "my_own_spotify_hitster" / "resources" / "sortable_element.js"):  # type: ignore
    """Sortable Row element."""

    def __init__(self, *args, group: str, on_change: Callable | None = None, **kwargs) -> None:
        """Assign the group and on_change-function."""
        super().__init__()
        self.on("item-drop", self.drop)
        self.on_change = on_change

        self._props["group"] = group

    def drop(self, e) -> None:
        """Run the on_change function."""
        if self.on_change:
            self.on_change(e)

    def makeSortable(self) -> None:
        """Make the element sortable."""
        self.run_method("makeSortable")

    def getitems(self) -> None:
        """Get the items in the element."""
        return self.run_method("getitems")


class SortableRow(SortableElement):
    """Sortable Row element."""

    def __init__(self, group: str, on_change: Callable | None = None, *args, **kwargs) -> None:
        """Initialize a row that is sortable."""
        super().__init__(*args, group=group, on_change=on_change, **kwargs)
        self._classes.append("nicegui-row")


class SortableColumn(SortableElement):
    """Sortable Column element."""

    def __init__(self, group: str, on_change: Callable | None = None, *args, **kwargs) -> None:
        """Initialize a column that is sortable."""
        super().__init__(*args, group=group, on_change=on_change, **kwargs)
        self._classes.append("nicegui-column")
