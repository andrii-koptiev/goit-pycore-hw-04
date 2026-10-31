from typing import Callable

from hw04.log import format_option, log_error, log_goodbye, log_prompt, log_title
from hw04.task1_salary import run as salary_task_run
from hw04.task2_cats import run as cats_task_run
from hw04.task3_tree import run as tree_task_run
from hw04.task4_bot import run as bot_task_run

TASKS: dict[
    str,
    tuple[str, Callable],
] = {
    "1": ("Salary", salary_task_run),
    "2": ("Cats", cats_task_run),
    "3": ("Folder Structure", tree_task_run),
    "4": ("Contacts Bot", bot_task_run),
}


def print_menu() -> None:
    print()
    log_title("Choose a task:")
    for key, (title, _) in TASKS.items():
        print(format_option(f"{key}.", title, width=2))
    print(format_option("0.", "Exit", width=2))


def main() -> None:
    while True:
        print_menu()
        choice = log_prompt("Your choice: ")

        if choice == "0":
            log_goodbye()
            break

        task = TASKS.get(choice)
        if task is None:
            log_error("Invalid choice, try again.")
            continue

        _, run = task
        run()
