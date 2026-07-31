import sys

s = sys.stdin.read()

pairs = {")": "(", "]" :"[", "}": "{"}
opened_brackets = []

for bracket in s:
    if bracket in ("(", "[", "{"):
        opened_brackets.append(bracket)
    elif len(opened_brackets) != 0 and opened_brackets[-1] == pairs[bracket]:
        del opened_brackets[-1]
    else:
        print("NO")
        break
else:
    print("YES" if len(opened_brackets) == 0 else "NO")
