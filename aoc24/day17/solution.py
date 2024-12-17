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
    if operand >= 0 and operand <= 3:
        return operand
    if operand == 4:
        return register["A"]
    if operand == 5:
        return register["B"]
    if operand == 6:
        return register["C"]

    assert False


def run_instruction(
    instruction: int, register: Registers, operand: int
) -> tuple[int | None, bool]:
    if instruction == 0:
        combo = combo_operand(operand, register)
        register["A"] = register["A"] // (2**combo)
    if instruction == 1:
        register["B"] = register["B"] ^ operand
    if instruction == 2:
        combo = combo_operand(operand, register)
        register["B"] = combo % 8
    if instruction == 3:
        if register["A"] == 0:
            return None, False
        return None, True
    if instruction == 4:
        register["B"] = register["B"] ^ register["C"]
    if instruction == 5:
        return combo_operand(operand, register) % 8, False
    if instruction == 6:
        combo = combo_operand(operand, register)
        register["B"] = register["A"] // (2**combo)
    if instruction == 7:
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
    result = ",".join(str(num) for num in output)
    if print_result:
        print("Part 1:", result)
    return result


def part2(input: Input, target: str) -> None:
    register, instructions = input
    solution = 0
    while True:
        new_register = deepcopy(register)
        new_register["A"] = solution
        result = part1((new_register, instructions), False)
        if result == target:
            print("Part 2:", solution)
            return
        solution += 1


def main(lines: list[str]) -> None:
    input = parse_input(lines)
    res = part1(deepcopy(input))
    part2(deepcopy(input), res)
