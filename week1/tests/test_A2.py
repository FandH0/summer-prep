from A2 import Rectangle, Circle, Triangle, Shape, total_area
from math import isclose, pi
from pytest import raises


def test_rectangle_area():
    assert Rectangle(1, 2).area() == 2


def test_circle_area():
    assert isclose(Circle(10).area(), 100 * pi)


def test_triangle_area():
    assert Triangle(3, 4, 5).area() == 6


def test_abstract_shape():
    with raises(TypeError):
        Shape()


def test_subclass_without_area_is_abstract():
    class Broken(Shape):
        pass
    with raises(TypeError):
        Broken()


def test_total_area():
    assert isclose(total_area([Rectangle(1, 2), Circle(1), Triangle(3, 4, 5)]), 8 + pi)
