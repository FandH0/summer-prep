from A8 import Timer, func_timer, suppress_and_log
import time
from pytest import raises, mark


@mark.parametrize("timer", (Timer, func_timer))
def test_timer_exception(timer):
    with raises(SystemExit):
        with timer() as t:
            time.sleep(0.01)
            raise SystemExit
    assert t.elapsed >= 0.01


@mark.parametrize("timer", (Timer, func_timer))
def test_timer_duration(monkeypatch, timer):
    sleep_time = 0

    def mocktime():
        return time.time() + sleep_time

    def mocksleep(t):
        nonlocal sleep_time
        sleep_time += t

    monkeypatch.setattr("A8.perf_counter", mocktime)
    monkeypatch.setattr("time.sleep", mocksleep)
    with timer() as t:
        time.sleep(10)
        t1 = t.elapsed
    time.sleep(10)
    t2 = t.elapsed
    assert t1 == 0  # внутри блока elapsed не изменяется
    assert (20 >= t2 >= 10)


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
