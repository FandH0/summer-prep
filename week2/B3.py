import sys


s = sys.stdin.readline().removesuffix('\n')
window = set()
left = 0
max_len = 0
for right, ch in enumerate(s):
    while ch in window:
        window.remove(s[left])
        left += 1
    window.add(ch)
    max_len = max(max_len, right - left + 1)

print(max_len)
