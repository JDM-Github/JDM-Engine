from engine.core.factory import Factory
from engine.ui.styles.fonts import Font

def run_config():
    Factory.set("DEFAULT_FONT_NAME", Font.SEGOE_UI)
    Factory.set("DEFAULT_FONT_SIZE", 24)
