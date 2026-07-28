# A1. Класс Vector
# Реализуйте класс двумерного вектора с поддержкой:
# v1 + v2, v1 - v2, v * 3 (умножение на скаляр),
# v1 == v2, abs(v) (длина), str(v) → "(x, y)"
# v1 @ v2 скалярным произведением через __matmul__.
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: float
    y: float

    def __add__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x + v.x, self.y + v.y)
        return NotImplemented

    def __sub__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x - v.x, self.y - v.y)
        return NotImplemented

    def __mul__(self, v):
        if isinstance(v, (int, float)):
            return Vector(v * self.x, v * self.y)
        return NotImplemented

    __rmul__ = __mul__

    def __eq__(self, v):
        if isinstance(v, Vector):
            return self.x == v.x and self.y == v.y
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __matmul__(self, v):
        if isinstance(v, Vector):
            return self.x * v.x + self.y * v.y
        return NotImplemented
