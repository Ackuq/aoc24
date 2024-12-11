from typing import Counter


def blink(stones: list[int], blinks: int) -> int:
    counter = Counter(stones)
    for _ in range(blinks):
        new_counter = Counter()
        for stone, count in counter.items():
            if stone == 0:
                new_counter[1] += count
            elif len(str(stone)) % 2 == 0:
                left_half = str(stone)[: len(str(stone)) // 2]
                new_counter[int(left_half)] += count
                right_half = str(stone)[len(str(stone)) // 2 :]
                new_counter[int(right_half)] += count
            else:
                new_counter[stone * 2024] += count
        counter = new_counter
    return sum(counter.values())


def part1(stones: list[int]) -> None:
    print("Part 1", blink(stones, 25))


def part2(stones: list[int]) -> None:
    print("Part 2:", blink(stones, 75))


def main(lines: list[str]) -> None:
    stones = list(map(int, lines[0].strip().split(" ")))
    part1(stones)
    part2(stones)
