import re
from collections import Counter
from copy import deepcopy
from functools import reduce
from operator import mul

from PIL import Image, ImageDraw

line_re = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

# x, y, vx, vy
Robot = tuple[int, int, int, int]

WIDTH = 101
HEIGHT = 103


def parse_input(lines: list[str]) -> set[Robot]:
    robots = set[Robot]()
    for line in lines:
        match = line_re.match(line.strip())
        assert match
        groups = tuple(map(int, match.groups()))
        assert len(groups) == 4
        robots.add(groups)

    return robots


def iterate(robots: set[Robot], seconds: int) -> set[Robot]:
    for _ in range(seconds):
        new_robots = set[Robot]()
        for robot in robots:
            x, y, vx, vy = robot
            x = (x + vx) % WIDTH
            y = (y + vy) % HEIGHT
            new_robots.add((x, y, vx, vy))
        robots = new_robots

    return robots


def print_robots(robots: set[Robot]) -> None:
    robot_coords = [robot[:2] for robot in robots]
    counter = Counter(robot_coords)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            count = counter.get((x, y), ".")
            print(count, end="")
        print()


def part1(robots: set[Robot]) -> None:
    robots = iterate(robots, 100)

    x_mid = WIDTH // 2
    y_mid = HEIGHT // 2
    quandrants = [0] * 4
    for robot in robots:
        x, y, _, _ = robot
        if x == x_mid or y == y_mid:
            continue
        if x > x_mid and y > y_mid:
            quandrants[0] += 1
        elif x < x_mid and y > y_mid:
            quandrants[1] += 1
        elif x < x_mid and y < y_mid:
            quandrants[2] += 1
        elif x >= x_mid and y < y_mid:
            quandrants[3] += 1

    safety_factor = reduce(mul, quandrants)

    print("Part 1:", safety_factor)


def part2(robots: set[Robot]) -> None:
    directory = "aoc24/day14/part2/"
    i = 0
    while i < 8280:
        i += 1
        robots = iterate(robots, 1)
        robot_coords = [robot[:2] for robot in robots]
        counter = Counter(robot_coords)

        img = Image.new("RGB", (WIDTH, HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                count = counter.get((x, y), 0)
                if count > 0:
                    draw.point((x, y), fill="black")

        img.save(f"{directory}{i}.png")


def main(lines: list[str]) -> None:
    robots = parse_input(lines)
    part1(deepcopy(robots))
    part2(deepcopy(robots))
