# A6. Класс Money (value object, «правильный» A1)
#
# Неизменяемый класс: сумма в копейках (целое!) + валюта.
# Нужны: +, -, * int, сравнения <, <=, >, >=, ==, hash, repr, str → "120.50 RUB".
# Требования:
# Все бинарные операции возвращают NotImplemented для чужих типов, а не бросают.
# Сложение разных валют → ValueError (это уже неверное значение, а не тип — почувствуйте разницу).
# Объект хешируемый и годится ключом словаря и элементом set.
# Реализуйте через @dataclass(frozen=True) — и отдельно ответьте себе,
# что frozen=True даёт бесплатно (__eq__, __hash__, __repr__, запрет присваивания).
# Порядковые сравнения — через @functools.total_ordering: определите только __eq__ и __lt__, остальное сгенерируется.
from dataclasses import dataclass
from functools import total_ordering

@dataclass(frozen=True)
@total_ordering
class Money:
    currency: str
    amount: int = 0

    def __post_init__(self):
        if self.amount < 0: raise ValueError

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError
        return Money(self.currency, self.amount + other.amount)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError
        return Money(self.currency, self.amount - other.amount)

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Money(self.currency, self.amount * other)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.currency, self.amount))

    def __repr__(self):
        return f"Money({self.currency}, {self.amount / 100})"

    def __str__(self):
        return f"{self.amount / 100} {self.currency}"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.currency, self.amount) == (other.currency, other.amount)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError
        return self.amount < other.amount
