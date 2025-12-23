import math
from engine.ui.styles.color import Color
import math
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QLinearGradient
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QColor

class Drawer:

    @staticmethod
    def _make_brush(instance, color: Color):
        if color.gradient and len(color.color_list) > 1:
            angle = color.gradient_angle or 0
            rect = instance._content_rect()
            rad    = math.radians(angle)
            cx, cy = rect.center().x(), rect.center().y()
            length = max(rect.width(), rect.height())
            dx = math.cos(rad) * length / 2
            dy = math.sin(rad) * length / 2
            start = QPointF(cx - dx, cy - dy)
            end   = QPointF(cx + dx, cy + dy)
            gradient = QLinearGradient(start, end)
            n        = len(color.color_list)
            for i, c in enumerate(color.color_list):
                gradient.setColorAt(i / (n - 1), QColor(c))
            return QBrush(gradient)

        return QBrush(color.to_qcolor())

    @staticmethod
    def _make_border_brush(instance, color: Color):
        if color.gradient and len(color.color_list) > 1:
            angle = color.gradient_angle or 0
            rect  = instance._content_rect()
            rad    = math.radians(angle)
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

        return QBrush(QColor(color.to_qcolor()))