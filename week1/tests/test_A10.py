import A10
from pytest import mark, raises, fixture
from random import seed, choice, randint
CACHE_CLASSES = (A10.LRUCacheLinked, A10.LRUCacheOrdered, A10.LRUCacheNaive)


def test_differential_against_model():
    seed(100)
    lru_cache = [c(10) for c in CACHE_CLASSES]
    history = []

    for step in range(10000):
        key = randint(0, 20)
        op = choice(["get", "put"])
        history.append((op, key))

        results = []
        for c in lru_cache:
            if op == "put":
                c.put(key, step)
                results.append(None)
            else:
                try:
                    results.append(("ok", c.get(key)))
                except KeyError:
                    results.append(("miss",))

        orders = [c.keys_in_lru_order() for c in lru_cache]
        assert len(set(map(str, results))) == 1, f"расхождение на {step}: {history[-10:]}"
        assert len(set(map(str, orders))) == 1, f"порядок разошёлся на {step}: {history[-10:]}"


@mark.parametrize("lru_class", CACHE_CLASSES)
def test_lrucache_leak(lru_class):
    seed(100)
    lru_cache = lru_class(10)

    for step in range(10000):
        key = randint(0, 20)
        lru_cache.put(key, step)

    assert len(lru_cache) == 10
    assert set(lru_cache.keys_in_lru_order()) == set(lru_cache.cache)


@fixture(params=CACHE_CLASSES)
def lrucache(request):
    """lru cache с одним свободным местом"""
    capacity = 14
    lru_cache = request.param(capacity)
    keys_values = [(-1000, 1), ('2', 1), (LookupError, '123'), ((1, 2), '123'), (2, [1, 2, 3]), (3, 1),
                   (-3.4, '123'), ('whatever', None), ('123', None), ('213', None), (1232, [1, 2, 3]),
                   (None, [1, 2, 3]), (12, LookupError)]

    for key, value in keys_values:
        lru_cache.put(key, value)
    return lru_cache


@mark.parametrize("lru_class", CACHE_CLASSES)
@mark.parametrize("length", (0, 1, 5, 10, 100))
def test_lrucache_length(length, lru_class):
    lru_cache = lru_class(capacity=10)
    for item in range(length):
        lru_cache.put(key=item, value=item)
    assert len(lru_cache.cache) == min(length, 10)
    assert len(lru_cache.keys_in_lru_order()) == min(length, 10)
    assert len(lru_cache) == min(length, 10)


@mark.parametrize("lru_class", CACHE_CLASSES)
@mark.parametrize("capacity", (None, [], "str", True, 1.5))
def test_lrucache_capacity_wrong_type(capacity, lru_class):
    with raises(TypeError):
        lru_class(capacity=capacity)


@mark.parametrize("lru_class", CACHE_CLASSES)
@mark.parametrize("capacity", (-1, 0))
def test_lrucache_capacity_non_positive(capacity, lru_class):
    with raises(ValueError):
        lru_class(capacity=capacity)


def test_lrucache_contains(lrucache):
    assert '2' in lrucache
    assert lrucache.keys_in_lru_order()[0] != '2'


def test_lrucache_get_not_existing(lrucache):
    old_lru_order = lrucache.keys_in_lru_order()
    with raises(KeyError):
        lrucache.get("new")
    assert old_lru_order == lrucache.keys_in_lru_order()


@mark.parametrize("key, value", [('123', None), (None, [1, 2, 3]), (-1000, 1), ('2', 1),])
def test_lrucache_get_lru_order(lrucache, key, value):
    assert lrucache.keys_in_lru_order()[0] != key
    assert lrucache.get(key) == value
    assert lrucache.keys_in_lru_order()[0] == key


def test_lrucache_put_capacity(lrucache):
    last = lrucache.keys_in_lru_order()[-1]
    lrucache.put("PLACEHOLDER", "PLACEHOLDER")  # заполнение lrucache
    lrucache.put("new", 1)  # новое значение
    assert len(lrucache) <= lrucache.capacity
    assert last not in lrucache


def test_lrucache_put_existing(lrucache):
    length = len(lrucache)
    lrucache.put('123', "new")  # существующее значение
    assert len(lrucache) == length
    assert lrucache.keys_in_lru_order().count('123') == 1
    assert lrucache.get('123') == "new"


@mark.parametrize("key, value", [('123', None), (None, [1, 2, 3]), (None, None), ("new", 1),])
def test_lrucache_put_lru_order(lrucache, key, value):
    # изменение в lru в обе стороны (после смещения и добавления)
    assert lrucache.keys_in_lru_order()[0] != key
    lrucache.put(key, value)
    assert lrucache.keys_in_lru_order()[0] == key
    lrucache.put("PLACEHOLDER", "PLACEHOLDER")
    assert lrucache.keys_in_lru_order()[0] != key


def test_lrucache_linked_put_reuse_nodes():
    lrucache_linked = A10.LRUCacheLinked(capacity=10)
    lrucache_linked.put(-1000, "old")
    old_id = id(lrucache_linked.cache[-1000])
    lrucache_linked.put(-1000, "new")
    new_id = id(lrucache_linked.cache[-1000])
    assert old_id == new_id
