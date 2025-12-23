from engine.core.factory import Factory
from engine.property.integer import IntegerProperty

class SizeBehavior:

    width     : int = IntegerProperty(100)
    height    : int = IntegerProperty(100)
    min_width : int = IntegerProperty(0)
    min_height: int = IntegerProperty(0)
    max_width : int = IntegerProperty(0)
    max_height: int = IntegerProperty(0)
    
    def __init__(self, *args, **kwargs):
        width  = kwargs.pop("width" , Factory.get("DEFAULT_WIDTH"))
        height = kwargs.pop("height", Factory.get("DEFAULT_HEIGHT"))

        min_width = kwargs.pop("min_width", 0)
        min_height = kwargs.pop("min_height", 0)
        max_width = kwargs.pop("max_width", 0)
        max_height = kwargs.pop("max_height", 0)

        super().__init__(*args, **kwargs)
        self.width      = width
        self.height     = height
        self.min_width  = min_width
        self.min_height = min_height
        self.max_width  = max_width
        self.max_height = max_height

        self.old_width  = width
        self.old_height = height
