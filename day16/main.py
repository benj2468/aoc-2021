from typing import Any, List

with open('./input') as f:
    data = f.read().strip()
    size = len(data) * 4
    data = bin(int(data, 16))[2:].zfill(size)


class Packet():
    def __init__(self,
                 version,
                 id,
                 length: int,
                 lit: str = None,
                 sub: List[Any] = []) -> None:
        self.length = length
        self.v = int(version, 2)
        self.id = id
        self.lit = lit
        self.sub = sub

    def version_sum(self):
        v = self.v
        for sub in self.sub:
            v += sub.version_sum()
        return v

    def __str__(self) -> str:
        res = f'Top level: length={self.length}; version={self.v}; {self.lit if self.lit else ""}'
        if len(self.sub):
            res += '\n'
            for sub in self.sub:
                res += f'\t{str(sub)}'
        return res + '\n'

    def calc(self, p_id: int):
        if p_id == 0:
            s = 0
            for p in self.sub:
                s += p.lit
            self.lit = s
        elif p_id == 1:
            r = 1
            for p in self.sub:
                r *= p.lit
            self.lit = r
        elif p_id == 2:
            self.lit = min(map(lambda x: x.lit, self.sub))
        elif p_id == 3:
            self.lit = max(map(lambda x: x.lit, self.sub))
        elif p_id == 5:
            self.lit = 1 if self.sub[0].lit > self.sub[1].lit else 0
        elif p_id == 6:
            self.lit = 1 if self.sub[0].lit < self.sub[1].lit else 0
        elif p_id == 7:
            self.lit = 1 if self.sub[0].lit == self.sub[1].lit else 0


def parse_packet(data: str):
    version = data[0:3]
    p_id = int(data[3:6], 2)

    def parse_lit(d: str):
        i = 0
        res = ''
        while True:
            res += d[i + 1:i + 5]
            if d[i] == '0':
                i += 5
                break
            i += 5
        return Packet(version, p_id, i + 6, lit=int(res, 2))

    def parse_op(d: str):
        ty_id = d[0]
        if ty_id == '0':
            # 15 bits that tells number of bits in subpackets
            length = int(d[1:16], 2)
            i = 16
            sub = []
            while i - 16 < length:
                packet = parse_packet(d[i:])
                i += packet.length
                sub.append(packet)

        else:
            # 11 bits that tell the number of subpackets
            length = int(d[1:12], 2)
            sub = []
            i = 12
            for j in range(length):
                packet = parse_packet(d[i:])
                i += packet.length
                sub.append(packet)

        return Packet(version, p_id, i + 6, sub=sub)

    if p_id == 4:
        return parse_lit(data[6:])
    else:
        packet = parse_op(data[6:])
        packet.calc(p_id)
        return packet


packet = parse_packet(data)
print(packet.lit)