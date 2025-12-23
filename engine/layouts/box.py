from engine.core.constant import Orientation
from engine.property import ObjectProperty, BooleanProperty
from .base import BaseLayout
from engine.widgets.widget import Widget

class BoxLayout(BaseLayout):

    orientation: Orientation = ObjectProperty(Orientation.HORIZONTAL, Orientation)
    use_fractional_hint: bool = BooleanProperty(False)
    reverse: bool = BooleanProperty(False) 

    def __init__(self, parent=None, **kwargs):
        orientation = kwargs.pop("orientation", Orientation.HORIZONTAL)
        use_fractional_hint = kwargs.pop("use_fractional_hint", False)
        reverse = kwargs.pop("reverse", False)
    
        super().__init__(parent, **kwargs)
        self.orientation = orientation
        self.use_fractional_hint = use_fractional_hint
        self.reverse = reverse

    def _reflow(self):
        rect = self._content_rect()
        children = [w for w in self.children() if isinstance(w, (Widget, BaseLayout))]

        if not children:
            return

        horizontal = self.orientation == Orientation.HORIZONTAL

        if horizontal:
            main_size = rect.width()
            get_main = lambda w: w.width
            set_main = lambda w, v: setattr(w, "width", int(v))
            get_main_hint = lambda w: getattr(w, "size_hint", (None, None))[0]
            get_cross_hint = lambda w: getattr(w, "size_hint", (None, None))[1]
        else:
            main_size = rect.height()
            get_main = lambda w: w.height
            set_main = lambda w, v: setattr(w, "height", int(v))
            get_main_hint = lambda w: getattr(w, "size_hint", (None, None))[1]
            get_cross_hint = lambda w: getattr(w, "size_hint", (None, None))[0]

        total_spacing = self.spacing * max(0, len(children) - 1)

        fixed = []
        hinted = []

        for w in children:
            w._updating = True
            hint = get_main_hint(w)
            if hint is None:
                fixed.append(w)
            else:
                hinted.append((w, float(hint)))

        fixed_space = sum(get_main(w) for w in fixed)
        remaining = max(0, main_size - fixed_space - total_spacing)

        if self.use_fractional_hint:
            hint_sum = sum(h for _, h in hinted)
            for w, h in hinted:
                size = remaining * (h / hint_sum) if hint_sum > 0 else 0
                if horizontal:
                    size = w._clamp_size(size, w.min_width, w.max_width)
                else:
                    size = w._clamp_size(size, w.min_height, w.max_height)
                set_main(w, size)
        else:
            for w, h in hinted:
                size = main_size * h
                if horizontal:
                    size = w._clamp_size(size, w.min_width, w.max_width)
                else:
                    size = w._clamp_size(size, w.min_height, w.max_height)
                set_main(w, size)

        for w in children:
            cross_hint = get_cross_hint(w)
            if cross_hint is not None:
                if horizontal:
                    w.height = w._clamp_size(int(rect.height() * cross_hint), w.min_height, w.max_height)
                else:
                    w.width = w._clamp_size(int(rect.width() * cross_hint), w.min_width, w.max_width)

        if horizontal:
            x = rect.right() if self.reverse else rect.left() 
            for w in children:
                w.x = int(x - w.width if self.reverse else x)
                w.y = int(rect.top())
                x += -(w.width + self.spacing) if self.reverse else (w.width + self.spacing)
                w._updating = False
                if isinstance(w, BaseLayout):
                    w._reflow()
        else:
            y = rect.bottom() if self.reverse else rect.top() 
            for w in children:
                w.y = int(y - w.height if self.reverse else y)
                w.x = int(rect.left())
                y += -(w.height + self.spacing) if self.reverse else (w.height + self.spacing)
                w._updating = False
                if isinstance(w, BaseLayout):
                    w._reflow()
