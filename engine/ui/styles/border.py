from dataclasses import dataclass
from engine.ui.styles.colors import Colors

@dataclass
class Border:
    width: int = 1
    color: str = Colors.gray["600"]
