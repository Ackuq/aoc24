from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue

Coord = tuple[int, int]


def get_start_and_end(lines: list[str]) -> tuple[Coord, Coord]:
    start: Coord = (0, 0)
    end: Coord = (0, 0)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)

    assert start != (0, 0)
    assert end != (0, 0)

    return start, end


class Direction(Enum):
    North = (0, -1)
    East = (1, 0)
    Down = (0, 1)
    West = (-1, 0)


direction_list = [Direction.North, Direction.East, Direction.Down, Direction.West]

CoordWithDirection = tuple[Coord, Direction]


def get_neighbors(
    lines: list[str], coord: Coord, dir: Direction
) -> list[tuple[Coord, Direction, int]]:
    neighbors: list[tuple[Coord, Direction, int]] = []
    x, y = coord

    for direction in direction_list:
        dx, dy = direction.value
        new_x, new_y = x + dx, y + dy
        if new_x < 0 or new_x >= len(lines[0]) or new_y < 0 or new_y >= len(lines):
            continue
        if lines[new_y][new_x] == "#":
            continue

        cost = abs(direction_list.index(dir) - direction_list.index(direction)) % 4
        if cost == 3:
            cost = 1

        neighbors.append(((new_x, new_y), direction, cost * 1000))

    return neighbors


@dataclass(order=True)
class PrioritizedItem:
    distance: int
    coord: Coord = field(compare=False)
    direction: Direction = field(compare=False)


def djikstra(
    lines: list[str], start: Coord, end: Coord
) -> tuple[int, dict[Coord, int]]:
    distances: dict[Coord, int] = {start: 0}

    queue: PriorityQueue[PrioritizedItem] = PriorityQueue()
    queue.put(PrioritizedItem(0, start, Direction.East))

    while queue:
        node = queue.get()

        for new_pos, new_direction, turn_cost in get_neighbors(
            lines, node.coord, node.direction
        ):
            if new_pos not in distances:
                cost = node.distance + turn_cost + 1
                distances[new_pos] = cost
                queue.put(PrioritizedItem(cost, new_pos, new_direction))

        if node.coord == end:
            return node.distance, distances


def part1(lines: list[str]) -> None:
    start, end = get_start_and_end(lines)
    min_steps, _ = djikstra(lines, start, end)

    print("Part 1:", min_steps)


def get_neighbors_nodes(
    nodes: set[Coord], coord: Coord, dir: Direction
) -> list[tuple[Coord, Direction, int]]:
    neighbors: list[tuple[Coord, Direction, int]] = []
    x, y = coord

    for direction in direction_list:
        dx, dy = direction.value
        new_x, new_y = x + dx, y + dy
        if (new_x, new_y) not in nodes:
            continue

        cost = abs(direction_list.index(dir) - direction_list.index(direction)) % 4
        if cost == 3:
            cost = 1

        neighbors.append(((new_x, new_y), direction, cost * 1000))

    return neighbors


def dfs(
    current: CoordWithDirection,
    end: Coord,
    nodes: set[Coord],
    visited: set[Coord],
    current_steps: int,
    distances: dict[Coord, int],
    min_steps: int,
) -> set[Coord] | None:
    coord, direction = current

    # Makes sure we do not make a unnecessary turn
    if current_steps > distances[coord] + 1000:
        return None

    visited = visited | {coord}

    if coord == end:
        return visited

    if current_steps >= min_steps:
        return None

    neighbors = get_neighbors_nodes(nodes, coord, direction)
    result = set[Coord]()

    for new_pos, new_dir, turn_cost in neighbors:
        if new_pos in visited:
            continue

        solution = dfs(
            (new_pos, new_dir),
            end,
            nodes,
            visited,
            current_steps + turn_cost + 1,
            distances,
            min_steps,
        )

        if solution is not None:
            result = result | solution

    return result


def part2(lines: list[str]) -> None:
    start, end = get_start_and_end(lines)
    min_steps, distances = djikstra(lines, start, end)
    nodes = {coord for coord, distance in distances.items() if distance <= min_steps}
    visited = dfs((start, Direction.East), end, nodes, set(), 0, distances, min_steps)
    assert visited is not None
    print("Part 2:", len(visited))


def main(lines: list[str]) -> None:
    part1(lines)
    part2(lines)
