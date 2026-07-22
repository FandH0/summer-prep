from A3 import chunked


def test_chunked():
    assert list(chunked(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]
