from enum import Enum

Coord = tuple[int, int]
Grid = set[Coord]


class Move(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


# pos, boxes, walls, moves
Input = tuple[Coord, Grid, Grid, list[Move]]


def parse(lines: list[str]) -> Input:
    pos: Coord | None = None
    boxes = set[Coord]()
    walls = set[Coord]()

    for y, line in enumerate(lines):
        if line.strip() == "":
            lines = lines[y + 1 :]
            break
        for x, char in enumerate(line.strip()):
            if char == "@":
                pos = (x, y)
            elif char == "#":
                walls.add((x, y))
            elif char == "O":
                boxes.add((x, y))

    assert pos is not None

    moves = list[Move]()
    for line in lines:
        for char in line.strip():
            if char == "^":
                moves.append(Move.UP)
            elif char == "v":
                moves.append(Move.DOWN)
            elif char == "<":
                moves.append(Move.LEFT)
            elif char == ">":
                moves.append(Move.RIGHT)

    return pos, boxes, walls, moves


# start, end
Boxes = dict[Coord, Coord]
Input2 = tuple[Coord, Boxes, set[Coord], list[Move]]


def parse2(lines: list[str]) -> Input2:
    pos: Coord | None = None
    boxes = Boxes()
    walls = set[Coord]()

    for y, line in enumerate(lines):
        if line.strip() == "":
            lines = lines[y + 1 :]
            break
        x_offset = 0
        for x, char in enumerate(line.strip()):
            if char == "@":
                pos = (x + x_offset, y)
            elif char == "#":
                walls.add((x + x_offset, y))
                walls.add((x + x_offset + 1, y))
            elif char == "O":
                boxes[(x + x_offset, y)] = (x + x_offset + 1, y)
                boxes[(x + x_offset + 1, y)] = (x + x_offset, y)

            x_offset += 1

    assert pos is not None

    moves = list[Move]()
    for line in lines:
        for char in line.strip():
            if char == "^":
                moves.append(Move.UP)
            elif char == "v":
                moves.append(Move.DOWN)
            elif char == "<":
                moves.append(Move.LEFT)
            elif char == ">":
                moves.append(Move.RIGHT)

    return pos, boxes, walls, moves


def part1(input: Input) -> None:
    pos, boxes, walls, moves = input
    for move in moves:
        x, y = pos
        dx, dy = move.value
        new_pos = (x + dx, y + dy)

        if new_pos in walls:
            continue

        box_pos = new_pos
        box_moves = list[tuple[Coord, Coord]]()
        blocked = False

        while box_pos in boxes:
            next_box_pos = (box_pos[0] + dx, box_pos[1] + dy)
            if next_box_pos in walls:
                blocked = True
                break
            box_moves.append((box_pos, next_box_pos))
            box_pos = next_box_pos

        if blocked:
            continue

        pos = new_pos
        for box_move in reversed(box_moves):
            old_box, new_box = box_move
            boxes.remove(old_box)
            boxes.add(new_box)

    result = sum(box[0] + box[1] * 100 for box in boxes)

    print("Part 1:", result)


def part2(input: Input2) -> None:
    pos, boxes, walls, moves = input

    for move in moves:
        x, y = pos
        dx, dy = move.value
        new_pos = (x + dx, y + dy)

        if new_pos in walls:
            continue

        box_moves = list[tuple[tuple[Coord, Coord], tuple[Coord, Coord]]]()
        pushed = set[Coord]([new_pos])
        blocked = False

        while pushed:
            used_boxes = set[Coord]()
            next_pushed_boxes = set[Coord]()
            for box_pos1 in pushed:
                if box_pos1 in used_boxes or box_pos1 not in boxes:
                    continue
                box_pos2 = boxes[box_pos1]

                next_box_pos1 = (box_pos1[0] + dx, box_pos1[1] + dy)
                next_box_pos2 = (box_pos2[0] + dx, box_pos2[1] + dy)

                if next_box_pos1 in walls or next_box_pos2 in walls:
                    blocked = True
                    break

                used_boxes = used_boxes.union({box_pos1, box_pos2})

                if next_box_pos1 != box_pos2:
                    next_pushed_boxes.add(next_box_pos1)
                if next_box_pos2 != box_pos1:
                    next_pushed_boxes.add(next_box_pos2)
                box_moves.append(((box_pos1, box_pos2), (next_box_pos1, next_box_pos2)))

            if blocked:
                break

            pushed = next_pushed_boxes

        if blocked:
            continue
        pos = new_pos
        for box_move in reversed(box_moves):
            (old_box1, old_box2), (new_box1, new_box2) = box_move
            del boxes[old_box1]
            del boxes[old_box2]
            boxes[new_box1] = new_box2
            boxes[new_box2] = new_box1

    result = 0
    visited = set[Coord]()
    for box1, box2 in boxes.items():
        if box1 in visited or box2 in visited:
            continue
        visited = visited.union({box1, box2})
        result += min(box1[0], box2[0]) + min(box1[1], box2[1]) * 100

    print("Part 2:", result)


def main(lines: list[str]) -> None:
    input = parse(lines)
    part1(input)
    input2 = parse2(lines)
    part2(input2)
