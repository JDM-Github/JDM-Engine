from engine.behavior.border_behavior import BorderBehavior
from engine.behavior.button_behavior import ButtonBehavior
from engine.behavior.text_behavior import TextBehavior

from engine.core.constant import *
from engine.ui.styles import *

from engine.property import *
from engine.widgets.widget import Widget

class Button(
    BorderBehavior,
    ButtonBehavior,
    TextBehavior,
    Widget
):
    text_click_color      : Color  = ObjectProperty( None, Color )
    background_click_color: Color  = ObjectProperty( None, Color )
    border_click          : Border = ObjectProperty( None, Border )

    def __init__(self, parent, **kwargs):
        text_click_color      : Color  = kwargs.pop("text_click_color", None)
        background_click_color: Color  = kwargs.pop("background_click_color", Color(Colors.gray["950"]))
        border_click          : Border = kwargs.pop("border_click", None)

        super().__init__(parent, **kwargs)
        self.text_click_color       = text_click_color
        self.background_click_color = background_click_color
        self.border_click           = border_click
