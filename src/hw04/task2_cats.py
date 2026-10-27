# Task 2: Cats info
#
# Write `get_cats_info(path)`. It reads a text file with one cat per line
# in the format `id,name,age` (comma, no spaces) and returns a list of dicts
# with the keys "id", "name" and "age". All values stay strings.
#
# Example file:
#   60b90c1c13067a15887e1ae1,Tayson,3
#   60b90c2413067a15887e1ae2,Vika,1
#   60b90c2e13067a15887e1ae3,Barsik,2
# Result:
#   [
#       {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
#       {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"},
#       {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": "2"},
#   ]
#
# Requirements:
#   - Read the file with `with open(..., encoding="utf-8")`.
#   - Keep the logic free of print/input; `run()` does the console I/O.
#   - Keep built-in errors as they are: FileNotFoundError, IsADirectoryError,
#     UnicodeDecodeError.
#   - Blank lines are skipped, but still count for line numbers.
#   - A line with too few or too many fields raises CorruptLineError
#     (with the line number).
#   - A file with no cats raises EmptyFileError.
#   - A repeated id raises DuplicateIdError (new exception in exceptions.py,
#     carries the id and the line number).
#   - `run()` asks for the path (Enter = default `data/cats.txt`), catches the
#     errors above and prints a message for each.

from typing import TypedDict

from hw04.exceptions import CorruptLineError, DuplicateIdError, EmptyFileError
from hw04.files import read_data_lines
from hw04.helpers import ask_path
from hw04.log import log_error, log_result


class CatInfo(TypedDict):
    id: str
    name: str
    age: str


DEFAULT_CATS_PATH = "data/cats.txt"
CATS_LINE_LEN = 3


def parse_cat_from_line(line_number: int, line: str) -> CatInfo:
    line_list = line.strip().split(",")
    if len(line_list) != CATS_LINE_LEN:
        raise CorruptLineError(line_number, line.strip())

    return {"id": line_list[0], "name": line_list[1], "age": line_list[2]}


def get_cats_info(path: str) -> list[CatInfo]:
    seen_ids: set[str] = set()
    cats_lines = read_data_lines(path)
    parsed_cats: list[CatInfo] = []

    for line_number, line in cats_lines:
        parsed_cat_info = parse_cat_from_line(line_number, line)
        if parsed_cat_info["id"] in seen_ids:
            raise DuplicateIdError(line_number, parsed_cat_info["id"])
        parsed_cats.append(parsed_cat_info)
        seen_ids.add(parsed_cat_info["id"])

    return parsed_cats


def run() -> None:
    path = ask_path("cats info", DEFAULT_CATS_PATH)

    try:
        cats = get_cats_info(path)
    except FileNotFoundError:
        log_error(f"File not found: {path}")
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as e:
        log_error(f"Cannot read file: {e}")
    except EmptyFileError as e:
        log_error(f"File is empty: {e}")
    except CorruptLineError as e:
        log_error(f"File corrupted, {e}")
    except DuplicateIdError as e:
        log_error(f"File has duplicated id, {e}")

    else:
        log_result(f"Cats info: {cats}")
