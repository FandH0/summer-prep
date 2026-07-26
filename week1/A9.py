from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


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


def read_lines(path: str | Path) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.removesuffix('\n')  # РЕШЕНИЕ: пробелы с правой стороны лога остаются в message
