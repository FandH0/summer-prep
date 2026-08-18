import sys


def memoize(f):
    cache = {}

    def internal_f(step):
        if step not in cache:
            cache[step] = f(step)
        return cache[step]

    return internal_f


@memoize
def recursive_max(step):  # step - индекс с 0, поэтому для последней ступени step = n - 1
    if step < 0:
        return 0
    return max(recursive_max(step - 2), recursive_max(step - 1)) + steps[step]


def iterative_max(step):  # step - количество ступенек, поэтому для последней ступени step = n
    if step == 1:
        return steps[0]
    table = [0] * step
    # при длине больше или равной 2 ссылка на предыдущие ступеньки не выйдет из-за грани и
    # для первых двух ступеней будет гарантированно иметь нуль в одном из table[i - 1] или table[i - 2]
    for i in range(step):
        table[i] = max(table[i - 1], table[i - 2]) + steps[i]
    return table[step - 1]


n, *steps = map(int, sys.stdin.read().split())

if n <= sys.getrecursionlimit() - 5:
    ans = recursive_max(n - 1)
else:
    ans = iterative_max(n)

sys.stdout.write(str(ans))
