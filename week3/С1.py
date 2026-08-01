import sys


# перевод в int по мере требования
data = sys.stdin.read().split()
n = int(data[0])
q = int(data[n + 1])
answers = []

for i in range(n + 2, n + q + 2):
    left, right = 1, n + 1  # data indices
    num = int(data[i])
    while left < right:
        mid = (left + right) // 2
        mid_num = int(data[mid])
        if mid_num > num:
            right = mid
        elif mid_num < num:
            left = mid + 1
        else:
            answers.append("YES")
            break
    else:
        answers.append("NO")

sys.stdout.write("\n".join(answers))
