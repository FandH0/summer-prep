from collections.abc import Hashable
from collections import OrderedDict
from typing import Any


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


class LRUCacheLinked:
    def __init__(self, capacity: int):
        # РЕШЕНИЕ: bool не принимается как подкласс int
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError(f"Capacity should be an integer: {type(capacity)}")
        if capacity < 1:
            raise ValueError(f"Capacity should be greater than zero: {capacity}")

        self.capacity = capacity
        self.cache: dict[Hashable, Node] = dict()
        self._list = LinkedList()

    def get(self, key: Hashable) -> Any:
        # исключения вызваны самим словарем
        node = self.cache[key]

        # lru реализация
        # remove вызван первым, так как иначе будут потеряны ссылки на объекты рядом с ним
        self._list.remove(node)
        self._list.push_front(node)

        return node.val

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

    def __contains__(self, key):
        return key in self.cache

    def keys_in_lru_order(self) -> list[Hashable]:
        current: Node = self._list.start.next
        keys = []
        while current is not self._list.end:
            keys.append(current.key)
            current = current.next
        return keys


class LRUCacheOrdered:
    """Начало OrderedDict для удаления излишних элементов, конец для добавления, обращения"""
    def __init__(self, capacity: int):
        # РЕШЕНИЕ: bool не принимается как подкласс int
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError(f"Capacity should be an integer: {type(capacity)}")
        if capacity < 1:
            raise ValueError(f"Capacity should be greater than zero: {capacity}")

        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: Hashable) -> Any:
        self.cache.move_to_end(key, last=True)
        return self.cache[key]

    def put(self, key: Hashable, value: Any) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key, last=True)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key: Hashable):
        return key in self.cache

    def keys_in_lru_order(self) -> list[Hashable]:
        # список развернут для совместимости с LRUCacheLinked (последний элемент выходит)
        return list(self.cache.keys())[::-1]
