from .property import Property
from typing import Any

class IntegerProperty(Property):
    def _is_same_type(self, value: Any):
        return int(value) if value is not None else 0

    def _validate(self, value: Any):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an int")
        return value
