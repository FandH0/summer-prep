from collections.abc import Hashable
from typing import Any


class Node:
    def __init__(self, key, val, prev=None, next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next


class LinkedList:
    def __init__(self):
        self._start = Node(None, None)
        self._end = Node(None, None)
        self._start.next = self._end
        self._end.prev = self._start

    @staticmethod
    def _remove(node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: Node) -> None:
        node.next = self._start.next
        node.prev = self._start
        self._start.next.prev = node
        self._start.next = node

    def _get_last(self) -> Node:
        return self._end.prev


class LRUCacheLinked(LinkedList):
    def __init__(self, capacity: int) -> None:
        # РЕШЕНИЕ: bool не принимается как подкласс int
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError(f"Capacity should be an interger: {type(capacity)}")
        if capacity < 1:
            raise ValueError(f"Capacity should be greater than zero: {capacity}")

        self.capacity = capacity
        self.cache: dict[Hashable, Node] = dict()
        self._length = 0
        super().__init__()

    def get(self, key: Hashable) -> Any:
        # исключения вызваны самим словарем
        node = self.cache[key]

        # lru реализация
        # _remove вызван первым, так как иначе будут потеряны ссылки на объекты рядом с ним
        self._remove(node)
        self._add_front(node)

        return node.val

    def put(self, key: Hashable, value: Any) -> None:
        if key not in self:
            self._length += 1
            # удаление элемента с конца
            if self._length > self.capacity:
                last = self._get_last()
                self._remove(last)
                del self.cache[last.key]
                del last
                self._length -= 1
        else:
            self._remove(self.cache[key])

        node = Node(key, value)
        self._add_front(node)
        self.cache[key] = node

    def __len__(self) -> int:
        return self._length

    def __contains__(self, key):
        return key in self.cache

    def keys_in_lru_order(self):
        current = self._start.next
        keys = []
        while current != self._end:
            keys.append(current.key)
            current = current.next
        return keys
