import sys


n = int(sys.stdin.readline().rstrip())
data = map(int, sys.stdin.read().split())
sections = []
for _ in range(n):
    sections.append([next(data), next(data)])
sections.sort()

answer = []
current = sections[0]
for i in range(1, n):
    after = sections[i]
    if current[1] >= after[0]:  # пересекается с данным отрезком
        current[1] = max(current[1], after[1])
    else:
        answer.append(current)
        current = after  # сменяем отрезок для слияния
answer.append(current)

sys.stdout.write(f"{len(answer)}\n")
sys.stdout.write("\n".join(f"{i[0]} {i[1]}" for i in answer))
