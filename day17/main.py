import regex as re
from copy import deepcopy

with open('./input') as f:
    input = f.read().strip()

    data = re.match(
        r'target area: x=(-{0,1}\d+\.\.-{0,1}\d+), y=(-{0,1}\d+\.\.-{0,1}\d+)',
        input).groups(0)

    x_zone = tuple(map(int, data[0].split('..')))
    y_zone = tuple(map(int, data[1].split('..')))

vel = [7, 2]


def make_moves(vel):
    def is_valid(position):
        return position[0] <= max(x_zone) and position[1] >= min(y_zone)

    position = [0, 0]
    valid = False
    maxi = 0
    while True:
        if x_zone[0] <= position[0] <= x_zone[1] and y_zone[0] <= position[
                1] <= y_zone[1]:
            valid = True
        new_pos = deepcopy(position)
        new_pos[0] += vel[0]
        new_pos[1] += vel[1]

        drag = 0 if vel[0] == 0 else -(vel[0] // abs(vel[0]))

        vel[0] += drag
        vel[1] -= 1

        if is_valid(new_pos):
            maxi = max(maxi, new_pos[1])
            position = new_pos
        else:
            break

    if valid:
        return maxi
    return None


maxi = 0
all = set()
for x_vel in range(1, max(x_zone) + 1):
    for y_vel in range(min(y_zone), 100):
        val = make_moves([x_vel, y_vel])
        if val != None:
            all.add((x_vel, y_vel))
            maxi = max(maxi, make_moves([x_vel, y_vel]))

print(len(all))
