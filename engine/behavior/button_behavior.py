from typing import Callable
from PyQt6.QtCore import Qt, QTimer
from engine.property import *

class ButtonBehavior:

    is_pressed: bool = BooleanProperty(False)
    on_pressed: Callable = FunctionProperty(None)
    on_release: Callable = FunctionProperty(None)
    on_down: Callable = FunctionProperty(None)
    on_down_interval: int = IntegerProperty(300)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._down_timer = QTimer(self)
        self._down_timer.timeout.connect(self._emit_on_down)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = True
            if hasattr(self, "update"): self.update()
            if self.on_pressed: self.on_pressed()
            if self.on_down: self._down_timer.start(self.on_down_interval)
        
        parent = super()
        if hasattr(parent, "mousePressEvent"):
            parent.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = False
            if hasattr(self, "update"): self.update()
            if self.on_release: self.on_release()
            self._down_timer.stop()

        parent = super()
        if hasattr(parent, "mouseReleaseEvent"):
            parent.mouseReleaseEvent(event)

    def _emit_on_down(self):
        if self.on_down: self.on_down()
