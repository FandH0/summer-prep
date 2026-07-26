from pytest import mark, raises
from datetime import datetime
import A9


# tests partition types, correct partition, message with ":", " " chars
@mark.parametrize("line, answer", [
    ("1023-12-01T23:12:34 CRITICAL litter:  message for someone",
     A9.LogRecord(datetime.fromisoformat("1023-12-01T23:12:34"), "CRITICAL", "litter", " message for someone")),
    ("1023-12-01T23:12:34 CRITICAL litter:  mess: a:: g::e fo   r someon   e",
     A9.LogRecord(datetime.fromisoformat("1023-12-01T23:12:34"), "CRITICAL", "litter", " mess: a:: g::e fo   r someon   e")),
])
def test_parse_correct_line_partition(line, answer):
    assert next(A9.parse([line,])) == answer


@mark.parametrize("iterable, answer", [
    (["", " ",
      "1023-12-01T23:12:34 CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL litter:message for someone",
      "1023-12-0eeT23:12:34 CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34  CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL1 litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL  litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL  :  message for someone",
      "1023-12-01T23:12:34 CRITICAL litter  message for someone",
      "1023-12-01T23:12:34 CRITICAL litter: ",],
     [A9.LogRecord(datetime.fromisoformat("1023-12-01T23:12:34"), "CRITICAL", "litter", " message for someone"),
      A9.LogRecord(datetime.fromisoformat("1023-12-01T23:12:34"), "CRITICAL", "litter", "")]),
    (["", " ",
      "1023-12-01T23:12:34 CRITICAL litter:message for someone",
      "1023-12-0eeT23:12:34 CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34  CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL1 litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL  litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL  :  message for someone",
      "1023-12-01T23:12:34 CRITICAL litter  message for someone",],
     []),
])
def test_parse_broken_line_skip(iterable, answer):
    text_logs = []
    parsed_logs = []

    def logger(text):
        text_logs.append(text)
    # broken lines are skipped test
    for log in A9.parse(iterable, logger=logger):
        parsed_logs.append(log)
    assert parsed_logs == answer
    # broken lines are logged test
    assert len(text_logs) == len(iterable) - len(parsed_logs)


def test_read_lines_empty_file(tmp_path):
    path = tmp_path / "empty_file.log"
    path.touch()
    assert list(A9.read_lines(path)) == []


@mark.parametrize("text, answer", [
    ("first \nsecond \nthird \n", ["first ", "second ", "third "]),
    ("first \nsecond \nthird", ["first ", "second ", "third"]),
])
def test_read_lines_ending_symbol(tmp_path, text, answer):
    f = tmp_path / "log_file.log"
    f.write_text(text)
    assert list(A9.read_lines(f)) == answer


def test_read_lines_init_check(tmp_path):
    f = tmp_path / "file"
    f.touch()
    with raises(FileNotFoundError):
        _ = A9.read_lines("file_dont_exist")
    with raises(LookupError):
        _ = A9.read_lines(f, encoding="encoding_dont_exist")


def test_read_lines_is_lazy(tmp_path):
    path = tmp_path / "big.log"
    good = b"\n".join(b"line %d" % i for i in range(1000))  # переполнение буфера TextIOWrapper
    path.write_bytes(good + b"\n" + b"\xff\xfe broken line\n")  # сломанная строка в конце

    log = A9.read_lines(path)
    assert next(log).startswith("line 0")

    with raises(UnicodeDecodeError):
        list(log)


@mark.parametrize("level", ["error", "LEVEL DONT EXIST"])
def test_filter_level_illegal_error(level):
    with raises(ValueError):
        A9.filter_level([], level)


@mark.parametrize("level, answer", [
    ("CRITICAL", [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "CRITICAL", "", ""),]),
    ("ERROR", [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", ""),
               A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", "")]),
    ("WARNING", [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "WARNING", "", ""),]),
    ("INFO", []), ("DEBUG", [])
])
def test_filter_level_check(level, answer):
    logs = [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "CRITICAL", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "WARNING", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", "")]
    assert list(A9.filter_level(logs, level)) == answer


@mark.parametrize("level, answer", [
    ("CRITICAL", [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "CRITICAL", "", "")]),
    ("ERROR", [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "CRITICAL", "", ""),
               A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", ""),
               A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", "")]),
])
def test_filter_min_level_check(level, answer):
    logs = [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "CRITICAL", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "WARNING", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", "")]
    assert list(A9.filter_min_level(logs, level)) == answer


def test_take_infinite_source():
    def infinite_source():
        while True:
            yield 1
    assert list(A9.take(infinite_source(), 3)) == [1, 1, 1]


def test_take_negative_n():
    with raises(ValueError):
        A9.take([], -1)


def test_take_wrong_type_args():
    with raises(TypeError):
        A9.take(1, 1)
    with raises(TypeError):
        A9.take([], [])


@mark.parametrize("n", [0, 1, 5, 15])
def test_take_non_negative_n(n):
    l = list(range(10))
    assert list(A9.take(l, n)) == l[:n]
