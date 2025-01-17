from time import perf_counter_ns
from typing import Iterable, Optional
from string import ascii_lowercase
from dataclasses import dataclass

time = perf_counter_ns()

START, END = -1, 26

@dataclass
class Tile:
    height: int
    visited: bool = False
    dist: int = 0

def tile_from_char(c: str) -> Tile:
    try:
        return Tile(ascii_lowercase.index(c))
    except ValueError as e:
        match c:
            case "S":
                return Tile(START)
            case "E":
                return Tile(END)
        raise e

def parse_tiles(lines: Iterable[str]) -> list[list[Tile]]:
    return [[tile_from_char(c) for c in line] for line in lines]

with open('input') as input_file:
    tiles = parse_tiles(map(lambda line: line.strip(), input_file))

    type Probe = tuple[int, int]
    probes: list[Probe] = []
    new_probes: list[Probe] = []
    for i, row in enumerate(tiles):
        for j, tile in enumerate(row):
            if tile.height == START:
                probes.append((i, j))

    offsets: list[Probe] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result: Optional[int] = None
    while result is None:
        for probe in probes:
            tile = tiles[probe[0]][probe[1]]

            for offset in offsets:
                i, j = probe[0] + offset[0], probe[1] + offset[1]

                if 0 <= i < len(tiles) and 0 <= j < len(tiles[0]):
                    neighbor = tiles[i][j]

                    if not neighbor.visited and neighbor.height <= tile.height + 1:
                        neighbor.visited = True
                        neighbor.dist = tile.dist + 1
                        new_probes.append((i, j))

                        if neighbor.height == END:
                            if result is not None:
                                result = min(result, neighbor.dist)
                            else:
                                result = neighbor.dist

        probes, new_probes = new_probes, probes
        new_probes.clear()

    print(f'from S to E: {result}')

print(f'elapsed: {(perf_counter_ns() - time) / 1_000_000} ms')
