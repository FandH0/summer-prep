import A7
from pytest import mark, raises, MonkeyPatch
from functools import lru_cache
from time import perf_counter
monkeypatch = MonkeyPatch()


def func1(x):
    return x ** x


def func2(x):
    for i in range(x):
        pass
    return None


def func3(x):
    if x > 0:
        func3(x - 1)
    return None


def fib(a):
    if a < 2:
        return a
    else:
        return fib(a - 1) + fib(a - 2)


@mark.parametrize("func, args", [
    (func1, 15),
    (func2, 10**6),
    (func3, 300)
])
def test_timed_return(func, args):
    @A7.timed
    def f_internal(args_internal):
        return func(args_internal)

    assert f_internal(args) == func(args)


def test_timed_name_doc():
    @A7.timed
    def f_internal():
        """None"""
        pass

    assert f_internal.__name__ == "f_internal"
    assert f_internal.__doc__ == "None"


@mark.parametrize("times", [
    1, 2, 3
])
def test_retry_delay_amount(times):
    @A7.retry(times=times, delay=5)
    def counter(count=[times]):
        count[0] -= 1
        if count[0] < 0:
            return None
        else:
            raise Exception

    counts = 0

    def mock_sleep(delay):
        nonlocal counts
        counts += 1

    monkeypatch.setattr("A7.sleep", mock_sleep)
    with raises(Exception):
        counter()

    assert counter() is None
    assert counts == times - 1


@mark.parametrize("times", [
    1, 2, 3
])
def test_retry_return(times):
    @A7.retry(times=4, delay=5)
    def counter(count=[times]):
        count[0] -= 1
        if count[0] < 0:
            return times
        else:
            raise Exception

    def mock_sleep(delay):
        pass

    monkeypatch.setattr("A7.sleep", mock_sleep)
    assert counter() == times


def test_retry_negative_delay():
    with raises(ValueError):
        A7.retry(delay=-10)


def test_retry_other_type_delay():
    with raises(ValueError):
        A7.retry(delay='a')


def test_retry_non_positive_times():
    with raises(ValueError):
        A7.retry(times=0)
    with raises(ValueError):
        A7.retry(times=-10)


def test_retry_other_type_times():
    with raises(ValueError):
        A7.retry(times='a')


def test_retry_name_doc():
    @A7.retry()
    def f_internal():
        """None"""
        pass

    assert f_internal.__name__ == "f_internal"
    assert f_internal.__doc__ == "None"


def test_memoize_time():
    @A7.memoize
    def fib_memoize(a):
        if a < 2:
            return a
        else:
            return fib_memoize(a - 1) + fib_memoize(a - 2)

    @lru_cache()
    def fib_lru_cache(a):
        if a < 2:
            return a
        else:
            return fib_lru_cache(a - 1) + fib_lru_cache(a - 2)

    t1 = perf_counter()
    fib(35)
    t2 = perf_counter()
    fib_memoize(35)
    t3 = perf_counter()
    fib_lru_cache(35)
    t4 = perf_counter()
    assert t2 - t1 > t3 - t2  # simple recur > memoize
    assert t2 - t1 > t4 - t2  # simple recur > lru_cache + memoize
