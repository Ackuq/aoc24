# Ordering x -> y means that x should come before y in the sorted list
from functools import cmp_to_key

Orderings = dict[int, set[int]]


Sequence = list[int]
Sequences = list[Sequence]


def parse_input(lines: list[str]) -> tuple[Orderings, Sequences]:
    empty_line = lines.index("\n")

    ordering_lines = lines[:empty_line]
    sequence_lines = lines[empty_line + 1 :]

    orderings = {}
    for line in ordering_lines:
        x, y = map(int, line.strip().split("|"))
        if x not in orderings:
            orderings[x] = set()
        orderings[x].add(y)

    sequences = [list(map(int, line.strip().split(","))) for line in sequence_lines]

    return orderings, sequences


def compare(orderings: Orderings):
    def cmp(x: int, y: int) -> int:
        if x in orderings and y in orderings[x]:
            return -1
        if y in orderings and x in orderings[y]:
            return 1
        return 0

    return cmp


def part1(lines: list[str]) -> None:
    orderings, sequences = parse_input(lines)

    correctly_sorted: Sequences = [
        sequence
        for sequence in sequences
        if sorted(sequence, key=cmp_to_key(compare(orderings))) == sequence
    ]

    result = sum(sequence[len(sequence) // 2] for sequence in correctly_sorted)

    print("Part 1:", result)


def part2(lines: list[str]) -> None:
    orderings, sequences = parse_input(lines)

    sorted_lists = [
        sorted(sequence, key=cmp_to_key(compare(orderings))) for sequence in sequences
    ]

    incorrect_sorted = [
        correct
        for correct, original in zip(sorted_lists, sequences)
        if correct != original
    ]

    result = sum(sequence[len(sequence) // 2] for sequence in incorrect_sorted)

    print("Part 2:", result)


def main(lines: list[str]) -> None:
    part1(lines)
    part2(lines)
