import sys


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


n, *nums = sys.stdin.read().split()
p = int(nums.pop())
linked_list = LinkedList(nums)
answer = []

# поиск среднего
tortoise, rabbit = linked_list.start, linked_list.start
while (rabbit.next or rabbit) is not linked_list.end:
    tortoise = tortoise.next
    rabbit = rabbit.next.next
# прогоняем четный случай на "вторую середину"
if rabbit is not linked_list.end:
    tortoise = tortoise.next
answer.append(tortoise.value)

"""
Заяц и черепаха при цикле всегда встретятся до того, как черепаха пройдет до последнего элемента включительно, а
без цикла они не встретятся вовсе.
Доказательство:
Обозначим за x передвижение черепахи, за 2x - передвижение зайца. Без цикла для x>0: x != 2x, то есть нет пересечения.
Однако если цикл есть, то заяц окажется позади черепахи с элемента p. Длина цикла: n - p. За каждый шаг заяц будет
приближаться на 1 клетку, пока не достигнет черепаху, как инвариантная разность скоростей:
5-7 - расстояние 2, 7-8 - расстояние 1, 9-9 - пересечение.
Так как максимальное расстояние от зайца до черепахи внутри цикла равно (длине цикла - 2) и оно уменьшается на 1
с каждым шагом, получим что черепаха не сможет пройти весь цикл, встретившись с зайцем в крайнем случае в последнем
элементе списка, что и требовалось доказать.
"""
# проверка на цикл
linked_list.create_loop(p)
tortoise, rabbit = linked_list.start, linked_list.start
while (rabbit.next or rabbit) is not linked_list.end:
    tortoise = tortoise.next
    rabbit = rabbit.next.next
    if rabbit is tortoise:
        print(rabbit.value)
        answer.append("YES")
        break
else:
    answer.append("NO")

sys.stdout.write("\n".join(answer))
