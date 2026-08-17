import sys
import heapq


n, k, *nums = map(int, sys.stdin.read().split())
k_largest = []
answer = ['-' for _ in range(k - 1)]
for num in nums:
    if len(k_largest) < k:
        heapq.heappush(k_largest, num)
    if len(k_largest) == k:
        if num > k_largest[0]:
            heapq.heappushpop(k_largest, num)
        answer.append(str(k_largest[0]))

sys.stdout.write('\n'.join(answer))
