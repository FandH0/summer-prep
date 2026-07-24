from time import perf_counter
from contextlib import contextmanager
from types import SimpleNamespace


class Timer:
    def __enter__(self):
        self.start = perf_counter()
        self.end = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = perf_counter()

    @property
    def elapsed(self):
        if self.end:
            return self.end - self.start
        return 0


@contextmanager
def func_timer():
    start = perf_counter()
    inner = SimpleNamespace(elapsed=0)
    try:
        yield inner
    finally:
        inner.elapsed = perf_counter() - start


@contextmanager
def suppress_and_log(exceptions: tuple[type[BaseException], ...] | type[BaseException]):
    if isinstance(exceptions, tuple):
        for e in exceptions:
            if not isinstance(e, type) or not issubclass(e, BaseException):
                raise ValueError("Exception in tuple needs to be an instance of BaseException type")
    elif not isinstance(exceptions, type) or not issubclass(exceptions, BaseException):
        raise ValueError("Exception needs to be an instance of BaseException type")

    try:
        yield
    except exceptions as e:
        print(type(e))
