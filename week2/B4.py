import sys


n, *nums = map(int, sys.stdin.read().split())
left, right = 0, n - 1
mid = left

while mid <= right:
    if nums[mid] == 0:
        nums[mid], nums[left] = nums[left], nums[mid]
        left += 1
        mid += 1
    elif nums[mid] == 2:
        nums[mid], nums[right] = nums[right], nums[mid]
        right -= 1
    else:
        mid += 1

print(*nums)
