from .property import Property

class ObjectProperty(Property):

    def __init__(self, default=None, expected_type=None):
        super().__init__(default)
        self.expected_type = expected_type

    def _is_same_type(self, value):
        return value

    def _validate(self, value):
        if value is None: return value
        if self.expected_type and not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")
        return value
