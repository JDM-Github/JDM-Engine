from enum import Enum

class TextHAlignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class TextVAlignment(Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"

class AspectRatio(Enum):
    NONE = "none"
    WIDTH = "width"
    HEIGHT = "height"

class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"