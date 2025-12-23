from typing import List, Union
from PyQt6.QtGui import QGuiApplication

def rgb_to_hex(rgb: Union[List[int], tuple]) -> str:

    if not isinstance(rgb, (list, tuple)):
        raise TypeError(f"RGB value must be a list or tuple, got {type(rgb).__name__}")
    if len(rgb) not in (3, 4):
        raise ValueError(f"RGB list must have 3 or 4 elements, got {len(rgb)}")
    if any(not (0 <= c <= 255) for c in rgb):
        raise ValueError(f"RGB values must be in 0-255, got {rgb}")
    if len(rgb) == 3:
        return "#{:02X}{:02X}{:02X}".format(*rgb)
    else:
        return "#{:02X}{:02X}{:02X}{:02X}".format(*rgb)

def center_window(width: int, height: int):
    screen = QGuiApplication.primaryScreen()
    geom = screen.availableGeometry()

    x = geom.x() + (geom.width()  - width)  // 2
    y = geom.y() + (geom.height() - height) // 2

    return x, y