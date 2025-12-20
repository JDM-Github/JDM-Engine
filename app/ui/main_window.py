from typing import override
from engine.core.constant import *
from engine.ui.styles import *
from engine.ui.window import EngineWindow
from engine.widgets import *
from engine.layouts import *

# TEST WINDOW
class MainWindow(EngineWindow):

    @override
    def render_everything(self):
        self.image = Image(self, allow_stretch=False, rounding=50)
        self.text = Button(self, text="IM IN LOVE", y=200)
