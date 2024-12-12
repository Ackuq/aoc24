Coord = tuple[int, int]
Grid = dict[Coord, str]


def parse_input(lines: list[str]) -> Grid:
    return {
        (x, y): c for y, line in enumerate(lines) for x, c in enumerate(line.strip())
    }


directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def get_regions(grid: Grid) -> dict[Coord, set[Coord]]:
    visited = set[Coord]()
    regions: dict[Coord, set[Coord]] = {}

    for pos in grid:
        if pos in visited:
            continue
        visited.add(pos)

        queue = [pos]
        region = set[Coord]([pos])
        while queue:
            x, y = queue.pop(0)
            for dx, dy in directions:
                new_pos = (x + dx, y + dy)
                if (
                    new_pos in grid
                    and new_pos not in region
                    and grid[new_pos] == grid[pos]
                ):
                    visited.add(new_pos)
                    queue.append(new_pos)
                    region.add(new_pos)

        regions[pos] = region

    return regions


CoordWithOrientation = tuple[Coord, Coord]


def get_perimeter(region: set[Coord]) -> set[CoordWithOrientation]:
    return set(
        ((x + dx, y + dy), (dx, dy))
        for x, y in region
        for dx, dy in directions
        if (x + dx, y + dy) not in region
    )


def part1(lines: list[str]) -> None:
    grid = parse_input(lines)
    regions = get_regions(grid)
    sum = 0
    for region in regions.values():
        area = len(region)
        perimiter = len(get_perimeter(region))
        sum += area * perimiter

    print("Part 1:", sum)


def get_sides(perimiter: set[CoordWithOrientation]) -> int:
    side_starts = set[CoordWithOrientation]()
    visited = set[CoordWithOrientation]()
    for cell in perimiter:
        if cell in visited:
            continue

        visited.add(cell)
        side_starts.add(cell)

        queue = [cell]

        while queue:
            pos, orientation = queue.pop(0)
            for dx, dy in directions:
                new_cell = ((pos[0] + dx, pos[1] + dy), orientation)
                if new_cell in perimiter and new_cell not in visited:
                    queue.append(new_cell)
                    visited.add(new_cell)

    return len(side_starts)


def part2(lines: list[str]) -> None:
    grid = parse_input(lines)
    regions = get_regions(grid)
    sum = 0
    for region in regions.values():
        area = len(region)
        perimiter = get_perimeter(region)
        sides = get_sides(perimiter)
        sum += area * sides

    print("Part 2:", sum)


def main(lines: list[str]) -> None:
    part1(lines)
    part2(lines)
