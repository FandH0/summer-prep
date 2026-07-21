# Базовый класс Shape с методом area(), наследники Circle, Rectangle, Triangle.
# Функция total_area(shapes) принимает список любых фигур и возвращает сумму площадей.
# Попытка создать Shape напрямую должна вызывать исключение.
from math import pi, sqrt

class Shape:
    def __init__(self):
        raise NotImplementedError('Implemented only as a parent class')
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
    return sum(map(lambda x: x.area(), shapes))

if __name__ == "__main__":
    a, b, c = Rectangle(1, 2), Circle(1), Triangle(3, 4, 5)
    try:
        d = Shape()
        assert False
    except NotImplementedError:
        pass
    assert total_area([a, b, c]) == 2 + pi + 6