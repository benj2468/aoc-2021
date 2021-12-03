gam = 0
eps = 0

with open('./input', 'r') as f:
    lines = 0
    ones = None
    for line in f.readlines():
        lines += 1
        val = line.strip()
        if not ones:
            ones = [0] * len(val)

        for i, b in enumerate(val):
            if b == '1':
                ones[i] += 1

    pow = 1
    for b in reversed(ones):
        if b > lines // 2:
            gam += pow
        else:
            eps += pow

        pow *= 2

print(f"Day 2 Solution: {gam * eps}")

# Part 2
o2 = 0
co2 = 0
with open('./input', 'r') as f:
    candidates = list(map(lambda x: x.strip(), f.readlines()))

    o2_candidates = set(candidates)
    for i in range(len(candidates[0])):
        if len(o2_candidates) == 1:
            break
        ones = set()
        for cand in o2_candidates:
            val = cand[i]
            if val == '1':
                ones.add(cand)

        if len(ones) >= len(o2_candidates) / 2:
            o2_candidates = ones
        else:
            o2_candidates.difference_update(ones)

    co2_candidates = set(candidates)
    for i in range(len(candidates[0])):
        if len(co2_candidates) == 1:
            break
        ones = set()
        for cand in co2_candidates:
            val = cand[i]
            if val == '1':
                ones.add(cand)

        if len(ones) >= len(co2_candidates) / 2:
            co2_candidates.difference_update(ones)
        else:
            co2_candidates = ones

    o2_b = int(o2_candidates.pop(), 2)
    co2_b = int(co2_candidates.pop(), 2)

print(f"Day 2 (part 2) Solution: {o2_b * co2_b}")