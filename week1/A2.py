# Базовый класс Shape с методом area(), наследники Circle, Rectangle, Triangle.
# Функция total_area(shapes) принимает список любых фигур и возвращает сумму площадей.
# Попытка создать Shape напрямую должна вызывать исключение.
from math import pi, sqrt
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self): pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        p = (self.a + self.b + self.c) / 2
        return sqrt(p * (p-self.a) * (p-self.b) * (p-self.c))


def total_area(shapes: list[Shape]):
    return sum(x.area() for x in shapes)
