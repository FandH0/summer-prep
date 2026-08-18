import sys
import heapq


n, k, *nums = map(int, sys.stdin.read().split())
k_largest = []
answer = ['-'] * min(k - 1, n)
for num in nums:
    if len(k_largest) < k:
        heapq.heappush(k_largest, num)
    elif num > k_largest[0]:
        heapq.heappushpop(k_largest, num)

    if len(k_largest) == k:
        answer.append(str(k_largest[0]))

sys.stdout.write('\n'.join(answer))
