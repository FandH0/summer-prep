import sys


# перевод в int по мере требования
data = sys.stdin.read().split()
n = int(data[0])
q = int(data[n + 1])
answers = []


def bisect_left(goal):
    global data
    left, right = 1, n + 1
    while left != right:
        mid = (left + right) // 2
        mid_num = int(data[mid])
        if mid_num == goal and (int(data[mid - 1]) < mid_num or mid == 1):
            return mid - 1  # учитываем сдвиг в 1 при подборе left, right
        elif mid_num < goal:
            left = mid + 1
        else:
            right = mid
    return -1


def bisect_right(goal):
    global data
    left, right = 1, n + 1
    while left != right:
        mid = (left + right) // 2
        mid_num = int(data[mid])
        if mid_num == goal and (int(data[mid + 1]) > mid_num or mid == n):
            return mid - 1  # учитываем сдвиг в 1 при подборе left, right
        elif mid_num > goal:
            right = mid
        else:
            left = mid + 1
    return -1


for i in range(n + 2, n + q + 2):
    goal = int(data[i])
    answers.append((bisect_left(goal), bisect_right(goal)))

sys.stdout.write("\n".join(f"{i[0]} {i[1]}" for i in answers))
