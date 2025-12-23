from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication

class Font:
    _registered_fonts = {}

    SYSTEM_DEFAULT = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont).family()
    FIXED         = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont).family()
    TITLE         = QFontDatabase.systemFont(QFontDatabase.SystemFont.TitleFont).family()
    SMALLEST      = QFontDatabase.systemFont(QFontDatabase.SystemFont.SmallestReadableFont).family()

    SEGOE_UI      = "Segoe UI"
    ARIAL         = "Arial"
    TIMES_NEW_ROMAN = "Times New Roman"

    @classmethod
    def register(cls, name: str, path: str):
        if QApplication.instance() is None:
            raise RuntimeError(
                "Font.register() called before QApplication was created"
            )
        
        font_id = QFontDatabase.addApplicationFont(path)
        if font_id == -1:
            raise ValueError(f"Failed to load font from {path}")
        
        families = QFontDatabase.applicationFontFamilies(font_id)
        if not families:
            raise ValueError(f"No font families found in {path}")
        
        family = families[0] 
        const_name = name.upper()
        setattr(cls, const_name, family)
        cls._registered_fonts[const_name] = family
        return family

    @classmethod
    def list_registered(cls):
        return cls._registered_fonts.copy()
