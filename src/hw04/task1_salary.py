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
from hw04.log import log_action_message, log_error, log_result

DEFAULT_SALARY_PATH = "data/staff.txt"


def parse_salary_from_line(line: str, line_number: int) -> float:
    try:
        return float(line.strip().split(",")[1])
    except (IndexError, ValueError):
        raise CorruptLineError(line_number, line.strip())


def total_salary(path: str) -> tuple[float, float]:
    with open(path, "r", encoding="utf-8") as file:
        salary_list = [
            parse_salary_from_line(line, index)
            for index, line in enumerate(file.readlines(), start=1)
            if line.strip()
        ]
        if not salary_list:
            raise EmptyFileError()

        total = sum(salary_list)
        average = total / len(salary_list)

        return total, average


def run() -> None:
    path = (
        log_action_message("Path to the salary file or press 'Enter' for default: ")
        or DEFAULT_SALARY_PATH
    )

    try:
        total, average = total_salary(path)
    except FileNotFoundError:
        log_error(f"File not found: {path}")
    except EmptyFileError as e:
        log_error(f"Cannot calculate: {e}")
    except CorruptLineError as e:
        log_error(f"File corrupted, {e}")

    else:
        log_result(f"Total salary: ${total:.2f}, average salary: ${average:.2f}")
