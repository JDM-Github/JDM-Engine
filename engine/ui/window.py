from .__window_impl import __EngineWindowImpl
from PyQt6.QtCore import QTimer

class EngineWindow(__EngineWindowImpl):

    def setup_everything(self): ...
    def render_everything(self): ...

    def run_window(self):
        self.setup_everything()
        self.render_everything()
        self.show()
    