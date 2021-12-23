class DeterministicDice():
    def __init__(self, sides: int) -> None:
        self.sides = sides

    def roll(self, n: int) -> int:
        return (n % self.sides) + 1


class Game():
    def __init__(self, dice=None) -> None:
        self.rolls = 0
        self.dice = dice

    def roll(self, times=3):
        for _i in range(times):
            roll = self.dice.roll(self.rolls)
            self.rolls += 1
            yield roll

    def simulate(self, p1: int, p2: int):
        player1 = [p1, 0]
        player2 = [p2, 0]
        turn = 0
        while True:
            player = player1 if not turn else player2
            for roll in self.roll():
                loc = player[0] + roll
                if loc % 10 == 0:
                    loc = 10
                else:
                    loc = loc % 10
                player[0] = loc
            player[1] += player[0]
            if player[1] >= 1000:
                break
            turn = (turn + 1) % 2

        return self.rolls * min(player1[1], player2[1])


example = Game(DeterministicDice(100)).simulate(4, 8)
assert (example == 739785)

my_data = Game(DeterministicDice(100)).simulate(1, 2)
print(my_data)


def simulatePart2(p1: int, p2: int):
    mem = {}

    def update_loc(loc, roll):
        l = loc + roll
        if l % 10 == 0:
            l = 10
        else:
            l = l % 10
        return l

    def helper(loc1: int, loc2: int, s1: int, s2: int, turn: bool, r_num: int):
        if s1 >= 21:
            return (1, 0)
        if s2 >= 21:
            return (0, 1)

        if (loc1, loc2, s1, s2, turn, r_num) in mem:
            return mem[(loc1, loc2, s1, s2, turn, r_num)]

        res = [0, 0]
        for roll in range(1, 4):
            if turn:
                loc = update_loc(loc2, roll)
                if r_num < 2:
                    a, b = helper(loc1, loc, s1, s2, turn, r_num + 1)
                if r_num == 2:
                    a, b = helper(loc1, loc, s1, s2 + loc, not turn, 0)
            else:
                loc = update_loc(loc1, roll)
                if r_num < 2:
                    a, b = helper(loc, loc2, s1, s2, turn, r_num + 1)
                if r_num == 2:
                    a, b = helper(loc, loc2, s1 + loc, s2, not turn, 0)
            res[0] += a
            res[1] += b

        mem[(loc1, loc2, s1, s2, turn, r_num)] = res
        return res

    return helper(p1, p2, 0, 0, False, 0)


print(max(simulatePart2(1, 2)))
