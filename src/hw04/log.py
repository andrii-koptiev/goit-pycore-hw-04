from colorama import Fore, Style


def log_result(message: str) -> None:
    print(f"{Fore.GREEN} [RESULT] {Fore.RESET} {message}")


def log_error(message: str) -> None:
    print(f"{Fore.RED} [ERROR] {Fore.RESET} {message}")


def log_action_message(message: str) -> str:
    return input(f"{Fore.CYAN} [ACTION] {Fore.RESET} {message}").strip()


def log_goodbye() -> None:
    print(
        f"\n{Fore.MAGENTA}{Style.BRIGHT}👋 Good bye! See you next time.{Style.RESET_ALL}"
    )
