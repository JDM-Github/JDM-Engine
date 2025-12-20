from .property import Property
from typing import Any


class StringProperty(Property):

    def _is_same_type(self, value: Any):
        return str(value) if value is not None else ""

    def _validate(self, value: Any):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a str")
        return value
