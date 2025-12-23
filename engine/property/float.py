from .property import Property
from typing import Any

class FloatProperty(Property):
    def _is_same_type(self, value: Any):
        return float(value) if value is not None else 0

    def _validate(self, value: Any):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError(f"{self.name} must be an float")
        return value
    