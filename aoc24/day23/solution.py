Connection = frozenset[str]
Connections = frozenset[Connection]
Computers = frozenset[str]


def parse_input(lines: list[str]) -> tuple[Connections, Computers]:
    connections = frozenset(frozenset(line.strip().split("-")) for line in lines)
    computers = frozenset(
        connection for connection in connections for connection in connection
    )

    return connections, computers


def part1(connections: Connections, computers: Computers) -> None:
    triples = set[frozenset[str]]()
    for connection in connections:
        for computer in computers:
            if computer in connection:
                continue
            if all(frozenset([computer, c]) in connections for c in connection):
                triples.add(frozenset(connection | {computer}))

    starts_with_t = {
        triple for triple in triples if any(t.startswith("t") for t in triple)
    }

    result = len(starts_with_t)
    print("Part 1:", result)


Graph = dict[str, set[str]]


def bron_kerbosch(graph: Graph, p: set[str], r: set[str] = set(), x: set[str] = set()):
    if not p and not x:
        yield r
        return

    u = next(iter(p | x))
    for v in p - graph[u]:
        yield from bron_kerbosch(graph, p & graph[v], r | {v}, x & graph[v])
        p.remove(v)
        x.add(v)


def part2(connections: Connections, computers: Computers) -> None:
    graph: Graph = {computer: set() for computer in computers}
    for connection in connections:
        for c in connection:
            graph[c] |= connection - {c}

    subgraphs = bron_kerbosch(graph, set(graph.keys()))

    largest_subgraph = max(subgraphs, key=len)

    password = ",".join(sorted(largest_subgraph))

    print("Part 2:", password)


def main(lines: list[str]) -> None:
    connections, computers = parse_input(lines)
    # part1(connections, computers)
    part2(connections, computers)
