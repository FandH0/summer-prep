import sys


k = int(sys.stdin.read().rstrip())
stack = [("(", k - 1, k)]
answer = []
while stack:
    pairs, left_capacity, right_capacity = stack.pop()
    if len(pairs) == 2 * k:
        answer.append(pairs)
        continue
    if right_capacity > 0 and left_capacity < right_capacity:
        stack.append((pairs + ')', left_capacity, right_capacity - 1))
    if left_capacity > 0:
        stack.append((pairs + '(', left_capacity - 1, right_capacity))

sys.stdout.write("\n".join(answer))
