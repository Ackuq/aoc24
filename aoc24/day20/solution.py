Coord = tuple[int, int]
Grid = set[Coord]


def parse_input(lines: list[str]) -> tuple[Grid, Coord]:
    grid = set()
    start: Coord | None = None

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            match char:
                case "S":
                    start = (x, y)
                case "E":
                    grid.add((x, y))
                case ".":
                    grid.add((x, y))

    assert start

    return grid, start


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def dfs(grid: Grid, start: Coord) -> dict[Coord, int]:
    visited = {start: 0}
    stack = [start]

    while stack:
        current = stack.pop()
        x, y = current
        distance = visited[current]

        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in grid and neighbor not in visited:
                visited[neighbor] = distance + 1
                stack.append(neighbor)

    return visited


def cheats(distances: dict[Coord, int], max_dist: int) -> dict[int, int]:
    count = dict[int, int]()
    for (x, y), distance in distances.items():
        possible_cheats = {
            (x + dx, y + dy): abs(dx) + abs(dy)
            for dx in range(-max_dist, max_dist + 1)
            for dy in range(-max_dist, max_dist + 1)
            if abs(dx) + abs(dy) <= max_dist and (x + dx, y + dy) in distances
        }
        for cheat, new_dist in possible_cheats.items():
            saved = distances[cheat] - distance - new_dist
            if saved <= 0:
                continue
            count[saved] = count.get(saved, 0) + 1

    return count


def part1(grid: Grid, start: Coord) -> None:
    distances = dfs(grid, start)
    cheat_count = cheats(distances, max_dist=2)
    result = sum(count for saved, count in cheat_count.items() if saved >= 100)
    print("Part 1:", result)


def part2(grid: Grid, start: Coord) -> None:
    distances = dfs(grid, start)
    cheat_count = cheats(distances, max_dist=20)
    result = sum(count for saved, count in cheat_count.items() if saved >= 100)
    print("Part 2:", result)


def main(lines: list[str]) -> None:
    grid, start = parse_input(lines)
    part1(grid, start)
    part2(grid, start)
