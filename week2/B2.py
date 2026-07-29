import sys

_, *words = sys.stdin.read().split()


def count_chars(word):
    counter = [0] * 26
    for ch in word:
        counter[ord(ch) - 97] += 1
    return tuple(counter)


print(len({count_chars(word) for word in words}))
