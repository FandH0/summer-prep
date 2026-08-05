import sys


"""
Подсчет инверсий при сортировке слиянием. Считаем инверсии при слиянии левой и правой части. Если добавляем элемент
правой части в слияние скорее элементов левой, значит что этот элемент образовывает инверсию с оставшимися 
в left числами. Добавляя количество оставшихся в left чисел к счетчику получим число инверсий при слиянии. Одна и та же
инверсия не появится снова при следующий слияниях, так как она будет разрешена. И ни одна инверсия не будет пропущена,
ведь при ней элемент из правой части окажется меньше соответствующего инверсии элемента с левой части. Из-за этого
счетчик будет отражать количество инверсий, встреченных при сортировке списка к упорядоченному виду, что и есть общее 
число инверсий.
Сортировка слиянием является устойчивой, так как в сравнении if left[li] <= right[ri] мы не меняем порядок равных по
ключу элементов. Элемент левее будет добавлен первым. Изменив на строгое сравнение получим неустойчивую сортировку.
"""
_, *nums = map(int, sys.stdin.read().split())
inverse_count = 0


def merge(left, right):
    global inverse_count
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
