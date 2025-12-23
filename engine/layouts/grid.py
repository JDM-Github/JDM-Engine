from engine.behavior.scroll_behavior import ScrollBehavior
from engine.property import IntegerProperty, BooleanProperty, ObjectProperty
from .base import BaseLayout
from engine.widgets.widget import Widget


class GridLayout(ScrollBehavior, BaseLayout):
    rows: int = IntegerProperty(0)
    cols: int = IntegerProperty(0)
    respect_width: bool = BooleanProperty(False)
    respect_height: bool = BooleanProperty(False)
    
    cols_list: list = ObjectProperty(None)  # list of tuples (cols, width_threshold)
    rows_list: list = ObjectProperty(None)  # list of tuples (rows, height_threshold)

    def __init__(self, parent=None, **kwargs):
        rows = kwargs.pop("rows", 0)
        cols = kwargs.pop("cols", 0)
        respect_width = kwargs.pop("respect_width", False)
        respect_height = kwargs.pop("respect_height", False)
        cols_list = kwargs.pop("cols_list", None)
        rows_list = kwargs.pop("rows_list", None)

        super().__init__(parent, **kwargs)

        if rows == 0 and cols == 0:
            raise ValueError("GridLayout cannot have both rows and cols as 0")

        GridLayout.rows.set_raw(self, rows)
        GridLayout.cols.set_raw(self, cols)

        self.respect_width = respect_width
        self.respect_height = respect_height
        self.cols_list = cols_list
        self.rows_list = rows_list

    def on_cols(self, instance, value, old): self._reflow()
    def on_rows(self, instance, value, old): self._reflow()

    def _update_dynamic_cols_rows(self):
        rect   = self._content_rect()
        width  = rect.width()
        height = rect.height()

        if self.cols_list:
            for cols, threshold in sorted(self.cols_list, key=lambda x: x[1]):
                if width < threshold:
                    if self.cols != cols:
                        self.cols = cols
                    break
            else:
                if self.cols != self.cols_list[-1][0]:
                    self.cols = self.cols_list[-1][0]

        if self.rows_list:
            for rows, threshold in sorted(self.rows_list, key=lambda x: x[1]):
                if height < threshold:
                    if self.rows != rows:
                        self.rows = rows
                    break
            else:
                if self.rows != self.rows_list[-1][0]:
                    self.rows = self.rows_list[-1][0]

    def _reflow(self):
        self._update_dynamic_cols_rows()

        rect = self._content_rect()
        children = [c for c in self.children() if isinstance(c, (Widget, BaseLayout))]
        if not children:
            return

        n_items = len(children)
        rows = self.rows
        cols = self.cols

        if rows == 0:
            cols = max(1, cols)
            rows = (n_items + cols - 1) // cols
        elif cols == 0:
            rows = max(1, rows)
            cols = (n_items + rows - 1) // rows

        total_h_spacing = self.spacing * (cols - 1)
        total_v_spacing = self.spacing * (rows - 1)

        available_w = rect.width() - total_h_spacing
        available_h = rect.height() - total_v_spacing

        cell_w = available_w // cols if not self.respect_width else 0
        cell_h = available_h // rows if not self.respect_height else 0

        for i, w in enumerate(children):
            w._updating = True
            r = i // cols
            c = i % cols

            x = rect.left() - self.scroll_start_x
            y = rect.top() - self.scroll_start_y

            if not self.respect_width:
                x += c * (cell_w + self.spacing)
            else:
                x += sum(children[j].width + self.spacing for j in range(c))

            if not self.respect_height:
                y += r * (cell_h + self.spacing)
            else:
                y += sum(children[j].height + self.spacing for j in range(r))

            w.x = int(x)
            w.y = int(y)

            hx, hy = getattr(w, "size_hint", (None, None))

            if not self.respect_width:
                if hx is not None:
                    w.width = int(cell_w * hx)
                else:
                    w.width = int(cell_w)
            else:
                if hx is not None:
                    w.width = int(rect.width() * hx)

            if not self.respect_height:
                if hy is not None:
                    w.height = int(cell_h * hy)
                else:
                    w.height = int(cell_h)
            else:
                if hy is not None:
                    w.height = int(rect.height() * hy)

            if isinstance(w, BaseLayout):
                w._reflow()
            
            w._updating = False
