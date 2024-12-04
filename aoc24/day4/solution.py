from typing import List


def part1(lines: List[str]) -> None:
    def find_xmas() -> int:
        count = 0
        directions = [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
        ]
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char != "X":
                    continue

                for di, dj in directions:
                    if all(
                        0 <= i + k * di < len(lines)
                        and 0 <= j + k * dj < len(line)
                        and lines[i + k * di][j + k * dj] == "XMAS"[k]
                        for k in range(4)
                    ):
                        count += 1

        return count

    print("Part 1:", find_xmas())


def part2(lines: List[str]) -> None:
    def find_xmas() -> int:
        missing_letters = set(["M", "S"])
        count = 0
        for i in range(1, len(lines) - 1):
            line = lines[i]
            for j in range(1, len(line) - 1):
                char = line[j]
                if char != "A":
                    continue

                up_right = lines[i - 1][j + 1]
                down_right = lines[i + 1][j + 1]
                down_left = lines[i + 1][j - 1]
                up_left = lines[i - 1][j - 1]

                if (
                    set([up_left, down_right]) == missing_letters
                    and set([up_right, down_left]) == missing_letters
                ):
                    count += 1

        return count

    print("Part 2:", find_xmas())


def main(lines: List[str]) -> None:
    striped = [line.strip() for line in lines]
    part1(striped)
    part2(striped)
