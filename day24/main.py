from __future__ import annotations


class Program():
    def __init__(self, file: str) -> None:
        with open(file) as f:
            lines = f.readlines()

        lines = list(map(lambda x: x.split(), lines))

        self.blocks = []

        block = []
        for line in lines:
            if line[0] == 'inp':
                if block:
                    self.blocks.append(block)
                block = []
            block.append(line)
        self.blocks.append(block)

    def solve_block(block, state):
        for line in block:
            command = line[0]
            lhs = line[1]
            if command == 'inp':
                continue
            rhs = int(line[2]) if not line[2].isalpha() else state[line[2]]
            if command == 'add':
                state[lhs] += rhs
            elif command == 'mul':
                state[lhs] *= rhs
            elif command == 'div':
                state[lhs] //= rhs
            elif command == 'mod':
                state[lhs] %= rhs
            elif command == 'eql':
                state[lhs] = int(state[lhs] == rhs)


mem = {}


def recurse(program, block_num, z, part2=False):
    if (block_num, z) in mem:
        return mem[(block_num, z)]
    mem[(block_num, z)] = None
    if z == 0 and block_num == len(program.blocks):
        return ''
    elif block_num == len(program.blocks):
        return None

    r = range(1, 10) if part2 else range(9, 0, -1)
    for i in r:
        state = {
            'x': 0,
            'y': 0,
            'z': z,
            'w': i,
        }

        # Observation drawn from the data that we were give
        x_val = int(program.blocks[block_num][5][2])
        if z % 26 + x_val != i and x_val < 0:
            continue

        Program.solve_block(program.blocks[block_num], state)
        res = recurse(program, block_num + 1, state['z'], part2)

        if res != None:
            mem[(block_num, z)] = str(i) + res
            break
    return mem[(block_num, z)]


print(recurse(Program('./example'), 0, 0))
mem = {}
print(recurse(Program('./example'), 0, 0, part2=True))
