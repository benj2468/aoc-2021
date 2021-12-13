from collections import defaultdict

with open('./input') as f:
    lines = map(lambda x: x.strip(), f.readlines())

    mem = defaultdict(lambda x: 0)
    turns = None
    for line in lines:
        if line == '':
            turns = []
            continue
        if turns == None:
            x, y = list(map(int, line.split(',')))
            mem[(x, y)] = 1
        else:
            turn = line.split(' ')[2]
            axis, val = turn.split('=')
            val = int(val)
            turns.append((axis, val))

for axis, val in turns:
    for (x, y) in list(mem):
        if axis == 'x' and x >= val:
            del mem[(x, y)]
            mem[(val - (x - val), y)] = 1
        if axis == 'y' and y >= val:
            del mem[(x, y)]
            mem[(x, val - (y - val))] = 1

m = 0
n = 0
for (x, y) in mem:
    m = max(x, m)
    n = max(y, n)
paper = []
for i in range(n + 1):
    row = ['.'] * (m + 1)
    paper.append(row)
for x, y in mem:
    paper[y][x] = "#"

for row in paper:
    print(''.join(row))
