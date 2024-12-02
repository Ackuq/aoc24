from typing import List

Input = List[List[int]]


def is_safe(report: List[int]) -> bool:
    parity = 0
    previous = report[0]

    for i in report[1:]:
        if i == previous:
            return False

        if abs(i - previous) > 3:
            return False

        new_parity = 1 if i > previous else -1
        if new_parity == -parity:
            return False
        parity = new_parity
        previous = i
    return True


def part1(input: Input) -> None:
    safe_reports = [report for report in input if is_safe(report)]
    print("Part 1:", len(safe_reports))


def part2(input: Input) -> None:
    def check_report(report: List[int]) -> bool:
        if is_safe(report):
            return True

        for i in range(0, len(report)):
            if is_safe(report[:i] + report[i + 1 :]):
                return True

        return False

    safe_reports = [report for report in input if check_report(report)]
    print("Part 2:", len(safe_reports))


def parse_input(lines: List[str]) -> Input:
    return [[int(x) for x in line.split()] for line in lines]


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
