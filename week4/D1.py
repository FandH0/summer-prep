import sys


class Node:
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


n, *nums = sys.stdin.read().split()
li = LinkedList(nums)


def reverse_iterative(linked_list: LinkedList):
    # разворот списка с сохранением sentinel
    linked_list.end.next = linked_list.start.next  # зацикливание списка
    # три указателя, меняем ссылку для среднего на pre
    pre = linked_list.end
    cur = pre.next
    new = cur.next
    # после цикла не-sentinel объекты получат нужные ссылки на предыдущий элемент, а в pre останется ссылка на последний
    while cur is not linked_list.end:
        cur.next = pre
        pre = cur
        cur = new
        new = new.next
    # поправка указателей sentinel
    linked_list.start.next = pre
    linked_list.end.next = None


# рекурсивный подход работает только для малых n < ~1000, так как рекурсия вызывается внутрь для каждого элемента списка
def reverse_recursive(linked_list: LinkedList):
    pointer = linked_list.end

    # reverse_node отправляется с начала списка до предыдущего pointer элементу и затем коллапсом рекурсии
    # меняет попарно связи до самого начала списка (start.next будет все ещё отсылать на раннее первый элемент)
    def reverse_node(pre: Node):
        nonlocal pointer
        if pre.next is not pointer:
            reverse_node(pre.next)
        pointer.next = pre
        pointer = pre

    reverse_node(linked_list.start)
    linked_list.start, linked_list.end = linked_list.end, linked_list.start
    linked_list.end.next = None  # обрезание списка с конца


reverse_iterative(li)
# вывод
answer = []
pointer = li.start.next
while pointer is not li.end:
    answer.append(pointer.value)
    pointer = pointer.next
sys.stdout.write(" ".join(answer) + "\n")
