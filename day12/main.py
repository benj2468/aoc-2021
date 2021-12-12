from collections import defaultdict
from typing import Any, List

graph = defaultdict(lambda: set())

with open('./input') as f:
    lines = list(map(lambda x: x.strip(), f.readlines()))
    for line in lines:
        v, u = line.split('-')
        graph[v].add(u)
        graph[u].add(v)


def count_occ(l: List[Any], e: Any) -> int:
    r = 0
    for c in l:
        if c == e:
            r += 1
    return r


def find_all_paths(current, path, visited_twice):
    if current == 'end':
        return [path + [current]]

    paths = []
    for n in graph[current]:
        visited_twice_sub = visited_twice
        if n == 'start' or (n.islower() and visited_twice and n in path):
            continue
        elif n.islower() and count_occ(path, n) == 1:
            visited_twice_sub = True

        sub = find_all_paths(n, path + [current], visited_twice_sub)
        if sub:
            paths.extend(sub)

    return paths


print(len(find_all_paths('start', [], False)))
