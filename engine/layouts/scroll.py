from engine.property import ObjectProperty, BooleanProperty, FloatProperty
from .base import BaseLayout
from PyQt6.QtCore import QEvent, QTimer, QRectF
from PyQt6.QtGui import QColor, QPainter
from engine.widgets.widget import Widget

class ScrollLayout(BaseLayout):
    scroll_pos_x: float = FloatProperty(0)
    scroll_pos_y: float = FloatProperty(0)

    scroll_target_x: float = FloatProperty(0)
    scroll_target_y: float = FloatProperty(0)

    scroll_x: bool = BooleanProperty(False)
    scroll_y: bool = BooleanProperty(True)

    content: BaseLayout = ObjectProperty(None, BaseLayout)

    scroll_speed: float = FloatProperty(10)
    smooth_speed: float = FloatProperty(0.2)
    overscroll_limit: float = FloatProperty(0)

    show_scrollbar: bool = BooleanProperty(True)

    def __init__(self, parent=None, **kwargs):

        scroll_x = kwargs.pop("scroll_x", False)
        scroll_y = kwargs.pop("scroll_y", True)
        scroll_pos_x = kwargs.pop("scroll_pos_x", 0)
        scroll_pos_y = kwargs.pop("scroll_pos_y", 0)
        show_scrollbar = kwargs.pop("show_scrollbar", True)

        super().__init__(parent, **kwargs)
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.scroll_pos_x = scroll_pos_x
        self.scroll_pos_y = scroll_pos_y
        self.scroll_target_x = self.scroll_pos_x
        self.scroll_target_y = self.scroll_pos_y
        self.show_scrollbar = show_scrollbar

        self.index = 0

        self.setFocusPolicy(self.focusPolicy())
        self.installEventFilter(self)

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_scroll)
        self._timer.start(16)

    def set_content(self, layout: BaseLayout):
        self.content = layout
        if layout:
            layout.setParent(self)

    def _max_scroll_y(self):
        if not self.content or not [
            c for c in self.content.children()
            if isinstance(c, (Widget, BaseLayout))
        ]:
            return 0

        childrens = [
            c for c in self.content.children()
            if isinstance(c, (Widget, BaseLayout))
        ]
        rect = self.content._content_rect()
        rows = getattr(self.content, "rows", 0)
        cols = getattr(self.content, "cols", 0)

        if rows == 0 and cols > 0:
            col_heights = []
            for c in range(cols):
                col_widgets = childrens[c::cols]
                height = sum(w.height + self.content.spacing for w in col_widgets)
                if col_widgets:
                    height -= self.content.spacing
                col_heights.append(height)
            total_height = max(col_heights)
        else:
            total_height = sum(w.height + self.content.spacing for w in childrens)
            if childrens:
                total_height -= self.content.spacing 
        return max(0, total_height - rect.height())

    def _max_scroll_x(self):
        if not self.content or not [
            c for c in self.content.children()
            if isinstance(c, (Widget, BaseLayout))
        ]:
            return 0
        childrens = [
            c for c in self.content.children()
            if isinstance(c, (Widget, BaseLayout))
        ]
        rect = self.content._content_rect()
        rows = getattr(self.content, "rows", 0)
        cols = getattr(self.content, "cols", 0)
        if cols == 0 and rows > 0:
            row_widths = []
            for r in range(rows):
                start = r
                row_widgets = childrens[start::rows]
                width = sum(w.width + self.content.spacing for w in row_widgets) - self.content.spacing
                row_widths.append(width)
            total_width = max(row_widths)
        else:
            total_width = sum(w.width + self.content.spacing for w in childrens)
        return max(0, total_width - rect.width())


    def scroll_by(self, dx=0, dy=0):
        if self.scroll_x:
            self.scroll_target_x += dx
        if self.scroll_y:
            self.scroll_target_y += dy

        self.scroll_target_y = min(
            max(-self.overscroll_limit, self.scroll_target_y),
            self._max_scroll_y() + self.overscroll_limit)
        self.scroll_target_x = min(
            max(-self.overscroll_limit, self.scroll_target_x),
            self._max_scroll_x() + self.overscroll_limit)

    def _update_scroll(self):
        if not self.content:
            return
        
        self.scroll_pos_x += (self.scroll_target_x - self.scroll_pos_x) * self.smooth_speed
        self.scroll_pos_y += (self.scroll_target_y - self.scroll_pos_y) * self.smooth_speed

        max_y = self._max_scroll_y()
        if self.scroll_pos_y < 0:
            self.scroll_pos_y += (0 - self.scroll_pos_y) * 0.1
        elif self.scroll_pos_y > max_y:
            self.scroll_pos_y += (max_y - self.scroll_pos_y) * 0.1

        max_x = self._max_scroll_x()
        if self.scroll_pos_x < 0:
            self.scroll_pos_x += (0 - self.scroll_pos_x) * 0.1
        elif self.scroll_pos_x > max_x:
            self.scroll_pos_x += (max_x - self.scroll_pos_x) * 0.1

        self._reflow()
        self.update()  


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            delta = event.angleDelta()
            dx = -delta.x() / 120 * self.scroll_speed
            dy = -delta.y() / 120 * self.scroll_speed

            self.scroll_by(dx, dy)
            return True

        return super().eventFilter(obj, event)


    def _reflow(self):
        if not self.content:
            return

        self.content.scroll_start_x = self.scroll_pos_x
        self.content.scroll_start_y = self.scroll_pos_y
        self.content._reflow()


    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.show_scrollbar or not self.content:
            return
        
        childrens = [
            c for c in self.content.children()
            if isinstance(c, (Widget, BaseLayout))
        ]

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self._content_rect()

        if self.scroll_y:
            max_scroll_y = self._max_scroll_y()
            if max_scroll_y > 0:
                content_height = sum(w.height + self.content.spacing for w in childrens)
                bar_height = max(20, rect.height() * rect.height() / max(content_height, rect.height()))
                bar_x = rect.right() - 6
                bar_y = rect.top() + (rect.height() - bar_height) * (self.scroll_pos_y / max_scroll_y)

                painter.setBrush(QColor(120, 120, 120, 180))
                painter.setPen(QColor(0, 0, 0, 0))
                painter.drawRoundedRect(QRectF(bar_x, bar_y, 6, bar_height), 3, 3)

        if self.scroll_x:
            max_scroll_x = self._max_scroll_x()
            if max_scroll_x > 0:
                content_width = sum(w.width + self.content.spacing for w in childrens)
                bar_width = max(20, rect.width() * rect.width() / max(content_width, rect.width()))
                bar_y = rect.bottom() - 6
                bar_x = rect.left() + (rect.width() - bar_width) * (self.scroll_pos_x / max_scroll_x)

                painter.setBrush(QColor(120, 120, 120, 180))
                painter.setPen(QColor(0, 0, 0, 0))
                painter.drawRoundedRect(QRectF(bar_x, bar_y, bar_width, 6), 3, 3)
