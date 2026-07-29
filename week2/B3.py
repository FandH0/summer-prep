import sys


s = sys.stdin.readline()[:-1]
chs = set()
left = 0
m = 0
for right, ch in enumerate(s):
    while ch in chs:
        chs.remove(s[left])
        left += 1
    chs.add(ch)
    m = max(m, right - left + 1)

print(m)
