from engine.core.factory import Factory
from engine.property.integer import IntegerProperty

class PosBehavior:

    x: int = IntegerProperty(0)
    y: int = IntegerProperty(0)

    def __init__(self, *args, **kwargs):
        x = kwargs.pop("x", Factory.get("DEFAULT_X_POS"))
        y = kwargs.pop("y", Factory.get("DEFAULT_Y_POS"))

        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y

        self.old_x = x
        self.old_y = y
