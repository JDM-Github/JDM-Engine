from typing import List
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QSize, QPoint

class __EngineWindowImpl(QMainWindow):

    __CONTROLLERS = []

    def _initialize(
        self,
        title    : str = "Application",
        width    : int = 800,
        height   : int = 600,
        x        : int = 100,
        y        : int = 100,
        resize_x : bool = True,
        resize_y : bool = True,
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(QSize (width, height))
        self.move  (QPoint(x, y))
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        if not resize_x: self.setFixedWidth(width)
        if not resize_y: self.setFixedHeight(height)

        from engine.controllers.base_controller import BaseController
        self._all_controllers: List[BaseController] = []

    def __set_all_controllers(self, all_controllers):
        self._all_controllers = all_controllers
