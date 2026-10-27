from typing import Callable

from colorama import Fore, Style

from hw04.log import log_error, log_goodbye
from hw04.task1_salary import run as salary_task_run
from hw04.task2_cats import run as cats_task_run

TASKS: dict[
    str,
    tuple[str, Callable],
] = {"1": ("Salary", salary_task_run), "2": ("Cats", cats_task_run)}


def print_menu() -> None:
    print(f"\n{Style.BRIGHT}{Fore.CYAN}Choose a task:")
    for key, (title, _) in TASKS.items():
        print(f"  {Fore.YELLOW}{key}.{Style.RESET_ALL} {title}")
    print(f"  {Fore.YELLOW}0.{Style.RESET_ALL} Exit")


def main() -> None:
    while True:
        print_menu()
        choice = input(f"{Fore.YELLOW}Your choice: {Style.RESET_ALL}")

        if choice == "0":
            log_goodbye()
            break

        task = TASKS.get(choice)
        if task is None:
            log_error("Invalid choice, try again.")
            continue

        _, run = task
        run()
