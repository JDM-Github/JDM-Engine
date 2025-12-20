from engine.behavior.text_behavior import TextBehavior
from engine.ui.styles import *
from engine.widgets.widget import Widget


class Text(
    TextBehavior,
    Widget
):
    ALLOWED_KWARGS = {
        "x",
        "y",
        "text",
        "font_size",
        "font_weight",
        "font_family",
        "padding",
        "text_color",
        "text_hover_color",
        "align_h",
        "align_v",
        "width",
        "height",
        "size_hint",
        "shadow_offset",
        "shadow_color",
        "shadow_blur",
        "rounding",
        "background_color",
        "background_hover_color",
    }

    def __init__(self, parent, **kwargs):
        invalid_keys = set(kwargs) - self.ALLOWED_KWARGS
        if invalid_keys:
            raise TypeError(
                f"{self.__class__.__name__} does not accept: {invalid_keys}"
            )

        background_color = kwargs.pop("background_color", None)
        background_hover_color = kwargs.pop("background_hover_color", None)

        super().__init__(parent, **kwargs)
        self.background_color = background_color
        self.background_hover_color = background_hover_color
