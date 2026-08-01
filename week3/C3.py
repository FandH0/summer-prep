import sys


n, k, *nums = map(int, sys.stdin.read().split())


def count_ropes(length):
    ans = 0
    for rope in nums:
        ans += rope // length
    return ans


left, right = 1, 1 + sum(nums) // k
answer = 0
while left != right:
    mid = (left + right) // 2
    amount = count_ropes(mid)
    if amount >= k:
        answer = mid
        left = mid + 1
    else:
        right = mid
sys.stdout.write(str(answer))
