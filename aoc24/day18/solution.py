max = 70
# max = 6

num_bytes = 1024
# num_bytes = 12

Coord = tuple[int, int]
Grid = list[Coord]


def parse_input(lines: list[str]) -> Grid:
    grid = list[Coord]()

    for line in lines:
        x, y = line.strip().split(",")
        grid.append((int(x), int(y)))

    return grid


directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def bfs(blocks: set[Coord]) -> int | None:
    queue = [((0, 0), 0)]
    visited = set[Coord]()

    while queue:
        coord, steps = queue.pop(0)

        if coord == (max, max):
            return steps

        if coord in visited:
            continue

        visited.add(coord)

        x, y = coord
        for dx, dy in directions:
            new_x, new_y = (x + dx, y + dy)
            new_pos = (new_x, new_y)
            if (
                new_x < 0
                or new_y < 0
                or new_x > max
                or new_y > max
                or new_pos in visited
                or new_pos in blocks
            ):
                continue
            queue.append((new_pos, steps + 1))

    return None


def part1(blocks: Grid) -> None:
    shortest_path = bfs(set(blocks[:num_bytes]))
    assert shortest_path

    print("Part 1:", shortest_path)


def part2(blocks: Grid) -> None:
    start = len(blocks) - 1
    while bfs(set(blocks[:start])) is None:
        start -= 1

    print("Part 2:", f"{blocks[start][0]},{blocks[start][1]}")


def main(lines: list[str]) -> None:
    grid = parse_input(lines)
    part1(grid)
    part2(grid)
