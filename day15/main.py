from copy import deepcopy
from heapq import heappush, heappop

with open('./input') as f:
    board = list(map(lambda x: list(map(int, x.strip())), f.readlines()))

    def wrap(i: int) -> int:
        if i >= 10:
            i += 1
        return i % 10

    additions = []

    for i in range(4):
        for j, line in enumerate(board):
            if j > len(additions) - 1:
                additions.append([])
            additions[j] += list(map(lambda x: wrap(x + 1 + i), line))

    for i, addition in enumerate(additions):
        board[i] += addition

    additional_lines = []
    for i in range(4):
        for line in board:
            additional_lines.append(list(map(lambda x: wrap(x + 1 + i), line)))

    board.extend(additional_lines)

start = (0, 0)
end = (len(board) - 1, len(board) - 1)

q = [(0, start)]
visited = {}

visited[(0, 0)] = 0

while len(q):
    cur_s, (x, y) = heappop(q)

    if visited[(x, y)] < cur_s:
        continue

    if (x, y) == end:
        print(cur_s)
        break

    deltas = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for n_i, n_j in deltas:
        if n_i < 0 or n_i == len(board) or n_j < 0 or n_j == len(board):
            continue

        if not (n_i, n_j) in visited or visited[
            (n_i, n_j)] > cur_s + board[n_j][n_i]:
            visited[(n_i, n_j)] = cur_s + board[n_j][n_i]

            heappush(q, (cur_s + board[n_j][n_i], (n_i, n_j)))
