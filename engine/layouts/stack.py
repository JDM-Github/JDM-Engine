from .base import BaseLayout
from engine.behavior import ScrollBehavior

class StackLayout(
    ScrollBehavior,
    BaseLayout
):

    def __init__(self, parent=None, orientation="vertical", **kwargs):
        super().__init__(parent, **kwargs)

        if orientation not in ("horizontal", "vertical"):
            raise ValueError("orientation must be 'horizontal' or 'vertical'")

        self.orientation = orientation

    def _reflow(self):
        rect = self._content_rect()
        if not self.widgets:
            return

        x = rect.left() - self.scroll_start_x
        y = rect.top() - self.scroll_start_y

        for w in self.widgets:
            w.x = int(x)
            w.y = int(y)

            if self.orientation == "horizontal":
                x += w.width + self.spacing
            else:
                y += w.height + self.spacing
