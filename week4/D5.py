import sys


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
    stack = [(0, 0, False)]
    pointer_y, pointer_x = 0, 1
    while stack:
        y, x, flood = stack.pop()
        if not stack and pointer_y < n:  # основной проход
            while pointer_x < m:
                stack.append((pointer_y, pointer_x, False))
                pointer_x += 1
            pointer_y += 1
            pointer_x = 0

        if not flood and not visited[y][x] and field[y][x] == '1':
            islands += 1
            flood = True

        if flood and field[y][x] == '1':
            if 0 <= y + 1 < n and not visited[y + 1][x]:
                visited[y + 1][x] = True
                stack.append((y + 1, x, True))
            if 0 <= y - 1 < n and not visited[y - 1][x]:
                visited[y - 1][x] = True
                stack.append((y - 1, x, True))
            if 0 <= x + 1 < m and not visited[y][x + 1]:
                visited[y][x + 1] = True
                stack.append((y, x + 1, True))
            if 0 <= x - 1 < m and not visited[y][x - 1]:
                visited[y][x - 1] = True
                stack.append((y, x - 1, True))
        visited[y][x] = True

    return islands


if n * m < sys.getrecursionlimit() - 1:
    answer = dfs_islands_recursive()
else:
    answer = dfs_island_iterative()

print(answer)
