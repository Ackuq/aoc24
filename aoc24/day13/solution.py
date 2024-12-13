# Input = ((X1, Y1), (X2, Y2), (WantX, WantY))
import re

Input = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]

button_re = re.compile(r"Button .: X\+(\d+), Y\+(\d+)")
prize_re = re.compile(r"Prize: X\=(\d+), Y\=(\d+)")


def parse_input(lines: list[str]) -> list[Input]:
    input = list[Input]()

    i = 0
    while i < len(lines):
        line1, line2, line3 = [line.strip() for line in lines[i : i + 3]]
        line1_match = button_re.match(line1)
        line2_match = button_re.match(line2)
        line3_match = prize_re.match(line3)

        assert line1_match and line2_match and line3_match
        input.append(
            (
                (int(line1_match.group(1)), int(line1_match.group(2))),
                (int(line2_match.group(1)), int(line2_match.group(2))),
                (int(line3_match.group(1)), int(line3_match.group(2))),
            )
        )
        i += 4

    return input


Line = tuple[int, int, int]


# Cramer's rule: https://en.wikipedia.org/wiki/Cramer%27s_rule
def cramers(line1: Line, line2: Line) -> tuple[int, int] | None:
    x1, y1, c1 = line1
    x2, y2, c2 = line2

    det = x1 * y2 - y1 * x2
    if det == 0:
        return None

    A = (c1 * y2 - c2 * y1) / det
    B = (x1 * c2 - x2 * c1) / det

    if A % 1 != 0 or B % 1 != 0:
        return None

    return int(A), int(B)


def part1(input: list[Input]) -> None:
    tokens = 0

    for (x1, y1), (x2, y2), (want_x, want_y) in input:
        solution = cramers((x1, x2, want_x), (y1, y2, want_y))
        if not solution:
            continue

        A, B = solution
        tokens += A * 3 + B

    print("Part 1:", tokens)


def part2(input: list[Input]) -> None:
    tokens = 0

    for (x1, y1), (x2, y2), (want_x, want_y) in input:
        solution = cramers(
            (x1, x2, want_x + 10000000000000), (y1, y2, want_y + 10000000000000)
        )
        if not solution:
            continue

        A, B = solution
        tokens += A * 3 + B

    print("Part 2:", tokens)


def main(lines: list[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
