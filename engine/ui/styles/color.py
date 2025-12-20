from PyQt6.QtGui import QColor
from dataclasses import dataclass, field
from typing import List, Optional

from engine.core.utils import rgb_to_hex

@dataclass
class Color:
    color_list: List[str] = field(default_factory=lambda: ["#FFFFFF"])
    gradient: bool = False
    gradient_angle: Optional[float] = 0.0

    def to_qcolor(self): return QColor(self.value)

    def __post_init__(self):
        if isinstance(self.color_list, str):
            self.color_list = [self.color_list]

        new_colors = []
        for c in self.color_list:
            if isinstance(c, (list, tuple)): new_colors.append(rgb_to_hex(c))
            elif isinstance(c, str): new_colors.append(c)
            else: raise TypeError(f"Color: unsupported color type {type(c).__name__}")
        self.color_list = new_colors

    @property
    def value(self) -> str: return self.color_list[0] if self.color_list else "#FFFFFF"
    def __str__(self): return self.value
    def __repr__(self):
        return f"Color({self.color_list}, gradient={self.gradient}, angle={self.gradient_angle})"
