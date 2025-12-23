from .base import BaseLayout

class AnchorLayout(BaseLayout):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def _reflow(self):
        rect = self._content_rect()
        if not self.widgets:
            return

        cx = rect.left() + rect.width() // 2
        cy = rect.top() + rect.height() // 2

        for w in self.widgets:
            ax = getattr(w, "anchor_x", "left")
            ay = getattr(w, "anchor_y", "top")

            if ax == "center":
                w.x = int(cx - w.width // 2)
            elif ax == "right":
                w.x = int(rect.right() - w.width)
            else:
                w.x = int(rect.left())

            if ay == "center":
                w.y = int(cy - w.height // 2)
            elif ay == "bottom":
                w.y = int(rect.bottom() - w.height)
            else:
                w.y = int(rect.top())
