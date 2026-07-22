from A6 import Money
from pytest import raises, mark


def test_eq_other():
    assert Money(12300, "RUB") != 12300


@mark.parametrize("amount,expected", [
    (-5, "-0.05 RUB"), (-550, "-5.50 RUB"), (0, "0.00 RUB"),
    (5, "0.05 RUB"), (12000, "120.00 RUB"), (12050, "120.50 RUB"),
])
def test_str(amount, expected):
    assert str(Money(amount, "RUB")) == expected


@mark.parametrize("other", ["100", None, [1]])
def test_add_foreign_type_raises_typeerror(other):
    with raises(TypeError):
        Money(100, "RUB") + other


def test_add():
    a = Money(12300, "RUB")
    b = Money(12400, "RUB")
    c = Money(12300, "USD")
    assert (a + b).amount == 24700
    # разные валюты
    with raises(ValueError):
        a + c


def test_sub():
    a = Money(12300, "RUB")
    b = Money(12400, "RUB")
    c = Money(12300, "USD")
    assert (b - a).amount == 100
    # разные валюты
    with raises(ValueError):
        c - a


def test_mul():
    a = Money(12300, "RUB")
    b = 2
    assert a * b == Money(24600, "RUB")
    assert b * a == Money(24600, "RUB")


def test_compare():
    a = Money(12300, "RUB")
    b = Money(12400, "RUB")
    c = Money(12300, "USD")
    assert (a > b) is False
    assert (a < b) is True
    assert (a >= b) is False
    assert (a <= b) is True
    # разные валюты
    with raises(ValueError):
        a > c


def test_hashable():
    assert Money(1, "RUB") in {Money(1, "RUB"): None}
    assert len({Money(1, "RUB"), Money(1, "RUB")}) == 1
