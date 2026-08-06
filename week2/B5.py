import sys


n, k, *nums = map(int, sys.stdin.read().split())

window_sum = sum(nums[:k])
max_sum = window_sum
for shift in range(k, n):
    window_sum += nums[shift]
    window_sum -= nums[shift - k]
    max_sum = max(max_sum, window_sum)

print(max_sum)
