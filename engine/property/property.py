from abc import ABC, abstractmethod

class Property(ABC):

    def __init__(self, default=None):
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None: return self
        return getattr(instance, self.private_name, self.default)

    def __set__(self, instance, value):
        old = getattr(instance, self.private_name, self.default)

        validate_callback = getattr(instance, f"on_{self.name}_validate_change", None)
        if validate_callback:
            value = validate_callback(self, value, old)
            if value is None: value = self._is_same_type(value)
        
        value = self._validate(value)

        setattr(instance, self.private_name, value)
        callback = getattr(instance, f"on_{self.name}", None)
        if callback: callback(self, value, old)
    
    def set_raw(self, instance, value):
        setattr(instance, self.private_name, value)

    @abstractmethod
    def _is_same_type(self, value): ...

    @abstractmethod
    def _validate(self, value): ...

