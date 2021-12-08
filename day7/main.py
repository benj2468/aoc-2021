from numpy import median, average, floor, ceil

with open('./input') as f:
    vals = list(map(int, f.read().strip().split(',')))

    mem = {0: 0}

    def calc(i: int) -> int:
        if not i in mem:
            mem[i] = i + calc(i - 1)

        return mem[i]

    med = median(vals)
    avg = average(vals)

    res_floor = 0
    for v in vals:
        res_floor += calc(abs(v - floor(avg)))

    res_ceil = 0
    for v in vals:
        res_ceil += calc(abs(v - ceil(avg)))

    print(min(res_ceil, res_floor))