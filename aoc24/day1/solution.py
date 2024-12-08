from collections import Counter

Input = list[tuple[int, int]]


def parse_input(lines: list[str]) -> Input:
    return [(int(line.split()[0]), int(line.split()[1])) for line in lines]


def part1(lines: Input) -> None:
    left = sorted(x[0] for x in lines)
    right = sorted(x[1] for x in lines)
    pairs = list(zip(left, right))
    distances = sum(abs(a - b) for a, b in pairs)
    print("Part 1:", distances)


def part2(lines: Input) -> None:
    counter = Counter(right for _, right in lines)

    similarity_score = 0
    for left, _ in lines:
        similarity_score += left * counter.get(left, 0)

    print("Part 2:", similarity_score)


def main(lines: list[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
