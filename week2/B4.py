import sys


n, *nums = map(int, sys.stdin.read().split())
left, mid, right = 0, 1, 2


while right < n:
    while nums[left] == 0 and left < n - 1:
        left += 1
    mid = max(mid, left)
    while nums[mid] == 1 and mid < n - 1:
        mid += 1
    right = max(right, mid)
    if nums[left] > nums[right]:
        nums[left], nums[right] = nums[right], nums[left]
    if nums[left] > nums[mid]:
        nums[left], nums[mid] = nums[mid], nums[left]
    if nums[mid] > nums[right]:
        nums[mid], nums[right] = nums[right], nums[mid]
    right += 1
print(*nums)