import math
from PyQt6.QtGui import QLinearGradient
from PyQt6.QtCore import QPointF
from typing import List
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import QRect, QEvent
from engine.behavior import *
from engine.core.constant import AspectRatio
from engine.core.factory import Factory
from engine.property import *
from engine.ui.styles import *
from engine.widgets.widget import Widget

class BaseLayout(
    SizeBehavior,
    PosBehavior,
    QWidget
):
    shadow_active         : bool = BooleanProperty(True)
    layout_padding        : Padding = ObjectProperty(None, Padding)
    padding               : Padding = ObjectProperty(None, Padding)
    pos_hint              : List[float] = ListProperty([None, None], None)
    size_hint             : List[float] = ListProperty([None, None], None)
    shadow_offset         : List[int] = ListProperty([0, 0], int)
    shadow_color          : Color = ObjectProperty( None, Color )
    shadow_blur           : float = FloatProperty(12)
    rounding              : float = FloatProperty(12)
    spacing               : float = FloatProperty(0)
    background_color      : Color = ObjectProperty( Color(Colors.gray["800"]), Color )
    aspect_ratio_follow   : AspectRatio = ObjectProperty(None, AspectRatio) 
    aspect_ratio          : float = FloatProperty(1)

    def __init__(self, parent=None, **kwargs):
        layout_padding         = kwargs.pop("layout_padding", Padding(*Factory.get("DEFAULT_LAYOUT_PADDING")))
        padding                = kwargs.pop("padding", Padding(*Factory.get("DEFAULT_LAYOUT_PADDING")))
        spacing                = kwargs.pop("spacing", 0)
        pos_hint               = kwargs.pop("pos_hint", [None, None])
        size_hint              = kwargs.pop("size_hint", [None, None])
        shadow_active          = kwargs.pop("shadow_active", False)
        shadow_color           = kwargs.pop("shadow_color", Color(Colors.gray["950"]))
        shadow_offset          = kwargs.pop("shadow_offset", [0, 2])
        background_color       = kwargs.pop("background_color", None)
        shadow_blur            = kwargs.pop("shadow_blur", 12)
        rounding               = kwargs.pop("rounding", 8)
        aspect_ratio_follow    = kwargs.pop("aspect_ratio_follow", AspectRatio.NONE)
        aspect_ratio           = kwargs.pop("aspect_ratio", 1)
        super().__init__(parent, **kwargs)

        self._updating              = False
        self.layout_padding         = layout_padding
        self.padding                = padding
        self.spacing                = spacing
        self.pos_hint               = pos_hint
        self.size_hint              = size_hint
        self.shadow_color           = shadow_color
        self.shadow_offset          = shadow_offset
        self.background_color       = background_color
        self.shadow_blur            = shadow_blur
        self.rounding               = rounding
        self.shadow_active          = shadow_active
        self.aspect_ratio_follow    = aspect_ratio_follow
        self.aspect_ratio           = aspect_ratio

        self.setMouseTracking(True)
        if self.parent():
            self._apply_size_hint()
            self._apply_pos_hint()
            self.parent().installEventFilter(self)
        
        self.show()

    def clear_widget_children(widget: QWidget):
        children_to_remove = [
            c for c in widget.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
            if isinstance(c, (Widget, BaseLayout))
        ]
        for child in children_to_remove:
            child.setParent(None)
            child.deleteLater()

    def paintEvent(self, *args):
        super().paintEvent(*args)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.background_color:
            if self.background_color.gradient and len(self.background_color.color_list) > 1:
                angle = self.background_color.gradient_angle or 0
                rect = self._content_rect_layout()
                rad = math.radians(angle)
                cx, cy = rect.center().x(), rect.center().y()
                length = max(rect.width(), rect.height())
                dx = math.cos(rad) * length / 2
                dy = math.sin(rad) * length / 2
                start_point = QPointF(cx - dx, cy - dy)
                end_point = QPointF(cx + dx, cy + dy)
                gradient = QLinearGradient(start_point, end_point)
                n = len(self.background_color.color_list)
                for i, c in enumerate(self.background_color.color_list):
                    gradient.setColorAt(i / (n - 1), QColor(c))
                painter.setBrush(QBrush(gradient))
            else:
                painter.setBrush(QBrush(self.background_color.to_qcolor()))

            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self._content_rect_layout(), self.rounding, self.rounding)

        if hasattr(self, "border"):
            border = getattr(self, "border")
            if hasattr(self, "is_pressed") and hasattr(self, "border_click"):
                if getattr(self, "is_pressed") and getattr(self, "border_click"):
                    border = getattr(self, "border_click")

            if border and border.width:
                pen = QPen(QColor(border.color), border.width)
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRoundedRect(self._content_rect_layout().adjusted(
                    border.width // 2,
                    border.width // 2,
                    -border.width // 2,
                    -border.width // 2
                ), self.rounding, self.rounding)

        if self.shadow_active: self._apply_shadow(self.shadow_blur)

    def _apply_shadow(self, blur: float):
        if not hasattr(self, "_shadow"):
            self._shadow = QGraphicsDropShadowEffect(self)
            self._shadow.setOffset(*self.shadow_offset)
            self.setGraphicsEffect(self._shadow)

        self._shadow.setBlurRadius(blur)
        color = self.shadow_color.to_qcolor()
        self._shadow.setColor(QColor(color))

    def _clamp_size(self, value, min_v, max_v):
        if max_v > 0: value = min(value, max_v)
        if min_v > 0: value = max(value, min_v)
        return value

    def is_layout_updating(self):
        from engine.layouts import GridLayout, BoxLayout
        if isinstance(self.parent(), (GridLayout, BoxLayout)):
            return getattr(self, "_updating", False)
        return True
    
    def on_x(self, _, value, old):
        if not self.is_layout_updating():
            BaseLayout.y.set_raw(self, old)
            return

        self.old_y = old
        self.move(value, self.y)

    def on_y(self, _, value, old):
        if not self.is_layout_updating():
            BaseLayout.x.set_raw(self, old)
            return

        self.old_x = old
        self.move(self.x, value)

    def on_width(self, _, value, old):
        if not self.is_layout_updating():
            BaseLayout.width.set_raw(self, old)
            return

        self.old_width = old
        w = self._clamp_size(value, self.min_width, self.max_width)
        h = self.height
        if self.aspect_ratio_follow == AspectRatio.WIDTH and self.aspect_ratio > 0:
            h = int(w / self.aspect_ratio)
            h = self._clamp_size(h, self.min_height, self.max_height)
        self.resize(w, h)

    def on_height(self, _, value, old):
        if not self.is_layout_updating():
            BaseLayout.height.set_raw(self, old)
            return

        self.old_height = old
        h = self._clamp_size(value, self.min_height, self.max_height)
        w = self.width

        if self.aspect_ratio_follow == AspectRatio.HEIGHT and self.aspect_ratio > 0:
            w = int(h * self.aspect_ratio)
            w = self._clamp_size(w, self.min_width, self.max_width)

        self.resize(w, h)

    def eventFilter(self, obj, event: QEvent):
        if obj == self.parent() and event.type() == event.Type.Resize:
            self._apply_size_hint()
            self._apply_pos_hint()
            self._reflow()
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
        if isinstance(self.parent(), (GridLayout, BoxLayout)):
            return

        pw = parent.width()  if callable(getattr(parent, "width", None)) else parent.width
        ph = parent.height() if callable(getattr(parent, "height", None)) else parent.height

        width_factor, height_factor = self.size_hint

        w = int(pw * width_factor)  if width_factor is not None else self.width
        h = int(ph * height_factor) if height_factor is not None else self.height

        w = self._clamp_size(w, self.min_width, self.max_width)
        h = self._clamp_size(h, self.min_height, self.max_height)

        self.width = w
        self.height = h

    def _content_rect(self) -> QRect:
        l, t, r, b = self.padding
        return self._content_rect_layout().adjusted(l, t, -r, -b)

    def _content_rect_layout(self) -> QRect:
        l, t, r, b = self.layout_padding
        return self.rect().adjusted(l, t, -r, -b)

    def _reflow(self): raise NotImplementedError
