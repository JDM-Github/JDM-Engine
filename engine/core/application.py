import sys
from typing import List
from PyQt6.QtWidgets import QApplication
from engine.controllers.base_controller import BaseController
from engine.controllers.loader import load_controllers
from engine.ui.window import EngineWindow

def run_app(
        window: EngineWindow,
        controllers: List[BaseController],
        title: str = "Application",
        resize_x: bool = True,
        resize_y: bool = True,
        x: int = 100,
        y: int = 100,
        width: int = 500,
        height: int = 500
    ):
    app = QApplication(sys.argv)
    _window: EngineWindow = window()
    _window._initialize(
        title=title,
        resize_x=resize_x,
        resize_y=resize_y,
        x=x,
        y=y,
        width=width,
        height=height
    )
    _window.render_everything()
    _window._EngineWindowImpl__set_all_controllers(
        load_controllers(_window, controllers))

    _window.show()
    sys.exit(app.exec())
