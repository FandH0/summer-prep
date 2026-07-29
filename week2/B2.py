import sys

_, *words = sys.stdin.read().split()


def count_chars(s):
    counter = [0] * 26
    for i in s:
        counter[ord(i) - 97] += 1
    return tuple(counter)


groups = set()
answer = 0
for word in words:
    key = count_chars(word)
    if key in groups:
        pass
    else:
        answer += 1
        groups.add(key)

print(answer)
