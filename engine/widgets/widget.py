from typing import List
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QEvent
from engine.behavior.hover_behavior import HoverBehavior
from engine.behavior.pos_behavior import PosBehavior
from engine.behavior.size_behavior import SizeBehavior

from engine.ui.styles import *
from engine.property import *

class Widget(
    HoverBehavior,
    SizeBehavior,
    PosBehavior,
    QWidget
):
    size_hint             : List[int] = ListProperty([None, None], None)
    shadow_offset         : List[int] = ListProperty([0, 0], int)
    shadow_color          : Color = ObjectProperty( None, Color )
    shadow_blur           : int = IntegerProperty(12)
    rounding              : int = IntegerProperty(12)
    background_color      : Color = ObjectProperty( Color(Colors.gray["800"]), Color )
    background_hover_color: Color = ObjectProperty( None, Color )

    def __init__(self, parent, **kwargs):
        size_hint              = kwargs.pop("size_hint", [0.3, None])
        shadow_color           = kwargs.pop("shadow_color", Color(Colors.gray["950"]))
        shadow_offset          = kwargs.pop("shadow_offset", [0, 2])
        background_color       = kwargs.pop("background_color", Color(Colors.gray["800"]))
        background_hover_color = kwargs.pop("background_hover_color", None)
        shadow_blur            = kwargs.pop("shadow_blur", 12)
        rounding               = kwargs.pop("rounding", 12)
        super().__init__(parent, **kwargs)

        self.size_hint              = size_hint
        self.shadow_color           = shadow_color
        self.shadow_offset          = shadow_offset
        self.background_color       = background_color
        self.background_hover_color = background_hover_color
        self.shadow_blur            = shadow_blur
        self.rounding               = rounding

        self.setMouseTracking(True)
        if self.parent():
            self._apply_size_hint()
            self.parent().installEventFilter(self)

    def paintEvent(self, *args):
        super().paintEvent(*args)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = None
        if self.is_hover and self.background_hover_color:
            bg = self.background_hover_color.to_qcolor()
        elif self.background_color:
            bg = self.background_color.to_qcolor()

        if hasattr(self, "is_pressed") and hasattr(self, "background_click_color"):
            is_pressed = getattr(self, "is_pressed")
            background_click_color: Color = getattr(self, "background_click_color")
            if is_pressed and background_click_color:
                bg = background_click_color.to_qcolor()

        if bg:
            brush = QBrush(bg)
            painter.setBrush(brush)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect(), self.rounding, self.rounding)

        if not hasattr(self, "border"): return

        border: Border = getattr(self, "border")
        if self.is_hover and hasattr(self, "border_hover"):
            border_hover = getattr(self, "border_hover")
            if border_hover: border = border_hover

        if hasattr(self, "is_pressed") and hasattr(self, "border_click"):
            is_pressed = getattr(self, "is_pressed")
            border_click = getattr(self, "border_click")
            if is_pressed and border_click: border = border_click

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
        
        self._apply_shadow(self.shadow_blur)

    def on_x(self, _, value): self.move(value, self.y)
    def on_y(self, _, value): return self.move(self.x, value)
    def on_width(self, _, value) : return self.resize(value, self.height)
    def on_height(self, _, value): return self.resize(self.width, value)
    
    def eventFilter(self, obj, event: QEvent):
        if obj == self.parent() and event.type() == event.Type.Resize:
            self._apply_size_hint()
        return super().eventFilter(obj, event)
    
    def _apply_size_hint(self):
        if self.parent() and self.size_hint:
            pw, ph = self.parent().width(), self.parent().height()
            width_factor, height_factor = self.size_hint

            self.width  = int(pw * width_factor)  if width_factor is not None else self.width
            self.height = int(ph * height_factor) if height_factor is not None else self.height

    def enterEvent(self, _):
        self.is_hover = True
        self.update()

    def leaveEvent(self, _):
        self.is_hover = False
        self.update()

    def _apply_shadow(self, blur: int):
        if not hasattr(self, "_shadow"):
            self._shadow = QGraphicsDropShadowEffect(self)
            self._shadow.setOffset(*self.shadow_offset)
            self.setGraphicsEffect(self._shadow)

        self._shadow.setBlurRadius(blur)
        color = self.shadow_color.to_qcolor()
        self._shadow.setColor(QColor(color))
