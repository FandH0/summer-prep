# Три декоратора возрастающей сложности:
#
# @timed — печатает время выполнения (замена вашей time_test из A5, но не ломающая сигнатуру).
# @retry(times=3, delay=0.1) — декоратор с параметрами, повторяет вызов при исключении,
# после последней попытки пробрасывает его дальше.
# @memoize — кэширует результат по аргументам в словаре.
from functools import wraps
from time import perf_counter, sleep


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = f(*args, **kwargs)
        end = perf_counter()
        print(f'Выполнено за {end - start}s')
        return result
    return wrapper


def retry(times: int = 3, delay: float = 0.1,
          exceptions: type[BaseException] | tuple[type[BaseException], ...] = (ConnectionError, TimeoutError)):
    if not isinstance(times, int) or times <= 0:
        raise ValueError(f"Function can only run positive int amount of times. Not {times}")
    if not isinstance(delay, (int, float)) or delay < 0:
        raise ValueError(f"Function can only be delayed for non-negative float time. Not {delay}")

    if isinstance(exceptions, tuple):
        for e in exceptions:
            if not isinstance(e, type) or not issubclass(e, BaseException):
                raise ValueError("Only BaseException type is allowed")
    elif not isinstance(exceptions, type) or not issubclass(exceptions, BaseException):
        raise ValueError("Only BaseException type is allowed")

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return f(*args, **kwargs)
                except exceptions:
                    if i + 1 < times:
                        sleep(delay)
                    else:
                        raise
        return wrapper

    return decorator


def memoize(f):
    cache = {}

    @wraps(f)
    def wrapper(*args, **kwargs):
        key = (*args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        answer = f(*args, **kwargs)
        cache[key] = answer
        return answer

    return wrapper
