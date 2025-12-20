from engine.core.factory import Factory
from engine.property.integer import IntegerProperty

class SizeBehavior:

    width : int = IntegerProperty(100)
    height: int = IntegerProperty(100)
    
    def __init__(self, *args, **kwargs):
        width  = kwargs.pop("width" , Factory.get("DEFAULT_WIDTH"))
        height = kwargs.pop("height", Factory.get("DEFAULT_HEIGHT"))

        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
