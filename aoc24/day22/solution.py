from typing import cast


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(secret: int) -> int:
    return secret % 16777216


def next_number(secret: int) -> int:
    value = secret * 64
    secret = mix(value, secret)
    secret = prune(secret)

    value = secret // 32
    secret = mix(value, secret)
    secret = prune(secret)

    value = secret * 2048
    secret = mix(value, secret)
    secret = prune(secret)

    return secret


def get_secret_at(secret: int, i: int) -> int:
    for _ in range(i):
        secret = next_number(secret)
    return secret


def part1(secrets: list[int]) -> None:
    result = sum(get_secret_at(secret, 2000) for secret in secrets)

    print("Part 1:", result)


Sequence = tuple[int, int, int, int]
SequenceMap = dict[Sequence, int]


def get_sequences(secret: int, i: int) -> SequenceMap:
    price = secret % 10
    sequences: SequenceMap = {}
    current_sequence = list[int]()
    for _ in range(i - 1):
        secret = next_number(secret)
        new_price = secret % 10
        price_diff = new_price - price
        current_sequence.append(price_diff)

        if len(current_sequence) == 4:
            seq = cast(Sequence, tuple(current_sequence))
            if seq not in sequences:
                sequences[seq] = new_price
            current_sequence.pop(0)

        price = new_price

    return sequences


def get_sequence_value(sequence: Sequence, sequence_maps: list[SequenceMap]) -> int:
    return sum(sequence_map.get(sequence, 0) for sequence_map in sequence_maps)


def part2(secrets: list[int]) -> None:
    all_sequences = set[Sequence]()
    sequence_maps = list[SequenceMap]()

    for secret in secrets:
        sequence_map = get_sequences(secret, 2000)
        all_sequences.update(sequence_map.keys())
        sequence_maps.append(sequence_map)

    result = max(
        get_sequence_value(sequence, sequence_maps) for sequence in all_sequences
    )

    print("Part 2:", result)


def main(lines: list[str]) -> None:
    secrets = [int(line.strip()) for line in lines]
    part1(secrets)
    part2(secrets)
