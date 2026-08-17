import sys


def key(j):
    return num_arrays[j][-1]


def heappop(heap):
    ans = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    if heap:
        sift_first_down(heap)
    return ans


def heappush(heap, item):
    heap.append(item)
    sift_last_up(heap)


def min_child(heap, i):
    return min(2 * i + 1 if 2 * i + 1 < len(heap) else i,
               2 * i + 2 if 2 * i + 2 < len(heap) else i,
               key=lambda j: key(heap[j]))


def sift_first_down(heap):
    i = 0
    c = min_child(heap, i)
    while i < len(heap) and key(heap[i]) > key(heap[c]):
        heap[i], heap[c] = heap[c], heap[i]
        i = c
        c = min_child(heap, i)


def sift_last_up(heap):
    i = len(heap) - 1
    p = (i - 1) // 2
    while i != 0 and key(heap[i]) < key(heap[p]):
        heap[i], heap[p] = heap[p], heap[i]
        i = p
        p = (i - 1) // 2


k, *data = map(int, sys.stdin.read().split())
i = 0
num_arrays = []
while i < len(data):
    l = data[i]
    # считываю num_arrays в обратном порядке, чтобы использовать pop() для быстрого удаления
    num_arrays.append(data[i + l: i: -1])
    i += l + 1

answer = []
smallest = []
for j in range(k):
    if num_arrays[j]:
        heappush(smallest, j)
while smallest:
    head = heappop(smallest)
    answer.append(str(num_arrays[head].pop()))
    if num_arrays[head]:
        heappush(smallest, head)

sys.stdout.write(" ".join(answer))
