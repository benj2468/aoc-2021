from typing import List, Pattern
from copy import deepcopy


class SignalPattern():
    def __init__(self, segments=None) -> None:
        self.segments = segments if segments else {
            c: set(range(7))
            for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        }

    def deduce(wires: List[str]):
        self = SignalPattern()
        for word in wires:
            self.update(word)

        self.segments = SignalPattern.find_solution(self.segments, wires)

        return self

    def find_solution(segments, wires):
        needs_deduction = False
        for k in segments:
            if len(segments[k]) == 0:
                return None
            if len(segments[k]) > 1:
                needs_deduction = True
                seg = deepcopy(segments)
                for option in seg[k]:
                    seg[k] = set({option})
                    for r in seg:
                        if r == k:
                            continue
                        seg[r].difference_update(set({option}))
                    sub = SignalPattern.find_solution(seg, wires)
                    if sub:
                        return sub
        if not needs_deduction:
            available = set(range(10))
            for word in wires:
                sol = SignalPattern(segments).solve(word)
                if not sol in available:
                    return None
                available.remove(sol)
            return segments

    def update(self, s: str):
        if len(s) == 2:
            options = set({2, 5})
            for c in s:
                self.segments[c].intersection_update(options)
            for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                if c not in s:
                    self.segments[c].difference_update(options)
        if len(s) == 3:
            options = set({0, 2, 5})
            for c in s:
                self.segments[c].intersection_update(options)
            for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                if c not in s:
                    self.segments[c].difference_update(options)
        if len(s) == 4:
            options = set({1, 2, 3, 5})
            for c in s:
                self.segments[c].intersection_update(options)
            for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                if c not in s:
                    self.segments[c].difference_update(options)

    def solve(self, s: str):
        solutions = {
            "0, 1, 2, 4, 5, 6": 0,
            "2, 5": 1,
            "0, 2, 3, 4, 6": 2,
            "0, 2, 3, 5, 6": 3,
            "1, 2, 3, 5": 4,
            "0, 1, 3, 5, 6": 5,
            "0, 1, 3, 4, 5, 6": 6,
            "0, 2, 5": 7,
            "0, 1, 2, 3, 4, 5, 6": 8,
            "0, 1, 2, 3, 5, 6": 9,
        }

        val = []
        for c in s:
            val += str(list(self.segments[c])[0])
        val = ', '.join(sorted(val))

        if not val in solutions:
            return None

        return solutions[val]


with open('./input') as f:
    res = 0
    for line in f.readlines():
        pre, output = line.strip().split('|')

        pat = SignalPattern.deduce(pre.strip().split(' '))

        solution = ''
        for word in output.strip().split(' '):
            solution += str(pat.solve(word))

        res += int(solution)

    print('Solution Day 8 (Part 1): ', res)