import os

directory = os.path.dirname(os.path.abspath(__file__))


def get_input(
    day: int,
    example: int | None = None,
    strip: bool = True,
) -> list[str]:
    day_directory = f"{directory}/day{day}"

    filename = (
        f"{day_directory}/example{example}.txt"
        if example is not None
        else f"{day_directory}/problem.txt"
    )
    file = open(filename)
    lines = file.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines
