from engine.ui.styles.fonts import Font

class Factory:
    _registry = {
        "DEFAULT_X_POS" : 0,
        "DEFAULT_Y_POS" : 0,
        "DEFAULT_WIDTH" : 100,
        "DEFAULT_HEIGHT": 100,

        "DEFAULT_FONT_NAME": Font.SYSTEM_DEFAULT,
        "DEFAULT_FONT_SIZE": 10,
        "DEFAULT_FONT_WEIGHT": 400,
        "DEFAULT_TEXT_PADDING": (0, 0),
    }

    @classmethod
    def set(cls, key: str, value):
        cls._registry[key] = value

    @classmethod
    def get(cls, key: str):
        return cls._registry.get(key)

    @classmethod
    def all(cls):
        return cls._registry.copy()
