import re
from copy import deepcopy

Registers = dict[str, int]
Input = tuple[Registers, list[int]]

register_re = re.compile(r"Register (.): (\d+)")
program_re = re.compile(r"Program: (.*)")


def parse_input(lines: list[str]) -> Input:
    register = dict[str, int]()
    programs = list[int]()

    for line in lines:
        register_match = register_re.match(line)
        program_match = program_re.match(line)

        if register_match:
            register[register_match.group(1)] = int(register_match.group(2))

        elif program_match:
            programs = [int(char) for char in program_match.group(1).split(",")]

    return register, programs


def combo_operand(operand: int, register: Registers) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register["A"]
        case 5:
            return register["B"]
        case 6:
            return register["C"]
    assert False


def run_instruction(
    instruction: int, register: Registers, operand: int
) -> tuple[int | None, bool]:
    match instruction:
        case 0:
            combo = combo_operand(operand, register)
            register["A"] = register["A"] // (2**combo)
        case 1:
            register["B"] = register["B"] ^ operand
        case 2:
            combo = combo_operand(operand, register)
            register["B"] = combo % 8
        case 3:
            if register["A"] == 0:
                return None, False
            return None, True
        case 4:
            register["B"] = register["B"] ^ register["C"]
        case 5:
            return combo_operand(operand, register) % 8, False
        case 6:
            combo = combo_operand(operand, register)
            register["B"] = register["A"] // (2**combo)
        case 7:
            combo = combo_operand(operand, register)
            register["C"] = register["A"] // (2**combo)

    return None, False


def part1(input: Input, print_result: bool = True) -> str:
    register, instructions = input
    i = 0
    output = list[int]()

    while i < len(instructions):
        inst = instructions[i]
        operand = instructions[i + 1]
        out, jump = run_instruction(inst, register, operand)
        if out is not None:
            output.append(out)

        if jump:
            i = operand
        else:
            i += 2
    result = ",".join(map(str, output))
    if print_result:
        print("Part 1:", result)
    return result


def find_lowest_solution(instructions: list[int], target: str) -> int:
    to_check = [(len(instructions) - 1, 0)]
    for pos, val in to_check:
        start = val * 8
        end = val * 8 + 8
        target_sub = ",".join(map(str, instructions[pos:]))
        for a in range(start, end):
            res = part1(({"A": a, "B": 0, "C": 0}, instructions), print_result=False)
            if res == target_sub:
                to_check.append((pos - 1, a))
                if pos == 0:
                    return a
    assert False


def part2(input: Input, target: str) -> None:
    min_solution = find_lowest_solution(input[1], target)
    print("Part 2:", min_solution)


def main(lines: list[str]) -> None:
    input = parse_input(lines)
    res = part1(deepcopy(input))
    part2(deepcopy(input), res)
