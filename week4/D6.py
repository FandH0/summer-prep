import sys
from collections import deque


n, m = map(int, sys.stdin.readline().split())
data = sys.stdin.read().split()
r1, c1, r2, c2 = map(int, data[-4:])
# BFS
queue = deque([(r1, c1, 0)])
visited = [[False] * n for _ in range(m)]
answer = -1
while queue:
    y, x, length = queue.popleft()
    if (y, x) == (r2, c2):  # конечная цель
        answer = length
        break
    if 0 <= y + 1 < n and not visited[y + 1][x] and data[y + 1][x] == '.':
        queue.append((y + 1, x, length + 1))
        visited[y + 1][x] = True
    if 0 <= y - 1 < n and not visited[y - 1][x] and data[y - 1][x] == '.':
        queue.append((y - 1, x, length + 1))
        visited[y - 1][x] = True
    if 0 <= x + 1 < m and not visited[y][x + 1] and data[y][x + 1] == '.':
        queue.append((y, x + 1, length + 1))
        visited[y][x + 1] = True
    if 0 <= x - 1 < m and not visited[y][x - 1] and data[y][x - 1] == '.':
        queue.append((y, x - 1, length + 1))
        visited[y][x - 1] = True

print(answer)
