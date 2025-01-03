import argparse
from importlib import import_module

from aoc24.utils import get_input

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--day",
        type=int,
        help="The day number to run",
        required=True,
    )
    parser.add_argument(
        "--example",
        type=int,
        help="The example number to run",
    )
    parser.add_argument(
        "--strip",
        action="store_true",
        help="If content should be stripped",
    )
    args = parser.parse_args()

    day: int = args.day
    example: int | None = args.example
    strip: bool = args.strip

    input = get_input(day, example, strip)

    module = import_module(f"aoc24.day{day}.solution")
    module.main(input)
