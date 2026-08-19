import sys
from itertools import accumulate
from collections import defaultdict


n, q, s = map(int, sys.stdin.readline().split())
nums = map(int, sys.stdin.readline().split())
requests = map(int, sys.stdin.read().split())

pref_sums = [0]
pref_sums.extend(accumulate(nums))

answer = []
i = 0
while i < q:
    a, b = next(requests), next(requests)
    answer.append(str(pref_sums[b + 1] - pref_sums[a]))
    i += 1

prev = defaultdict(int)
counts = 0
for pref in pref_sums:
    counts += prev[pref - s]
    prev[pref] += 1
answer.append(str(counts))

sys.stdout.write("\n".join(answer))
