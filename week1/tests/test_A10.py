import A10
from pytest import mark, raises, fixture


@fixture
def lrucache_linked():
    """lru cache с одним свободным местом"""
    capacity = 14
    lru_cache = A10.LRUCacheLinked(capacity)
    keys_values = [(-1000, 1), ('2', 1), (LookupError, '123'), ((1, 2), '123'), (2, [1, 2, 3]), (3, 1),
                   (-3.4, '123'), ('whatever', None), ('123', None), ('213', None), (1232, [1, 2, 3]),
                   (None, [1, 2, 3]), (12, LookupError)]

    for key, value in keys_values:
        lru_cache.put(key, value)
    return lru_cache


@mark.parametrize("length", (0, 1, 5, 10, 100))
def test_lrucache_linked_length(length):
    lru_cache = A10.LRUCacheLinked(capacity=10)
    for item in range(length):
        lru_cache.put(key=item, value=item)
    assert len(lru_cache.cache) == min(length, 10)
    assert len(lru_cache.keys_in_lru_order()) == min(length, 10)
    assert len(lru_cache) == min(length, 10)


def test_lrucache_linked_contains(lrucache_linked):
    assert '2' in lrucache_linked
    assert lrucache_linked.keys_in_lru_order()[0] != '2'


@mark.parametrize("capacity", (None, [], "str", True, 1.5))
def test_lrucache_linked_capacity_wrong_type(capacity):
    with raises(TypeError):
        A10.LRUCacheLinked(capacity=capacity)


@mark.parametrize("capacity", (-1, 0))
def test_lrucache_linked_capacity_non_positive(capacity):
    with raises(ValueError):
        A10.LRUCacheLinked(capacity=capacity)


def test_lrucache_linked_get_not_existing(lrucache_linked):
    old_lru_order = lrucache_linked.keys_in_lru_order()
    with raises(KeyError):
        lrucache_linked.get("new")
    assert old_lru_order == lrucache_linked.keys_in_lru_order()


@mark.parametrize("key, value", [('123', None), (None, [1, 2, 3]), (-1000, 1), ('2', 1),])
def test_lrucache_linked_get_lru_order(lrucache_linked, key, value):
    assert lrucache_linked.keys_in_lru_order()[0] != key
    assert lrucache_linked.get(key) == value
    assert lrucache_linked.keys_in_lru_order()[0] == key


def test_lrucache_linked_put_capacity(lrucache_linked):
    last = lrucache_linked.keys_in_lru_order()[-1]
    lrucache_linked.put("PLACEHOLDER", "PLACEHOLDER")  # заполнение lrucache_linked
    lrucache_linked.put("new", 1)  # новое значение
    assert len(lrucache_linked) <= lrucache_linked.capacity
    assert last not in lrucache_linked


def test_lrucache_linked_put_existing(lrucache_linked):
    length = len(lrucache_linked)
    lrucache_linked.put('123', "new")  # существующее значение
    assert len(lrucache_linked) == length
    assert lrucache_linked.keys_in_lru_order().count('123') == 1
    assert lrucache_linked.get('123') == "new"


@mark.parametrize("key, value", [('123', None), (None, [1, 2, 3]), (None, None), ("new", 1),])
def test_lrucache_linked_put_lru_order(lrucache_linked, key, value):
    # изменение в lru в обе стороны (после смещения и добавления)
    assert lrucache_linked.keys_in_lru_order()[0] != key
    lrucache_linked.put(key, value)
    assert lrucache_linked.keys_in_lru_order()[0] == key
    lrucache_linked.put("PLACEHOLDER", "PLACEHOLDER")
    assert lrucache_linked.keys_in_lru_order()[0] != key


def test_lrucache_linked_put_reuse_nodes(lrucache_linked):
    old_id = id(lrucache_linked.cache[-1000])
    lrucache_linked.put(-1000, "new")
    new_id = id(lrucache_linked.cache[-1000])
    assert old_id == new_id
