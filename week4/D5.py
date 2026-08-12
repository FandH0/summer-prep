import sys
from collections import deque


n, m = map(int, sys.stdin.readline().split())
field = sys.stdin.read().split()


def dfs_islands_recursive():
    islands = 0
    visited = [[False] * m for _ in range(n)]

    def flood(y, x):
        if field[y][x] == '1':
            visited[y][x] = True
            if 0 <= y + 1 < n and not visited[y + 1][x]:
                flood(y + 1, x)
            if 0 <= y - 1 < n and not visited[y - 1][x]:
                flood(y - 1, x)
            if 0 <= x + 1 < m and not visited[y][x + 1]:
                flood(y, x + 1)
            if 0 <= x - 1 < m and not visited[y][x - 1]:
                flood(y, x - 1)

    for y in range(n):
        for x in range(m):
            if not visited[y][x] and field[y][x] == '1':
                flood(y, x)
                islands += 1

    return islands


def dfs_island_iterative():
    islands = 0
    visited = [[False] * m for _ in range(n)]

    def mark_island(y, x):
        stack = [(y, x)]
        visited[y][x] = True
        while stack:
            y, x = stack.pop()
            if 0 <= y + 1 < n and not visited[y + 1][x] and field[y + 1][x] == '1':
                stack.append((y + 1, x))
                visited[y + 1][x] = True
            if 0 <= y - 1 < n and not visited[y - 1][x] and field[y - 1][x] == '1':
                stack.append((y - 1, x))
                visited[y - 1][x] = True
            if 0 <= x + 1 < m and not visited[y][x + 1] and field[y][x + 1] == '1':
                stack.append((y, x + 1))
                visited[y][x + 1] = True
            if 0 <= x - 1 < m and not visited[y][x - 1] and field[y][x - 1] == '1':
                stack.append((y, x - 1))
                visited[y][x - 1] = True

    for y in range(n):
        for x in range(m):
            if not visited[y][x] and field[y][x] == '1':
                mark_island(y, x)
                islands += 1

    return islands


def bfs_island():
    islands = 0
    visited = [[False] * m for _ in range(n)]

    def mark_island(y, x):
        queue = deque([(y, x)])
        visited[y][x] = True
        while queue:
            y, x = queue.popleft()
            if 0 <= y + 1 < n and not visited[y + 1][x] and field[y + 1][x] == '1':
                queue.append((y + 1, x))
                visited[y + 1][x] = True
            if 0 <= y - 1 < n and not visited[y - 1][x] and field[y - 1][x] == '1':
                queue.append((y - 1, x))
                visited[y - 1][x] = True
            if 0 <= x + 1 < m and not visited[y][x + 1] and field[y][x + 1] == '1':
                queue.append((y, x + 1))
                visited[y][x + 1] = True
            if 0 <= x - 1 < m and not visited[y][x - 1] and field[y][x - 1] == '1':
                queue.append((y, x - 1))
                visited[y][x - 1] = True

    for y in range(n):
        for x in range(m):
            if not visited[y][x] and field[y][x] == '1':
                mark_island(y, x)
                islands += 1

    return islands


if n * m < sys.getrecursionlimit() - 1:
    answer = dfs_islands_recursive()
elif n * m < 100000:
    answer = dfs_island_iterative()
else:
    answer = bfs_island()
print(answer)
