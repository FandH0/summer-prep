import sys


def find_parent(x):
    if parent[x] == x:  # дошли до корня
        return x
    else:
        # первая оптимизация - сокращение путей
        parent[x] = find_parent(parent[x])
        return parent[x]


def union(x, y):
    x = find_parent(x)
    y = find_parent(y)
    # вторая оптимизация - выбор по рангу
    if rang[x] > rang[y]:
        parent[y] = x
    elif rang[x] < rang[y]:
        parent[x] = y
    else:
        parent[y] = x
        rang[x] += 1


def get(x, y):
    return "YES" if find_parent(x) == find_parent(y) else "NO"


n, q = map(int, sys.stdin.readline().split())
requests = sys.stdin.read().split()
parent = [x for x in range(n)]  # создание n множеств
rang = [1 for x in range(n)]  # ранги для второй оптимизации

answer = []
for i in range(0, q):
    a, b = int(requests[3 * i + 1]), int(requests[3 * i + 2])
    print(parent)
    if requests[3 * i] == 'get':
        answer.append(get(a, b))
    else:
        union(a, b)

sys.stdout.write("\n".join(answer))
