from collections import defaultdict

with open('./input') as f:
    lines = list(map(lambda x: x.strip(), f.readlines()))

    res = 0

    def check_smaller(i, j) -> bool:
        if i + 1 < len(lines) and lines[i + 1][j] <= line[j]:
            return False
        if i - 1 >= 0 and lines[i - 1][j] <= line[j]:
            return False
        if j + 1 < len(line) and lines[i][j + 1] <= line[j]:
            return False
        if j - 1 >= 0 and lines[i][j - 1] <= line[j]:
            return False
        return True

    for i, line in enumerate(lines):
        for j in range(len(line)):
            if check_smaller(i, j):
                res += int(line[j]) + 1

    print(res)

with open('./input') as f:
    lines = list(map(lambda x: x.strip(), f.readlines()))

    visited = dict()

    def bleed(i: int, j: int):
        if lines[i][j] == '9':
            return {}, None
        res = set({(i, j)})
        m = (i, j)
        deltas = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for delta in filter(
                lambda x: len(lines) > x[0] > -1 and len(lines[i]) > x[1] > -1,
                deltas):
            n_i, n_j = delta

            if lines[n_i][n_j] < lines[i][j]:
                if (n_i, n_j) in visited:
                    return res, visited[(n_i, n_j)]
                sub, sub_m = bleed(n_i, n_j)
                if sub_m:
                    m = sub_m
                res = res.union(sub)
        return res, m

    res = defaultdict(lambda: 0)

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i, j) in visited:
                continue

            locations, dest = bleed(i, j)
            res[dest] += len(locations)
            for loc in locations:
                visited[loc] = dest

    res = sorted(res.items(), key=lambda x: x[1], reverse=True)

    r = 1
    for i in range(3):
        r *= res[i][1]
    print(r)
