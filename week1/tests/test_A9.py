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
