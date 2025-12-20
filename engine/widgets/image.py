from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QColor

from engine.behavior.button_behavior import ButtonBehavior
from engine.property import *
from engine.widgets.widget import Widget
from engine.resources.images import get_image_path


class Image(
    ButtonBehavior,
    Widget
):
    image_source        : str = StringProperty("")
    image_hover_source  : str = StringProperty("")
    image_click_source  : str = StringProperty("")
    allow_stretch       : bool = BooleanProperty(False)

    def __init__(self, parent, **kwargs):
        image_source       = kwargs.pop("image_source", get_image_path("default.png"))
        image_hover_source = kwargs.pop("image_hover_source", "")
        image_click_source = kwargs.pop("image_click_source", "")
        allow_stretch      = kwargs.pop("allow_stretch", False)

        super().__init__(parent, **kwargs)

        self.image_source       = image_source
        self.image_hover_source = image_hover_source
        self.image_click_source = image_click_source
        self.allow_stretch      = allow_stretch


    def on_image_source(self, _, value):
        self._pixmap = self._load_pixmap(value)

    def on_image_hover_source(self, _, value):
        self._hover_pixmap = self._load_pixmap(value) if value else None

    def on_image_click_source(self, _, value):
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

        rect = QRectF(self.rect())

        if self.rounding > 0:
            from PyQt6.QtGui import QPainterPath
            path = QPainterPath()
            path.addRoundedRect(rect, self.rounding, self.rounding)
            painter.setClipPath(path)

        pixmap = self._pixmap
        overlay_alpha = 0

        if getattr(self, "is_pressed", False):
            if hasattr(self, "_click_pixmap") and self._click_pixmap:
                pixmap = self._click_pixmap
            else:
                overlay_alpha = 120
        elif self.is_hover:
            if hasattr(self, "_hover_pixmap") and self._hover_pixmap:
                pixmap = self._hover_pixmap
            else:
                overlay_alpha = 60 

        size = self.size()
        if self.allow_stretch:
            pix = pixmap.scaled(
                size,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(rect, pix)
        else:
            pix = pixmap.scaled(
                size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )

            x = (pix.width() - size.width()) // 2
            y = (pix.height() - size.height()) // 2

            painter.drawPixmap(
                rect,
                pix,
                QRectF(x, y, size.width(), size.height())
            )

        if overlay_alpha > 0:
            painter.fillRect(
                rect,
                QColor(0, 0, 0, overlay_alpha)
            )
        self._apply_shadow(self.shadow_blur)