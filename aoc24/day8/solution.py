import itertools

Grid = list[list[str]]
Coord = tuple[int, int]
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


def part1(grid: Grid) -> None:
    character_locations = get_character_locations(grid)

    antinodes = set[Coord]()

    for _, locations in character_locations.items():
        combinations = itertools.combinations(locations, 2)

        for (x1, y1), (x2, y2) in combinations:
            antinode1 = (x1 + (x1 - x2), y1 + (y1 - y2))
            if is_inside(grid, antinode1):
                antinodes.add(antinode1)

            antinode2 = (x2 + (x2 - x1), y2 + (y2 - y1))
            if is_inside(grid, antinode2):
                antinodes.add(antinode1)

    print("Part 1:", len(antinodes))


def part2(grid: Grid) -> None:
    character_locations = get_character_locations(grid)
    antinodes = set[Coord]()

    for _, locations in character_locations.items():
        combinations = itertools.combinations(locations, 2)

        for (x1, y1), (x2, y2) in combinations:
            dx, dy = x2 - x1, y2 - y1

            i = 1
            while is_inside(grid, (x1 + dx * i, y1 + dy * i)):
                antinodes.add((x1 + dx * i, y1 + dy * i))
                i += 1

            i = 1
            while is_inside(grid, (x2 - dx * i, y2 - dy * i)):
                antinodes.add((x2 - dx * i, y2 - dy * i))
                i += 1

    print("Part 2:", len(antinodes))


def main(lines: list[str]) -> None:
    grid = parse(lines)
    part1(grid)
    part2(grid)
