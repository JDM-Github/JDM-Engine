from engine.core.factory import Factory
from engine.property import FloatProperty

class ScrollBehavior:

    scroll_start_x: float = FloatProperty(0)
    scroll_start_y: float = FloatProperty(0)
    
    def __init__(self, *args, **kwargs):
        scroll_start_x = kwargs.pop("scroll_start_x" , 0)
        scroll_start_y = kwargs.pop("scroll_start_y", 0)

        super().__init__(*args, **kwargs)
        self.scroll_start_x = scroll_start_x
        self.scroll_start_y = scroll_start_y
