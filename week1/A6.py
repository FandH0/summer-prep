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
    amount: int
    currency: str

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Addition of different currencies unsupported")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Substitution of different currencies unsupported")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Money(self.amount * other, self.currency)

    __rmul__ = __mul__

    def __str__(self):
        return f"{self.amount // 100}.{self.amount % 100:02d} {self.currency}"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.currency, self.amount) == (other.currency, other.amount)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Comparison of different currencies unsupported")
        return self.amount < other.amount
