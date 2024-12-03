import re

mul_regex = re.compile(r"^mul\((\d+),(\d+)\)")


def part1(input: list[str]) -> None:
    sum = 0
    for line in input:
        while line:
            match = mul_regex.match(line)
            if match:
                a, b = map(int, match.groups())
                sum += a * b
                line = line[match.end() :]
                continue

            line = line[1:]

    print("Part 1:", sum)


def part2(input: list[str]) -> None:
    sum = 0
    mul_enabled = True
    for line in input:
        while line:
            if line.startswith("do()"):
                mul_enabled = True
                line = line[4:]
                continue
            if line.startswith("don't()"):
                mul_enabled = False
                line = line[7:]
                continue

            match = mul_regex.match(line)
            if mul_enabled and match:
                a, b = map(int, match.groups())
                sum += a * b
                line = line[match.end() :]
                continue

            line = line[1:]

    print("Part 2:", sum)


def main(lines: list[str]) -> None:
    part1(lines)
    part2(lines)
