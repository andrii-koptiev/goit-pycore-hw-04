from hw04.exceptions import EmptyFileError


def read_data_lines(path: str) -> list[tuple[int, str]]:
    with open(path, "r", encoding="utf-8") as file:
        lines = [
            (index, line) for index, line in enumerate(file, start=1) if line.strip()
        ]

    if not lines:
        raise EmptyFileError()

    return lines
