import sys
from itertools import batched


"""
Решение через сортировку по времени начала встречи. Для любого набора непересекающихся встреч замена последней встречи
на встречу с более поздним началом увеличивает "окно" для встреч и не уменьшает их общее количество, позволяя вместить 
больше встреч при построении графика с конца. Аналогичным является решение по сортировке времени окончания 
при построении графика с начала.
"""
n = int(sys.stdin.readline().rstrip())
meetings = list(batched(map(int, sys.stdin.read().split()), 2))
meetings.sort(key=lambda x: x[0], reverse=True)


right_border = 10 ** 9
answer = 0
for start, end in meetings:
    if right_border >= end:
        right_border = start
        answer += 1
print(answer)
