from PyQt6.QtCore import QRect
from typing import List
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QEvent
from engine.behavior.hover_behavior import HoverBehavior
from engine.behavior.pos_behavior import PosBehavior
from engine.behavior.size_behavior import SizeBehavior

from engine.core.constant import AspectRatio
from engine.core.factory import Factory
from engine.ui._drawer import Drawer
from engine.ui.styles import *
from engine.property import *

class Widget(
    HoverBehavior,
    SizeBehavior,
    PosBehavior,
    QWidget
):
    padding               : Padding = ObjectProperty(None, Padding)
    shadow_active         : bool = BooleanProperty(True)
    anchor_x              : str = StringProperty("left")
    anchor_y              : str = StringProperty("top")
    pos_hint              : List[float] = ListProperty([None, None], None)
    size_hint             : List[float] = ListProperty([None, None], None)
    shadow_offset         : List[float] = ListProperty([0, 0], int)
    shadow_color          : Color = ObjectProperty( None, Color )
    shadow_blur           : float = FloatProperty(12)
    rounding              : float = FloatProperty(12)
    background_color      : Color = ObjectProperty( Color(Colors.gray["800"]), Color )
    background_hover_color: Color = ObjectProperty( None, Color )
    aspect_ratio_follow   : AspectRatio = ObjectProperty(None, AspectRatio) 
    aspect_ratio          : float = FloatProperty(1)

    def __init__(self, parent=None, **kwargs):
        padding                = kwargs.pop("padding", Padding(*Factory.get("DEFAULT_WIDGET_PADDING")))
        anchor_x               = kwargs.pop("anchor_x", "left")
        anchor_y               = kwargs.pop("anchor_y", "top")
        pos_hint               = kwargs.pop("pos_hint", [None, None])
        size_hint              = kwargs.pop("size_hint", [None, None])
        shadow_active          = kwargs.pop("shadow_active", False)
        shadow_color           = kwargs.pop("shadow_color", Color(Colors.gray["950"]))
        shadow_offset          = kwargs.pop("shadow_offset", [0, 2])
        background_color       = kwargs.pop("background_color", Color(Colors.gray["100"]))
        background_hover_color = kwargs.pop("background_hover_color", None)
        shadow_blur            = kwargs.pop("shadow_blur", 12)
        rounding               = kwargs.pop("rounding", 8)
        aspect_ratio_follow    = kwargs.pop("aspect_ratio_follow", AspectRatio.NONE)
        aspect_ratio           = kwargs.pop("aspect_ratio", 1)
        super().__init__(parent, **kwargs)

        self._updating              = False
        self.padding                = padding
        self.shadow_active          = shadow_active
        self.anchor_x               = anchor_x
        self.anchor_y               = anchor_y
        self.pos_hint               = pos_hint
        self.size_hint              = size_hint
        self.shadow_color           = shadow_color
        self.shadow_offset          = shadow_offset
        self.background_color       = background_color
        self.background_hover_color = background_hover_color
        self.shadow_blur            = shadow_blur
        self.rounding               = rounding
        self.aspect_ratio_follow    = aspect_ratio_follow
        self.aspect_ratio           = aspect_ratio

        self.setMouseTracking(True)
        if self.parent():
            self._apply_size_hint()
            self._apply_pos_hint()
            self.parent().installEventFilter(self)
        self.show()

    def paint_border(self, painter: QPainter):
        if not hasattr(self, "border"):
            return

        border: Border = getattr(self, "border")
        if self.is_hover and getattr(self, "border_hover", None):
            border = self.border_hover

        if (
            getattr(self, "is_pressed", False)
            and getattr(self, "border_click", None)
        ):
            border = self.border_click
        
        if (
            getattr(self, "is_toggled", False)
            and getattr(self, "border_toggle", None)
        ):
            border = self.border_toggle

        if not border or not border.width:
            return

        pen = QPen()
        pen.setWidth(border.width)
        pen.setBrush(Drawer._make_border_brush(self, border.color))
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        w = border.width // 2
        painter.drawRoundedRect(
            self._content_rect().adjusted(w, w, -w, -w),
            self.rounding,
            self.rounding
        )

    def paintEvent(self, *args):
        super().paintEvent(*args)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = None

        if self.is_hover and getattr(self, "background_hover_color", None):
            color = self.background_hover_color
        elif getattr(self, "background_color", None):
            color = self.background_color

        if (
            getattr(self, "is_pressed", False)
            and getattr(self, "background_click_color", None)
        ):
            color = self.background_click_color
        
        if (
            getattr(self, "is_toggled", False)
            and getattr(self, "background_toggle_color", None)
        ):
            color = self.background_toggle_color

        if color:
            painter.setBrush(Drawer._make_brush(self, color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self._content_rect(), self.rounding, self.rounding)

        self.paint_border(painter)
        if self.shadow_active: self._apply_shadow(self.shadow_blur)

    def _clamp_size(self, value, min_v, max_v):
        if max_v > 0: value = min(value, max_v)
        if min_v > 0: value = max(value, min_v)
        return value

    def is_layout_updating(self):
        parent = self.parent()
        from engine.layouts import GridLayout, BoxLayout
        if isinstance(parent, GridLayout) or \
            isinstance(parent, BoxLayout):
            return getattr(self, "_updating", False)
        return True

    def on_x(self, _, value, old):
        if not self.is_layout_updating():
            Widget.y.set_raw(self, old)
            return

        self.old_y = old
        self.move(value, self.y)

    def on_y(self, _, value, old):
        if not self.is_layout_updating():
            Widget.x.set_raw(self, old)
            return

        self.old_x = old
        self.move(self.x, value)

    def on_width(self, _, value, old):
        if not self.is_layout_updating():
            Widget.width.set_raw(self, old)
            return

        self.old_width = old
        w = self._clamp_size(value, self.min_width, self.max_width)
        h = self.height

        if self.aspect_ratio_follow == AspectRatio.HEIGHT and self.aspect_ratio > 0:
            w = int(h * self.aspect_ratio)
            w = self._clamp_size(w, self.min_width, self.max_width)

        if self.aspect_ratio_follow == AspectRatio.WIDTH and self.aspect_ratio > 0:
            h = int(w / self.aspect_ratio)
            h = self._clamp_size(h, self.min_height, self.max_height)
        
        Widget.width.set_raw(self, w)
        Widget.height.set_raw(self, h)
        self.resize(w, h)

    def on_height(self, _, value, old):
        if not self.is_layout_updating():
            Widget.height.set_raw(self, old)
            return

        self.old_height = old
        h = self._clamp_size(value, self.min_height, self.max_height)
        w = self.width

        if self.aspect_ratio_follow == AspectRatio.HEIGHT and self.aspect_ratio > 0:
            w = int(h * self.aspect_ratio)
            w = self._clamp_size(w, self.min_width, self.max_width)

        if self.aspect_ratio_follow == AspectRatio.WIDTH and self.aspect_ratio > 0:
            h = int(w / self.aspect_ratio)
            h = self._clamp_size(h, self.min_height, self.max_height)
        
        Widget.width.set_raw(self, w)
        Widget.height.set_raw(self, h)
        self.resize(w, h)

    def eventFilter(self, obj, event: QEvent):
        if obj == self.parent() and event.type() == event.Type.Resize:
            self._apply_size_hint()
            self._apply_pos_hint()
        return super().eventFilter(obj, event)

    def _apply_pos_hint(self):
        if not (self.parent() and self.pos_hint):
            return

        parent = self.parent()
        from engine.layouts import GridLayout, BoxLayout
        if isinstance(parent, (GridLayout, BoxLayout)):
            return

        pw = parent.width()  if callable(getattr(parent, "width", None)) else parent.width
        ph = parent.height() if callable(getattr(parent, "height", None)) else parent.height

        hx, hy = self.pos_hint
        x = self.x
        y = self.y

        if hx is not None:
            x = pw * hx
            Widget.x.set_raw(self, int(x))

        if hy is not None:
            y = ph * hy
            Widget.y.set_raw(self, int(y))

        self.move(int(x), int(y))

    def _apply_size_hint(self):
        if not (self.parent() and self.size_hint):
            return

        parent = self.parent()

        from engine.layouts import GridLayout, BoxLayout
        if isinstance(parent, (GridLayout, BoxLayout)):
            return

        pw = parent.width()  if callable(getattr(parent, "width", None)) else parent.width
        ph = parent.height() if callable(getattr(parent, "height", None)) else parent.height

        width_factor, height_factor = self.size_hint

        w = int(pw * width_factor)  if width_factor is not None else self.width
        h = int(ph * height_factor) if height_factor is not None else self.height

        w = self._clamp_size(w, self.min_width, self.max_width)
        h = self._clamp_size(h, self.min_height, self.max_height)

        if self.aspect_ratio_follow and self.aspect_ratio > 0:
            if self.aspect_ratio_follow == AspectRatio.WIDTH:
                h = int(w / self.aspect_ratio)
                h = self._clamp_size(h, self.min_height, self.max_height)
            elif self.aspect_ratio_follow == AspectRatio.HEIGHT:
                w = int(h * self.aspect_ratio)
                w = self._clamp_size(w, self.min_width, self.max_width)

        Widget.width.set_raw(self, int(w))
        Widget.height.set_raw(self, int(h))
        self.resize(int(w), int(h))

    def _cursor_enabled(self):
        return (
            callable(getattr(self, "on_pressed", None)) or
            callable(getattr(self, "on_release", None)) or
            callable(getattr(self, "on_down", None))
        )

    def enterEvent(self, event):
        self.is_hover = True

        if self._cursor_enabled():
            if getattr(self, "is_pressed", False):
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            else:
                self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if callable(getattr(self, "on_toggle", None)):
            if not getattr(self, "is_toggled", False):
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            else:
                self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.update()

    def leaveEvent(self, event):
        self.is_hover = False

        if self._cursor_enabled():
            self.unsetCursor()

        self.update()

    def _apply_shadow(self, blur: float):
        if not hasattr(self, "_shadow"):
            self._shadow = QGraphicsDropShadowEffect(self)
            self._shadow.setOffset(*self.shadow_offset)
            self.setGraphicsEffect(self._shadow)

        self._shadow.setBlurRadius(blur)
        color = self.shadow_color.to_qcolor()
        self._shadow.setColor(QColor(color))
    
    def _content_rect(self) -> QRect:
        l, t, r, b = self.padding
        return self.rect().adjusted(l, t, -r, -b)
