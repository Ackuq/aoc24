import itertools

Grid = list[list[str]]
Coord = tuple[int, int]
CoordWithDirection = tuple[Coord, Coord]
CharacterLocation = dict[str, set[Coord]]


def parse(lines: list[str]) -> Grid:
    return [list(line.strip()) for line in lines]


def get_character_locations(grid: Grid) -> CharacterLocation:
    character_locations: CharacterLocation = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == ".":
                continue
            if char not in character_locations:
                character_locations[char] = set()
            character_locations[char].add((x, y))

    return character_locations


def is_inside(grid: Grid, pos: Coord) -> bool:
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def get_antinodes(grid: Grid, pos1: Coord, pos2: Coord) -> list[CoordWithDirection]:
    x1, y1 = pos1
    x2, y2 = pos2
    antinodes = list[CoordWithDirection]()

    dx, dy = abs(x2 - x1), abs(y2 - y1)

    dx1 = dx if x1 > x2 else -dx
    dy1 = dy if y1 > y2 else -dy
    antinode1 = (x1 + dx1, y1 + dy1)
    if is_inside(grid, antinode1):
        antinodes.append((antinode1, (dx1, dy1)))

    dx2 = dx if x2 > x1 else -dx
    dy2 = dy if y2 > y1 else -dy
    antinode2 = (x2 + dx2, y2 + dy2)
    if is_inside(grid, antinode2):
        antinodes.append((antinode2, (dx2, dy2)))

    return antinodes


def part1(grid: Grid) -> None:
    character_locations = get_character_locations(grid)

    antinodes = set[Coord]()

    for _, locations in character_locations.items():
        combinations = itertools.combinations(locations, 2)

        for (x1, y1), (x2, y2) in combinations:
            antinodes |= {coord for coord, _ in get_antinodes(grid, (x1, y1), (x2, y2))}

    print("Part 1:", len(antinodes))


def part2(grid: Grid) -> None:
    character_locations = get_character_locations(grid)
    antinodes = set[Coord]()

    for _, locations in character_locations.items():
        combinations = itertools.combinations(locations, 2)

        for (x1, y1), (x2, y2) in combinations:
            antinodes |= {(x1, y1), (x2, y2)}

            antinodes_with_direction = get_antinodes(grid, (x1, y1), (x2, y2))

            while antinodes_with_direction:
                antinodes |= {coord for coord, _ in antinodes_with_direction}

                antinodes_with_direction: list[CoordWithDirection] = [
                    ((x + dx, y + dy), (dx, dy))
                    for (x, y), (dx, dy) in antinodes_with_direction
                    if is_inside(grid, (x + dx, y + dy))
                ]

    print("Part 2:", len(antinodes))


def main(lines: list[str]) -> None:
    grid = parse(lines)
    part1(grid)
    part2(grid)
