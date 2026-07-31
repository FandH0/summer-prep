import A7
from pytest import mark, raises


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
def test_retry_delay_amount(monkeypatch, times):
    count = times

    @A7.retry(times=times, delay=5)
    def counter():
        nonlocal count
        count -= 1
        if count < 0:
            return None
        else:
            raise ConnectionError

    counts = 0

    def mock_sleep(delay):
        nonlocal counts
        counts += 1

    monkeypatch.setattr("A7.sleep", mock_sleep)
    with raises(ConnectionError):
        counter()

    assert counter() is None
    assert counts == times - 1


@mark.parametrize("failure", [
    1, 2, 3
])
def test_retry_return(monkeypatch, failure):
    count = failure

    @A7.retry(times=4, delay=5)
    def counter():
        nonlocal count
        count -= 1
        if count < 0:
            return failure
        else:
            raise ConnectionError

    def mock_sleep(delay):
        pass

    monkeypatch.setattr("A7.sleep", mock_sleep)
    assert counter() == failure


def test_retry_not_intended_e():
    counts = 0

    @A7.retry(times=3)
    def counter():
        nonlocal counts
        counts += 1
        raise TypeError

    with raises(TypeError):
        counter()
    assert counts == 1


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


def test_memoize_collision():
    @A7.memoize
    def f(x):
        return x**2

    assert [4, 1, 0, 1, 4] == [f(2), f(1), f(0), f(-1), f(-2)]


def test_memoize_call():
    calls = []

    @A7.memoize
    def f(x):
        calls.append(x)
        return x

    f(1)
    f(1)
    f(2)
    assert calls == [1, 2]
