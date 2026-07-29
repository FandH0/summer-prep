import sys

_, s, *nums = map(int, sys.stdin.read().split())
passed_nums = {}
answer = None

for i, num in enumerate(nums):
    need = s - num
    if need in passed_nums:
        answer = (passed_nums[need], i)
        break
    passed_nums[num] = i

if answer is not None:
    print(*answer)
else:
    print(-1)
