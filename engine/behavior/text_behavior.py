from PyQt6.QtGui import QPainter, QPen, QFontMetrics
from PyQt6.QtGui import QFont

from engine.behavior.hover_behavior import HoverBehavior
from engine.behavior.size_behavior import SizeBehavior
from engine.core.constant import *
from engine.core.factory import Factory
from engine.property import *
from engine.ui.styles import *

class TextBehavior(
    HoverBehavior,
    SizeBehavior
):
    text            : str = StringProperty("")
    font_size       : int = IntegerProperty(10)
    font_weight     : int = IntegerProperty(400)
    font_family     : str = StringProperty("")

    padding         : Padding = ObjectProperty(Padding(), Padding)
    text_color      : Color = ObjectProperty( None, Color )
    text_hover_color: Color = ObjectProperty( None, Color )

    align_h = ObjectProperty(TextHAlignment.CENTER, TextHAlignment)
    align_v = ObjectProperty(TextVAlignment.CENTER, TextVAlignment)

    def __init__(self, *args, **kwargs):
        text             = kwargs.pop("text", "Button")
        padding          = kwargs.pop("padding", Padding(*Factory.get("DEFAULT_TEXT_PADDING")))
        font_size        = kwargs.pop("font_size", Factory.get("DEFAULT_FONT_SIZE"))
        font_weight      = kwargs.pop("font_weight", Factory.get("DEFAULT_FONT_WEIGHT"))
        font_family      = kwargs.pop("font_family", Factory.get("DEFAULT_FONT_NAME"))
        text_color       = kwargs.pop("text_color", Color(Colors.gray["200"]))
        text_hover_color = kwargs.pop("text_hover_color", Color(Colors.gray["200"]))
        align_h          = kwargs.pop("align_h", TextHAlignment.CENTER)
        align_v          = kwargs.pop("align_v", TextVAlignment.CENTER)

        super().__init__(*args, **kwargs)
        self.text             = text
        self.padding          = padding
        self.font_size        = font_size
        self.font_weight      = font_weight
        self.font_family      = font_family
        self.text_color       = text_color
        self.text_hover_color = text_hover_color
        self.align_h          = align_h
        self.align_v          = align_v


    def paintEvent(self, *args):
        parent = super()
        if hasattr(parent, "paintEvent"):
            parent.paintEvent(*args)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.is_hover and self.text_hover_color:
            if self.text_hover_color: text_color = self.text_hover_color.to_qcolor()
        else:
            if self.text_color: text_color = self.text_color.to_qcolor()

        if hasattr(self, "is_pressed") and hasattr(self, "text_click_color"):
            is_pressed = getattr(self, "is_pressed")
            text_click_color: Color = getattr(self, "text_click_color")
            if is_pressed and text_click_color:
                text_color = text_click_color.to_qcolor()

        f = QFont(self.font_family, self.font_size)
        f.setWeight(self.font_weight)
        painter.setFont(f)

        fm = QFontMetrics(painter.font())
        text = self.text

        x = self.padding.x
        if self.align_h == TextHAlignment.CENTER:
            x = (self.width - fm.horizontalAdvance(text)) // 2
        elif self.align_h == TextHAlignment.RIGHT:
            x = self.width - fm.horizontalAdvance(text) - self.padding.x

        y = self.padding.y + fm.ascent()
        if self.align_v == TextVAlignment.CENTER:
            y = (self.height + fm.ascent() - fm.descent()) // 2
        elif self.align_v == TextVAlignment.BOTTOM:
            y = self.height - self.padding.y - fm.descent()

        painter.setPen(QPen(text_color))
        painter.drawText(x, y, text)
