import sys


data = map(int, sys.stdin.read().split())
n = next(data)
value, left, right = [], [], []
for _ in range(n):
    value.append(next(data))
    left.append(next(data))
    right.append(next(data))


def in_order_is_bst():
    stack = [(0, 1)]  # (node, current_depth)
    depth = 0
    answer = "YES"
    last_in_order = -float("inf")

    while left[stack[-1][0]] != -1:
        stack.append((left[stack[-1][0]], stack[-1][1] + 1))

    while stack:
        current = stack.pop()
        if value[current[0]] <= last_in_order:
            answer = "NO"
        last_in_order = value[current[0]]
        depth = max(depth, current[1])

        if right[current[0]] == -1:
            continue
        # сдвиг вправо
        stack.append((right[current[0]], current[1] + 1))
        while left[stack[-1][0]] != -1:
            stack.append((left[stack[-1][0]], stack[-1][1] + 1))

    return answer, str(depth)


def window_is_bst():
    # используем pre-order
    stack = [(0, -float("inf"), float("inf"), 1)]
    depth = 0
    answer = "YES"
    while stack:
        node, min_border, max_border, cur_depth = stack.pop()

        depth = max(depth, cur_depth)
        if not (min_border < value[node] < max_border):
            answer = "NO"

        if right[node] != -1:
            stack.append((right[node], value[node], max_border, cur_depth + 1))
        if left[node] != -1:
            stack.append((left[node], min_border, value[node], cur_depth + 1))

    return answer, str(depth)


if n > 1000:  # используем in_order на больших входах так как он использует меньше памяти
    answer = in_order_is_bst()
else:
    answer = window_is_bst()
sys.stdout.write('\n'.join(answer))
