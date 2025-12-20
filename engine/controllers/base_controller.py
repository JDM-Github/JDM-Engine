from abc import ABC, abstractmethod
from engine.ui.window import EngineWindow

class BaseController(ABC):

    def __init__(self, window: EngineWindow):
        self.window = window

    @abstractmethod
    def connect(self) -> None:
        pass
