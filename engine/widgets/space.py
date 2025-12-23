from engine.ui.styles import *
from engine.widgets.widget import Widget


class Space(
    Widget
):
    def __init__(self, parent=None, **kwargs):
        background_color = kwargs.pop("background_color", None)
        background_hover_color = kwargs.pop("background_hover_color", None)

        super().__init__(parent, **kwargs)
        self.background_color = background_color
        self.background_hover_color = background_hover_color
