import sys

s = sys.stdin.read().rstrip('\n')

pairs = {")": "(", "]": "[", "}": "{"}
opened_brackets = []

for bracket in s:
    if bracket not in pairs:
        opened_brackets.append(bracket)
    elif opened_brackets and opened_brackets[-1] == pairs[bracket]:
        opened_brackets.pop()
    else:
        print("NO")
        break
else:
    print("YES" if len(opened_brackets) == 0 else "NO")
