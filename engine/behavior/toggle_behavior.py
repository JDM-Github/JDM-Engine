from typing import Callable
from PyQt6.QtCore import Qt, QTimer
from engine.property import *


class ToggleBehavior:

    is_toggled        : bool     = BooleanProperty(False)
    on_toggle         : Callable = FunctionProperty(None)
    on_down           : Callable = FunctionProperty(None)
    on_down_interval  : int      = IntegerProperty(300)

    def __init__(self, *args, **kwargs):
        is_toggled = kwargs.pop("is_toggled", False)
        super().__init__(*args, **kwargs)
        self.is_toggled = is_toggled
        self._down_timer = QTimer(self)
        self._down_timer.timeout.connect(self._emit_on_down)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.on_down:
                self._down_timer.start(self.on_down_interval)

        parent = super()
        if hasattr(parent, "mousePressEvent"):
            parent.mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:

            radio = getattr(self, "radio_mode", False)
            group = getattr(self, "group", None)
            if radio and group is not None and self.is_toggled:
                self._down_timer.stop()
                return

            new_state = not self.is_toggled
            if new_state and group is not None:
                self._untoggle_group_peers()

            self.is_toggled = new_state
            if hasattr(self, "update"):
                self.update()

            if self.on_toggle:
                self.on_toggle(self.is_toggled)

            self._down_timer.stop()

        parent = super()
        if hasattr(parent, "mouseReleaseEvent"):
            parent.mouseReleaseEvent(event)


    def _untoggle_group_peers(self):
        parent = self.parent()
        if not parent:
            return

        group = getattr(self, "group", None)
        for child in parent.children():
            if child is self:
                continue

            if (
                hasattr(child, "group")
                and child.group == group
                and hasattr(child, "is_toggled")
            ):
                if child.is_toggled:
                    child.is_toggled = False
                    if hasattr(child, "update"):
                        child.update()
                    if hasattr(child, "on_toggle") and child.on_toggle:
                        child.on_toggle(False)


    def _emit_on_down(self):
        if self.on_down:
            self.on_down()
