import sys


class Node:
    def __init__(self, value, next):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, values=[]):
        self.start = Node("start", None)
        self.end = Node("end", None)
        pointer = self.start
        for value in values:
            new = Node(value, None)
            pointer.next = new
            pointer = new
        pointer.next = self.end


n, *nums = sys.stdin.read().split()
l = LinkedList(nums)


# разворот списка с сохранением sentinel
l.end.next = l.start.next  # зацикливание списка
# три указателя, меняем ссылку для среднего на pre
pre = l.end
cur = pre.next
new = cur.next
# после цикла не-sentinel объекты получат нужные ссылки на предыдущий элемент, а в pre останется ссылка на последний
while cur is not l.end:
    cur.next = pre
    pre = cur
    cur = new
    new = new.next
# поправка указателей sentinel
l.start.next = pre
l.end.next = None

# вывод
answer = []
pointer = l.start.next
while pointer is not l.end:
    answer.append(pointer.value)
    pointer = pointer.next
sys.stdout.write(" ".join(answer) + "\n")
