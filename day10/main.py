from numpy import median

match = {'(': ')', '{': '}', '<': '>', '[': ']'}

points = {')': 3, ']': 57, '}': 1197, '>': 25137}
points2 = {')': 1, ']': 2, '}': 3, '>': 4}


def first_in_line(line):
    queue = []
    for i, c in enumerate(line):
        if c in ['(', '{', '<', '[']:
            queue.append(c)
        else:
            last = queue.pop()
            if c != match[last]:
                return None

    return list(map(lambda x: match[x], reversed(queue)))


res = []
with open('./input') as f:
    lines = list(map(lambda x: x.strip(), f.readlines()))

for line in lines:
    val = first_in_line(line)
    if val and len(val):
        count = 0
        for v in val:
            count *= 5
            count += points2[v]
        res.append(count)
print(median(res))
