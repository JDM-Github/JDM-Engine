from config import run_config
run_config()

from app.ui.main_window import MainWindow
from app.core.registry import CONTROLLERS
from engine.core.application import run_app

if __name__ == "__main__":
    run_app(
        MainWindow,
        CONTROLLERS,
        "Main Application",
        resize_x=True,
        resize_y=False,
        x=10,
        y=10,
        width=650,
        height=650,
    )
