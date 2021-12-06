from collections import defaultdict

with open('./input') as f:
    lines = f.readlines()

    m = defaultdict(lambda: 0)

    for i, line in enumerate(lines):
        line = line.strip()
        start, end = line.split(' -> ')
        start = list(map(int, start.split(',')))
        end = list(map(int, end.split(',')))

        if start[0] == end[0]:
            for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                m[(start[0], i)] += 1
        elif start[1] == end[1]:
            for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                m[(i, start[1])] += 1
        else:
            dx = -1 if end[0] < start[0] else 1
            dy = -1 if end[1] < start[1] else 1
            cur = start
            while cur != end:
                m[tuple(cur)] += 1
                cur[0] += dx
                cur[1] += dy
            m[tuple(cur)] += 1

    res = 0
    for v in m.values():
        if v > 1:
            res += 1

    print(f"Day 5 Solution Part 2: {res}")
