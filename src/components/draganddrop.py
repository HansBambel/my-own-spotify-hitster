import logging
from collections.abc import Callable
from typing import ClassVar, Self

from nicegui import ui
from nicegui.awaitable_response import AwaitableResponse
from nicegui.events import GenericEventArguments

from src.config import ROOT_DIR
from src.spotify_functions import SpotifySong

logger = logging.getLogger(__name__)


class Card(ui.card):
    """A draggable card."""

    def __init__(self, item: SpotifySong) -> None:
        """Initialize the card with the info of the SpotifySong it represents."""
        super().__init__()
        self.item = item
        with self.props("draggable").classes("w-full cursor-pointer bg-grey-1"):
            self.info_spot = ui.column()
            self.show_reveal()

    @ui.refreshable_method
    def show_reveal(self) -> None:
        """Update the information on the card. Depends on reveal."""
        self.info_spot.clear()
        with self.info_spot:
            if self.item.reveal:
                ui.label(f"{self.item.artist}")
                # ui.label("-")
                ui.label(f"{self.item.title}")
                # ui.label(f"Album: \n{self.item.album}")
                ui.input(placeholder=f"{self.item.release_year}").classes("text-xl font-bold")
            else:
                ui.label("?")


class SortableElement(ui.element, component=ROOT_DIR / "resources" / "sortable_element.js"):  # type: ignore
    """Sortable Row element."""

    sortable_list: ClassVar[dict[int, Self]] = {}

    def __init__(self, *args, group: str, on_change: Callable | None = None, **kwargs) -> None:
        """Assign the group and on_change-function."""
        super().__init__()
        self.on("item-drop", self.drop)
        self.on_change = on_change

        self._classes.append("nicegui-column")
        self._props["group"] = group
        SortableElement.sortable_list[self.id] = self

    def drop(self, e: GenericEventArguments) -> None:
        """Run the on_change function."""
        print(e)
        if self.on_change:
            self.on_change(
                e.args["new_index"],
                e.args["old_index"],
                SortableElement.sortable_list[e.args["new_list"]],
                SortableElement.sortable_list[e.args["old_list"]],
            )
        else:
            logger.debug(e.args)

    def makeSortable(self) -> None:
        """Make the element sortable."""
        self.run_method("makeSortable")

    def getitems(self) -> AwaitableResponse:
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
