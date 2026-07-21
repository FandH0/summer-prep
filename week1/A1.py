# A1. Класс Vector
# Реализуйте класс двумерного вектора с поддержкой:
# v1 + v2, v1 - v2, v * 3 (умножение на скаляр), v1 == v2, abs(v) (длина), str(v) → "(x, y)"
# v1 @ v2 скалярным произведением через __matmul__.
class Vector:
    def __init__(self, x1: float, x2: float):
        self.x1 = x1
        self.x2 = x2

    def __add__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x1 + v.x1, self.x2 + v.x2)
        raise TypeError(f'Cannot add a Vector with {type(v)} using this operator')

    def __sub__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x1 - v.x1, self.x2 - v.x2)
        raise TypeError(f'Cannot subtract a Vector with {type(v)} using this operator')

    def __mul__(self, v):
        if isinstance(v, int) or isinstance(v, float):
            return Vector(v * self.x1, v * self.x2)
        raise TypeError(f'Cannot multiply a Vector with {type(v)} using this operator')

    __rmul__ = __mul__

    def __eq__(self, v):
        if isinstance(v, Vector):
            return self.x1 == v.x1 and self.x2 == v.x2
        raise TypeError(f'Cannot compare a Vector with {type(v)} using this operator')

    def __abs__(self):
        return (self.x1**2 + self.x2**2) ** 0.5

    def __str__(self):
        return f'({self.x1}, {self.x2})'

    def __matmul__(self, v):
        if isinstance(v, Vector):
            return self.x1 * v.x1 + self.x2 * v.x2
        raise TypeError(f'Cannot multiply a Vector with {type(v)} using this operator')

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2, v1 - v2, v1 @ v2, abs(v1), v1 == v2)