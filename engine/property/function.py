from .property import Property
from typing import Callable, Any

class FunctionProperty(Property):

    def _is_same_type(self, value: Any):
        return value

    def _validate(self, value: Any):
        if value is None:
            return value
        if not callable(value):
            raise TypeError(f"{self.name} must be callable or None")
        return value
