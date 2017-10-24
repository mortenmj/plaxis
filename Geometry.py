from collections import namedtuple
from math import cos, sin, pi


class Mock(object):
    def __init__(self):
        pass

    def polygon(self, *args):
        print('polygon %s' % str(args))
        return 'polygon %s' % str(args)

    def line(self, *args):
        print('line %s' % str(args))
        return 'line %s' % str(args)


class CommandProxy(object):
    def __init__(self, g):
        self._g = g


class Polygon(CommandProxy):
    def __init__(self, g, points):
        super(Polygon, self).__init__(g)

        self.handles = [self._g.polygon(*points)]


class Polyline(CommandProxy):
    def __init__(self, g, points):
        super(Polyline, self).__init__(g)

        # Make a generator for the segments
        segments = (Line(v, w) for v, w in zip(points, points[1:]))

        # Create line for each segment
        self.handles = [self._g.line(*segment) for segment in segments]


Point = namedtuple('Point', ['x', 'y'])


class Shape(tuple):
    def __new__(cls, points):
        cls.polygon = None
        cls.polyline = None
        return super(Shape, cls).__new__(cls, points)

    def createPolygon(self, g):
        if self.polygon is None:
            self.polygon = Polygon(g, self)
        return self.polygon

    def createPolyline(self, g):
        if self.polyline is None:
            self.polyline = Polyline(g, self)
        return self.polyline


class Line(Shape):
    def __new__(cls, p1, p2):
        points = (p1, p2)
        return super(Line, cls).__new__(cls, points)

    def __repr__(self):
        return 'Line((%s, %s), (%s, %s))' % (p1.x, p1.y, p2.x, p2.y)


class Circle(Shape):
    def __new__(cls, r, n, center=Point(0, 0)):
        points = [Point(center.x + cos(2*pi/n*i)*r, center.y + sin(2*pi/n*i * r)) for i in range(0, n+1)]
        return super(Circle, cls).__new__(cls, points)


if __name__ == "__main__":
    handle = Mock()

    p1 = Point(0, 1)
    p2 = Point(1, 2)

    line = Line(p1, p2)
    circle = Circle(10, 10)

    polygon = circle.createPolygon(handle)
    polyline = circle.createPolyline(handle)
