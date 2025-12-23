from .base import BaseLayout

class OverlayLayout(BaseLayout):

    def _reflow(self):
        if not self.widgets:
            return

        rect = self._content_rect()
        for w in self.widgets:

            w.x = int(rect.left())
            w.y = int(rect.top())
            w.width = int(rect.width())
            w.height = int(rect.height())
