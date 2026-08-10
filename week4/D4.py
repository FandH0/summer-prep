import sys


data = map(int, sys.stdin.read().split())
n = next(data)
value, left, right = [], [], []
for _ in range(n):
    value.append(next(data))
    left.append(next(data))
    right.append(next(data))


def in_order_is_bst():
    stack = [0]
    depth, cur_depth = 1, 1
    answer = "YES"
    last_in_order = -float("inf")

    while left[stack[-1]] != -1:
        cur_depth += 1
        stack.append(left[stack[-1]])

    while stack:
        current = stack.pop()
        if value[current] <= last_in_order:
            answer = "NO"
        last_in_order = value[current]

        depth = max(depth, cur_depth)
        cur_depth -= 1
        if right[current] == -1:
            continue

        # сдвиг вправо
        stack.append(right[current])
        cur_depth += 2
        while left[stack[-1]] != -1:
            stack.append(left[stack[-1]])
            cur_depth += 1

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
