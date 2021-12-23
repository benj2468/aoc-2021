from copy import deepcopy
from astar_search import astar_search
from AmphipodWorld import AmphipodProblem, Amphipod, State, BLANK_BOARD

problem = AmphipodProblem('./input')
res = astar_search(problem, problem.heuristic)
print(res)