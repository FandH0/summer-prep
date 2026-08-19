import sys


n, S, *coins = map(int, sys.stdin.read().split())

sums = [[float("inf"), 0] for _ in range(S + 1)]  # минимальный путь, количество способов
sums[0] = [0, 1]
# проход по монетам гарантирует, что монеты будут поступать только в одном порядке, из-за чего нет перестановок
for coin in coins:
    for s in range(S):
        if s + coin <= S:
            sums[s + coin][0] = min(sums[s][0] + 1, sums[s + coin][0])
            sums[s + coin][1] += sums[s][1]

if sums[S][0] == float("inf"):
    sums[S][0] = -1
sys.stdout.write("\n".join(map(str, sums[S])))
