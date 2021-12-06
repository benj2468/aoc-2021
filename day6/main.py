with open('./input') as f:
    lines = f.read().strip()

    fish = list(map(int, lines.split(',')))

    res = 0
    mem = {}

    def live(i: int, length: int) -> int:
        if length == 0:
            return 1
        if not (i, length) in mem:
            res = 0
            if i == 0:
                res += live(6, length - 1)
                res += live(8, length - 1)
            else:
                res += live(i - 1, length - 1)

            mem[(i, length)] = res
        return mem[(i, length)]

    for f in fish:
        if not f in mem:
            mem[(f, 256)] = live(f, 256)
        res += mem[(f, 256)]

    print(res)