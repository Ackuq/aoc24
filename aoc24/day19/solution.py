def has_solution(towels: set[str], design: str) -> bool:
    if design == "":
        return True

    for i in range(1, len(design) + 1):
        if design[:i] in towels:
            if has_solution(towels, design[i:]):
                return True

    return False


def parse_input(lines: list[str]) -> tuple[set[str], list[str]]:
    towels = set(lines[0].strip().split(", "))
    designs = [line.strip() for line in lines[2:]]

    return towels, designs


def part1(towels: set[str], designs: list[str]) -> None:
    result = sum(has_solution(towels, design) for design in designs)

    print("Part 1:", result)


memo: dict[str, int] = {}


def find_all_solutions(towels: set[str], design: str) -> int:
    if design in memo:
        return memo[design]

    if design == "":
        return 1

    result = 0
    for i in range(1, len(design) + 1):
        if design[:i] in towels:
            result += find_all_solutions(towels, design[i:])

    memo[design] = result
    return result


def part2(towels: set[str], designs: list[str]) -> None:
    result = sum(find_all_solutions(towels, design) for design in designs)

    print("Part 2:", result)


def main(lines: list[str]) -> None:
    towels, designs = parse_input(lines)
    part1(towels, designs)
    part2(towels, designs)
