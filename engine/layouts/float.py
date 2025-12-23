from .base import BaseLayout
from engine.widgets.widget import Widget

class FloatLayout(BaseLayout):

    def _reflow(self):
        childrens = [
            widget for widget in self.children()
            if isinstance(widget, (Widget, BaseLayout))
        ]
        for child in childrens:
            if isinstance(child, BaseLayout):
                child._reflow()
