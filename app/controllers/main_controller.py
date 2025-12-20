
from app.ui.main_window import MainWindow
from engine.controllers.base_controller import BaseController

class MainController(BaseController):

    def connect(self):
        self.window.image.on_pressed = self.btn_pressed
        self.window.image.on_release = self.btn_released
        self.window.image.on_down    = self.btn_down

    def btn_pressed(self):
        print("Button pressed once")

    def btn_released(self):
        print("Button released")

    def btn_down(self):
        print("Button held down event")
