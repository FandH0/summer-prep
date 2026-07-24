from A8 import Timer, func_timer, suppress_and_log
import time
from pytest import raises, mark


def test_class_timer_exception():
    with raises(Exception):
        with Timer() as t:
            time.sleep(0.01)
            raise Exception
    assert t.elapsed >= 0.01


def test_class_timer_elapsed(monkeypatch):
    sleep_time = 0

    def mocktime():
        return time.time() + sleep_time

    def mocksleep(t):
        nonlocal sleep_time
        sleep_time += t

    monkeypatch.setattr("A8.time", mocktime)
    monkeypatch.setattr("time.sleep", mocksleep)
    with Timer() as t:
        time.sleep(10)
    assert t.elapsed >= 10


def test_func_timer_exception():
    with raises(ZeroDivisionError):
        with func_timer() as elapsed:
            time.sleep(0.01)
            raise ZeroDivisionError
    assert elapsed[0] >= 0.01


def test_func_timer_elapsed(monkeypatch):
    sleep_time = 0

    def mocktime():
        return time.time() + sleep_time

    def mocksleep(t):
        nonlocal sleep_time
        sleep_time += t

    monkeypatch.setattr("A8.time", mocktime)
    monkeypatch.setattr("time.sleep", mocksleep)
    with func_timer() as elapsed:
        time.sleep(10)
    assert elapsed[0] >= 10


@mark.parametrize("exceptions", ["0", (SystemExit, IndexError, 0), 0])
def test_suppress_and_log_exception_type(exceptions):
    with raises(ValueError, match="Exception"):
        with suppress_and_log(exceptions):
            pass


@mark.parametrize("exception, exceptions", [(SystemExit, IndexError),
                                            (SystemExit, (IndexError, ZeroDivisionError))])
def test_suppress_and_log_exception_pass(exception, exceptions):
    with raises(exception):
        with suppress_and_log(exceptions):
            raise exception


@mark.parametrize("exception, exceptions", [(IndexError, BaseException),
                                            (ZeroDivisionError, (IndexError, ZeroDivisionError))])
def test_suppress_and_log_exception_withhold(exception, exceptions):
    with suppress_and_log(exceptions):
        raise exception
