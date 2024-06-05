import sys
sys.path.append('../../..')

import math
import numpy as np
from shapely import Polygon
from pnid_recognition_project.common.vector2 import Vector2


class SymbolObject:
    def __init__(self, type, cls, min_point, max_point, degree, flip, is_large, is_from_fourpoint, four_points):
        self.type = type
        self.cls = cls
        self.min_point = min_point # min & max points are points before rotated
        self.max_point = max_point
        self.degree = degree
        self.flip = flip
        self.is_large = is_large

        self.is_from_fourpoint = is_from_fourpoint
        self.four_points = four_points # four point is rotated points

        self.is_text: bool = False
        if "text" in type:
            self.is_text = True

    def get_class_name(self):
        if self.is_text:
            return self.type
        else:
            return self.cls

    @classmethod
    def from_fourpoint(self, type, cls, x1, y1, x2, y2, x3, y3, x4, y4, degree, flip=False, is_large=False):
        raw_points = [Vector2() for i in range(4)]
        raw_points[0] = Vector2(x1,y1)
        raw_points[1] = Vector2(x2,y2)
        raw_points[2] = Vector2(x3,y3)
        raw_points[3] = Vector2(x4,y4)

        # four point is already rotated. invert rotation
        center = Vector2((x1 + x2 + x3 + x4) / 4.0, (y1 + y2 + y3 + y4) / 4.0)
        min_p = (raw_points[0] - center).rotated(math.radians(degree)) + center # degree convention is reverse in case of four point XML (training data)
        max_p = (raw_points[2] - center).rotated(math.radians(degree)) + center
        min_p = min_p.to_int()
        max_p = max_p.to_int()
        return SymbolObject(type, cls, min_p, max_p, degree, flip, is_large, is_from_fourpoint=True, four_points=raw_points)

    @classmethod
    def from_twopoint(self, type, cls, min_point, max_point, degree, flip=False, is_large=False):
        p1 = min_point
        p2 = Vector2(max_point.x, min_point.y)
        p3 = max_point
        p4 = Vector2(min_point.x, max_point.y)

        center = (p3 + p1)/2.0
        four_points = [Vector2() for i in range(4)]
        four_points[0] = ((p1-center).rotated(math.radians(-degree)) + center).to_int() # degree convention is reverse
        four_points[1] = ((p2-center).rotated(math.radians(-degree)) + center).to_int()
        four_points[2] = ((p3-center).rotated(math.radians(-degree)) + center).to_int()
        four_points[3] = ((p4-center).rotated(math.radians(-degree)) + center).to_int()

        return SymbolObject(type, cls, min_point, max_point, degree, flip, is_large, is_from_fourpoint=False, four_points=four_points)

    def to_dota_str(self, difficulty = 0):
        category = self.get_class_name()
        str = f'{self.four_points[0].x} {self.four_points[0].y} '
        str += f'{self.four_points[1].x} {self.four_points[1].y} '
        str += f'{self.four_points[2].x} {self.four_points[2].y} '
        str += f'{self.four_points[3].x} {self.four_points[3].y} '
        str += f'{category} {difficulty}'

        return str

    def get_aabb(self):
        # return aabb (minx, miny, width, height) of symbol
        # if symbol is rotated, larger bounding box is returned
        minx = min(self.four_points[0].x, self.four_points[1].x, self.four_points[2].x, self.four_points[3].x)
        miny = min(self.four_points[0].y, self.four_points[1].y, self.four_points[2].y, self.four_points[3].y)
        maxx = max(self.four_points[0].x, self.four_points[1].x, self.four_points[2].x, self.four_points[3].x)
        maxy = max(self.four_points[0].y, self.four_points[1].y, self.four_points[2].y, self.four_points[3].y)

        width = maxx-minx
        height = maxy-miny

        return (minx, miny, width, height)


    def get_fourpoint_polygon(self):
        coords = [round(float(self.four_points[0].x)), round(float(self.four_points[0].y)),
                round(float(self.four_points[1].x)), round(float(self.four_points[1].y)),
                round(float(self.four_points[2].x)), round(float(self.four_points[2].y)),
                round(float(self.four_points[3].x)), round(float(self.four_points[3].y)),]
        coords = np.array([int(i) for i in coords])
        coords = coords.reshape(4, 2)
        coords = coords.tolist()

        return Polygon(coords)

    def apply_scale(self, scale = 1.0):
        self.min_point = self.min_point * scale
        self.max_point = self.min_point * scale
        for i, p in enumerate(self.four_points):
            self.four_points[i] = p * scale


    def __repr__(self):
        return "[{}, {}, min({}), max({}), degree({})]".format(self.type, self.cls, self.min_point, self.max_point, self.degree)


if __name__ == "__main__":
    two_symbol = SymbolObject.from_twopoint("pipe_symbol", "check_valve", Vector2(1774, 1086), Vector2(1867, 1133), 0,
                                            True)
    print(two_symbol.min_point)
    print(two_symbol.four_points)
    print(two_symbol)
    print(two_symbol.to_dota_str())

    four_symbol = SymbolObject.from_fourpoint("pipe_symbol", "check_valve", 1559, 5975, 1559, 6067, 1511, 6067, 1511, 5975, -90, True)
    print(four_symbol.min_point)
    print(four_symbol.four_points)
    print(four_symbol)
    print(four_symbol.to_dota_str())



