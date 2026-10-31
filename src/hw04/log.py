from colorama import Fore, Style


def log_result(message: str) -> None:
    print(f"{Fore.GREEN} [RESULT] {Fore.RESET} {message}")


def log_error(message: str) -> None:
    print(f"{Fore.RED} [ERROR] {Fore.RESET} {message}")


def log_prompt(message: str) -> str:
    return input(f"{Fore.CYAN} [ACTION] {Fore.RESET} {message}").strip()


def log_title(message: str) -> None:
    print(f"{Style.BRIGHT}{Fore.CYAN}{message}{Style.RESET_ALL}")


def format_option(key: str, description: str, width: int = 0) -> str:
    return f"  {Fore.YELLOW}{key:<{width}}{Style.RESET_ALL}  {description}"


def log_goodbye() -> None:
    print(
        f"\n{Fore.MAGENTA}{Style.BRIGHT}👋 Good bye! See you next time.{Style.RESET_ALL}"
    )
