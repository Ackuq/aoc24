from copy import deepcopy


def get_checksum(disk: list[int]) -> int:
    checksum = 0
    for i, val in enumerate(disk):
        checksum += i * val
    return checksum


def get_disk(disk_map: str) -> list[int]:
    # iterate through pairs
    disk: list[int] = []
    id = 0
    for i in range(0, len(disk_map), 2):
        num_files = int(disk_map[i])
        empty_space_index = int(disk_map[i + 1]) if i + 1 != len(disk_map) else 0
        disk += [id] * num_files + [-1] * empty_space_index
        id += 1
    return disk


def part1(disk: list[int]) -> None:
    try:
        while True:
            empty_space_index = disk.index(-1)
            if empty_space_index == len(disk) - 1:
                disk = disk[:-1]
                continue
            last_letter = disk[-1]
            disk = disk[:-1]
            disk[empty_space_index] = last_letter
    except ValueError:
        pass

    checksum = get_checksum(disk)

    print("Part 1:", checksum)


def part2(disk: list[int]) -> None:
    pass


def main(lines: list[str]) -> None:
    disk = get_disk(lines[0].strip())
    part1(deepcopy(disk))
    part2(deepcopy(disk))
