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
    prev_step2, prev_step1 = 0, 0
    for i in range(step):
        current = max(prev_step2, prev_step1) + steps[i]
        prev_step2 = prev_step1
        prev_step1 = current
    return current


n, *steps = map(int, sys.stdin.read().split())

if n <= sys.getrecursionlimit() - 5:
    ans = recursive_max(n - 1)
else:
    ans = iterative_max(n)

sys.stdout.write(str(ans))
