from .base import BaseLayout

class AspectLayout(BaseLayout):

    def __init__(self, parent=None, aspect_ratio=1.0, **kwargs):
        super().__init__(parent, **kwargs)
        self.aspect_ratio = aspect_ratio 

    def _reflow(self):
        if not self.widgets:
            return

        rect = self._content_rect()
        for w in self.widgets:
            if rect.width() / rect.height() > self.aspect_ratio:
                height = rect.height()
                width = height * self.aspect_ratio
            else:
                width = rect.width()
                height = width / self.aspect_ratio

            w.width = int(width)
            w.height = int(height)

            w.x = int(rect.left() + (rect.width() - width) / 2)
            w.y = int(rect.top() + (rect.height() - height) / 2)
