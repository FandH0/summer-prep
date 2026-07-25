from pytest import mark
from datetime import datetime
import A9


# tests partition types, correct partition, message with ";", " " chars
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
      "1023-12-0eeT23:12:34 CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34  CRITICAL litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL1 litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL  litter:  message for someone",
      "1023-12-01T23:12:34 CRITICAL  :  message for someone",
      "1023-12-01T23:12:34 CRITICAL litter  message for someone",
      "1023-12-01T23:12:34 CRITICAL litter: ",],
     [A9.LogRecord(datetime.fromisoformat("1023-12-01T23:12:34"), "CRITICAL", "litter", " message for someone"),
      A9.LogRecord(datetime.fromisoformat("1023-12-01T23:12:34"), "CRITICAL", "litter", "")]),
])
def test_parse_broken_line_skip(iterable, answer):
    logs = []

    def logger(text):
        logs.append(text)
    # broken lines are skipped test
    for i, log in enumerate(A9.parse(iterable, logger=logger)):
        assert i < len(answer)
        assert answer[i] == log

    # broken lines are logged test
    assert len(logs) == len(iterable) - (i + 1)
