from engine.behavior import ToggleBehavior, BorderBehavior, TextBehavior
from engine.core.constant import *
from engine.ui.styles import *
from engine.property import *
from engine.widgets.widget import Widget


class Toggle(
    BorderBehavior,
    ToggleBehavior,
    TextBehavior,
    Widget
):
    group                   : object = ObjectProperty(None)
    radio_mode              : bool   = BooleanProperty(False)

    text_toggle_color        : Color  = ObjectProperty(None, Color)
    background_toggle_color  : Color  = ObjectProperty(None, Color)
    border_toggle            : Border = ObjectProperty(None, Border)

    def __init__(self, parent=None, **kwargs):
        group                   = kwargs.pop("group", None)
        radio_mode              = kwargs.pop("radio_mode", False)
        text_toggle_color       = kwargs.pop("text_toggle_color", None)
        background_toggle_color = kwargs.pop(
            "background_toggle_color",
            Color(Colors.gray["950"])
        )
        border_toggle           = kwargs.pop("border_toggle", None)

        super().__init__(parent, **kwargs)

        self.group = group
        self.radio_mode = radio_mode
        self.text_toggle_color       = text_toggle_color
        self.background_toggle_color = background_toggle_color
        self.border_toggle           = border_toggle
