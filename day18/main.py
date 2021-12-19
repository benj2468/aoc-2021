from math import floor, ceil
from copy import deepcopy


def split(s):
    i = 1
    stack = 0
    while True:
        if s[i] == '[':
            stack += 1
        if s[i] == ']':
            stack -= 1
        if s[i] == ',' and stack == 0:
            return i
        i += 1


class BinaryTree:
    def __init__(self, left=None, right=None, reg: int = None) -> None:
        self.left = left
        self.right = right
        self.reg = reg

    def __add__(self, other):
        return BinaryTree(self, other)

    def __eq__(self, __o: object) -> bool:
        r = self.reg == __o.reg
        if self.left:
            r = r and self.left == __o.left

        if self.right:
            r = r and self.right == __o.right

        return r

    def reduce(self):
        while self.explode(0) or self.split():
            pass

    def explode(self, depth):
        if depth >= 4 and self.left and self.left.reg != None and self.right and self.right.reg != None:
            res = [self.left.reg, self.right.reg]
            self.left = None
            self.right = None
            self.reg = 0
            return res

        expl = self.left.explode(depth + 1) if self.left else None

        if expl and expl[1] and self.right:
            cur = self.right
            while cur.left:
                cur = cur.left

            cur.reg += expl[1]
            expl[1] = None

        if not expl:
            expl = self.right.explode(depth + 1) if self.right else None

            if expl and expl[0] and self.left:
                cur = self.left
                while cur.right:
                    cur = cur.right
                cur.reg += expl[0]
                expl[0] = None

        return expl

    def split(self):
        if self.reg and self.reg >= 10:
            self.left = BinaryTree(reg=floor(self.reg / 2))
            self.right = BinaryTree(reg=ceil(self.reg / 2))
            self.reg = None
            return True

        return (self.left and self.left.split()) or (self.right
                                                     and self.right.split())

    def parse(s: str):
        s = s.strip()
        if len(s) == 1:
            return BinaryTree(reg=int(s))

        j = split(s)
        left = BinaryTree.parse(s[1:j])
        right = BinaryTree.parse(s[j + 1:-1])

        return BinaryTree(left, right)

    def __str__(self) -> str:
        if self.reg != None:
            return f'{self.reg}'
        else:
            return f"[{self.left}, {self.right}]"

    def __abs__(self):
        r = self.reg or 0
        if self.left:
            r += (3 * abs(self.left))
        if self.right:
            r += (2 * abs(self.right))
        return r


with open('./input') as f:
    lines = list(map(BinaryTree.parse, f.readlines()))

res = 0
for l1 in lines:
    for l2 in lines:

        if l1 == l2:
            continue

        s = deepcopy(l1) + deepcopy(l2)
        s.reduce()

        res = max(abs(s), res)
print(res)