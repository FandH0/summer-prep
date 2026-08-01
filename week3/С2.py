import sys


data = list(map(int, sys.stdin.read().split()))
n = data[0]
q = data[n + 1]
answers = []


def bisect_left(goal):
    left, right = 1, n + 1
    while left != right:
        mid = (left + right) // 2
        mid_num = data[mid]
        if mid_num == goal and (data[mid - 1] < mid_num or mid == 1):
            return mid - 1  # учитываем сдвиг в 1 при подборе left, right
        elif mid_num < goal:
            left = mid + 1
        else:
            right = mid
    return -1


def bisect_right(goal):
    left, right = 1, n + 1
    while left != right:
        mid = (left + right) // 2
        mid_num = data[mid]
        if mid_num == goal and (data[mid + 1] > mid_num or mid == n):
            return mid - 1  # учитываем сдвиг в 1 при подборе left, right
        elif mid_num > goal:
            right = mid
        else:
            left = mid + 1
    return -1


for i in range(n + 2, n + q + 2):
    goal = data[i]
    answers.append((bisect_left(goal), bisect_right(goal)))

sys.stdout.write("\n".join(f"{i[0]} {i[1]}" for i in answers))
