from copy import deepcopy

Coord = tuple[int, int]
Grid = list[list[str]]


def parse_input(lines: list[str]) -> Grid:
    return [list(line.strip()) for line in lines]


def find_start_position(grid: Grid) -> Coord:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "^":
                return x, y
    raise ValueError("No start position found")


def part1(grid: Grid) -> None:
    x, y = find_start_position(grid)
    dx, dy = (0, -1)

    visited: set[Coord] = set()

    try:
        while True:
            if grid[y + dy][x + dx] == "#":
                dx, dy = -dy, dx
            x, y = x + dx, y + dy
            visited.add((x, y))
    except IndexError:
        pass

    print("Part 1:", len(visited))


CoordWithDirection = tuple[int, int, int, int]


def check_if_loops(grid: Grid, x: int, y: int, dx: int, dy: int) -> bool:
    visited: set[CoordWithDirection] = set()

    try:
        while True:
            if grid[y + dy][x + dx] == "#":
                dx, dy = -dy, dx

            x, y = x + dx, y + dy

            if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
                return False

            if (x, y, dx, dy) in visited:
                return True

            visited.add((x, y, dx, dy))
    except IndexError:
        return False


def part2(grid: Grid) -> None:
    x, y = find_start_position(grid)
    dx = 0
    dy = -1

    visited: set[CoordWithDirection] = set()
    possible_obstacle: set[Coord] = set()

    try:
        while True:
            if grid[y + dy][x + dx] == "#":
                dx, dy = -dy, dx
            else:
                if (x + dx, y + dy) not in possible_obstacle:
                    dx2, dy2 = -dy, dx
                    new_grid = deepcopy(grid)
                    new_grid[y + dy][x + dx] = "#"
                    loops = check_if_loops(new_grid, x, y, dx2, dy2)
                    if loops:
                        possible_obstacle.add((x + dx, y + dy))

            x, y = x + dx, y + dy

            visited.add((x, y, dx, dy))
    except IndexError:
        pass

    print("Part 2:", len(possible_obstacle))


def main(lines: list[str]) -> None:
    grid = parse_input(lines)
    part1(grid)
    part2(grid)
