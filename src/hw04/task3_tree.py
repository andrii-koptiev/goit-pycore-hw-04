"""Task 3: directory tree.

Requirements:

* ``build_tree(path)`` returns a list of plain text lines (no colours, no print).
  - Every entry is on its own line, indented by 4 spaces per nesting level.
  - Directory names end with ``/``; file names have no suffix.
  - The root directory itself is not listed, only its content.
  - In each directory: subdirectories first, then files, both sorted by name.
  - Hidden files and directories (names starting with ``.``) are included.
  - Subdirectories are walked recursively. An empty directory gives ``[]``.
* Errors are raised by ``build_tree`` (it never prints):
  - path does not exist -> ``FileNotFoundError``
  - path is a file      -> ``NotADirectoryError``
* ``run()`` asks for a directory path with ``input()``, prints the tree using
  ``colorama`` (directories ``Fore.BLUE``, files ``Fore.GREEN``) and prints a
  readable message for the errors above instead of crashing.
"""

from pathlib import Path

from colorama import Fore, Style

from hw04.helpers import ask_path
from hw04.log import log_error, log_result

SAMPLE_FOLDER_PATH = "data/tree_sample"


def directory_traverse(directory_path: Path, depth: int) -> list[str]:
    lines: list[str] = []
    for item in sorted(
        directory_path.iterdir(), key=lambda item: (item.is_file(), item.name)
    ):
        name = "    " * depth + item.name
        if item.is_dir():
            name += "/"
        lines.append(name)

        if item.is_dir():
            lines.extend(directory_traverse(item, depth + 1))
    return lines


def colorize_line(line: str) -> str:
    name = line.lstrip()
    indent = line[: len(line) - len(name)]
    color = Fore.BLUE if name.endswith("/") else Fore.GREEN
    return f"{indent}{color}{name}{Style.RESET_ALL}"


def count_entries(lines: list[str]) -> tuple[int, int]:
    folders = sum(1 for line in lines if line.endswith("/"))
    return folders, len(lines) - folders


def print_tree(root_name: str, lines: list[str]) -> None:
    print(f"{root_name}/")
    if not lines:
        print("(empty)")
        return

    for line in lines:
        print(colorize_line(line))

    folders, files = count_entries(lines)
    log_result(f"{folders} folders, {files} files")


def build_tree(path: str) -> list[str]:
    return directory_traverse(Path(path), 0)


def run() -> None:
    path = ask_path("folder", SAMPLE_FOLDER_PATH)

    try:
        folder_tree = build_tree(path)
    except FileNotFoundError as e:
        log_error(f"Folder not found {e}")
    except NotADirectoryError as e:
        log_error(f"Path is not a folder {e}")
    else:
        print_tree(Path(path).name, folder_tree)
