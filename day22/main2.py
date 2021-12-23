from __future__ import annotations
from collections import defaultdict
from typing import Any, Generator, List, Mapping, Set, Tuple
import regex as re
from pprint import pprint
from copy import deepcopy

from regex.regex import split


def into_parts(i1, i2):
    a = set(range(*i1))
    b = set(range(*i2))

    overlap = a.intersection(b)
    overlap = (min(overlap), max(overlap) + 1)

    if b.issubset(a):
        a_parts = [(min(a), overlap[0]),
                   (overlap[1], max(a) + 1)] if len(a) else []
    else:
        a_parts = a.difference(b)
        a_parts = [(min(a_parts), max(a_parts) + 1)] if len(a_parts) else []

    a_parts = list(filter(lambda x: x[0] < x[1], a_parts))

    return a_parts, overlap


def read_input(file: str) -> List[str]:
    with open(file) as f:
        for line in f.readlines():
            yield line.strip()


def do_overlap(i1, i2) -> bool:
    s1, e1 = i1
    s2, e2 = i2

    return s2 < e1 and e2 > s1


def parse_line(line: str):
    def clean(x):
        return x[0], x[1] + 1

    data = re.match(
        r'(.*) x=(-{0,1}\d+\.\.-{0,1}\d+),y=(-{0,1}\d+\.\.-{0,1}\d+),z=(-{0,1}\d+\.\.-{0,1}\d+)',
        line).groups(0)

    command = True if data[0] == 'on' else False

    return command, [
        clean(tuple(map(int, data[i].split('..')))) for i in range(1, 4)
    ]


class Cube():
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def intersects(self, o: Cube) -> bool:
        return do_overlap(self.x, o.x) and do_overlap(
            self.y, o.y) and do_overlap(self.z, o.z)

    def explode(self, o: Cube) -> bool:
        x_parts, x_overlap = into_parts(self.x, o.x)
        y_parts, y_overlap = into_parts(self.y, o.y)
        z_parts, z_overlap = into_parts(self.z, o.z)
        for x in x_parts:
            yield Cube(x, y_overlap, z_overlap)
            for y in y_parts:
                yield Cube(x, y, z_overlap)
                for z in z_parts:
                    yield Cube(x, y, z)
        for y in y_parts:
            yield Cube(x_overlap, y, z_overlap)
            for z in z_parts:
                yield Cube(x_overlap, y, z)
        for x in x_parts:
            for z in z_parts:
                yield Cube(x, y_overlap, z)
        for z in z_parts:
            yield Cube(x_overlap, y_overlap, z)

    def size(self) -> int:
        return (abs(self.x[0] - self.x[1])) * (abs(self.y[0] - self.y[1])) * (
            abs(self.z[0] - self.z[1]))

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))


def solution(file):
    cubes = []
    for line in read_input(file):
        command, (x, y, z) = parse_line(line)

        new = Cube(x, y, z)

        for cube in list(cubes):
            if cube.intersects(new):
                cubes.remove(cube)
                for c in cube.explode(new):
                    cubes.append(c)

        if command:
            cubes.append(new)

        s = 0
        for cube in cubes:
            s += cube.size()
    return s


print(solution('./input'))