from PyQt6.QtCore import Qt, QRect, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPainterPath, QRegion

from engine.behavior.button_behavior import ButtonBehavior
from engine.property import *
from engine.ui.styles.color import Color
from engine.widgets.widget import Widget
from engine.resources.images import get_image_path


class Image(ButtonBehavior, Widget):

    overlay_active      : bool = BooleanProperty(False)
    image_source        : str = StringProperty("")
    image_hover_source  : str = StringProperty("")
    image_click_source  : str = StringProperty("")
    allow_stretch       : bool = BooleanProperty(False)
    anchor_image_x      : str = StringProperty("center")
    anchor_image_y      : str = StringProperty("center")
    image_color         : Color = ObjectProperty(None, Color)

    def __init__(self, parent=None, **kwargs):
        overlay_active     = kwargs.pop("overlay_active", False)
        image_source       = kwargs.pop("image_source", get_image_path("default.png"))
        image_hover_source = kwargs.pop("image_hover_source", "")
        image_click_source = kwargs.pop("image_click_source", "")
        allow_stretch      = kwargs.pop("allow_stretch", False)
        anchor_image_x     = kwargs.pop("anchor_image_x", "center")
        anchor_image_y     = kwargs.pop("anchor_image_y", "center")
        image_color        = kwargs.pop("image_color", None)

        super().__init__(parent, **kwargs)
        self.overlay_active     = overlay_active
        self.image_source       = image_source
        self.image_hover_source = image_hover_source
        self.image_click_source = image_click_source
        self.allow_stretch      = allow_stretch
        self.anchor_image_x     = anchor_image_x
        self.anchor_image_y     = anchor_image_y
        self.image_color        = image_color

    def on_image_source(self, _, value, __):
        self._pixmap = self._load_pixmap(value)

    def on_image_hover_source(self, _, value, __):
        self._hover_pixmap = self._load_pixmap(value) if value else None

    def on_image_click_source(self, _, value, __):
        self._click_pixmap = self._load_pixmap(value) if value else None

    def _load_pixmap(self, path: str) -> QPixmap:
        pix = QPixmap(path)
        if pix.isNull():
            raise ValueError(f"Invalid image source: {path}")
        return pix

    def paintEvent(self, *args):
        if not hasattr(self, "_pixmap"):
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        pad = self.padding

        padded_rect = QRect(
            rect.left() + pad.left,
            rect.top() + pad.top,
            rect.width() - pad.left - pad.right,
            rect.height() - pad.top - pad.bottom,
        )

        if self.rounding > 0:
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), self.rounding, self.rounding)
            painter.setClipPath(path)

        pixmap = self._pixmap
        overlay_alpha = 0
        if getattr(self, "is_pressed", False):
            if hasattr(self, "_click_pixmap") and self._click_pixmap:
                pixmap = self._click_pixmap
            elif self.overlay_active:
                overlay_alpha = 120
        elif getattr(self, "is_hover", False):
            if hasattr(self, "_hover_pixmap") and self._hover_pixmap:
                pixmap = self._hover_pixmap
            elif self.overlay_active:
                overlay_alpha = 60

        if self.image_color:
            temp_pix = pixmap.copy()
            temp_painter = QPainter(temp_pix)
            temp_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)

            if self.image_color.gradient and len(self.image_color.color_list) > 1:
                gradient = None
                if self.image_color.gradient_angle is not None:
                    from PyQt6.QtGui import QLinearGradient
                    import math
                    angle_rad = math.radians(self.image_color.gradient_angle)
                    w, h = temp_pix.width(), temp_pix.height()
                    cx = w / 2
                    cy = h / 2
                    dx = math.cos(angle_rad) * w / 2
                    dy = math.sin(angle_rad) * h / 2
                    gradient = QLinearGradient(cx - dx, cy - dy, cx + dx, cy + dy)
                else:
                    gradient = QLinearGradient(0, 0, temp_pix.width(), 0)

                step = 1 / (len(self.image_color.color_list) - 1)
                for i, c in enumerate(self.image_color.color_list):
                    gradient.setColorAt(i * step, QColor(c))

                temp_painter.fillRect(temp_pix.rect(), gradient)
            else:
                temp_painter.fillRect(temp_pix.rect(), self.image_color.to_qcolor())

            temp_painter.end()
            pixmap = temp_pix

        if self.allow_stretch:
            pix = pixmap.scaled(
                padded_rect.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        else:
            pix = pixmap.scaled(
                padded_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        x = padded_rect.left()
        y = padded_rect.top()

        new_padding_x = (pad.left + pad.right) / 4
        new_padding_y = (pad.top + pad.bottom) / 4

        if self.anchor_image_x != "center":
            x += new_padding_x if self.anchor_image_x == "right" else -new_padding_x
        if self.anchor_image_y != "center":
            y += new_padding_y if self.anchor_image_y == "bottom" else -new_padding_y

        target_rect = QRect(int(x), int(y), pix.width(), pix.height())
        painter.drawPixmap(target_rect, pix)

        if overlay_alpha > 0:
            mask = pix.mask()
            if mask and not mask.isNull():
                region = QRegion(mask)
                painter.save()
                painter.setClipRegion(region.translated(target_rect.topLeft()))
                painter.fillRect(target_rect, QColor(0, 0, 0, overlay_alpha))
                painter.restore()

        if self.shadow_active:
            self._apply_shadow(self.shadow_blur)
