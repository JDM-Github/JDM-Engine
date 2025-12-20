from .base import BaseLayout

class GridLayout(BaseLayout):
    def __init__(self, parent=None, rows=1, cols=1, **kwargs):
        super().__init__(parent, **kwargs)
        self.rows = rows
        self.cols = cols

    def _reflow(self):
        rect = self._content_rect()
        if self.rows <= 0 or self.cols <= 0:
            return

        cell_w = rect.width() // self.cols
        cell_h = rect.height() // self.rows

        for i, w in enumerate(self._items):
            r = i // self.cols
            c = i % self.cols

            if r >= self.rows:
                break

            x = rect.left() + c * cell_w
            y = rect.top() + r * cell_h
            w.setGeometry(x, y, cell_w, cell_h)
