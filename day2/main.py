position = [0, 0]

with open('./input', 'r') as f:
    for line in f.readlines():
        val = line.strip()
        op, dist = val.split(' ')

        if op == 'forward':
            position[0] += int(dist)
        else:
            if op == 'up':
                position[1] -= int(dist)
            else:
                position[1] += int(dist)

print(f"Day 2 Solution: {position[0] * position[1]}")

# Part 2
position = [0, 0]
aim = 0

with open('./input', 'r') as f:
    for line in f.readlines():
        val = line.strip()
        op, dist = val.split(' ')
        dist = int(dist)

        if op == 'forward':
            position[0] += dist
            position[1] += (aim * dist)
        else:
            if op == 'up':
                aim -= dist
            else:
                aim += dist

print(f"Day 2 (part 2) Solution: {position[0] * position[1]}")