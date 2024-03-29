import math


class Vector2:
    def __init__(self, x: float=0, y:float=0):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def rotated(self, angle_rad):
        return Vector2(self.x * math.cos(angle_rad) - self.y * math.sin(angle_rad),
                       self.x * math.sin(angle_rad) + self.y * math.cos(angle_rad))

    def __repr__(self):
        return "[{}, {}]".format(self.x, self.y)

class SymbolObject:
    def __init__(self, type, cls, min_point, max_point, degree, flip, is_large):
        self.type = type
        self.cls = cls
        self.min_point = min_point
        self.max_point = max_point
        self.degree = degree
        self.flip = flip
        self.is_large = is_large

    @classmethod
    def from_fourpoint(self, type, cls, x1, y1, x2, y2, x3, y3, x4, y4, degree, flip=False, is_large=False):
        self.is_from_fourpoint = True

        raw_points = [Vector2() for i in range(4)]
        raw_points[0] = Vector2(x1,y1)
        raw_points[1] = Vector2(x2,y2)
        raw_points[2] = Vector2(x3,y3)
        raw_points[3] = Vector2(x4,y4)
        self.raw_points = raw_points

        center = Vector2((x1 + x2 + x3 + x4) / 4.0, (y1 + y2 + y3 + y4) / 4.0)
        min_p = (raw_points[0] - center).rotated(math.radians(degree)) + center
        max_p = (raw_points[2] - center).rotated(math.radians(degree)) + center
        return SymbolObject(type, cls, min_p, max_p, degree, flip, is_large)


    @classmethod
    def from_twopoint(self, type, cls, min_point, max_point, degree, flip=False, is_large=False):
        self.is_from_fourpoint = False
        self.raw_points = None
        return SymbolObject(type, cls, min_point, max_point, degree, flip, is_large)

    def __repr__(self):
        return "[{}, {}, min({}), max({}), degree({})]".format(self.type, self.cls, self.min_point, self.max_point, self.degree)


if __name__ == "__main__":
    two_symbol = SymbolObject.from_twopoint("pipe_symbol", "check_valve", Vector2(1774, 1086), Vector2(1867, 1133), 0,
                                            True)
    print(two_symbol.min_point)
    print(two_symbol.raw_points)
    print(two_symbol)

    four_symbol = SymbolObject.from_fourpoint("pipe_symbol", "check_valve", 1559, 5975, 1559, 6067, 1511, 6067, 1511, 5975, -90, True)
    print(four_symbol.min_point)
    print(four_symbol.raw_points)
    print(four_symbol)



