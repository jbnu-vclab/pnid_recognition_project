import math

class Vector2:
    def __init__(self, x: float=0, y:float=0):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __floordiv__(self, other):
        return Vector2(math.floor(self.x / other), math.floor(self.y / other))

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __mul__(self, other):
        return Vector2(math.floor(self.x * other), math.floor(self.y * other))

    def rotated(self, angle_rad):
        return Vector2(self.x * math.cos(angle_rad) - self.y * math.sin(angle_rad),
                       self.x * math.sin(angle_rad) + self.y * math.cos(angle_rad))

    def to_int(self):
        return Vector2(int(self.x), int(self.y))

    def __repr__(self):
        return "[{}, {}]".format(self.x, self.y)