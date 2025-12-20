# base_layout.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect

class BaseLayout(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        self.padding = kwargs.get("padding", (0, 0, 0, 0))  # l, t, r, b
        self.spacing = kwargs.get("spacing", 0)

        self._items: list[QWidget] = []

    # -------- Public API --------

    def add_widget(self, widget: QWidget):
        widget.setParent(self)
        self._items.append(widget)
        self._reflow()

    def remove_widget(self, widget: QWidget):
        if widget in self._items:
            self._items.remove(widget)
            widget.setParent(None)
            self._reflow()

    def clear(self):
        for w in self._items:
            w.setParent(None)
        self._items.clear()
        self._reflow()

    def resizeEvent(self, _):
        self._reflow()

    def _content_rect(self) -> QRect:
        l, t, r, b = self.padding
        return self.rect().adjusted(l, t, -r, -b)

    # -------- Override --------

    def _reflow(self):
        raise NotImplementedError
