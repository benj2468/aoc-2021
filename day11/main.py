matrix = []

with open('./input') as f:
    for line in f.readlines():
        l = []
        for c in line.strip():
            l.append(int(c))
        matrix.append(l)

steps = 100
res = 0
k = 0
while True:
    too_large = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] += 1
            if matrix[i][j] > 9:
                too_large.append((i, j))

    flashed = set()

    while len(too_large):
        i, j = too_large.pop()
        if (i, j) in flashed:
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0 or i + dx >= len(
                        matrix) or i + dx < 0 or j + dy >= len(
                            matrix[i]) or j + dy < 0:
                    continue
                matrix[i + dx][j + dy] += 1
                if matrix[i + dx][j + dy] > 9:
                    too_large.append((i + dx, j + dy))
        flashed.add((i, j))

    if len(flashed) == 100:
        break

    for (i, j) in flashed:
        matrix[i][j] = 0
    res += len(flashed)
    k += 1

print(f"Part 2: {k + 1}")
