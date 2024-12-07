from operator import add, mul
from typing import Callable

Equations = list[tuple[int, list[int]]]
Operator = Callable[[int, int], int]


def parse(lines: list[str]) -> Equations:
    splitted = [line.strip().split(": ") for line in lines]
    equations: Equations = [
        (int(line[0]), [int(num) for num in line[1].split(" ")]) for line in splitted
    ]

    return equations


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


def is_solvable(
    answer: int, digits: list[int], operators: list[Operator], acc: set[int] = {0}
) -> bool:
    if not digits:
        return answer in acc

    acc = {op(prev, digits[0]) for prev in acc for op in operators}
    acc = {num for num in acc if num <= answer}

    return is_solvable(answer, digits[1:], operators, acc)


def part1(equations: Equations) -> None:
    solvable = sum(
        answer
        for answer, digits in equations
        if is_solvable(answer, digits, [add, mul])
    )

    print("Part 1:", solvable)


def part2(equations: Equations) -> None:
    solvable = sum(
        answer
        for answer, digits in equations
        if is_solvable(answer, digits, [add, mul, concat])
    )

    print("Part 2:", solvable)


def main(lines: list[str]) -> None:
    equations = parse(lines)
    part1(equations)
    part2(equations)
