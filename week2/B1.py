import sys

n, s, *nums = map(int, sys.stdin.read().split())
passed_nums = dict()
answer = None
for i in range(len(nums)):
    if s - nums[i] in passed_nums:
        answer = (passed_nums[s-nums[i]], i)
    passed_nums[nums[i]] = i

if answer:
    print(*answer)
else:
    print(-1)
