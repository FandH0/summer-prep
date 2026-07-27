from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from codecs import lookup
from dataclasses import dataclass
from datetime import datetime
from itertools import islice
LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}


@dataclass(frozen=True)
class LogRecord:
    ts: datetime  # принимается любой валидный ISO-8601
    level: str
    module: str
    message: str


def parse(lines: Iterable[str], logger=print) -> Iterator[LogRecord]:
    if not isinstance(lines, Iterable):
        raise TypeError("Object provided is not Iterable")
    if not isinstance(logger, Callable):
        raise TypeError("Logger is not Callable")
    for line in lines:
        try:
            if line == "":
                raise ValueError("Empty string")
            # если больше одного пробела или начинается с пробела, то сдвиг будет обнаружен дальше
            # если без пробела, то line == ""
            dt, _, rest = line.partition(" ")
            ts = datetime.fromisoformat(dt)  # проверка по стандарту ISO-8601, бросает ValueError при несоответствии
            if ts.tzinfo is not None:
                raise ValueError("Timezones unsupported")  # условие в специфике A9

            level, _, rest = rest.partition(" ")
            if level not in LEVELS:
                if level == "":
                    raise ValueError("Blank level name or illegal intend or space")
                raise ValueError(f"Illegal level value: {level}")

            module, _, rest = rest.partition(": ")
            if module == "":
                raise ValueError("Blank module name or illegal intend or space")
            if " " in module or ":" in module:
                raise ValueError("Illegal module name or illegal intend or space")

            yield LogRecord(ts, level, module, rest)
        except ValueError as e:
            logger(f"line: {line} is broken because: {e}")


def read_lines(path: str | Path, encoding: str = "utf-8") -> Iterator[str]:
    # проверка на существование файла и кодировки при инициализации
    if not isinstance(path, Path):
        path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No such file or directory: {str(path)}")
    if path.is_dir():
        raise IsADirectoryError(f"Cannot open a directory: {str(path)}")
    lookup(encoding)

    def generator_read_lines():
        with open(path, encoding=encoding) as f:
            for line in f:
                yield line.removesuffix('\n')  # РЕШЕНИЕ: пробелы с правой стороны лога остаются в message

    return generator_read_lines()


def _validate_filter(logs: Iterable[LogRecord], level: str) -> None:
    if level not in LEVELS:
        raise ValueError(f"Illegal level: {level}")
    if not isinstance(logs, Iterable):
        raise TypeError(f"logs should be iterable, not {type(logs)}")


def filter_level(logs: Iterable[LogRecord], level: str) -> Iterator[LogRecord]:
    _validate_filter(logs, level)

    def generator_filter_level():
        for log in logs:
            if log.level not in LEVELS:
                raise ValueError(f"Log has unknown level: {log.level}")
            if LEVELS[log.level] == LEVELS[level]:
                yield log

    return generator_filter_level()


def filter_min_level(logs: Iterable[LogRecord], level: str) -> Iterator[LogRecord]:
    _validate_filter(logs, level)

    def generator_filter_min_level():
        for log in logs:
            if log.level not in LEVELS:
                raise ValueError(f"Log has unknown level: {log.level}")
            if LEVELS[log.level] >= LEVELS[level]:
                yield log

    return generator_filter_min_level()


def _validate_take(items: Iterable, n: int) -> None:
    if not isinstance(items, Iterable):
        raise TypeError(f"items should be an iterable, not {type(items)}")
    if not isinstance(n, int) or isinstance(n, bool):  # РЕШЕНИЕ: не принимает bool: True == 1 и False == 0
        raise TypeError(f"n should be an integer, not {type(n)}")
    if n < 0:
        raise ValueError(f"n cannot be less than 0: {n} < 0")


def take(items: Iterable, n: int) -> Iterator:
    _validate_take(items, n)

    def generator_take():
        if n == 0:
            return
        for i, item in enumerate(items):
            yield item
            if i + 1 == n:
                return

    return generator_take()


def take_islice(items: Iterable, n: int) -> Iterator:
    _validate_take(items, n)

    return islice(items, n)
