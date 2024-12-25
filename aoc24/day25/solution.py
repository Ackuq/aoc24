def parse(lines: list[str]) -> tuple[set[tuple[int, ...]], set[tuple[int, ...]]]:
    locks = list[list[str]]()
    keys = list[list[str]]()
    current_grid = list[str]()
    is_keys: bool | None = None

    for line in [line.strip() for line in lines]:
        if line == "":
            if is_keys:
                keys.append(current_grid)
            else:
                locks.append(current_grid)
            current_grid = []
            is_keys = None
            continue
        if is_keys is None:
            if all(c == "#" for c in line):
                is_keys = False
            else:
                is_keys = True
        current_grid.append(line)

    if is_keys:
        keys.append(current_grid)
    else:
        locks.append(current_grid)

    lock_heights = set(
        tuple(
            len([a for a in col if a == "#"]) - 1 for col in list(map(list, zip(*lock)))
        )
        for lock in locks
    )
    key_heights = set(
        tuple(
            len([a for a in col if a == "#"]) - 1 for col in list(map(list, zip(*key)))
        )
        for key in keys
    )

    return lock_heights, key_heights


def part1(locks: set[tuple[int, ...]], keys: set[tuple[int, ...]]) -> None:
    result = 0
    for lock in locks:
        for key in keys:
            pairs = zip(lock, key)
            if all(pin1 + pin2 < 6 for pin1, pin2 in pairs):
                result += 1
    print("Part 1:", result)


def main(lines: list[str]) -> None:
    locks, keys = parse(lines)
    part1(locks, keys)
