from collections import UserDict, defaultdict
from copy import deepcopy


def find_all(S, sub):
    i = 0
    while i < len(S) - 1:
        found = S.find(sub, i)
        if found >= 0:
            i = found + 1
            yield i
        else:
            break


def solve(ticks):
    word = defaultdict(lambda: 0)
    updates = {}
    first = None
    last = None

    with open('./input') as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))

        first = lines[0][0]
        last = lines[0][-1]
        for i in range(len(lines[0]) - 1):
            word[lines[0][i:i + 2]] += 1

        for line in lines[2:]:
            rule, delta = line.split(' -> ')
            updates[rule] = delta

    for tick in range(ticks):
        deltas = []
        for rule, delta in updates.items():
            if rule in word:
                deltas.append((rule, delta))

        new_word = deepcopy(word)
        for rule, delta in deltas:
            new_word[rule[0] + delta] += word[rule]
            new_word[delta + rule[1]] += word[rule]
            new_word[rule] -= word[rule]
            if new_word[rule] == 0:
                del new_word[rule]
        word = new_word

    freq = defaultdict(lambda: 0.0)
    for a, b in word:
        val = word[a + b]
        freq[a] += (val / 2)
        freq[b] += (val / 2)

    freq[first] += .5
    freq[last] += .5

    freq = freq.values()

    return max(freq) - min(freq)


print(solve(40))
2422444761283