class OceanFloor:
    def __init__(self, file: str) -> None:
        east = set()
        south = set()

        with open(file) as f:
            lines = f.readlines()

            self.size = len(lines), len(lines[0]) - 1
            for i, line in enumerate(lines):
                line = line.strip()
                for j, c in enumerate(line):
                    if c == 'v':
                        south.add((i, j))
                    elif c == '>':
                        east.add((i, j))

        self.state = [east, south]

    def execute(self, turn=0, moved=False):
        delta = (1, 0) if turn else (0, 1)
        new = set()
        for y, x in self.state[turn]:
            next = (y + delta[0]) % self.size[0], (x + delta[1]) % self.size[1]
            if next in self.state[turn] or next in self.state[int(not turn)]:
                new.add((y, x))
            else:
                moved = True
                new.add(next)

        self.state[turn] = new

        if not turn:
            return self.execute(1, moved)
        return moved


def part1(file):

    game = OceanFloor(file)

    i = 1
    while game.execute():
        i += 1

    print(f'Part 1: {i}')


part1('./example')
part1('./input')
