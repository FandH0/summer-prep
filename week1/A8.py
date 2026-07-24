from time import time
from contextlib import contextmanager


class Timer:
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattr__(self, item):
        if item == 'elapsed':
            return time() - self.start
        raise AttributeError


@contextmanager
def func_timer():
    start = time()
    try:
        elapsed = [time() - start]
        yield elapsed
    finally:
        elapsed[0] = time() - start


@contextmanager
def suppress_and_log(exceptions: tuple[type(BaseException), ...] | type(BaseException)):
    if isinstance(exceptions, tuple):
        for e in exceptions:
            if not isinstance(e, type(BaseException)):
                raise ValueError("Exception in tuple needs to be an instance of BaseException type")
    elif not isinstance(exceptions, type(BaseException)):
        raise ValueError("Exception needs to be an instance of BaseException type")

    try:
        yield
    except exceptions as e:
        print(type(e))
        return True
