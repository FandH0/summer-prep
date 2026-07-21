# Дан список чисел и окно k. Верните список максимумов каждого окна.
# Сначала решите наивно за O(n·k), затем через collections.deque за O(n)
from collections import deque
from random import randint
from time import perf_counter

def time_test(f, *args) -> float:
    start = perf_counter()
    f(*args)
    end = perf_counter()
    return end - start

def naive_window_max(nums: list[int], k: int) -> list[int]:
    answer = []
    for i in range(k, len(nums) + 1):
        answer.append(max(nums[i-k: i]))
    return answer

def deque_window_max(nums: list[int], k: int) -> list[int]:
    window = deque([], maxlen=k)
    answer = []
    for index, val in enumerate(nums):
        if window and window[0] < index - k + 1:  # очистка deque от старых элементов
            window.popleft()
        while window and nums[window[-1]] <= val:  # подготовка к добавлению нового элемента
            window.pop()
        window.append(index)
        if index >= k - 1 or index == len(nums) - 1:
            answer.append(nums[window[0]])
    return answer


if __name__ == "__main__":
    nums = [randint(1, 100) for i in range(10**6)]
    # time test naive k = 10
    print(f'For k=10 and len(nums)=10**6 naive approach takes {time_test(naive_window_max, nums, 10)}s')
    # time test naive k = 100
    print(f'For k=100 and len(nums)=10**6 naive approach takes {time_test(naive_window_max, nums, 100)}s')
    # time test deque k = 10
    print(f'For k=10 and len(nums)=10**6 deque approach takes {time_test(deque_window_max, nums, 10)}s')
    # time test deque k = 100
    print(f'For k=100 and len(nums)=10**6 deque approach takes {time_test(deque_window_max, nums, 100)}s')
    assert naive_window_max(nums, 10) == deque_window_max(nums, 10)
    assert naive_window_max([1, 2, 3, 4, 1, 2, 3, 1], 3) == [3, 4, 4, 4, 3, 3]
    assert deque_window_max([1, 2, 3, 4, 1, 2, 3, 1], 3) == [3, 4, 4, 4, 3, 3]
    assert deque_window_max([1], 3) == [1]
