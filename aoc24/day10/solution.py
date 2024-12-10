class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.reachable = set["Node"]()

    def __str__(self) -> str:
        return f"{self.value}: {self.reachable}"

    def __repr__(self) -> str:
        return f"{self.value}"


def create_graph(lines: list[str]) -> list[Node]:
    nodes = {
        (x, y): Node(int(char))
        for y, line in enumerate(lines)
        for x, char in enumerate(line.strip())
        if char != "."
    }

    for (x, y), node in nodes.items():
        for dy in range(-1, 2):
            if (x, y + dy) not in nodes:
                continue
            other = nodes[(x, y + dy)]
            if other.value - node.value == 1:
                node.reachable.add(other)

        for dx in range(-1, 2):
            if (x + dx, y) not in nodes:
                continue
            other = nodes[(x + dx, y)]
            if other.value - node.value == 1:
                node.reachable.add(other)

    return [node for node in nodes.values() if node.value == 0]


def get_reachable_tops(start: Node) -> int:
    visited = set[Node]()
    stack = [start]

    while stack:
        node = stack.pop()
        visited.add(node)
        stack.extend(node.reachable - visited)

    return sum(node.value == 9 for node in visited)


def part1(lines: list[str]) -> None:
    trailheads = create_graph(lines)

    result = sum(get_reachable_tops(trailhead) for trailhead in trailheads)

    print("Part 1:", result)


def get_unique_paths(node: Node, visited: set[Node] = set()) -> int:
    if node.value == 9:
        return 1

    visited.add(node)

    result = 0

    for neighbor in node.reachable - visited:
        result += get_unique_paths(neighbor, set(visited))

    return result


def part2(lines: list[str]) -> None:
    trailheads = create_graph(lines)

    result = sum(get_unique_paths(trailhead) for trailhead in trailheads)

    print("Part 2:", result)


def main(lines: list[str]) -> None:
    part1(lines)
    part2(lines)
