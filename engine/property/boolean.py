from .property import Property
from typing import Any

class BooleanProperty(Property):

    def _is_same_type(self, value: Any):
        return bool(value) if value is not None else False

    def _validate(self, value: Any):
        if not isinstance(value, bool):
            raise TypeError(f"{self.name} must be a bool")
        return value


