import sys


_, *nums = map(int, sys.stdin.read().split())
inverse_count = 0


def merge(left, right):
    merged = []
    while left and right:
        if left[0] <= right[0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
            global inverse_count
            inverse_count += len(left)

    merged.extend(left or right)
    return merged


def merge_sort(array):
    if len(array) == 1:
        return array
    mid = len(array) // 2
    left, right = merge_sort(array[:mid]), merge_sort(array[mid:])
    return merge(left, right)


answer = merge_sort(nums)
print(inverse_count)
print(*answer)
