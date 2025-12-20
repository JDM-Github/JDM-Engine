from .base import BaseLayout

class BoxLayout(BaseLayout):
    HORIZONTAL = "horizontal"
    VERTICAL   = "vertical"

    def __init__(self, parent=None, orientation=HORIZONTAL, **kwargs):
        super().__init__(parent, **kwargs)
        self.orientation = orientation

    def _reflow(self):
        rect = self._content_rect()

        x, y = rect.left(), rect.top()

        for w in self._items:
            hint = w.sizeHint()

            if self.orientation == self.HORIZONTAL:
                width = hint.width()
                w.setGeometry(x, rect.top(), width, rect.height())
                w.resize(width, rect.height())
                w.move(x, rect.top())
                x += width + self.spacing
            else:
                height = hint.height()
                w.setGeometry(rect.left(), y, rect.width(), height)
                w.repaint()
                y += height + self.spacing
