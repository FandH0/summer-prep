import sys
import time


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, values=None):
        self.start = Node("start", None)
        self.end = Node("end", None)
        pointer = self.start
        for value in values or []:
            new = Node(value, None)
            pointer.next = new
            pointer = new
        pointer.next = self.end

    def create_loop(self, p):
        if p == -1:
            return
        i = -1
        pointer = self.start
        while pointer.next is not self.end:  # проход до последнего не-sentinel
            pointer = pointer.next
            i += 1
            if i == p:
                cycle_enter = pointer
        pointer.next = cycle_enter


start = time.perf_counter()
data = list(sys.stdin.read().split())
nums, p = data[1:-1], int(data[-1])
linked_list = LinkedList(nums)
answer = []

# поиск среднего
rabbit, tortoise = linked_list.start, linked_list.start
while (tortoise.next or tortoise) is not linked_list.end:
    rabbit = rabbit.next
    tortoise = tortoise.next.next
# прогоняем четный случай на "вторую середину"
if tortoise is not linked_list.end:
    rabbit = rabbit.next
answer.append(rabbit.value)

"""
Заяц и черепаха при цикле всегда встретятся до того, как черепаха пройдет до последнего элемента включительно, а
без цикла они не встретятся вовсе.
Доказательство:
Обозначим за x передвижение черепахи, за 2x - передвижение зайца. Без цикла для x>0: x != 2x, то есть нет пересечения.
Однако если цикл есть, то передвижение зайца после прохождения списка начинается с начала + индекс начала цикла, то есть
по закону 2x - n + p. Обозначим условие того, чтобы заяц и черепаха встретились до конца прохода черепахи как x <= n.
Рассмотрим систему: x = 2x - n + p (встреча черепахи и зайца), x <= n (до того, как черепаха дойдет до конца).
её решение: x = n - p (место встречи), x <= n (следует из первого уравнения, выполняется всегда)
Система имеет решение => встреча до конца прохода, что и требовалось доказать.
"""
# проверка на цикл
linked_list.create_loop(p)
rabbit, tortoise = linked_list.start, linked_list.start
while (tortoise.next or tortoise) is not linked_list.end:
    rabbit = rabbit.next
    tortoise = tortoise.next.next
    if rabbit is tortoise:
        answer.append("YES")
        break
else:
    answer.append("NO")

sys.stdout.write("\n".join(answer))
