from collections.abc import Hashable
from collections import OrderedDict
from abc import ABC
from typing import Any


class LRUCache(ABC):
    def __init__(self, capacity: int):
        # РЕШЕНИЕ: bool не принимается как подкласс int
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError(f"Capacity should be an integer: {type(capacity)}")
        if capacity < 1:
            raise ValueError(f"Capacity should be greater than zero: {capacity}")
        self.capacity = capacity

    def get(self, key: Hashable) -> Any:
        pass

    def put(self, key: Hashable, value: Any) -> None:
        pass

    def __len__(self):
        pass

    def __contains__(self, key: Hashable):
        pass

    def keys_in_lru_order(self) -> list[Hashable]:
        pass


class Node:
    def __init__(self, key, val, prev=None, next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next


class LinkedList:
    def __init__(self):
        self.start = Node(None, None)
        self.end = Node(None, None)
        self.start.next = self.end
        self.end.prev = self.start

    @staticmethod
    def remove(node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def push_front(self, node: Node) -> None:
        node.next = self.start.next
        node.prev = self.start
        self.start.next.prev = node
        self.start.next = node

    @property
    def last(self) -> Node:
        return self.end.prev


class LRUCacheLinked(LRUCache):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.cache: dict[Hashable, Node] = dict()
        self._list = LinkedList()

    def get(self, key: Hashable) -> Any:
        if key in self.cache:
            node = self.cache[key]
            # lru реализация
            # remove вызван первым, так как иначе будут потеряны ссылки на объекты рядом с ним
            self._list.remove(node)
            self._list.push_front(node)
            return node.val
        raise KeyError(f"Key not found: {key}")

    def put(self, key: Hashable, value: Any) -> None:
        if key not in self:
            # удаление элемента с конца
            if len(self) == self.capacity:
                last = self._list.last
                self._list.remove(last)
                del self.cache[last.key]

            node = Node(key, value)
            self._list.push_front(node)
            self.cache[key] = node
        else:
            self.cache[key].val = value
            self._list.remove(self.cache[key])
            self._list.push_front(self.cache[key])

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key: Hashable):
        return key in self.cache

    def keys_in_lru_order(self) -> list[Hashable]:
        current: Node = self._list.start.next
        keys = []
        while current is not self._list.end:
            keys.append(current.key)
            current = current.next
        return keys


class LRUCacheOrdered(LRUCache):
    """Начало OrderedDict для добавления, обновления или обращения элементов,
    удаление излишних элементов с конца"""
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.cache = OrderedDict()

    def get(self, key: Hashable) -> Any:
        if key in self.cache:
            self.cache.move_to_end(key, last=False)
            return self.cache[key]
        raise KeyError(f"Key not fount: {key}")

    def put(self, key: Hashable, value: Any) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key, last=False)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=True)

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key: Hashable):
        return key in self.cache

    def keys_in_lru_order(self) -> list[Hashable]:
        return list(self.cache.keys())


class LRUCacheNaive(LRUCache):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.cache = dict()
        self._order = []

    def get(self, key: Hashable) -> Any:
        if key in self.cache:
            self._order.remove(key)
            self._order.insert(0, key)
            return self.cache[key]
        raise KeyError(f"Key not found: {key}")

    def put(self, key: Hashable, value: Any) -> None:
        if key not in self.cache:
            self._order.insert(0, key)
            self.cache[key] = value
            if len(self._order) > self.capacity:
                last_key = self._order[-1]
                self._order.remove(last_key)
                del self.cache[last_key]
        else:
            self._order.remove(key)
            self._order.insert(0, key)
            self.cache[key] = value

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key: Hashable):
        return key in self.cache

    def keys_in_lru_order(self) -> list[Hashable]:
        return self._order[:]
