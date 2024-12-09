from copy import deepcopy


def get_checksum(disk: list[int]) -> int:
    checksum = 0
    for i, val in enumerate(disk):
        checksum += i * val
    return checksum


def get_disk(disk_map: str) -> list[int]:
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


# (id, count)
Group = tuple[int, int]


def get_checksum_groups(disk: list[Group]) -> int:
    checksum = 0
    i = 0
    for id, count in disk:
        if id == -1:
            i += count
            continue

        for _ in range(count):
            checksum += i * id
            i += 1

    return checksum


def get_compressed_groups(disk: list[int]) -> list[Group]:
    compressed_groups = []
    for id in disk:
        if not compressed_groups:
            compressed_groups.append((disk[0], 1))
            continue

        last_group = compressed_groups[-1]
        if last_group[0] == id:
            compressed_groups[-1] = (last_group[0], last_group[1] + 1)
        else:
            compressed_groups.append((id, 1))

    return compressed_groups


def get_rightmost_group_index(
    compressed_groups: list[Group], starting_index: int
) -> int:
    for i in range(starting_index, -1, -1):
        if compressed_groups[i][0] != -1:
            return i
    return -1


def get_leftmost_empty_group_of_size(
    compressed_groups: list[Group], size: int, max_index: int
) -> int:
    for i, (id, empty_size) in enumerate(compressed_groups[:max_index]):
        if id == -1 and size <= empty_size:
            return i
    return -1


def part2(disk: list[int]) -> None:
    compressed_groups = get_compressed_groups(disk)

    right = len(compressed_groups) - 1
    seen_groups = set[int]()
    while right >= 0:
        rightmost_group_index = get_rightmost_group_index(compressed_groups, right)

        if rightmost_group_index == -1:
            break

        right = rightmost_group_index - 1

        (id, size) = compressed_groups[rightmost_group_index]

        if id in seen_groups:
            continue
        seen_groups.add(id)

        empty_group_index = get_leftmost_empty_group_of_size(
            compressed_groups, size, rightmost_group_index
        )
        if empty_group_index == -1:
            continue

        assert empty_group_index < rightmost_group_index

        empty_group_size = compressed_groups[empty_group_index][1]

        assert empty_group_size >= size

        compressed_groups[rightmost_group_index] = (
            -1,
            size,
        )

        if empty_group_size == size:
            compressed_groups[empty_group_index] = (id, size)
        else:
            compressed_groups[empty_group_index] = (-1, empty_group_size - size)
            compressed_groups.insert(empty_group_index, (id, size))
            # Adjust for the added group
            right += 1

    checksum = get_checksum_groups(compressed_groups)
    print("Part 2:", checksum)


def main(lines: list[str]) -> None:
    disk = get_disk(lines[0].strip())
    part1(deepcopy(disk))
    part2(deepcopy(disk))
