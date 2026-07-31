import sys


n, *nums = map(int, sys.stdin.read().split())
left, right = 0, n - 1

while left < n and nums[left] == 0:
    left += 1
while right > 0 and nums[right] == 2:
    right -= 1
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

print(nums)
