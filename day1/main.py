count = 0

with open('./input', 'r') as f:
    prev = float('inf')
    for line in f.readlines():
        val = int(line.strip())
        if val > prev:
            count += 1
        prev = val

print(f"Day 1 (part 1) Solution: {count}")

# Part 2
count = 0
with open('./input', 'r') as f:
    window = []
    for line in f.readlines():
        val = int(line.strip())
        if len(window) == 3:
            s = sum(window)
            window = window[1:]
            window.append(val)
            s2 = sum(window)

            if s2 > s:
                count += 1
        if len(window) < 3:
            window.append(val)

print(f"Day 1 (part 2) Solution: {count}")
