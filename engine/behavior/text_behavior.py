import math
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QFont,
    QFontMetrics,
    QPainterPath,
    QLinearGradient,
    QColor,
    QBrush,
)

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

    text_padding    : Padding = ObjectProperty(None, Padding)

    text_color        : Color = ObjectProperty(None, Color)
    text_hover_color  : Color = ObjectProperty(None, Color)
    text_click_color  : Color = ObjectProperty(None, Color)
    text_toggle_color : Color = ObjectProperty(None, Color)

    align_h = ObjectProperty(TextHAlignment.CENTER, TextHAlignment)
    align_v = ObjectProperty(TextVAlignment.CENTER, TextVAlignment)

    def __init__(self, *args, **kwargs):
        text             = kwargs.pop("text", "Button")
        text_padding     = kwargs.pop("text_padding", Padding(*Factory.get("DEFAULT_TEXT_PADDING")))
        font_size        = kwargs.pop("font_size", Factory.get("DEFAULT_FONT_SIZE"))
        font_weight      = kwargs.pop("font_weight", Factory.get("DEFAULT_FONT_WEIGHT"))
        font_family      = kwargs.pop("font_family", Factory.get("DEFAULT_FONT_NAME"))
        text_color       = kwargs.pop("text_color", Color(Colors.gray["200"]))
        text_hover_color = kwargs.pop("text_hover_color", None)
        align_h          = kwargs.pop("align_h", TextHAlignment.CENTER)
        align_v          = kwargs.pop("align_v", TextVAlignment.CENTER)

        super().__init__(*args, **kwargs)

        self.text             = text
        self.text_padding     = text_padding
        self.font_size        = font_size
        self.font_weight      = font_weight
        self.font_family      = font_family
        self.text_color       = text_color
        self.text_hover_color = text_hover_color
        self.align_h          = align_h
        self.align_v          = align_v

    # -------------------------------------------------------------

    def _resolve_text_color(self) -> Color | None:
        if self.is_hover and self.text_hover_color:
            return self.text_hover_color

        color = self.text_color

        if getattr(self, "is_pressed", False) and getattr(self, "text_click_color", None):
            color = self.text_click_color

        if getattr(self, "is_toggled", False) and getattr(self, "text_toggle_color", None):
            color = self.text_toggle_color

        return color

    def _make_gradient_brush(self, color: Color, rect):
        angle = color.gradient_angle or 0
        rad = math.radians(angle)

        cx, cy = rect.center().x(), rect.center().y()
        length = max(rect.width(), rect.height())

        dx = math.cos(rad) * length / 2
        dy = math.sin(rad) * length / 2

        start = QPointF(cx - dx, cy - dy)
        end   = QPointF(cx + dx, cy + dy)

        gradient = QLinearGradient(start, end)
        n = len(color.color_list)

        for i, c in enumerate(color.color_list):
            gradient.setColorAt(i / (n - 1), QColor(c))

        return QBrush(gradient)

    # -------------------------------------------------------------

    def paintEvent(self, *args):
        parent = super()
        if hasattr(parent, "paintEvent"):
            parent.paintEvent(*args)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._resolve_text_color()
        if not color:
            return

        font = QFont(self.font_family, self.font_size)
        font.setWeight(self.font_weight)
        painter.setFont(font)

        fm = QFontMetrics(font)
        text = self.text
        pad = self.text_padding

        text_width = fm.horizontalAdvance(text)

        # ---------------------------------------------------------
        # horizontal alignment
        # ---------------------------------------------------------
        if self.align_h == TextHAlignment.CENTER:
            x = (self.width - text_width) // 2
        elif self.align_h == TextHAlignment.RIGHT:
            x = self.width - text_width - pad.right
        else: 
            x = pad.left

        # ---------------------------------------------------------
        # vertical alignment
        # ---------------------------------------------------------
        if self.align_v == TextVAlignment.CENTER:
            y = (self.height + fm.ascent() - fm.descent()) // 2
        elif self.align_v == TextVAlignment.BOTTOM:
            y = self.height - pad.bottom - fm.descent()
        else:
            y = pad.top + fm.ascent()

        # ---------------------------------------------------------
        # FAST PATH: solid color
        # ---------------------------------------------------------
        if not color.gradient or len(color.color_list) <= 1:
            painter.setPen(QPen(color.to_qcolor()))
            painter.drawText(x, y, text)
            return

        # ---------------------------------------------------------
        # GRADIENT PATH
        # ---------------------------------------------------------
        path = QPainterPath()
        path.addText(x, y, font, text)
        text_rect = path.boundingRect().toRect()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._make_gradient_brush(color, text_rect))
        painter.drawPath(path)
