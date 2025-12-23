import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from engine.controllers.loader import load_controllers
from engine.ui.window import EngineWindow

def _resolve_window_position(
    width: int,
    height: int,
    x: int | None,
    y: int | None,
    anchor_x: str | None,
    anchor_y: str | None
):
    screen = QGuiApplication.primaryScreen()
    geom = screen.availableGeometry()

    if anchor_x == "center":
        x = geom.x() + (geom.width() - width) // 2
    elif anchor_x == "right":
        x = geom.right() - width
    elif anchor_x == "left":
        x = geom.x()

    if anchor_y == "center":
        y = geom.y() + (geom.height() - height) // 2
    elif anchor_y == "bottom":
        y = geom.bottom() - height
    elif anchor_y == "top":
        y = geom.y()

    return x or 0, y or 0

def run_app(
        window: EngineWindow,
        controllers,
        title: str = "Application",
        resize_x: bool = True,
        resize_y: bool = True,

        x: int | None = None,
        y: int | None = None,
        anchor_x: str | None = None,
        anchor_y: str | None = None,

        width: int = 500,
        height: int = 500
    ):

    app = QApplication(sys.argv)

    x, y = _resolve_window_position(
        width, height,
        x, y,
        anchor_x, anchor_y
    )

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
    _window.run_window()
    _window._EngineWindowImpl__set_all_controllers(
        load_controllers(_window, controllers)
    )
    sys.exit(app.exec())