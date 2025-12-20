from .base import BaseLayout

class StackLayout(BaseLayout):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

    def __init__(self, parent=None, orientation=HORIZONTAL, **kwargs):
        super().__init__(parent, **kwargs)
        self.orientation = orientation

    def _reflow(self):
        rect = self._content_rect()

        x, y = rect.left(), rect.top()
        line_max = 0

        for w in self._items:
            hint = w.sizeHint()

            if self.orientation == self.HORIZONTAL:
                if x + hint.width() > rect.right():
                    x = rect.left()
                    y += line_max + self.spacing
                    line_max = 0

                w.setGeometry(x, y, hint.width(), hint.height())
                x += hint.width() + self.spacing
                line_max = max(line_max, hint.height())

            else:
                if y + hint.height() > rect.bottom():
                    y = rect.top()
                    x += line_max + self.spacing
                    line_max = 0

                w.setGeometry(x, y, hint.width(), hint.height())
                y += hint.height() + self.spacing
                line_max = max(line_max, hint.width())
