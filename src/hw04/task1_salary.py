# Task 1: Salary statistics
#
# Write `total_salary(path)`. It reads a text file with one employee per line
# in the format `Name,salary` (comma, no spaces) and returns a tuple
# `(total, average)`: the sum of all salaries and their average.
#
# Example file:
#   Alex Korp,3000
#   Nikita Borysenko,2000
#   Sitarama Raju,1000
# Result: (6000, 2000)
#
# Requirements:
#   - Read the file with `with open(..., encoding="utf-8")`.
#   - Handle a missing or corrupt file explicitly.
#   - Keep the logic free of print/input; `run()` does the console I/O.


from hw04.exceptions import CorruptLineError, EmptyFileError
from hw04.files import read_data_lines
from hw04.helpers import ask_path
from hw04.log import log_error, log_result

DEFAULT_SALARY_PATH = "data/staff.txt"


def parse_salary_from_line(line_number: int, line: str) -> float:
    try:
        return float(line.strip().split(",")[1])
    except (IndexError, ValueError):
        raise CorruptLineError(line_number, line.strip())


def total_salary(path: str) -> tuple[float, float]:
    parsed_salary_list = [
        parse_salary_from_line(line, line_number)
        for line, line_number in read_data_lines(path)
    ]

    total = sum(parsed_salary_list)
    average = total / len(parsed_salary_list)

    return total, average


def run() -> None:
    path = ask_path("salary", DEFAULT_SALARY_PATH)

    try:
        total, average = total_salary(path)
    except FileNotFoundError:
        log_error(f"File not found: {path}")
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as e:
        log_error(f"Cannot read file: {e}")
    except EmptyFileError as e:
        log_error(f"File is empty: {e}")
    except CorruptLineError as e:
        log_error(f"File corrupted, {e}")

    else:
        log_result(f"Total salary: ${total:.2f}, average salary: ${average:.2f}")
