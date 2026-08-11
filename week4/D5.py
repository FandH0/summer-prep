import sys


n, m = map(int, sys.stdin.readline().split())
field = sys.stdin.read().split()


def dfs_islands_recursive():
    islands = {}  # id острова: True если самостоятельный иначе False
    visited = [[False] * m for _ in range(n)]

    def pre_order_islands(y, x, current_island):
        # посещение снова только при проверке самостоятельности острова сверху (то есть при спуске вниз)
        if visited[y][x]:
            if field[y][x] == '1' and current_island is not None:
                islands[current_island] = False
            return
        if x == 0:
            # обнуление острова при переходе на новый слой (что происходит при x == 0)
            # для того чтобы избегать острова, которые сами на себя ссылаются при проверке самостоятельности
            current_island = None
        # создание острова если его нет
        if field[y][x] == '1' and current_island is None:
            current_island = len(islands)
            islands[current_island] = True
            if y + 1 < n and x == 0:
                # требуем проверки на самостоятельность из-за того, что она не запускается на левом хребте
                pre_order_islands(y + 1, x, current_island)
        elif field[y][x] == '0':
            current_island = None
        visited[y][x] = True


        if y + 1 < n:
            # спуск вниз при левом хребте или проверке на самостоятельность
            pre_order_islands(y + 1, x, current_island)
        if x + 1 < m:
            pre_order_islands(y, x + 1, current_island)

    pre_order_islands(0, 0, None)

    # считаем самостоятельные острова
    return sum(islands.values())


print(dfs_islands_recursive())