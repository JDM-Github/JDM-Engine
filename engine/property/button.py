from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QFontMetrics

from engine.behavior.button_behavior import ButtonBehavior
from engine.core.constant import TextHAlignment, TextVAlignment
from engine.ui.styles.border import Border
from engine.ui.styles.color import Color
from engine.ui.styles.colors import Colors
from engine.ui.styles.font import Font

from engine.property import *
from engine.widgets.text import Text

class Button(ButtonBehavior, Text):

    text_click_color      : Color = ObjectProperty( Color(Colors.gray["200"]), Color )
    background_click_color: Color = ObjectProperty( Color(Colors.gray["950"]), Color )

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.border      : Border = kwargs.get("border", None)
        self.border_hover: Border = kwargs.get("border_hover", None)
        self.border_click: Border = kwargs.get("border_click", None)

        self.font_style  : Font = kwargs.get("font", None)
        self.rounding      = kwargs.get("rounding", 12)

        if kwargs.get("shadow", False):
            self._apply_shadow(kwargs.get("shadow_blur", 50))


    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.is_pressed and self.background_click_color:
            bg = self.background_click_color.to_qcolor()
            if self.text_click_color: text_color = self.text_click_color.to_qcolor()
        elif self.is_hover and self.background_hover_color:
            bg = self.background_hover_color.to_qcolor()
            if self.text_hover_color: text_color = self.text_hover_color.to_qcolor()
        else:
            bg = self.background_color.to_qcolor()
            if self.text_color: text_color = self.text_color.to_qcolor()


        # Draw background
        brush = QBrush(bg)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.rounding, self.rounding)


        # Draw border
        border = self.border
        if self.is_pressed and self.border_click:
            border = self.border_click
        elif self.is_hover and self.border_hover:
            border = self.border_hover

        if border and border.width:
            pen = QPen(QColor(border.color), border.width)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(self.rect().adjusted(
                border.width // 2,
                border.width // 2,
                -border.width // 2,
                -border.width // 2),
                self.rounding, self.rounding)


        # Draw text
        if self.font_style:
            font = self.font_style.to_qfont()
            painter.setFont(font)

        fm = QFontMetrics(painter.font())
        text = self.text()

        x = self.padding.x
        if self.align_h == TextHAlignment.CENTER:
            x = (self.width() - fm.horizontalAdvance(text)) // 2
        elif self.align_h == TextHAlignment.RIGHT:
            x = self.width() - fm.horizontalAdvance(text) - self.padding.x

        y = self.padding.y + fm.ascent()
        if self.align_v == TextVAlignment.CENTER:
            y = (self.height() + fm.ascent() - fm.descent()) // 2
        elif self.align_v == TextVAlignment.BOTTOM:
            y = self.height() - self.padding.y - fm.descent()

        if self.font_style:
            if self.font_style.shadow_color:
                shadow_color = QColor(self.font_style.shadow_color)
                dx, dy = self.font_style.shadow_offset
                painter.setPen(shadow_color)
                painter.drawText(x+dx, y+dy, text)

        painter.setPen(QPen(text_color))
        painter.drawText(x, y, text)

