from typing import List


def part1(lines: List[str]) -> None:
    def find_xmas() -> int:
        count = 0
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char != "X":
                    continue

                up = (
                    "".join(lines[i - k][j] for k in range(4)) if i - 3 >= 0 else "----"
                )
                up_right = (
                    "".join(lines[i - k][j + k] for k in range(4))
                    if i - 3 >= 0 and j + 4 <= len(line)
                    else "----"
                )
                right = line[j : j + 4] if j + 4 <= len(line) else "----"

                down_right = (
                    "".join(lines[i + k][j + k] for k in range(4))
                    if i + 4 <= len(lines) and j + 4 <= len(line)
                    else "----"
                )
                down = (
                    "".join(lines[i + k][j] for k in range(4))
                    if i + 4 <= len(lines)
                    else "----"
                )
                down_left = (
                    "".join(lines[i + k][j - k] for k in range(4))
                    if i + 4 <= len(lines) and j - 3 >= 0
                    else "----"
                )
                left = (
                    "".join(lines[i][j - k] for k in range(4)) if j - 3 >= 0 else "----"
                )
                up_left = (
                    "".join(lines[i - k][j - k] for k in range(4))
                    if i - 3 >= 0 and j - 3 >= 0
                    else "----"
                )
                # print(up, up_right, right, down_right, down, down_left, left, up_left)

                count += len(
                    [
                        x
                        for x in [
                            up,
                            up_right,
                            right,
                            down_right,
                            down,
                            down_left,
                            left,
                            up_left,
                        ]
                        if x == "XMAS"
                    ]
                )

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
