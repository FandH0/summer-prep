import sys
from collections import deque


class Node:
    __slots__ = ("value", "left", "right")

    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right


class Tree:
    # преобразует nodes из списка кортежей в список объектов Node
    def __init__(self, nodes):
        nodes.append(None)  # для отсутствующих детей
        # создание древа за один проход
        for i in range(len(nodes) - 1):
            if not isinstance(nodes[i], Node):
                nodes[i] = Node(*nodes[i])
            node = nodes[i]

            # создание детей
            if isinstance(node.left, int) and node.left > i:
                nodes[node.left] = Node(*nodes[node.left])
            if isinstance(node.right, int) and node.right > i:
                nodes[node.right] = Node(*nodes[node.right])

            # присваивание детей
            node.left = nodes[node.left]
            node.right = nodes[node.right]
        self.root = nodes[0]
        nodes.pop()  # удаление None в конце


def in_order(node, answer_buffer):
    if node:
        in_order(node.left, answer_buffer)
        answer_buffer.append(node.value)
        in_order(node.right, answer_buffer)


def pre_order(node, answer_buffer):
    if node:
        answer_buffer.append(node.value)
        pre_order(node.left, answer_buffer)
        pre_order(node.right, answer_buffer)


def post_order(node, answer_buffer):
    if node:
        post_order(node.left, answer_buffer)
        post_order(node.right, answer_buffer)
        answer_buffer.append(node.value)


def in_order_iterative(node, answer_buffer):
    stack = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, int):
            answer_buffer.append(current)
            continue
        if current.right:
            stack.append(current.right)
        stack.append(current.value)
        if current.left:
            stack.append(current.left)


def pre_order_iterative(node, answer_buffer):
    stack = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, int):
            answer_buffer.append(current)
            continue
        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)
        stack.append(current.value)


def post_order_iterative(node, answer_buffer):
    stack = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, int):
            answer_buffer.append(current)
            continue
        stack.append(current.value)
        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)


def by_depth_order(node, answer_buffer):
    queue = deque([node])
    while queue:
        current = queue.popleft()
        if isinstance(current, int):
            answer_buffer.append(current)
            continue
        queue.append(current.value)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)


data = map(int, sys.stdin.read().split())
n = next(data)
nodes_list = []
for _ in range(n):
    nodes_list.append((next(data), next(data), next(data)))

tree = Tree(nodes_list)

answers = [[], [], [], []]
if n < sys.getrecursionlimit() - 1:
    in_order(tree.root, answers[0])
    pre_order(tree.root, answers[1])
    post_order(tree.root, answers[2])
else:
    in_order_iterative(tree.root, answers[0])
    pre_order_iterative(tree.root, answers[1])
    post_order_iterative(tree.root, answers[2])
by_depth_order(tree.root, answers[3])

sys.stdout.write("\n".join(" ".join(map(str, answer)) for answer in answers))
