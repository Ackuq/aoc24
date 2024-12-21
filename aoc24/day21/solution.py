from functools import cache

from frozendict import frozendict

Coord = tuple[int, int]

Keypad = frozendict[str, Coord]

door_keypad: Keypad = frozendict(
    {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        " ": (0, 3),
        "0": (1, 3),
        "A": (2, 3),
    }
)
numeric_keypad: Keypad = frozendict(
    {
        " ": (0, 0),
        "^": (1, 0),
        "A": (2, 0),
        "<": (0, 1),
        "v": (1, 1),
        ">": (2, 1),
    }
)


def path_to_destination(start: Coord, destination: Coord, gap: Coord) -> list[str]:

    if start == destination:
        return ["A"]

    vertical_arrow = "v" if start[1] < destination[1] else "^"
    vertical_moves = abs(destination[1] - start[1])

    if start[0] == destination[0]:
        return [vertical_arrow * vertical_moves + "A"]

    horizontal_arrow = ">" if start[0] < destination[0] else "<"
    horizontal_moves = abs(destination[0] - start[0])

    if start[1] == destination[1]:
        return [horizontal_arrow * horizontal_moves + "A"]

    x_range = range(min(start[0], destination[0]), max(start[0], destination[0]) + 1)
    y_range = range(min(start[1], destination[1]), max(start[1], destination[1]) + 1)

    paths = list[str]()
    if not (
        # If the gap blocks us from moving horizontally first
        (gap[0] == destination[0] and gap[1] in y_range)
        or (gap[1] == start[1] and gap[0] in x_range)
    ):
        paths.append(
            horizontal_arrow * horizontal_moves + vertical_arrow * vertical_moves + "A"
        )
    if not (
        # If the gap blocks us from moving vertically first
        (gap[0] == start[0] and gap[1] in y_range)
        or (gap[1] == destination[1] and gap[0] in x_range)
    ):
        paths.append(
            vertical_arrow * vertical_moves + horizontal_arrow * horizontal_moves + "A"
        )
    return paths


def possible_sequences(code: str, keypad: Keypad, start: str = "A") -> list[list[str]]:
    if code == "":
        return [[]]
    pos = keypad[start]
    next_pos = keypad[code[0]]
    gap = keypad[" "]

    return [
        [move, *rest]
        for rest in possible_sequences(code[1:], keypad, code[0])
        for move in path_to_destination(pos, next_pos, gap)
    ]


@cache
def shortest_path(code: str, robots: int, keypad: Keypad) -> int:
    sequences = possible_sequences(code, keypad)
    if robots == 0:
        return min(sum(len(part) for part in sequence) for sequence in sequences)

    return min(
        sum(shortest_path(part, robots - 1, numeric_keypad) for part in sequence)
        for sequence in sequences
    )


def part1(codes: list[str]) -> None:
    result = sum(shortest_path(code, 2, door_keypad) * int(code[:-1]) for code in codes)

    print("Part 1:", result)


def part2(codes: list[str]) -> None:
    result = sum(
        shortest_path(code, 25, door_keypad) * int(code[:-1]) for code in codes
    )
    print("Part 2:", result)


def main(lines: list[str]) -> None:
    codes = [line.strip() for line in lines]
    part1(codes)
    part2(codes)
