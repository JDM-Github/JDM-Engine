from dataclasses import dataclass

@dataclass
class Padding:
    left  : int = 0
    top   : int = 0
    right : int = 0
    bottom: int = 0

    def __init__(self, *values: int):
        if not values: l = t = r = b = 0
        elif len(values) == 1:
            l = t = r = b = values[0]
        elif len(values) == 2:
            l = r = values[0]
            t = b = values[1]
        elif len(values) == 3:
            l, t, r = values
            b = t
        elif len(values) == 4:
            l, t, r, b = values
        else:
            raise TypeError("Padding accepts 1 to 4 integers")

        self.left = int(l)
        self.top = int(t)
        self.right = int(r)
        self.bottom = int(b)

    def __iter__(self):
        yield self.left
        yield self.top
        yield self.right
        yield self.bottom