from A1 import Vector


def test_oper():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1 + v2 == Vector(4, 6)
    assert v1 - v2 == Vector(-2, -2)
    assert v1 @ v2 == 11
    assert abs(v2) == 5
    assert (v1 == v2) is False


def test_hashable():
    assert Vector(1, 2) in {Vector(1, 2)}
