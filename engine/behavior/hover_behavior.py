
from engine.property.boolean import BooleanProperty

class HoverBehavior:
    is_hover: bool = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
