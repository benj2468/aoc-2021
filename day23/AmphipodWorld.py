# Benjamin Cape - 21F - CS76
# PA2
# 10.02.10

from __future__ import annotations
from copy import deepcopy
from itertools import count
from typing import Generator, List, Mapping, Set, Tuple

ROOMS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

Action = Tuple[Tuple[int, int], Tuple[int, int]]

INVALID_STOPS = set([(1, i) for i in [3, 5, 7, 9]])

BLANK_BOARD = list(
    map(
        list, """#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########
""".split('\n')))


class Amphipod():
    def __init__(self, ty: str, location: Tuple[int, int]) -> None:
        self.ty = ty
        self.loc = location

    def in_hallway(self) -> bool:
        return self.loc[0] == 1

    def in_correct_room(self) -> bool:
        return ROOMS[self.ty] == self.loc[1]


class State:
    def __init__(self, amphipods: List[Amphipod]) -> None:
        self.amphipods: Mapping[Tuple[int, int], Amphipod] = {}
        for pod in amphipods:
            self.amphipods[pod.loc] = pod

    def hashed(self):
        return str(
            sorted(map(lambda x: (x.loc, x.ty),
                       self.amphipods.values()))).__hash__()

    def __str__(state: State):
        board = deepcopy(BLANK_BOARD)
        for (i, j) in state.amphipods:
            board[i][j] = state.amphipods[(i, j)].ty

        fixed = (''.join(x) for x in board)

        res = '\n'.join(fixed)
        return res


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def distance_to(pod, b):
    if pod.loc[1] != b[1]:
        return (pod.loc[0] - 1) + abs(pod.loc[1] - b[1]) + (b[0] - 1)
    else:
        return abs(pod.loc[0] - b[0])


class AmphipodProblem:
    def __init__(self, file):
        with open('./input') as f:
            board = list(map(list, f.readlines()))

            pods = []

            i = 1
            while i < len(board) - 1:
                for j in range(len(board[i])):
                    if board[i][j] in ROOMS:
                        pods.append(Amphipod(board[i][j], (i, j)))
                i += 1
        self.VALID_LOCATIONS = set([(y, x) for x in [3, 5, 7, 9]
                                    for y in range(2, i)] +
                                   [(1, x) for x in range(1, 12)])

        self.size = i

        self.start_state = State(pods)

        def heuristic(state: State) -> int:
            s = 0
            for pod in state.amphipods.values():
                s += 2 * COST[pod.ty] * distance_to(pod, (
                    (self.size + 1) / 2, ROOMS[pod.ty]))
            return s

        self.heuristic = lambda x: 0

    def transition(self, state: State, action: Action) -> State:
        new = deepcopy(state)
        cost = COST[state.amphipods[action[0]].ty] * action[2]
        new.amphipods[action[1]] = new.amphipods[action[0]]
        new.amphipods[action[1]].loc = action[1]
        del new.amphipods[action[0]]
        return cost, new

    def goal_test(self, state: State) -> bool:
        return all(map(lambda x: x.in_correct_room(),
                       state.amphipods.values()))

    def get_successors(self, state: State) -> Generator[Tuple[int, State]]:
        for action in self.legal_actions(state):
            yield self.transition(state, action)

    def legal_actions(self, state: State) -> Generator[Action]:
        def delta(a, b):
            return a[0] + b[0], a[1] + b[1]

        def valid_room(ty: str):
            room = ROOMS[ty]
            c = 0
            for i in range(2, self.size):
                if (i, room) in state.amphipods:
                    if state.amphipods[(i, room)].ty != ty:
                        return False
                    else:
                        c += 1
            return c < self.size - 2

        def valid_from_room(pod: Amphipod, start: Tuple[int, int], moves: int,
                            visited: Set[Tuple[int, int]]):
            visited.add(start)
            options = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for op in options:
                dest = delta(start, op)
                if dest in visited or dest in state.amphipods or dest not in self.VALID_LOCATIONS:
                    continue
                if dest[1] in [3, 5, 7, 9]:
                    if dest[0] in range(2, self.size) and ROOMS[
                            pod.ty] == dest[1] and valid_room(pod.ty):
                        yield pod.loc, dest, moves
                else:
                    yield pod.loc, dest, moves
                yield from valid_from_room(pod, dest, moves + 1, visited)

        def path_clear(pod: Amphipod) -> Tuple[int, int]:
            loc = pod.loc

            i = loc[0]
            j = loc[1]
            while ((i, j) not in state.amphipods or
                   (i, j) == loc) and (i, j) in self.VALID_LOCATIONS:
                if (i, j) == (1, loc[1]):
                    if j < ROOMS[pod.ty]:
                        j += 1
                    else:
                        j -= 1
                elif j == ROOMS[pod.ty]:
                    i += 1
                elif j == pod.loc[1]:
                    i -= 1
                else:
                    if j < ROOMS[pod.ty]:
                        j += 1
                    else:
                        j -= 1

            if j == ROOMS[pod.ty] and i > 2 and (i - 1, j) != loc:
                return (i - 1, j)
            else:
                return None

        moves = []
        for loc in state.amphipods:
            pod = state.amphipods[loc]
            if valid_room(pod.ty):
                dest = path_clear(pod)
                if dest:
                    return [(pod.loc, dest, distance_to(pod, dest))]
            if not pod.in_hallway():
                moves += list(valid_from_room(pod, loc, 1, set()))
        return moves
