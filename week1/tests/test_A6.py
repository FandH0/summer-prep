from A6 import Money
from pytest import raises


def test_negative_amount():
    with raises(ValueError):
        Money("RUB", -100)

def test_add():
    a = Money("RUB", 12300)
    b = Money("RUB", 12400)
    c = Money("USD", 12400)
    assert (a + b).amount == 24700
    # разные валюты
    with raises(ValueError):
        a + c

def test_sub():
    a = Money("RUB", 12300)
    b = Money("RUB", 12400)
    c = Money("USD", 12400)
    assert (b - a).amount == 100
    # отрицательные значения
    with raises(ValueError):
        a - b
    # разные валюты
    with raises(ValueError):
        c - a

def test_mul():
    a = Money("RUB", 12300)
    b = 2
    assert a * b == Money("RUB", 24600)
    assert b * a == Money("RUB", 24600)

def test_hash():
    try:
        {Money("RUB"): Money("RUB")}
    except TypeError:
        assert False

def test_compare():
    a = Money("RUB", 12300)
    b = Money("RUB", 12400)
    c = Money("USD", 12400)
    assert (a > b) is False
    assert (a < b) is True
    assert (a >= b) is False
    assert (a <= b) is True
    # разные валюты
    with raises(ValueError):
        a > c