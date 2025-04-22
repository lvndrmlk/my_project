# from pytest import *
# from r2point import R2Point
# from convex import Figure, Void, Point, Segment, Polygon

from pytest import *
# from deq import Deq
from r2point import R2Point
from convex import Void, Point, Segment, Polygon

def test_void_find_intersections():
    void = Void()
    assert void.find_intersections() == 0

def test_point_on_circle():
    point = Point(R2Point(1.0, 0.0))  # Точка на окружности
    assert point.find_intersections() == 1

def test_point_not_on_circle():
    point = Point(R2Point(0.5, 0.5))  # Точка внутри окружности
    assert point.find_intersections() == 0

def test_segment_no_intersections():
    p = R2Point(0.1, 0.1)
    q = R2Point(0.2, 0.2)
    segment = Segment(p, q)
    assert segment.find_intersections() == 0

def test_segment_both_points_on_circle():
    p = R2Point(-1.0, 0.0)  # На окружности
    q = R2Point(1.0, 0.0)   # На окружности
    segment = Segment(p, q)
    assert segment.find_intersections() == 2  # 2 точки на окружности, 0 пересечений внутри

def test_segment_one_point_on_circle():
    p = R2Point(1.0, 0.0)   # На окружности
    q = R2Point(2.0, 0.0)   # Вне окружности
    segment = Segment(p, q)
    assert segment.find_intersections() == 1  # 1 точка на окружности, 0 пересечений внутри

def test_segment_intersecting_circle():
    p = R2Point(-2.0, 0.0)  # Вне окружности
    q = R2Point(2.0, 0.0)   # Вне окружности
    segment = Segment(p, q)
    assert segment.find_intersections() == 2  # 2 пересечения внутри отрезка, 0 точек на окружности

def test_polygon_no_intersections():
    a = R2Point(0.1, 0.1)
    b = R2Point(0.2, 0.1)
    c = R2Point(0.1, 0.2)
    polygon = Polygon(a, b, c, 0)
    assert polygon.find_intersections() == 0

def test_polygon_all_points_on_circle():
    a = R2Point(-1.0, 0.0)  # На окружности
    b = R2Point(1.0, 0.0)   # На окружности
    c = R2Point(0.0, 1.0)   # На окружности
    polygon = Polygon(a, b, c, 0)
    assert polygon.find_intersections() == 3  # 3 точки на окружности, 0 пересечений рёбер

def test_polygon_mixed_intersections():
    a = R2Point(-1.0, 0.0)  # На окружности
    b = R2Point(1.0, 0.0)   # На окружности
    c = R2Point(0.0, 2.0)   # Вне окружности
    polygon = Polygon(a, b, c, 0)
    assert polygon.find_intersections() == 4  # 2 точки на окружности + 2 пересечения рёбер (a-c и b-c)

