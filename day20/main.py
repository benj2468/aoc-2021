from __future__ import annotations
# T = 0:
# . . . . . . . . .
# . . . . . . . . .
# . . # . . . . . .
# . . . # . # . . .
# . . . . # . . . .
# . . # . . # # . .
# . . . . . . . . .
# . . . . . . . . .

# # T = 1:
# # # # # # # # # #
# # . . . . . . . #
# # . # . . . . . #
# # . . # . # . . #
# # . . . # . . . #
# # . # . . # # . #
# # . . . . . . . #
# # # # # # # # # #

# T = 2
# # # # # # # # # # #
# # # # # # # # # # #
# # . . . . . . . # #
# # . # . . . . . # #
# # . . # . # . . # #
# # . . . # . . . # #
# # . # . . # # . # #
# # . . . . . . . # #
# # # # # # # # # # #
# # # # # # # # # # #

with open('./input') as f:
    lines = list(map(lambda x: list(x.strip()), f.readlines()))
    algorithm = lines[0]
    input = lines[2:]


def enhance_image(algorithm, image, background):
    def calculate(enhanced, x, y):
        res = ''
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if j < 0 or j >= len(enhanced) or i < 0 or i >= len(
                        enhanced[j]):
                    val = background
                else:
                    val = enhanced[j][i]
                res += '0' if val == '.' else '1'
        return algorithm[int(res, 2)]

    enhanced = []

    for i, line in enumerate(image):
        if i == 0:
            enhanced.append([background] * (len(line) + 2))
        enhanced.append([background] + line + [background])
        if i == len(image) - 1:
            enhanced.append([background] * (len(line) + 2))

    updates = []
    for y in range(len(enhanced)):
        for x in range(len(enhanced[y])):
            updates.append(((x, y), calculate(enhanced, x, y)))

    ones = 0
    for (x, y), val in updates:
        enhanced[y][x] = val
        if val == '#':
            ones += 1

    if algorithm[0] == '#' and algorithm[511] == '.':
        background = '#' if background == '.' else '.'

    return enhanced, ones, background


image = input
background = '.'
for i in range(50):
    image, ones, background = enhance_image(algorithm, image, background)

    print(i, ones)