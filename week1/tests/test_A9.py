from pytest import mark, raises, fixture
from datetime import datetime
import A9


@fixture
def log_file(tmp_path):
    file = tmp_path / "log_file"
    file.write_text("1023-12-01T23:12:34 INFO db: message for someone\n"          # correct
                    "2023-12-01T23:12:34 CRITICAL db: message for someone\n"      # correct
                    "\n"                                                            # broken
                    "31023-12aedadfa23:12:34 CRITICe asdsage for someonf\n"       # broken
                    "1023-01-01T23:12:34 CRITICAL token: message for someone\n"   # correct
                    "1023-12-01T23:12:32 WARNING db: message for someone\n"       # correct
                    "1023-01-01T23:12:34 CRITICAL auth: message for someone\n"    # correct
                    "1223-12-01T23:12:34 WARNING linter: message for someone\n"   # correct
                    "1023-01-01T23:12:34 INFO linter: message for someone\n"      # correct
                    "1023-01-01T23:12:34 CRITICAL token: message for someone\n"   # correct
                    "2023-13-01T23:12:34 CRITICAL db: message for someone")       # broken
    return file


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
    with raises(FileNotFoundError):
        _ = A9.read_lines("file_dont_exist")
    f = tmp_path / "dir"
    f.mkdir()
    with raises(IsADirectoryError):
        _ = A9.read_lines(f)
    f = tmp_path / "file"
    f.touch()
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
def test_filter_level_illegal_level(level):
    with raises(ValueError):
        A9.filter_level([], level)


@mark.parametrize("filter_func", [A9.filter_level, A9.filter_min_level])
def test_filter_level_illegal_iter(filter_func):
    with raises(TypeError):
        filter_func(0, "INFO")
    with raises(ValueError):
        next(filter_func(
                [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "LEVEL_DONT_EXIST", "", ""),], "INFO"
            ))


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


@mark.parametrize("filter_func", (A9.filter_level, A9.filter_min_level))
def test_filter_is_lazy(filter_func):
    counter = 0

    def generator():
        nonlocal counter
        for _ in range(100):
            counter += 1
            yield A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "ERROR", "", "")

    filter_gen = filter_func(generator(), "ERROR")
    for _ in range(5):
        next(filter_gen)
    assert counter == 5


@mark.parametrize("take_func", (A9.take, A9.take_islice))
def test_take_infinite_source(take_func):
    def infinite_source():
        while True:
            yield 1
    assert list(take_func(infinite_source(), 3)) == [1, 1, 1]


@mark.parametrize("take_func", (A9.take, A9.take_islice))
def test_take_negative_n(take_func):
    with raises(ValueError):
        take_func([], -1)


@mark.parametrize("take_func", (A9.take, A9.take_islice))
@mark.parametrize("n", (True, "string", [], None))
def test_take_wrong_type_args(take_func, n):
    with raises(TypeError):
        take_func(1, 1)
    with raises(TypeError):
        take_func([], n)


@mark.parametrize("take_func", (A9.take, A9.take_islice))
@mark.parametrize("n", (0, 1, 5, 15))
def test_take_non_negative_n(take_func, n):
    iterable = list(range(10))
    assert list(take_func(iterable, n)) == iterable[:n]


@mark.parametrize("take_func", (A9.take, A9.take_islice))
def test_take_is_lazy(take_func):
    counter = 0

    def generator():
        nonlocal counter
        for _ in range(100):
            counter += 1
            yield

    for _ in take_func(generator(), 5):
        pass
    assert counter == 5


def test_top_modules_empty_iter():
    assert A9.top_modules([], 10) == []


def test_top_modules_negative_n():
    with raises(ValueError):
        A9.top_modules([], -10)


@mark.parametrize("n", (True, "string", [1, 2, 3], None))
def test_top_modules_wrong_type_args(n):
    with raises(TypeError):
        A9.top_modules(n, 1)
    with raises(TypeError):
        A9.top_modules([], n)


def test_top_modules_alphabet_check():
    logs = [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "ABC", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "ABC", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "D", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "A", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "C", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "B", ""),]
    assert A9.top_modules(logs, 3) == [("ABC", 2), ("A", 1), ("B", 1)]


def test_group_by_date_illegal_iter():
    with raises(TypeError):
        A9.group_by_date(1)
    with raises(TypeError):
        next(A9.group_by_date([1]))


def test_group_by_date_sorted_logs():
    logs = [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-02T23:12:35"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-03T23:12:37"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-03T23:12:37"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-04T23:12:38"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-04T23:12:38"), "", "", ""),]
    answer = [(datetime.fromisoformat("1234-12-01T23:12:34").date(), logs[:1]),
              (datetime.fromisoformat("1234-12-02T23:12:35").date(), logs[1:2]),
              (datetime.fromisoformat("1234-12-03T23:12:37").date(), logs[2:4]),
              (datetime.fromisoformat("1234-12-04T23:12:38").date(), logs[4:]),]
    assert list(A9.group_by_date(logs)) == answer


def test_group_by_date_unsorted_logs():
    logs = [A9.LogRecord(datetime.fromisoformat("1234-12-01T23:12:34"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-02T23:12:35"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-03T23:12:37"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-04T23:12:38"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-04T23:12:38"), "", "", ""),
            A9.LogRecord(datetime.fromisoformat("1234-12-03T23:12:37"), "", "", ""),]
    answer = [(datetime.fromisoformat("1234-12-01T23:12:34").date(), logs[:1]),
              (datetime.fromisoformat("1234-12-02T23:12:35").date(), logs[1:2]),
              (datetime.fromisoformat("1234-12-03T23:12:37").date(), logs[2:3]),
              (datetime.fromisoformat("1234-12-04T23:12:38").date(), logs[3:5]),
              (datetime.fromisoformat("1234-12-03T23:12:37").date(), logs[5:]),]
    # разделение 1234-12-03T23:12:37 на две группы
    assert list(A9.group_by_date(logs)) == answer


@mark.parametrize("n, answer", [
    (5, [("db", 3), ("auth", 1), ("token", 1)]),
    (6, [("db", 3), ("auth", 1), ("linter", 1)]),
    (7, [("db", 3), ("linter", 2), ("auth", 1)]),
    (8, [("db", 3), ("linter", 2), ("token", 2)]),
    (100, [("db", 3), ("linter", 2), ("token", 2)]),
])
def test_chain_read_to_top_modules(log_file, n, answer):
    r = A9.read_lines(log_file)
    p = A9.parse(r)
    logs = A9.take(p, n)
    assert A9.top_modules(logs, 3) == answer
