class Board():
    def __init__(self) -> None:
        self.lines = []

    def add_line(self, line: str):
        new_line = []
        for i in line.split(' '):
            i = i.strip()
            if len(i):
                new_line.append(int(i.strip()))
        if len(new_line):
            self.lines.append(new_line)

    def mark(self, val: int):
        unmarked = 0
        for line in self.lines:
            for i, v in enumerate(line):
                if v == val:
                    line[i] = -v
                elif v > 0:
                    unmarked += v

        for line in self.lines:
            line_win = True
            for i, v in enumerate(line):
                if v > 0:
                    line_win = False

            if line_win:
                return True, unmarked

        for i in range(len(self.lines[0])):
            col_win = True
            for line in self.lines:
                if line[i] > 0:
                    col_win = False
            if col_win:
                return True, unmarked

        return False, unmarked

    def __str__(self) -> str:
        return str(self.lines)


class BingoSystem():
    def __init__(self, file_name: str) -> None:
        self.boards = []
        self.draws = []

        with open(file_name) as f:
            lines = f.readlines()

            self.draws = list(map(int, lines[0].strip().split(',')))

            board = Board()
            for line in lines[3:]:
                if line == '\n':
                    self.boards.append(board)
                    board = Board()
                else:
                    board.add_line(line.strip())

            self.boards.append(board)

    def find(self) -> int:
        i = 0
        while len(self.boards) >= 1:
            draw = self.draws[i]
            for board in list(self.boards):
                res, unmarked = board.mark(draw)
                if res:
                    self.boards.remove(board)
            i += 1
        return self.draws[i - 1] * unmarked


score = BingoSystem('./input').find()
print(score)