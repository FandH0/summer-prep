from A5 import naive_window_max, deque_window_max
from random import randint


def test_functions_to_each_other():
    nums = [randint(1, 100) for i in range(100)]
    assert naive_window_max(nums, 10) == deque_window_max(nums, 10)


def test_naive():
    assert naive_window_max([1, 2, 3, 4, 1, 2, 3, 1], 3) == [3, 4, 4, 4, 3, 3]


def test_deque():
    assert deque_window_max([1, 2, 3, 4, 1, 2, 3, 1], 3) == [3, 4, 4, 4, 3, 3]


def test_empty_case_deque():
    assert deque_window_max([1], 3) == []


def test_empty_case_naive():
    assert naive_window_max([1], 3) == []
