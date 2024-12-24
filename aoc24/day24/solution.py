import random
import re
from copy import deepcopy

Wires = dict[str, int]


def gate_op(gate: str, in1: int, in2: int) -> int:
    if gate == "AND":
        return in1 & in2
    elif gate == "OR":
        return in1 | in2
    elif gate == "XOR":
        return in1 ^ in2
    else:
        raise ValueError("Invalid gate")


Connection = tuple[str, str, str]
Connections = dict[Connection, list[str]]


Input = tuple[Wires, Connections]

wire_re = re.compile(r"((?:x|y)\d+): (\d+)")
connection_re = re.compile(r"(.*) (AND|OR|XOR) (.*) -> (.*)")


def parse_input(lines: list[str]) -> Input:
    wires: Wires = {}
    connections: Connections = {}
    split_index = lines.index("\n")

    for line in lines[:split_index]:
        match = wire_re.match(line.strip())
        if not match:
            break
        wires[match.group(1)] = int(match.group(2))

    for line in lines[split_index + 1 :]:
        match = connection_re.match(line.strip())
        if not match:
            break
        in1, gate, in2, out = (
            match.group(1),
            match.group(2),
            match.group(3),
            match.group(4),
        )
        connections.setdefault((in1, gate, in2), []).append(out)

    return wires, connections


def to_decimal(prefix: str, wires: Wires) -> int:
    bit_arr = ""
    i = 0
    while True:
        wire = f"{prefix}{i:02d}"
        if wire not in wires:
            break
        bit_arr = str(wires[wire]) + bit_arr
        i += 1

    if bit_arr == "":
        return 0

    return int(bit_arr, 2)


def run_connections(wires: Wires, connections: Connections) -> Wires:
    current_values = deepcopy(wires)
    connections_to_process = set(connections.keys())
    while len(connections_to_process) != 0:
        new_connections_to_process = deepcopy(connections_to_process)

        for connection in connections_to_process:
            in1, gate, in2 = connection
            if in1 not in current_values or in2 not in current_values:
                continue
            out_value = gate_op(gate, current_values[in1], current_values[in2])
            for out in connections[connection]:
                current_values[out] = out_value
            new_connections_to_process.remove(connection)

        connections_to_process = new_connections_to_process

    return current_values


def part1(wires: Wires, connections: Connections) -> None:
    end_state = run_connections(wires, connections)

    result = to_decimal("z", end_state)
    print("Part 1:", result)


def try_solution(wires: Wires, connections: Connections) -> None:
    faulty_bits = dict[int, int]()
    expected_bits = len(wires) // 2

    for _ in range(100):
        for wire in wires:
            wires[wire] = random.getrandbits(1)

        goal = to_decimal("x", wires) + to_decimal("y", wires)
        res = run_connections(wires, connections)
        z = to_decimal("z", res)
        diff = goal ^ z
        for i in range(expected_bits):
            if diff & (1 << i):
                faulty_bits[i] = faulty_bits.get(i, 0) + 1

    if len(faulty_bits) == 0:
        print("Solution found!!")
        return
    print("Try again")
    print(sorted([key for key in faulty_bits]))


def part2(wires: Wires, connections: Connections) -> None:
    try_solution(wires, connections)


def main(lines: list[str]) -> None:
    wires, connections = parse_input(lines)
    part1(wires, connections)
    part2(wires, connections)
