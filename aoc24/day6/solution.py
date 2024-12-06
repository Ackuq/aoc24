from copy import deepcopy

Coord = tuple[int, int]
CoordWithDirection = tuple[int, int, int, int]
Grid = list[list[str]]


def parse_input(lines: list[str]) -> Grid:
    return [list(line.strip()) for line in lines]


def find_start_position(grid: Grid) -> Coord:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "^":
                return x, y
    raise ValueError("No start position found")


def is_inside(grid: Grid, x: int, y: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def next_step(grid: Grid, x: int, y: int, dx: int, dy: int) -> CoordWithDirection:
    next_x, next_y = x + dx, y + dy
    while is_inside(grid, x + dx, y + dy) and grid[y + dy][x + dx] == "#":
        dx, dy = -dy, dx
        next_x, next_y = x + dx, y + dy

    return next_x, next_y, dx, dy


def get_visisted(grid: Grid) -> set[Coord]:
    x, y = find_start_position(grid)
    dx, dy = (0, -1)
    visited: set[Coord] = set()

    while is_inside(grid, x, y):
        visited.add((x, y))
        x, y, dx, dy = next_step(grid, x, y, dx, dy)

    return visited


def part1(grid: Grid) -> None:
    visited = get_visisted(grid)
    print("Part 1:", len(visited))


def check_if_loops(grid: Grid, start: Coord) -> bool:
    visited: set[CoordWithDirection] = set()
    x, y = start
    dx, dy = (0, -1)

    while is_inside(grid, x, y):
        if (x, y, dx, dy) in visited:
            return True
        visited.add((x, y, dx, dy))
        x, y, dx, dy = next_step(grid, x, y, dx, dy)

    return False


def part2(grid: Grid) -> None:
    start = find_start_position(grid)
    path = get_visisted(grid)
    path.remove(start)
    possible_obstacle: set[Coord] = set()

    for x, y in path:
        new_grid = deepcopy(grid)
        new_grid[y][x] = "#"
        if check_if_loops(new_grid, start):
            possible_obstacle.add((x, y))

    print("Part 2:", len(possible_obstacle))


def main(lines: list[str]) -> None:
    grid = parse_input(lines)
    part1(grid)
    part2(grid)
