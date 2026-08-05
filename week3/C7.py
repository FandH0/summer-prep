import sys


_, *nums = map(int, sys.stdin.read().split())
inverse_count = 0


def merge(left, right):
    merged = []
    li, ri = 0, 0
    len_left, len_right = len(left), len(right)
    while li < len_left and ri < len_right:
        if left[li] <= right[ri]:
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
            global inverse_count
            inverse_count += len_left - li

    merged.extend(left[li:] or right[ri:])
    return merged


def merge_sort(array):
    if len(array) == 1:
        return array
    mid = len(array) // 2
    left, right = merge_sort(array[:mid]), merge_sort(array[mid:])
    return merge(left, right)


answer = merge_sort(nums)
sys.stdout.writelines([str(inverse_count) + '\n', " ".join(map(str, answer))])
