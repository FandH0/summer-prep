import sys
from collections import defaultdict
from heapq import heappush, heappop


n, m = map(int, sys.stdin.readline().split())
data = map(int, sys.stdin.read().split())
out_nodes = defaultdict(list)
in_degree = defaultdict(int)
for _ in range(m):
    a, b = next(data), next(data)
    out_nodes[a].append(b)
    in_degree[b] += 1

answer = []
in_zero = []
for node in range(n, 0, -1):
    if in_degree[node] == 0:
        heappush(in_zero, node)
while in_zero:
    node = heappop(in_zero)
    answer.append(str(node))
    for dependant in out_nodes[node]:
        in_degree[dependant] -= 1
        if in_degree[dependant] == 0:
            heappush(in_zero, dependant)

if len(answer) < n:
    sys.stdout.write("-1")
else:
    sys.stdout.write(" ".join(answer))
