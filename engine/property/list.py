from .property import Property
from typing import Any

class ListProperty(Property):
    def __init__(self, default=None, item_type=None):
        super().__init__(default if default is not None else [])
        self.item_type = item_type

    def _is_same_type(self, value: Any):
        if value is None: return []
        if not isinstance(value, list):
            return [value]
        return value

    def _validate(self, value: Any):
        if not isinstance(value, list):
            raise TypeError(f"{self.name} must be a list")
        if self.item_type:
            for i, item in enumerate(value):
                if self.item_type is float:
                    if not isinstance(item, float) and not isinstance(item, int):
                        raise TypeError(f"{self.name}[{i}] must be {self.item_type.__name__}")

                elif not isinstance(item, self.item_type):
                    raise TypeError(f"{self.name}[{i}] must be {self.item_type.__name__}")
        return value
